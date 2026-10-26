
from dataclasses import dataclass, field as dataclass_field


@dataclass
class StudentProfile:
    education_level: str | None = None
    field: str | None = None
    annual_income: float | None = None
    state: str | None = None
    rural: bool | None = None
    first_generation: bool | None = None
    interests: list[str] = dataclass_field(default_factory=list)
