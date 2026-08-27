import asyncio
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.core.database import SessionLocal, engine
from app.models.analysis import Analysis, AnalysisStep
from app.models.criteria import TrialCriterion
from app.models.matching import CriterionEvaluation, MatchingResult
from app.models.patient import Patient, PatientLab, PatientProfileAttribute, PatientTreatment
from app.models.trial import Trial
from app.utils.ids import generate_analysis_code, generate_patient_code


def seed_patients(db: Session, count: int = 10) -> list[Patient]:
    patients = []
    diagnoses = ["Glioblastoma", "Astrocytoma", "Oligodendroglioma", "Medulloblastoma", "Meningioma"]
    
    for i in range(count):
        patient = Patient(
            patient_code=generate_patient_code(i + 1),
            name=f"Demo Patient {i + 1}",
            age=40 + (i % 30),
            gender="Male" if i % 2 == 0 else "Female",
            diagnosis=diagnoses[i % len(diagnoses)],
            disease_stage="Grade IV" if i % 3 == 0 else "Grade III",
            clinical_notes=f"Synthetic clinical notes for patient {i + 1}.",
            medical_history=f"Synthetic medical history for patient {i + 1}.",
            performance_status=f"ECOG {i % 3}",
            status="active",
        )
        db.add(patient)
        patients.append(patient)
    
    db.flush()
    
    for patient in patients:
        for j in range(3):
            lab = PatientLab(
                patient_id=patient.id,
                test_name=["Hemoglobin", "Platelet Count", "White Blood Cell"][j],
                value=str(10 + j + (patient.age % 5)),
                unit=["g/dL", "x10^9/L", "x10^9/L"][j],
                reference_range="12-16 g/dL" if j == 0 else "150-400 x10^9/L",
                status="NORMAL" if j % 2 == 0 else "ABNORMAL",
                measured_at=datetime.now(timezone.utc) - timedelta(days=j),
            )
            db.add(lab)
        
        for j in range(2):
            treatment = PatientTreatment(
                patient_id=patient.id,
                treatment_name=["Temozolomide", "Radiation Therapy"][j],
                treatment_type="Chemotherapy" if j == 0 else "Radiation",
                start_date=datetime.now(timezone.utc) - timedelta(days=30 + j * 15),
                end_date=datetime.now(timezone.utc) - timedelta(days=15 + j * 10),
                status="Completed",
                notes=f"Standard {['chemotherapy' if j == 0 else 'radiation'][j]} protocol.",
            )
            db.add(treatment)
        
        attrs = [
            PatientProfileAttribute(
                patient_id=patient.id,
                attribute_name="diagnosis",
                attribute_value=patient.diagnosis,
                source="clinical_notes",
                confidence=0.95,
            ),
            PatientProfileAttribute(
                patient_id=patient.id,
                attribute_name="performance_status",
                attribute_value=patient.performance_status,
                source="clinical_notes",
                confidence=0.90,
            ),
        ]
        for attr in attrs:
            db.add(attr)
    
    db.flush()
    return patients


def seed_trials(db: Session, count: int = 20) -> list[Trial]:
    trials = []
    conditions = ["Glioblastoma", "Astrocytoma", "Brain Tumor"]
    phases = ["Phase 1", "Phase 2", "Phase 3"]
    statuses = ["Recruiting", "Active, not recruiting", "Completed"]
    
    for i in range(count):
        trial = Trial(
            nct_id=f"NCT{20240000 + i:08d}",
            title=f"Study of {['Immunotherapy', 'Targeted Therapy', 'Chemotherapy'][i % 3]} for {conditions[i % len(conditions)]}",
            brief_summary=f"This is a synthetic trial summary for trial {i + 1}.",
            official_title=f"A Randomized, Double-Blind, Placebo-Controlled Study of {['Drug A', 'Drug B', 'Drug C'][i % 3]}",
            phases=[phases[i % len(phases)]],
            study_type="Interventional",
            status=statuses[i % len(statuses)],
            conditions=[conditions[i % len(conditions)]],
            intervention=f"{['Drug A', 'Drug B', 'Drug C'][i % 3]}",
            locations=["Boston, MA", "New York, NY", "Los Angeles, CA"][i % 3 : (i % 3) + 1],
            source="seed",
            eligibility_text=f"Inclusion: Age >= 18 years. Histologically confirmed {conditions[i % len(conditions)]}. ECOG 0-2. Exclusion: Pregnant or breastfeeding. Prior therapy with similar agent.",
            last_updated=datetime.now(timezone.utc) - timedelta(days=i),
        )
        db.add(trial)
        trials.append(trial)
    
    db.flush()
    
    for trial in trials:
        criteria = [
            TrialCriterion(
                trial_id=trial.id,
                criterion_type="INCLUSION",
                criterion_text="Age >= 18 years",
                structured_field="age",
                operator=">=",
                value="18",
                unit="years",
            ),
            TrialCriterion(
                trial_id=trial.id,
                criterion_type="INCLUSION",
                criterion_text=f"Histologically confirmed {trial.condition}",
                structured_field="diagnosis",
                operator="==",
                value=trial.condition,
                unit=None,
            ),
            TrialCriterion(
                trial_id=trial.id,
                criterion_type="INCLUSION",
                criterion_text="ECOG performance status 0-2",
                structured_field="performance_status",
                operator="in",
                value="ECOG 0, ECOG 1, ECOG 2",
                unit=None,
            ),
            TrialCriterion(
                trial_id=trial.id,
                criterion_type="EXCLUSION",
                criterion_text="Pregnant or breastfeeding",
                structured_field="pregnancy_status",
                operator="==",
                value="Not pregnant",
                unit=None,
            ),
        ]
        for criterion in criteria:
            db.add(criterion)
    
    db.flush()
    return trials


def seed_analyses(db: Session, patients: list[Patient], trials: list[Trial]) -> list[Analysis]:
    analyses = []
    
    for patient in patients[:5]:
        year = datetime.now(timezone.utc).year
        analysis = Analysis(
            analysis_code=generate_analysis_code(year, len(analyses) + 1),
            patient_id=patient.id,
            status="COMPLETED",
            progress=100,
            current_step=None,
            started_at=datetime.now(timezone.utc) - timedelta(hours=2),
            completed_at=datetime.now(timezone.utc) - timedelta(hours=1),
        )
        db.add(analysis)
        analyses.append(analysis)
    
    db.flush()
    
    step_names = [
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
    
    for analysis in analyses:
        for idx, step_name in enumerate(step_names):
            step = AnalysisStep(
                analysis_id=analysis.id,
                step_name=step_name,
                step_order=idx,
                status="COMPLETED",
                started_at=analysis.started_at + timedelta(minutes=idx * 5),
                completed_at=analysis.started_at + timedelta(minutes=(idx + 1) * 5),
                duration_ms=300000,
                message=f"{step_name} completed successfully",
            )
            db.add(step)
    
    db.flush()
    
    for analysis in analyses:
        patient = next(p for p in patients if p.id == analysis.patient_id)
        matching_trials = [t for t in trials if t.condition == patient.diagnosis][:14]
        
        for trial in matching_trials:
            eligible_count = sum(1 for _ in trial.criteria if _.criterion_type == "INCLUSION")
            passed = eligible_count - (hash(str(analysis.id) + trial.nct_id) % 3)
            failed = hash(str(analysis.id) + trial.nct_id) % 2
            unknown = len(trial.criteria) - passed - failed
            
            match_score = (passed / (passed + failed)) * 100 if (passed + failed) > 0 else 0
            
            eligibility_status = "ELIGIBLE" if failed == 0 else ("NOT_ELIGIBLE" if failed > 0 else "UNCERTAIN")
            
            matching_result = MatchingResult(
                analysis_id=analysis.id,
                patient_id=patient.id,
                trial_id=trial.id,
                match_score=match_score,
                eligibility_status=eligibility_status,
                criteria_passed=passed,
                criteria_failed=failed,
                criteria_unknown=unknown,
            )
            db.add(matching_result)
        
        db.flush()
        
        matching_results = [
            r for r in analysis.matching_results if r.analysis_id == analysis.id
        ]
        
        for result in matching_results:
            trial = next(t for t in trials if t.id == result.trial_id)
            
            for criterion in trial.criteria:
                eval_result = "PASS" if hash(str(result.id) + str(criterion.id)) % 3 != 0 else "FAIL"
                
                evaluation = CriterionEvaluation(
                    matching_result_id=result.id,
                    criterion_id=criterion.id,
                    result=eval_result,
                    patient_evidence=f"Patient {criterion.structured_field} data available",
                    patient_value=str(getattr(patient, criterion.structured_field, "N/A")) if criterion.structured_field else "N/A",
                    required_value=criterion.value,
                    explanation=f"Patient {'satisfies' if eval_result == 'PASS' else 'does not satisfy'} the criterion.",
                )
                db.add(evaluation)
    
    db.flush()
    return analyses


def main():
    print("Starting database seed...")
    
    db = SessionLocal()
    
    try:
        print("Clearing existing data...")
        db.execute(CriterionEvaluation.__table__.delete())
        db.execute(MatchingResult.__table__.delete())
        db.execute(AnalysisStep.__table__.delete())
        db.execute(Analysis.__table__.delete())
        db.execute(TrialCriterion.__table__.delete())
        db.execute(Trial.__table__.delete())
        db.execute(PatientProfileAttribute.__table__.delete())
        db.execute(PatientTreatment.__table__.delete())
        db.execute(PatientLab.__table__.delete())
        db.execute(Patient.__table__.delete())
        db.flush()
        
        print("Seeding patients...")
        patients = seed_patients(db, count=10)
        print(f"Created {len(patients)} patients")
        
        print("Seeding trials...")
        trials = seed_trials(db, count=20)
        print(f"Created {len(trials)} trials")
        
        print("Seeding analyses...")
        analyses = seed_analyses(db, patients, trials)
        print(f"Created {len(analyses)} analyses")
        
        db.commit()
        print("Database seed completed successfully!")
        
        print("\nSummary:")
        print(f"- Patients: {len(patients)}")
        print(f"- Trials: {len(trials)}")
        print(f"- Analyses: {len(analyses)}")
        
        for analysis in analyses:
            patient = next(p for p in patients if p.id == analysis.patient_id)
            results = [r for r in analysis.matching_results if r.analysis_id == analysis.id]
            eligible = sum(1 for r in results if r.eligibility_status == "ELIGIBLE")
            uncertain = sum(1 for r in results if r.eligibility_status == "UNCERTAIN")
            not_eligible = sum(1 for r in results if r.eligibility_status == "NOT_ELIGIBLE")
            print(f"  - {analysis.analysis_code} ({patient.patient_code}): {len(results)} trials - {eligible} eligible, {uncertain} uncertain, {not_eligible} not eligible")
        
    except Exception as e:
        db.rollback()
        print(f"Error during seed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
