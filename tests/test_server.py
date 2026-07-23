import json
import sys
import threading
from pathlib import Path
import unittest
from urllib.request import urlopen


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from student_portal_demo.automation import PortalClient
from student_portal_demo.server import make_server


class DemoServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.server = make_server(port=0)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def setUp(self) -> None:
        self.server.store.reset()

    def test_health_endpoint_declares_local_scope(self) -> None:
        with urlopen(f"{self.base_url}/api/health", timeout=2) as response:
            payload = json.loads(response.read().decode("utf-8"))
        self.assertEqual(payload, {"status": "ok", "scope": "local-mock-only"})

    def test_home_page_is_served(self) -> None:
        with urlopen(f"{self.base_url}/", timeout=2) as response:
            html = response.read().decode("utf-8")
        self.assertIn("Northstar Learning Lab", html)
        self.assertIn("Local mock environment", html)

    def test_automation_completes_only_pending_mock_lessons(self) -> None:
        client = PortalClient(self.base_url)
        before = client.state()["summary"]
        events = client.run()
        after = client.state()["summary"]

        self.assertEqual(len(events), before["pending"])
        self.assertEqual(after["pending"], 0)
        self.assertEqual(after["completed"], after["lessons"])
        self.assertEqual(client.run(), [])

    def test_server_rejects_non_loopback_binding(self) -> None:
        with self.assertRaises(ValueError):
            make_server(host="0.0.0.0", port=0)


if __name__ == "__main__":
    unittest.main()

