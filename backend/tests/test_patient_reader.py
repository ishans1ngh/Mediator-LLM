import pytest
from app.ai.mock_client import MockLLMClient
from app.agents.patient_reader.agent import PatientReaderAgent
from app.agents.patient_reader.schemas import PatientProfile, PatientAttribute


@pytest.fixture
def mock_llm():
    return MockLLMClient()


@pytest.fixture
def patient_reader_agent(mock_llm):
    return PatientReaderAgent(mock_llm)


@pytest.mark.asyncio
async def test_extract_age(patient_reader_agent):
    patient_data = {
        "patient_id": "test-1",
        "age": 52,
        "gender": "Male",
        "diagnosis": "Glioblastoma",
    }
    
    profile = await patient_reader_agent.run(patient_data)
    
    assert profile.overall_status == "COMPLETED"
    age_attr = next((a for a in profile.attributes if a.field == "age"), None)
    assert age_attr is not None
    assert age_attr.value == 52
    assert age_attr.status.value == "KNOWN"
    assert age_attr.confidence == 1.0


@pytest.mark.asyncio
async def test_extract_sex_male(patient_reader_agent):
    patient_data = {
        "patient_id": "test-1",
        "age": 52,
        "gender": "Male",
        "diagnosis": "Glioblastoma",
    }
    
    profile = await patient_reader_agent.run(patient_data)
    
    sex_attr = next((a for a in profile.attributes if a.field == "sex"), None)
    assert sex_attr is not None
    assert sex_attr.value == "Male"
    assert sex_attr.normalized_value == "MALE"
    assert sex_attr.status.value == "KNOWN"


@pytest.mark.asyncio
async def test_extract_sex_female(patient_reader_agent):
    patient_data = {
        "patient_id": "test-1",
        "age": 45,
        "gender": "Female",
        "diagnosis": "Glioblastoma",
    }
    
    profile = await patient_reader_agent.run(patient_data)
    
    sex_attr = next((a for a in profile.attributes if a.field == "sex"), None)
    assert sex_attr is not None
    assert sex_attr.value == "Female"
    assert sex_attr.normalized_value == "FEMALE"


@pytest.mark.asyncio
async def test_extract_diagnosis(patient_reader_agent):
    patient_data = {
        "patient_id": "test-1",
        "age": 52,
        "gender": "Male",
        "diagnosis": "Glioblastoma",
    }
    
    profile = await patient_reader_agent.run(patient_data)
    
    diag_attr = next((a for a in profile.attributes if a.field == "diagnosis"), None)
    assert diag_attr is not None
    assert diag_attr.value == "Glioblastoma"
    assert diag_attr.status.value == "KNOWN"


@pytest.mark.asyncio
async def test_extract_ecog(patient_reader_agent):
    patient_data = {
        "patient_id": "test-1",
        "age": 52,
        "gender": "Male",
        "diagnosis": "Glioblastoma",
        "performance_status": "ECOG 1",
    }
    
    profile = await patient_reader_agent.run(patient_data)
    
    ecog_attr = next((a for a in profile.attributes if a.field == "performance_status"), None)
    assert ecog_attr is not None
    assert ecog_attr.value == "ECOG 1"
    assert ecog_attr.unit == "ECOG"


@pytest.mark.asyncio
async def test_biomarker_unknown_when_not_present(patient_reader_agent):
    patient_data = {
        "patient_id": "test-1",
        "age": 52,
        "gender": "Male",
        "diagnosis": "Glioblastoma",
    }
    
    profile = await patient_reader_agent.run(patient_data)
    
    mgmt_attr = next((a for a in profile.attributes if a.field == "MGMT_status"), None)
    idh_attr = next((a for a in profile.attributes if a.field == "IDH_status"), None)
    
    assert mgmt_attr is not None
    assert mgmt_attr.status.value == "UNKNOWN"
    assert mgmt_attr.value is None
    
    assert idh_attr is not None
    assert idh_attr.status.value == "UNKNOWN"
    assert idh_attr.value is None


@pytest.mark.asyncio
async def test_no_hallucination_of_missing_info(patient_reader_agent):
    patient_data = {
        "patient_id": "test-1",
        "age": 52,
        "gender": "Male",
        "diagnosis": "Glioblastoma",
    }
    
    profile = await patient_reader_agent.run(patient_data)
    
    # Check that biomarkers are marked UNKNOWN, not invented
    for attr in profile.attributes:
        if attr.field in ["MGMT_status", "IDH_status", "EGFR_status"]:
            assert attr.status.value == "UNKNOWN"
            assert attr.value is None


@pytest.mark.asyncio
async def test_source_text_preserved(patient_reader_agent):
    patient_data = {
        "patient_id": "test-1",
        "age": 52,
        "gender": "Male",
        "diagnosis": "Glioblastoma",
    }
    
    profile = await patient_reader_agent.run(patient_data)
    
    age_attr = next((a for a in profile.attributes if a.field == "age"), None)
    assert age_attr is not None
    assert age_attr.source_text is not None
    assert "52" in age_attr.source_text


@pytest.mark.asyncio
async def test_confidence_values(patient_reader_agent):
    patient_data = {
        "patient_id": "test-1",
        "age": 52,
        "gender": "Male",
        "diagnosis": "Glioblastoma",
    }
    
    profile = await patient_reader_agent.run(patient_data)
    
    for attr in profile.attributes:
        if attr.status.value == "KNOWN":
            assert attr.confidence is not None
            assert 0 <= attr.confidence <= 1.0


@pytest.mark.asyncio
async def test_determinism(patient_reader_agent):
    patient_data = {
        "patient_id": "test-1",
        "age": 52,
        "gender": "Male",
        "diagnosis": "Glioblastoma",
    }
    
    profile1 = await patient_reader_agent.run(patient_data)
    profile2 = await patient_reader_agent.run(patient_data)
    
    assert len(profile1.attributes) == len(profile2.attributes)
    
    for attr1, attr2 in zip(profile1.attributes, profile2.attributes):
        assert attr1.field == attr2.field
        assert attr1.value == attr2.value
        assert attr1.status == attr2.status
