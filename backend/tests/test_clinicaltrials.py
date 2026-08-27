import pytest
from app.parsers.eligibility_parser import DeterministicEligibilityParser, StructuredCriterion


@pytest.fixture
def parser():
    return DeterministicEligibilityParser()


@pytest.mark.asyncio
async def test_parse_age_ge(parser):
    text = "Age >= 18 years"
    criteria = await parser.parse(text)
    
    assert len(criteria) == 1
    assert criteria[0].structured_field == "age"
    assert criteria[0].operator == ">="
    assert criteria[0].value == "18"
    assert criteria[0].unit == "years"
    assert criteria[0].parser_status == "STRUCTURED"


@pytest.mark.asyncio
async def test_parse_age_le(parser):
    text = "Age <= 65 years"
    criteria = await parser.parse(text)
    
    assert len(criteria) == 1
    assert criteria[0].structured_field == "age"
    assert criteria[0].operator == "<="
    assert criteria[0].value == "65"
    assert criteria[0].parser_status == "STRUCTURED"


@pytest.mark.asyncio
async def test_parse_at_least(parser):
    text = "at least 18 years old"
    criteria = await parser.parse(text)
    
    assert len(criteria) == 1
    assert criteria[0].structured_field == "age"
    assert criteria[0].operator == ">="
    assert criteria[0].value == "18"
    assert criteria[0].parser_status == "STRUCTURED"


@pytest.mark.asyncio
async def test_parse_years_older(parser):
    text = "18 years or older"
    criteria = await parser.parse(text)
    
    assert len(criteria) == 1
    assert criteria[0].structured_field == "age"
    assert criteria[0].operator == ">="
    assert criteria[0].value == "18"
    assert criteria[0].parser_status == "STRUCTURED"


@pytest.mark.asyncio
async def test_parse_sex_male(parser):
    text = "Male participants only"
    criteria = await parser.parse(text)
    
    assert len(criteria) == 1
    assert criteria[0].structured_field == "sex"
    assert criteria[0].operator == "=="
    assert criteria[0].value == "Male"
    assert criteria[0].parser_status == "STRUCTURED"


@pytest.mark.asyncio
async def test_parse_sex_female(parser):
    text = "Female patients"
    criteria = await parser.parse(text)
    
    assert len(criteria) == 1
    assert criteria[0].structured_field == "sex"
    assert criteria[0].value == "Female"
    assert criteria[0].parser_status == "STRUCTURED"


@pytest.mark.asyncio
async def test_parse_diagnosis(parser):
    text = "confirmed glioblastoma"
    criteria = await parser.parse(text)
    
    assert len(criteria) == 1
    assert criteria[0].structured_field == "diagnosis"
    assert criteria[0].operator == "=="
    assert criteria[0].value == "glioblastoma"
    assert criteria[0].parser_status == "STRUCTURED"


@pytest.mark.asyncio
async def test_parse_unstructured(parser):
    text = "Adequate organ function is required"
    criteria = await parser.parse(text)
    
    assert len(criteria) == 1
    assert criteria[0].structured_field is None
    assert criteria[0].operator is None
    assert criteria[0].value is None
    assert criteria[0].parser_status == "UNSTRUCTURED"


@pytest.mark.asyncio
async def test_split_inclusion_exclusion(parser):
    text = """
    Inclusion Criteria:
    Age >= 18 years.
    Confirmed glioblastoma.
    
    Exclusion Criteria:
    Pregnant or breastfeeding.
    """
    criteria = await parser.parse(text)
    
    inclusion = [c for c in criteria if c.criterion_type == "INCLUSION"]
    exclusion = [c for c in criteria if c.criterion_type == "EXCLUSION"]
    
    assert len(inclusion) == 2
    assert len(exclusion) == 1
    assert inclusion[0].structured_field == "age"
    assert inclusion[1].structured_field == "diagnosis"
    assert exclusion[0].parser_status == "UNSTRUCTURED"


@pytest.mark.asyncio
async def test_empty_text(parser):
    criteria = await parser.parse("")
    assert len(criteria) == 0


@pytest.mark.asyncio
async def test_multiple_sentences(parser):
    text = "Age >= 18 years. Male participants only."
    criteria = await parser.parse(text)
    
    assert len(criteria) == 2
    assert criteria[0].structured_field == "age"
    assert criteria[1].structured_field == "sex"


@pytest.mark.asyncio
async def test_confidence_structured(parser):
    text = "Age >= 18 years"
    criteria = await parser.parse(text)
    
    assert criteria[0].confidence == 1.0


@pytest.mark.asyncio
async def test_confidence_unstructured(parser):
    text = "Adequate organ function"
    criteria = await parser.parse(text)
    
    assert criteria[0].confidence is None


@pytest.mark.asyncio
async def test_parser_version(parser):
    text = "Age >= 18 years"
    criteria = await parser.parse(text)
    
    assert criteria[0].parser_version == "v1-deterministic"
