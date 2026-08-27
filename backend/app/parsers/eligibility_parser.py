from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from app.core.logging import get_logger

logger = get_logger(__name__)


@dataclass
class StructuredCriterion:
    criterion_type: str
    criterion_text: str
    structured_field: str | None = None
    operator: str | None = None
    value: str | None = None
    unit: str | None = None
    parser_status: str = "UNSTRUCTURED"
    parser_version: str = "v1-deterministic"
    confidence: float | None = None


class EligibilityParser(ABC):
    @abstractmethod
    async def parse(self, eligibility_text: str) -> list[StructuredCriterion]:
        pass


class DeterministicEligibilityParser(EligibilityParser):
    def __init__(self):
        self.parser_version = "v1-deterministic"

    async def parse(self, eligibility_text: str) -> list[StructuredCriterion]:
        if not eligibility_text:
            return []

        criteria = []
        sections = self._split_sections(eligibility_text)

        for section_type, text in sections:
            section_criteria = self._parse_section(section_type, text)
            criteria.extend(section_criteria)

        logger.info(
            "criteria_parsed",
            extra={
                "total_criteria": len(criteria),
                "structured": sum(1 for c in criteria if c.parser_status == "STRUCTURED"),
                "unstructured": sum(1 for c in criteria if c.parser_status == "UNSTRUCTURED"),
            },
        )

        return criteria

    def _split_sections(self, text: str) -> list[tuple[str, str]]:
        sections = []
        current_type = "INCLUSION"
        current_lines = []

        lines = text.split("\n")
        for line in lines:
            line = line.strip()
            if not line:
                continue

            lower_line = line.lower()
            if "inclusion" in lower_line and "exclusion" not in lower_line:
                if current_lines:
                    sections.append((current_type, "\n".join(current_lines)))
                current_type = "INCLUSION"
                current_lines = []
            elif "exclusion" in lower_line:
                if current_lines:
                    sections.append((current_type, "\n".join(current_lines)))
                current_type = "EXCLUSION"
                current_lines = []
            else:
                current_lines.append(line)

        if current_lines:
            sections.append((current_type, "\n".join(current_lines)))

        if not sections:
            sections.append(("INCLUSION", text))

        return sections

    def _parse_section(self, criterion_type: str, text: str) -> list[StructuredCriterion]:
        criteria = []
        sentences = self._split_sentences(text)

        for sentence in sentences:
            criterion = self._parse_sentence(criterion_type, sentence)
            criteria.append(criterion)

        return criteria

    def _split_sentences(self, text: str) -> list[str]:
        sentences = re.split(r"[.\n]+", text)
        return [s.strip() for s in sentences if s.strip()]

    def _parse_sentence(self, criterion_type: str, sentence: str) -> StructuredCriterion:
        age_result = self._parse_age(sentence)
        if age_result:
            return StructuredCriterion(
                criterion_type=criterion_type,
                criterion_text=sentence,
                structured_field="age",
                operator=age_result["operator"],
                value=age_result["value"],
                unit="years",
                parser_status="STRUCTURED",
                parser_version=self.parser_version,
                confidence=1.0,
            )

        sex_result = self._parse_sex(sentence)
        if sex_result:
            return StructuredCriterion(
                criterion_type=criterion_type,
                criterion_text=sentence,
                structured_field="sex",
                operator="==",
                value=sex_result,
                unit=None,
                parser_status="STRUCTURED",
                parser_version=self.parser_version,
                confidence=1.0,
            )

        diagnosis_result = self._parse_diagnosis(sentence)
        if diagnosis_result:
            return StructuredCriterion(
                criterion_type=criterion_type,
                criterion_text=sentence,
                structured_field="diagnosis",
                operator="==",
                value=diagnosis_result,
                unit=None,
                parser_status="STRUCTURED",
                parser_version=self.parser_version,
                confidence=0.9,
            )

        return StructuredCriterion(
            criterion_type=criterion_type,
            criterion_text=sentence,
            structured_field=None,
            operator=None,
            value=None,
            unit=None,
            parser_status="UNSTRUCTURED",
            parser_version=self.parser_version,
            confidence=None,
        )

    def _parse_age(self, sentence: str) -> dict[str, Any] | None:
        patterns = [
            (r"age\s*[>=]+\s*(\d+)", ">="),
            (r"age\s*[<=]+\s*(\d+)", "<="),
            (r"age\s*[=]+\s*(\d+)", "=="),
            (r"at least\s+(\d+)\s+years?", ">="),
            (r"(\d+)\s+years?\s+or\s+older", ">="),
            (r"(\d+)\s+years?\s+or\s+older\s+of\s+age", ">="),
            (r"(\d+)\s+years?\s+and\s+older", ">="),
            (r"(\d+)\s+years?\s+or\s+greater", ">="),
            (r"(\d+)\s+years?\s+or\s+younger", "<="),
            (r"(\d+)\s+years?\s+and\s+younger", "<="),
            (r"(\d+)\s+years?\s+of\s+age\s+or\s+younger", "<="),
            (r"older\s+than\s+(\d+)", ">"),
            (r"younger\s+than\s+(\d+)", "<"),
            (r"between\s+(\d+)\s+and\s+(\d+)\s+years?", "BETWEEN"),
        ]

        for pattern, operator in patterns:
            match = re.search(pattern, sentence, re.IGNORECASE)
            if match:
                if operator == "BETWEEN":
                    return {"operator": "BETWEEN", "value": f"{match.group(1)}-{match.group(2)}"}
                return {"operator": operator, "value": match.group(1)}

        return None

    def _parse_sex(self, sentence: str) -> str | None:
        if re.search(r"\bmale\b", sentence, re.IGNORECASE):
            return "Male"
        if re.search(r"\bfemale\b", sentence, re.IGNORECASE):
            return "Female"
        return None

    def _parse_diagnosis(self, sentence: str) -> str | None:
        patterns = [
            r"confirmed\s+(\w+(?:\s+\w+)*)",
            r"histologically\s+confirmed\s+(\w+(?:\s+\w+)*)",
            r"must\s+have\s+(\w+(?:\s+\w+)*)",
            r"diagnosis\s+of\s+(\w+(?:\s+\w+)*)",
        ]

        for pattern in patterns:
            match = re.search(pattern, sentence, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return None
