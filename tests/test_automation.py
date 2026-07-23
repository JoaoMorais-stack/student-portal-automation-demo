import sys
from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from student_portal_demo.automation import AutomationSafetyError, validate_local_base_url


class LocalTargetValidationTests(unittest.TestCase):
    def test_accepts_loopback_origins(self) -> None:
        accepted = (
            "http://127.0.0.1:8765",
            "http://localhost:8765/",
            "http://[::1]:8765",
        )
        for url in accepted:
            with self.subTest(url=url):
                self.assertTrue(validate_local_base_url(url).startswith("http://"))

    def test_rejects_non_local_or_ambiguous_targets(self) -> None:
        rejected = (
            "https://127.0.0.1:8765",
            "http://example.com",
            "http://203.0.113.10:8765",
            "http://localhost:8765/api/state",
            "http://user:password@localhost:8765",
        )
        for url in rejected:
            with self.subTest(url=url):
                with self.assertRaises(AutomationSafetyError):
                    validate_local_base_url(url)


if __name__ == "__main__":
    unittest.main()
