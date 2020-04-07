import json
import unittest

from app.server import app
from app.blueprints.device_blueprint import device


class DeviceBlueprintUnitTest(unittest.TestCase):

    def setUp(self) -> None:
        self._blueprint_url = "/device"

        app.testing = True
        app.register_blueprint(device, url_prefix=self._blueprint_url)

        self.client = app.test_client()

    def test_get_bluetooth_status(self):
        response = self.client.post(f"{self._blueprint_url}/getBluetoothStatus")
        json_dict = json.loads(response.data)
        self.assertIn(json_dict["retCode"], ["000000", "999999"])

    def test_get_ip_address(self):
        response = self.client.post(f"{self._blueprint_url}/getIPAddress")
        json_dict = json.loads(response.data)
        self.assertEqual(json_dict["retCode"], "000000")

    def test_get_user_info(self):
        response = self.client.post(f"{self._blueprint_url}/getUserInfo")
        json_dict = json.loads(response.data)
        self.assertEqual(json_dict["retCode"], "000000")

    def test_get_memory_info_success(self):
        post_data = {"mode": "MB"}
        response = self.client.post(
            f"{self._blueprint_url}/getMemoryInfo",
            data=json.dumps(post_data),
            content_type="application/json",
        )
        json_dict = json.loads(response.data)
        self.assertEqual(json_dict["retCode"], "000000")

    def test_get_memory_info_failure(self):
        response = self.client.post(f"{self._blueprint_url}/getMemoryInfo")
        json_dict = json.loads(response.data)
        self.assertEqual(json_dict["retCode"], "999999")

    def test_make_system_notification_success(self):
        post_data = {
            "title": "Test Title",
            "content": "Content is here!",
            "subtitle": "Subtitle is here!",
        }
        response = self.client.post(
            f"{self._blueprint_url}/makeNotification",
            data=json.dumps(post_data),
            content_type="application/json",
        )
        json_dict = json.loads(response.data)
        self.assertEqual(json_dict["retCode"], "000000")

    def test_make_system_notification_failure(self):
        post_data = {
            "title": "Test Title",
            "content": "Content is here!Content is here!"
                       "Content is here!Content is here!"
                       "Content is here!",
            "subtitle": "Subtitle is here!",
        }
        response = self.client.post(
            f"{self._blueprint_url}/makeNotification",
            data=json.dumps(post_data),
            content_type="application/json",
        )
        json_dict = json.loads(response.data)
        self.assertEqual(json_dict["retCode"], "999999")
