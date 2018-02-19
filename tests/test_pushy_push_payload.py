import mock
import json
from django.test import TestCase
from push_notifications.pushy import (
    pushy_send_message,
    pushy_send_bulk_message
)
from tests.mock_responses import (
    PUSHY_JSON_RESPONSE,
    PUSHY_MULTIPLE_JSON_RESPONSE
)


class PushyPushPayloadTest(TestCase):
    def test_push_payload(self):
        with mock.patch("push_notifications.pushy._pushy_send",
                        return_value=PUSHY_JSON_RESPONSE) as p:
            pushy_send_message("abc", {"message": "Hello world"})
            p.assert_called_once_with(
                b'{"data":{"message":"Hello world"},"registration_ids":["abc"]}',
                "application/json"
            )

    def test_push_nested_payload(self):
        with mock.patch("push_notifications.pushy._pushy_send",
                        return_value=PUSHY_JSON_RESPONSE) as p:
            payload = {
                "message": "Hello world",
                "extra": {
                    "key0": ["value0_0", "value0_1", "value0_2"],
                    "key1": "value1",
                    "key2": {"key2_0": "value2_0"}
                }
            }
            payload_string = json.dumps(payload,
                                        separators=(",", ":"),
                                        sort_keys=True).encode("utf-8")
            pushy_send_message("abc", payload)
            p.assert_called_once_with(
                b'{"data":' + payload_string + b',"registration_ids":["abc"]}',
                "application/json")

    def test_bulk_push_payload(self):
        with mock.patch("push_notifications.pushy._pushy_send",
                        return_value=PUSHY_MULTIPLE_JSON_RESPONSE) as p:
            pushy_send_bulk_message(["abc", "123"], {"message": "Hello world"})
            p.assert_called_once_with(
                b'{"data":{"message":"Hello world"},"registration_ids":["abc","123"]}',
                "application/json")


class PushyPushPayloadTestCustomKey(TestCase):
    def test_push_payload(self):
        with mock.patch("push_notifications.pushy._pushy_send",
                        return_value=PUSHY_JSON_RESPONSE) as p:
            pushy_send_message("abc", {"message": "Hello world"}, key="MY_KEY")
            p.assert_called_once_with(
                b'{"data":{"message":"Hello world"},"registration_ids":["abc"]}',
                "application/json",
                "MY_KEY"
            )

    def test_push_nested_payload(self):
        with mock.patch("push_notifications.pushy._pushy_send",
                        return_value=PUSHY_JSON_RESPONSE) as p:
            payload = {
                "message": "Hello world",
                "extra": {
                    "key0": ["value0_0", "value0_1", "value0_2"],
                    "key1": "value1",
                    "key2": {"key2_0": "value2_0"}
                }
            }
            payload_string = json.dumps(payload,
                                        separators=(",", ":"),
                                        sort_keys=True).encode("utf-8")
            pushy_send_message("abc", payload, key="MY_KEY")
            p.assert_called_once_with(
                b'{"data":' + payload_string + b',"registration_ids":["abc"]}',
                "application/json",
                "MY_KEY"
            )

    def test_bulk_push_payload(self):
        with mock.patch("push_notifications.pushy._pushy_send",
                        return_value=PUSHY_MULTIPLE_JSON_RESPONSE) as p:
            pushy_send_bulk_message(
                ["abc", "123"],
                {"message": "Hello world"},
                key="MY_KEY"
            )
            p.assert_called_once_with(
                b'{"data":{"message":"Hello world"},"registration_ids":["abc","123"]}',
                "application/json",
                "MY_KEY"
            )
