import pytest
from app.ai.mock_client import MockLLMClient
from app.agents.trial_parser.agent import TrialParserAgent
from app.agents.trial_parser.schemas import ParsedEligibility, ParsedCriterion


@pytest.fixture
def mock_llm():
    return MockLLMClient()


@pytest.fixture
def trial_parser_agent(mock_llm):
    return TrialParserAgent(mock_llm)


@pytest.mark.asyncio
async def test_parse_age_criteria(trial_parser_agent):
    trial_data = {
        "trial_id": "test-1",
        "title": "Test Trial",
        "eligibility_text": "Age >= 18 years.",
    }
    
    eligibility = await trial_parser_agent.run(trial_data)
    
    assert eligibility.overall_status == "COMPLETED"
    age_criterion = next((c for c in eligibility.criteria if c.structured_field == "age"), None)
    assert age_criterion is not None
    assert age_criterion.operator == ">="
    assert age_criterion.value == 18
    assert age_criterion.unit == "years"
    assert age_criterion.parser_status.value == "STRUCTURED"


@pytest.mark.asyncio
async def test_parse_ecog_criteria(trial_parser_agent):
    trial_data = {
        "trial_id": "test-1",
        "title": "Test Trial",
        "eligibility_text": "ECOG performance status 0-2.",
    }
    
    eligibility = await trial_parser_agent.run(trial_data)
    
    ecog_criterion = next((c for c in eligibility.criteria if c.structured_field == "performance_status"), None)
    assert ecog_criterion is not None
    assert ecog_criterion.operator == "BETWEEN"
    assert ecog_criterion.unit == "ECOG"


@pytest.mark.asyncio
async def test_parse_diagnosis_criteria(trial_parser_agent):
    trial_data = {
        "trial_id": "test-1",
        "title": "Glioblastoma Study",
        "conditions": ["Glioblastoma"],
        "eligibility_text": "Histologically confirmed glioblastoma.",
    }
    
    eligibility = await trial_parser_agent.run(trial_data)
    
    diag_criterion = next((c for c in eligibility.criteria if c.structured_field == "diagnosis"), None)
    assert diag_criterion is not None
    assert diag_criterion.operator == "CONTAINS"
    assert "glioblastoma" in diag_criterion.value.lower()
    assert diag_criterion.parser_status.value == "STRUCTURED"


@pytest.mark.asyncio
async def test_unstructured_criteria(trial_parser_agent):
    trial_data = {
        "trial_id": "test-1",
        "title": "Test Trial",
        "eligibility_text": "Adequate organ function as determined by the investigator.",
    }
    
    eligibility = await trial_parser_agent.run(trial_data)
    
    unstructured = next((c for c in eligibility.criteria if c.parser_status.value == "UNSTRUCTURED"), None)
    assert unstructured is not None
    assert unstructured.structured_field is None
    assert unstructured.operator is None
    assert unstructured.value is None


@pytest.mark.asyncio
async def test_criterion_type_inclusion(trial_parser_agent):
    trial_data = {
        "trial_id": "test-1",
        "title": "Test Trial",
        "eligibility_text": "Inclusion Criteria:\nAge >= 18 years.",
    }
    
    eligibility = await trial_parser_agent.run(trial_data)
    
    inclusion_criteria = [c for c in eligibility.criteria if c.criterion_type.value == "INCLUSION"]
    assert len(inclusion_criteria) > 0


@pytest.mark.asyncio
async def test_source_textPreserved(trial_parser_agent):
    trial_data = {
        "trial_id": "test-1",
        "title": "Test Trial",
        "eligibility_text": "Age >= 18 years.",
    }
    
    eligibility = await trial_parser_agent.run(trial_data)
    
    age_criterion = next((c for c in eligibility.criteria if c.structured_field == "age"), None)
    assert age_criterion is not None
    assert age_criterion.source_text is not None


@pytest.mark.asyncio
async def test_confidence_structured(trial_parser_agent):
    trial_data = {
        "trial_id": "test-1",
        "title": "Test Trial",
        "eligibility_text": "Age >= 18 years.",
    }
    
    eligibility = await trial_parser_agent.run(trial_data)
    
    age_criterion = next((c for c in eligibility.criteria if c.structured_field == "age"), None)
    assert age_criterion is not None
    if age_criterion.parser_status.value == "STRUCTURED":
        assert age_criterion.confidence is not None
        assert 0 <= age_criterion.confidence <= 1.0


@pytest.mark.asyncio
async def test_confidence_unstructured(trial_parser_agent):
    trial_data = {
        "trial_id": "test-1",
        "title": "Test Trial",
        "eligibility_text": "Adequate organ function as determined by the investigator.",
    }
    
    eligibility = await trial_parser_agent.run(trial_data)
    
    unstructured = next((c for c in eligibility.criteria if c.parser_status.value == "UNSTRUCTURED"), None)
    assert unstructured is not None
    assert unstructured.confidence is None


@pytest.mark.asyncio
async def test_determinism(trial_parser_agent):
    trial_data = {
        "trial_id": "test-1",
        "title": "Test Trial",
        "eligibility_text": "Age >= 18 years.",
    }
    
    eligibility1 = await trial_parser_agent.run(trial_data)
    eligibility2 = await trial_parser_agent.run(trial_data)
    
    assert len(eligibility1.criteria) == len(eligibility2.criteria)


@pytest.mark.asyncio
async def test_preserve_original_text(trial_parser_agent):
    trial_data = {
        "trial_id": "test-1",
        "title": "Test Trial",
        "eligibility_text": "Age >= 18 years.",
    }
    
    eligibility = await trial_parser_agent.run(trial_data)
    
    for criterion in eligibility.criteria:
        assert criterion.criterion_text is not None
        assert len(criterion.criterion_text) > 0


@pytest.mark.asyncio
async def test_no_invented_thresholds(trial_parser_agent):
    trial_data = {
        "trial_id": "test-1",
        "title": "Test Trial",
        "eligibility_text": "Adequate organ function as determined by the investigator.",
    }
    
    eligibility = await trial_parser_agent.run(trial_data)
    
    unstructured = next((c for c in eligibility.criteria if c.parser_status.value == "UNSTRUCTURED"), None)
    assert unstructured is not None
    assert unstructured.value is None
