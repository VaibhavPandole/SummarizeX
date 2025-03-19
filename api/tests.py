from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.test import APITestCase

from api.models import SummaryBulletPoints


class GenerateSummaryTestCase(APITestCase):
    def setUp(self):
        self.username = "testuser"
        self.password = "password123"
        self.email = "testuser@example.com"
        self.user = get_user_model().objects.create_user(
            username=self.username, password=self.password, email=self.email
        )
        # Get the token for the user using the TokenObtainPairView
        self.token_url = reverse("token_obtain_pair")
        self.token_response = self.client.post(
            self.token_url, {"username": self.username, "password": self.password}
        )

        # Extract the access token from the response
        self.token = self.token_response.data["access"]
        self.url = reverse(
            "generate-summary"
        )  # Make sure your URL name is correctly set
        self.valid_data = {
            "text": "This is a long paragraph that we want to summarize."
        }
        self.invalid_data = {"text": ""}  # Empty text should return an error

    @patch("api.views.client.chat.completions.create")
    @patch("api.views.GenerateSummary.permission_classes")
    def test_generate_summary_success(self, mock_permission, mock_openai_response):
        # Mock the permission class to bypass authentication
        mock_permission.return_value = [IsAuthenticated]
        # Mock the OpenAI response
        mock_openai_response.return_value = {
            "choices": [
                {"message": {"content": "This is a short summary of the input text."}}
            ]
        }

        # Make a POST request to the endpoint
        response = self.client.post(
            self.url, self.valid_data, HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        # Check for success status
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("summary", response.data)
        self.assertEqual(
            response.data["summary"], "This is a short summary of the input text."
        )

        # Verify that the data has been saved in the database
        summary = SummaryBulletPoints.objects.first()
        self.assertEqual(summary.original_text, self.valid_data["text"])
        self.assertEqual(summary.summary, "This is a short summary of the input text.")
        self.assertEqual(summary.bullet_points, "")

    def test_generate_summary_missing_text(self):
        # Missing text should return a 400 status with error message
        response = self.client.post(
            self.url, self.invalid_data, HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Text is required")

    @patch("api.views.client.chat.completions.create")
    def test_generate_summary_openai_error(self, mock_openai_response):
        # Simulate an OpenAI error by raising an exception
        mock_openai_response.side_effect = Exception("OpenAI API failed")

        # Make a POST request to the endpoint
        response = self.client.post(
            self.url, self.valid_data, HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        # Check for error response
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "OpenAI API failed")


class GenerateBulletPointsTestCase(APITestCase):
    def setUp(self):
        self.username = "testuser"
        self.password = "password123"
        self.email = "testuser@example.com"
        self.user = get_user_model().objects.create_user(
            username=self.username, password=self.password, email=self.email
        )
        # Get the token for the user using the TokenObtainPairView
        self.token_url = reverse("token_obtain_pair")
        self.token_response = self.client.post(
            self.token_url, {"username": self.username, "password": self.password}
        )

        # Extract the access token from the response
        self.token = self.token_response.data["access"]
        self.url = reverse(
            "generate-bullet-points"
        )  # Make sure your URL name is correctly set
        self.valid_data = {
            "text": "This is a long paragraph that we want to convert into bullet points."
        }
        self.invalid_data = {"text": ""}  # Empty text should return an error

    @patch("api.views.client.chat.completions.create")
    def test_generate_bullet_points_success(self, mock_openai_response):
        # Mock the OpenAI response
        mock_openai_response.return_value = {
            "choices": [{"message": {"content": "• Point 1\n• Point 2\n• Point 3"}}]
        }

        # Make a POST request to the endpoint
        response = self.client.post(
            self.url, self.valid_data, HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        # Check for success status
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("bullet_points", response.data)
        self.assertEqual(
            response.data["bullet_points"], "• Point 1\n• Point 2\n• Point 3"
        )

        # Verify that the data has been saved in the database
        bullet_points = SummaryBulletPoints.objects.first()
        self.assertEqual(bullet_points.original_text, self.valid_data["text"])
        self.assertEqual(bullet_points.summary, "")
        self.assertEqual(bullet_points.bullet_points, "• Point 1\n• Point 2\n• Point 3")

    def test_generate_bullet_points_missing_text(self):
        # Missing text should return a 400 status with error message
        response = self.client.post(
            self.url, self.invalid_data, HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Text is required")

    @patch("api.views.client.chat.completions.create")
    def test_generate_bullet_points_openai_error(self, mock_openai_response):
        # Simulate an OpenAI error by raising an exception
        mock_openai_response.side_effect = Exception("OpenAI API failed")

        # Make a POST request to the endpoint
        response = self.client.post(
            self.url, self.valid_data, HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        # Check for error response
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "OpenAI API failed")


class UserRegistrationTestCase(APITestCase):
    def setUp(self):
        self.url = reverse(
            "user-register"
        )  # Adjust URL name as per your implementation
        self.valid_data = {
            "email": "testuser@example.com",
            "password": "password123",
        }
        self.invalid_data = {
            "email": "invalidemail",
            "password": "short",
        }

    def test_user_registration_success(self):
        # Test successful user registration
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "User registered successfully")

    def test_user_registration_invalid_data(self):
        # Test user registration with invalid data
        response = self.client.post(self.url, self.invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
