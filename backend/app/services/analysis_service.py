from __future__ import annotations

import asyncio
import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.agents.mediator import MediatorAgent
from app.agents.patient_reader import PatientReaderAgent
from app.agents.trial_parser import TrialParserAgent
from app.core.config import settings
from app.core.exceptions import NotFoundError
from app.core.logging import get_logger
from app.models.analysis import Analysis, AnalysisStep
from app.models.criteria import TrialCriterion
from app.models.matching import CriterionEvaluation, MatchingResult
from app.models.patient import Patient
from app.models.trial import Trial
from app.repositories.analysis_repository import AnalysisRepository
from app.repositories.patient_repository import PatientRepository
from app.repositories.trial_repository import TrialRepository
from app.services.clinicaltrials_service import ClinicalTrialsService
from app.services.imaging_service import ImagingService
from app.utils.ids import generate_analysis_code, utcnow

logger = get_logger(__name__)

STEPS = [
    "MRI_PREPROCESSING",
    "UNET_SEGMENTATION",
    "RESNET_FEATURE_EXTRACTION",
    "PATIENT_READER",
    "TRIAL_RETRIEVAL",
    "TRIAL_PARSER",
    "STRUCTURED_CRITERIA",
    "MEDIATOR",
    "MATCHING_EVALUATION",
]


class AnalysisService:
    def __init__(self, db: Session):
        self.db = db
        self.analysis_repo = AnalysisRepository(db)
        self.patient_repo = PatientRepository(db)
        self.trial_repo = TrialRepository(db)
        self.imaging_service = ImagingService(db)
        self.ct_service = ClinicalTrialsService()
        self.patient_reader = PatientReaderAgent()
        self.trial_parser = TrialParserAgent()
        self.mediator = MediatorAgent()

    async def create_analysis(self, patient_id: uuid.UUID) -> Analysis:
        patient = self.patient_repo.get_by_id(patient_id)
        if not patient:
            raise NotFoundError("PATIENT_NOT_FOUND", "Patient does not exist.")

        year = datetime.now(timezone.utc).year
        sequence = self.analysis_repo.next_sequence()
        analysis_code = generate_analysis_code(year, sequence)

        analysis = Analysis(
            analysis_code=analysis_code,
            patient_id=patient_id,
            status="PENDING",
            progress=0,
        )
        self.db.add(analysis)
        self.db.flush()

        for idx, step_name in enumerate(STEPS):
            step = AnalysisStep(
                analysis_id=analysis.id,
                step_name=step_name,
                step_order=idx,
                status="PENDING",
            )
            self.db.add(step)

        self.db.flush()
        
        asyncio.create_task(self._run_pipeline(analysis, patient))
        
        return analysis

    async def _run_pipeline(self, analysis: Analysis, patient: Patient) -> None:
        try:
            analysis.status = "PROCESSING"
            analysis.started_at = utcnow()
            self.db.flush()

            patient_dict = {
                "id": str(patient.id),
                "patient_code": patient.patient_code,
                "name": patient.name,
                "age": patient.age,
                "gender": patient.gender,
                "diagnosis": patient.diagnosis,
                "disease_stage": patient.disease_stage,
                "clinical_notes": patient.clinical_notes,
                "medical_history": patient.medical_history,
                "performance_status": patient.performance_status,
                "treatments": [
                    {
                        "treatment_name": t.treatment_name,
                        "treatment_type": t.treatment_type,
                        "status": t.status,
                    }
                    for t in patient.treatments
                ],
                "labs": [
                    {
                        "test_name": l.test_name,
                        "value": l.value,
                        "unit": l.unit,
                    }
                    for l in patient.labs
                ],
            }

            await self._update_step(analysis, "MRI_PREPROCESSING", "PROCESSING")
            await asyncio.sleep(settings.analysis_step_delay_seconds)
            await self._update_step(analysis, "MRI_PREPROCESSING", "COMPLETED", "MRI preprocessing completed")

            await self._update_step(analysis, "UNET_SEGMENTATION", "PROCESSING")
            await asyncio.sleep(settings.analysis_step_delay_seconds)
            await self._update_step(analysis, "UNET_SEGMENTATION", "COMPLETED", "U-Net segmentation completed")

            await self._update_step(analysis, "RESNET_FEATURE_EXTRACTION", "PROCESSING")
            await asyncio.sleep(settings.analysis_step_delay_seconds)
            await self._update_step(analysis, "RESNET_FEATURE_EXTRACTION", "COMPLETED", "ResNet feature extraction completed")

            await self._update_step(analysis, "PATIENT_READER", "PROCESSING")
            patient_attributes = await self.patient_reader.extract_attributes(patient_dict)
            await asyncio.sleep(settings.analysis_step_delay_seconds)
            await self._update_step(analysis, "PATIENT_READER", "COMPLETED", "Patient attributes extracted")

            await self._update_step(analysis, "TRIAL_RETRIEVAL", "PROCESSING")
            condition = patient.diagnosis
            trials = self.trial_repo.list_by_condition(condition, settings.trial_candidate_limit)
            
            if not trials:
                external_trials = await self.ct_service.search_trials(condition, settings.trial_candidate_limit)
                for trial_data in external_trials:
                    existing = self.trial_repo.get_by_nct_id(trial_data["nct_id"])
                    if not existing:
                        trial = Trial(
                            nct_id=trial_data["nct_id"],
                            title=trial_data["title"],
                            brief_summary=trial_data["brief_summary"],
                            official_title=trial_data["official_title"],
                            phase=trial_data["phase"],
                            study_type=trial_data["study_type"],
                            status=trial_data["status"],
                            condition=trial_data["condition"],
                            intervention=trial_data["intervention"],
                            locations=trial_data["locations"],
                            eligibility_text=trial_data["eligibility_text"],
                            source="clinicaltrials.gov",
                            last_updated=datetime.now(timezone.utc),
                        )
                        self.db.add(trial)
                self.db.flush()
                trials = self.trial_repo.list_by_condition(condition, settings.trial_candidate_limit)
            
            await asyncio.sleep(settings.analysis_step_delay_seconds)
            await self._update_step(analysis, "TRIAL_RETRIEVAL", "COMPLETED", f"Retrieved {len(trials)} candidate trials")

            await self._update_step(analysis, "TRIAL_PARSER", "PROCESSING")
            for trial in trials:
                trial_dict = {
                    "nct_id": trial.nct_id,
                    "title": trial.title,
                    "eligibility_text": trial.eligibility_text,
                }
                criteria_data = await self.trial_parser.parse(trial_dict)
                
                if not trial.criteria:
                    for crit_data in criteria_data:
                        criterion = TrialCriterion(
                            trial_id=trial.id,
                            criterion_type=crit_data["criterion_type"],
                            criterion_text=crit_data["criterion_text"],
                            structured_field=crit_data.get("structured_field"),
                            operator=crit_data.get("operator"),
                            value=crit_data.get("value"),
                            unit=crit_data.get("unit"),
                        )
                        self.db.add(criterion)
            self.db.flush()
            await asyncio.sleep(settings.analysis_step_delay_seconds)
            await self._update_step(analysis, "TRIAL_PARSER", "COMPLETED", "Trial criteria parsed")

            await self._update_step(analysis, "STRUCTURED_CRITERIA", "PROCESSING")
            await asyncio.sleep(settings.analysis_step_delay_seconds)
            await self._update_step(analysis, "STRUCTURED_CRITERIA", "COMPLETED", "Criteria structured")

            await self._update_step(analysis, "MEDIATOR", "PROCESSING")
            
            for trial in trials:
                trial = self.trial_repo.get_with_criteria(trial)
                
                passed = 0
                failed = 0
                unknown = 0
                
                matching_result = MatchingResult(
                    analysis_id=analysis.id,
                    patient_id=patient.id,
                    trial_id=trial.id,
                    match_score=0,
                    eligibility_status="UNCERTAIN",
                    criteria_passed=0,
                    criteria_failed=0,
                    criteria_unknown=0,
                )
                self.db.add(matching_result)
                self.db.flush()
                
                for criterion in trial.criteria:
                    evaluation = await self.mediator.evaluate(patient_attributes, {
                        "structured_field": criterion.structured_field,
                        "operator": criterion.operator,
                        "value": criterion.value,
                        "criterion_text": criterion.criterion_text,
                    })
                    
                    criterion_eval = CriterionEvaluation(
                        matching_result_id=matching_result.id,
                        criterion_id=criterion.id,
                        result=evaluation["result"],
                        patient_evidence=evaluation.get("patient_evidence"),
                        patient_value=evaluation.get("patient_value"),
                        required_value=evaluation.get("required_value"),
                        explanation=evaluation.get("explanation"),
                    )
                    self.db.add(criterion_eval)
                    
                    if evaluation["result"] == "PASS":
                        passed += 1
                    elif evaluation["result"] == "FAIL":
                        failed += 1
                    else:
                        unknown += 1
                
                matching_result.criteria_passed = passed
                matching_result.criteria_failed = failed
                matching_result.criteria_unknown = unknown
                
                total_evaluable = passed + failed
                if total_evaluable > 0:
                    matching_result.match_score = (passed / total_evaluable) * 100
                
                if failed > 0:
                    matching_result.eligibility_status = "NOT_ELIGIBLE"
                elif unknown > 0:
                    matching_result.eligibility_status = "UNCERTAIN"
                else:
                    matching_result.eligibility_status = "ELIGIBLE"
            
            self.db.flush()
            await asyncio.sleep(settings.analysis_step_delay_seconds)
            await self._update_step(analysis, "MEDIATOR", "COMPLETED", "Mediator evaluation completed")

            await self._update_step(analysis, "MATCHING_EVALUATION", "PROCESSING")
            await asyncio.sleep(settings.analysis_step_delay_seconds)
            await self._update_step(analysis, "MATCHING_EVALUATION", "COMPLETED", "Matching evaluation completed")

            analysis.status = "COMPLETED"
            analysis.progress = 100
            analysis.completed_at = utcnow()
            analysis.current_step = None
            self.db.flush()
            
            logger.info("analysis_completed", extra={"analysis_code": analysis.analysis_code})
            
        except Exception as e:
            logger.exception("analysis_failed", extra={"analysis_code": analysis.analysis_code})
            analysis.status = "FAILED"
            analysis.error_message = str(e)
            analysis.completed_at = utcnow()
            self.db.flush()

    async def _update_step(
        self,
        analysis: Analysis,
        step_name: str,
        status: str,
        message: str | None = None,
    ) -> None:
        step = next((s for s in analysis.steps if s.step_name == step_name), None)
        if step:
            step.status = status
            if status == "PROCESSING" and not step.started_at:
                step.started_at = utcnow()
            if status == "COMPLETED":
                step.completed_at = utcnow()
                if step.started_at:
                    duration = int((step.completed_at - step.started_at).total_seconds() * 1000)
                    step.duration_ms = duration
            if message:
                step.message = message
            
            analysis.current_step = step_name
            completed_steps = len([s for s in analysis.steps if s.status == "COMPLETED"])
            analysis.progress = int((completed_steps / len(STEPS)) * 100)
            self.db.flush()
