from rest_framework.views import APIView
from rest_framework.response import Response


class HealthCheckView(APIView):
    """
    A simple API view to check the health status of the application.
    """

    def get(self, request):
        return Response({"status": "ok"})