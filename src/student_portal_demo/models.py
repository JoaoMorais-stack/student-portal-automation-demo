from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass
class Lesson:
    id: str
    title: str
    duration_minutes: int
    completed: bool = False


@dataclass
class Course:
    id: str
    title: str
    code: str
    instructor: str
    accent: str
    lessons: list[Lesson] = field(default_factory=list)

    @property
    def completed_lessons(self) -> int:
        return sum(lesson.completed for lesson in self.lessons)

    @property
    def progress(self) -> int:
        if not self.lessons:
            return 0
        return round((self.completed_lessons / len(self.lessons)) * 100)

    def to_dict(self) -> dict:
        result = asdict(self)
        result["completed_lessons"] = self.completed_lessons
        result["progress"] = self.progress
        return result


def build_demo_courses() -> list[Course]:
    return [
        Course(
            id="course-digital-culture",
            title="Digital Culture and Society",
            code="DCS-204",
            instructor="Prof. Marina Costa",
            accent="#2274a5",
            lessons=[
                Lesson("dcs-01", "Networks and everyday life", 18, True),
                Lesson("dcs-02", "Responsible digital citizenship", 24),
                Lesson("dcs-03", "Information quality workshop", 20),
            ],
        ),
        Course(
            id="course-data-literacy",
            title="Applied Data Literacy",
            code="ADL-118",
            instructor="Prof. Rafael Lima",
            accent="#d1495b",
            lessons=[
                Lesson("adl-01", "Reading charts with context", 16, True),
                Lesson("adl-02", "Sampling and uncertainty", 22, True),
                Lesson("adl-03", "Communicating a finding", 19),
            ],
        ),
        Course(
            id="course-project-practice",
            title="Project Practice Lab",
            code="PPL-310",
            instructor="Prof. Camila Nunes",
            accent="#2a9d6f",
            lessons=[
                Lesson("ppl-01", "Defining a useful problem", 14),
                Lesson("ppl-02", "Planning an iteration", 17),
                Lesson("ppl-03", "Presenting evidence", 21),
            ],
        ),
    ]

