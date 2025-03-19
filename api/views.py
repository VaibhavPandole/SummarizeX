from openai import OpenAI
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import SummaryBulletPoints
from api.serializers import SummaryBulletPointsSerializer, UserRegistrationSerializer
from summarify import settings

client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)  # Store your API key in Django settings


class UserRegistrationView(APIView):
    """
    A view to register a new user with a username, email, and password.
    """

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenerateSummary(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        text = request.data.get("text")
        if not text:
            return Response({"error": "Text is required"}, status=400)

        # Call OpenAI API for summary
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {
                        "role": "user",
                        "content": f"Summarize the following text:\n{text}",
                    },
                ],
            )

            summary = response["choices"][0]["message"]["content"].strip()
            summary_data = SummaryBulletPoints.objects.create(
                original_text=text, summary=summary, bullet_points=""
            )
            serializer = SummaryBulletPointsSerializer(summary_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=500)


class GenerateBulletPoints(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        text = request.data.get("text")
        if not text:
            return Response({"error": "Text is required"}, status=400)

        # Call OpenAI API for bullet points
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {
                        "role": "user",
                        "content": f"Convert this text into bullet points:\n{text}",
                    },
                ],
            )

            bullet_points = response["choices"][0]["message"]["content"].strip()
            bullet_points_data = SummaryBulletPoints.objects.create(
                original_text=text, summary="", bullet_points=bullet_points
            )
            serializer = SummaryBulletPointsSerializer(bullet_points_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
