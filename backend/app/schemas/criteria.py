from pydantic import BaseModel


class StructuredCriterion(BaseModel):
    criterion_type: str
    criterion_text: str
    structured_field: str | None = None
    operator: str | None = None
    value: str | None = None
    unit: str | None = None
