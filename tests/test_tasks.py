import json
from unittest.mock import patch

from django.test import TestCase

from django_amazon_sns_mobile_push_notification.models import Device, Log
from django_amazon_sns_mobile_push_notification.tasks import (
    deregister_device,
    refresh_device,
    register_device,
    send_sns_mobile_push_notification_to_device,
)


class TestNotificationTasks(TestCase):
    @classmethod
    def setUpClass(cls):
        Device.objects.all().delete()
        Log.objects.all().delete()

    @classmethod
    def tearDownClass(cls):
        Device.objects.all().delete()
        Log.objects.all().delete()

    @patch("django_amazon_sns_mobile_push_notification.models.Client")
    def test_register(self, mock_Client):
        Log.objects.all().delete()
        token = "token"
        device = Device.objects.create(token=token, os=Device.ANDROID_OS, arn="arn")

        mock_response = {"EndpointArn": "arn"}
        mock_Client().create_android_platform_endpoint.return_value = mock_response
        response = register_device(device)
        device.refresh_from_db()
        self.assertEquals(response["EndpointArn"], mock_response["EndpointArn"])
        self.assertEquals(device.arn, mock_response["EndpointArn"])

    @patch("django_amazon_sns_mobile_push_notification.models.Client")
    def test_refresh_when_enabled(self, mock_Client):
        Log.objects.all().delete()
        token = "token"
        device = Device.objects.create(token=token, os=Device.ANDROID_OS, arn="arn")
        mock_response = {"Enabled": "true", "Token": token}
        mock_Client().retrieve_platform_endpoint_attributes.return_value = mock_response
        mock_Client().delete_platform_endpoint.return_value = ""
        response = refresh_device(device)
        self.assertEquals(response, mock_response)
        self.assertEquals(device.token, mock_response["Token"])

    @patch("django_amazon_sns_mobile_push_notification.models.Client")
    def test_refresh_when_disabled(self, mock_Client):
        Log.objects.all().delete()
        token = "token"
        device = Device.objects.create(token=token, os=Device.ANDROID_OS, arn="arn")
        mock_response_1 = {"Enabled": "false", "Token": token}
        mock_Client().retrieve_platform_endpoint_attributes.return_value = (
            mock_response_1
        )
        mock_response_2 = {"EndpointArn": "arn"}
        mock_Client().create_android_platform_endpoint.return_value = mock_response_2
        mock_Client().delete_platform_endpoint.return_value = ""
        response = refresh_device(device)
        self.assertEquals(response, mock_response_1)
        self.assertEquals(device.arn, mock_response_2["EndpointArn"])

    @patch("django_amazon_sns_mobile_push_notification.models.Client")
    def test_deregister(self, mock_Client):
        Log.objects.all().delete()
        token = "token"
        device = Device.objects.create(token=token, os=Device.ANDROID_OS, arn="arn")
        mock_Client().delete_platform_endpoint.return_value = None
        deregister_device(device)
        self.assertEquals(True, True)

    @patch("django_amazon_sns_mobile_push_notification.models.Client")
    def test_publish_to_android(self, mock_Client):
        Log.objects.all().delete()
        token = "token"
        device = Device.objects.create(token=token, os=Device.ANDROID_OS, arn="arn")

        mock_response = (
            "message",
            {
                "EndpointArn": "arn",
                "ResponseMetadata": {
                    "RetryAttempts": 0,
                    "HTTPHeaders": {
                        "x-amzn-requestid": "e08722bb-4218-5b6a-8e55-71fa82e9ffc3",
                        "content-length": "424",
                        "date": "Fri, 06 Apr 2018 18:38:40 GMT",
                        "content-type": "text/xml",
                    },
                    "HTTPStatusCode": 200,
                    "RequestId": "e08722bb-4218-5b6a-8e55-71fa82e9ffc3",
                },
            },
        )
        mock_Client().publish_to_android.return_value = mock_response
        response = send_sns_mobile_push_notification_to_device(
            device=device,
            notification_type="type",
            text="text",
            data={"a": "b"},
            title="title",
        )
        self.assertEquals(response["ResponseMetadata"]["HTTPStatusCode"], 200)

        log = Log.objects.first()
        self.assertEquals(log.device_id, device.id)
        self.assertEquals(log.message, "message")
        self.assertEquals(log.response, json.dumps(mock_response[1]).replace('"', "'"))

    @patch("django_amazon_sns_mobile_push_notification.models.Client")
    def test_publish_to_ios(self, mock_Client):
        Log.objects.all().delete()
        token = "token"
        device = Device.objects.create(token=token, os=Device.IOS_OS, arn="arn")

        mock_response = (
            "message",
            {
                "EndpointArn": "arn",
                "ResponseMetadata": {
                    "RetryAttempts": 0,
                    "HTTPHeaders": {
                        "x-amzn-requestid": "e08722bb-4218-5b6a-8e55-71fa82e9ffc3",
                        "content-length": "424",
                        "date": "Fri, 06 Apr 2018 18:38:40 GMT",
                        "content-type": "text/xml",
                    },
                    "HTTPStatusCode": 200,
                    "RequestId": "e08722bb-4218-5b6a-8e55-71fa82e9ffc3",
                },
            },
        )
        mock_Client().publish_to_ios.return_value = mock_response

        response = send_sns_mobile_push_notification_to_device(
            device=device,
            notification_type="type",
            text="text",
            data={"a": "b"},
            title="title",
            badge=4,
        )
        self.assertEquals(response["ResponseMetadata"]["HTTPStatusCode"], 200)

        log = Log.objects.first()
        self.assertEquals(log.device_id, device.id)
        self.assertEquals(log.message, "message")
        self.assertEquals(log.response, json.dumps(mock_response[1]).replace('"', "'"))
