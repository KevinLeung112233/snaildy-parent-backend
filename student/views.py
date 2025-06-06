import uuid
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.cache import cache

from .models import StudentSession


class BindStudentView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    SESSION_TTL = 60 * 60 * 24 * 30  # 30 days

    def generate_session_id(self):
        return str(uuid.uuid4())

    def store_stu_token_for_session(self, session_id, jwt_token, refresh_token, user_id):
        # Store a dict with token and user_id for binding
        cache.set(
            session_id,
            {
                "student_token": jwt_token,
                "refresh_token": refresh_token,
                "user_id": user_id,
            },
            timeout=self.SESSION_TTL,
        )

    def get_stu_token_for_session(self, session_id):
        return cache.get(session_id)

    def delete_session(self, session_id):
        cache.delete(session_id)

    def post(self, request):
        external_jwt = request.data.get("student_token")
        external_refresh_jwt = request.data.get("refresh_token")
        strn = request.data.get("strn")
        id_no = request.data.get("id_no")

        if not external_jwt:
            return Response(
                {"detail": "student_token required"}, status=status.HTTP_400_BAD_REQUEST
            )

        user = request.user  # Authenticated user from your server

        session_id = self.generate_session_id()

        # Store external JWT along with user ID for binding
        self.store_stu_token_for_session(
            session_id, external_jwt, external_refresh_jwt, user.id)

        # Create StudentSession record with optional strn and id_no
        StudentSession.objects.create(
            user=user,
            session_id=session_id,
            strn=strn if strn else None,
            id_no=id_no if id_no else None,
        )

        return Response({"session_id": session_id})


class GetAllBindedStudentTokensView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Get all sessions bound to this user
        sessions = StudentSession.objects.filter(user=user)

        if not sessions.exists():
            return Response(
                {"detail": "No bound student sessions found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        tokens_list = []
        for session in sessions:
            cached_data = cache.get(session.session_id)
            if cached_data:
                tokens_list.append(
                    {
                        "session_id": session.session_id,
                        "student_token": cached_data.get("student_token"),
                        "refresh_token": cached_data.get("refresh_token"),
                        "user_id": cached_data.get("user_id"),
                        "strn": session.strn,
                        "id_no": session.id_no,
                    }
                )

        if not tokens_list:
            return Response(
                {"detail": "No active cached tokens found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(tokens_list)
