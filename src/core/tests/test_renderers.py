import json
from http import HTTPMethod
from django.test import SimpleTestCase
from rest_framework.test import APIRequestFactory
from rest_framework.response import Response


from core.renderers import EnvelopeJSONRenderer, get_response_message


class TestEnvelopeJSONRenderer(SimpleTestCase):
    def get_renderer_context(self, status_code, method=HTTPMethod.GET):
        request = APIRequestFactory().generic(method, "/")
        response = Response(status=status_code)
        return {"request": request, "response": response}

    def json_to_dict(self, json_str):
        return json.loads(json_str)

    def test_success_response(self):
        data = {"key": "value"}
        response_json = EnvelopeJSONRenderer().render(
            data, renderer_context=self.get_renderer_context(200)
        )
        response_dict = self.json_to_dict(response_json)

        self.assertIn("status", response_dict)
        self.assertIn("message", response_dict)
        self.assertIn("data", response_dict)
        self.assertEqual(response_dict["status"], True)
        self.assertEqual(response_dict["data"], data)

    def test_error_response(self):
        data = {"key": "value"}
        response_json = EnvelopeJSONRenderer().render(
            data, renderer_context=self.get_renderer_context(400)
        )
        response_dict = self.json_to_dict(response_json)

        self.assertIn("status", response_dict)
        self.assertIn("errors", response_dict)
        self.assertIn("message", response_dict)
        self.assertEqual(response_dict["status"], False)
        self.assertEqual(response_dict["errors"], ["value"])
        self.assertEqual(response_dict["message"], "value")

    def test_get_response_message(self):
        context = self.get_renderer_context(200)
        message = get_response_message(**context)
        self.assertEqual(message, "Successfully retrieved")

        context = self.get_renderer_context(200, HTTPMethod.PUT)
        message = get_response_message(**context)
        self.assertEqual(message, "Successfully updated")

        context = self.get_renderer_context(201)
        message = get_response_message(**context)
        self.assertEqual(message, "Successfully created")

        context = self.get_renderer_context(400)
        message = get_response_message(**context)
        self.assertEqual(message, "Validation errors")

        context = self.get_renderer_context(401)
        message = get_response_message(**context)
        self.assertEqual(message, "Authentication credentials were not provided")

        context = self.get_renderer_context(403)
        message = get_response_message(**context)
        self.assertEqual(message, "You do not have permission to perform this action")

        context = self.get_renderer_context(404)
        message = get_response_message(**context)
        self.assertEqual(message, "Resource not found")

        context = self.get_renderer_context(500)
        message = get_response_message(**context)
        self.assertEqual(message, "Internal server error")
