from __future__ import annotations

from threading import RLock

from .models import Course, Lesson, build_demo_courses


class PortalStore:
    def __init__(self) -> None:
        self._lock = RLock()
        self._courses: list[Course] = []
        self.reset()

    def reset(self) -> dict:
        with self._lock:
            self._courses = build_demo_courses()
            return self.snapshot()

    def snapshot(self) -> dict:
        with self._lock:
            courses = [course.to_dict() for course in self._courses]
            lesson_count = sum(len(course.lessons) for course in self._courses)
            completed_count = sum(course.completed_lessons for course in self._courses)
            overall_progress = round((completed_count / lesson_count) * 100) if lesson_count else 0
            return {
                "student": {
                    "name": "Alex Morgan",
                    "program": "Interdisciplinary Studies",
                    "term": "Demo Term 2026",
                },
                "summary": {
                    "courses": len(courses),
                    "lessons": lesson_count,
                    "completed": completed_count,
                    "pending": lesson_count - completed_count,
                    "overall_progress": overall_progress,
                },
                "courses": courses,
            }

    def complete_lesson(self, lesson_id: str) -> tuple[Lesson | None, bool]:
        with self._lock:
            for course in self._courses:
                for lesson in course.lessons:
                    if lesson.id == lesson_id:
                        changed = not lesson.completed
                        lesson.completed = True
                        return lesson, changed
        return None, False

