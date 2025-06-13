import uuid
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.cache import cache
from .serializers import StudentCreateSerializer
from rest_framework import generics, permissions
import requests
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth import get_user_model
from school.models import School
from student.models import Student, Grade  # Assuming Grade model exists
from django.db import transaction
from .models import StudentSession


class StudentCreateAPIView(generics.CreateAPIView):
    serializer_class = StudentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Set the parent to the currently authenticated user
        serializer.save(parent=self.request.user)


# 校本 student acc
class BindStudentView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    SESSION_TTL = 60 * 60 * 24 * 30  # 30 days

    def generate_session_id(self):
        return str(uuid.uuid4())

    def store_stu_token_for_session(self, session_id, jwt_token, refresh_token, user_id):
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

    def call_external_api_and_create_students(self, token, user):
        external_api_url = 'https://school.snaildiverse.com/api/parent-portal/students/'
        headers = {
            'Authorization': f'Bearer {token}',
            'Accept': 'application/json',
        }

        try:
            response = requests.get(
                external_api_url, headers=headers, timeout=10)
            response.raise_for_status()
            students_data = response.json()
            print("External API response:", response)
        except Exception as e:
            print("Error fetching external data:", e)
            return []

        created_students = []

        with transaction.atomic():
            for record in students_data:
                data = {
                    'chinese_name': record.get('zhName'),
                    'english_name': record.get('enName'),
                    # 'parent': user,
                }
                print("Processing student data:", data)

                school_name = record.get('schoolName')
                if not data['chinese_name'] or not data['english_name']:
                    print(
                        f"Skipping record due to missing required fields: {record}")
                    continue

                try:
                    school = School.objects.get(name_cn=school_name.strip(
                    )) if school_name and school_name.strip() else None
                except School.DoesNotExist:
                    school = None

                if school:
                    data['school'] = school.id

                class_name = record.get('className')
                class_no = record.get('classNo')
                grade = None

                if class_name and class_name.strip() and school:
                    grade = Grade.objects.filter(
                        name=class_name.strip(), school=school).first()

                if not grade and class_no is not None and school:
                    try:
                        class_no_int = int(class_no)
                        grade = Grade.objects.filter(
                            number=class_no_int, school=school).first()
                    except (ValueError, TypeError):
                        print(
                            f"Invalid classNo value: {class_no} in record: {record}")

                if grade:
                    data['grade'] = grade.id

                print("Final student data for serializer:", data)

                serializer = StudentCreateSerializer(
                    data=data, context={'request': self.request})
                try:
                    if serializer.is_valid():
                        student = serializer.save(parent=user)
                        created_students.append(student)
                        print(f"Created student: {student}")
                    else:
                        print("Validation errors:", serializer.errors)
                except Exception as e:
                    print(f"Serializer exception: {e}")
                    continue

        return created_students

    def post(self, request):
        external_jwt = request.data.get("student_token")
        external_refresh_jwt = request.data.get("refresh_token")
        strn = request.data.get("strn")
        id_no = request.data.get("id_no")

        if not external_jwt:
            return Response({"detail": "student_token required"}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        session_id = self.generate_session_id()

        # Store external JWT along with user ID for binding
        self.store_stu_token_for_session(
            session_id, external_jwt, external_refresh_jwt, user.id)

        # Call external API to get student info and create students
        created_students = self.call_external_api_and_create_students(
            external_jwt, user)

        # Create StudentSession for each created student
        for student in created_students:
            StudentSession.objects.create(
                user=user,
                session_id=session_id,
                student=student,
                strn=strn if strn else None,
                id_no=id_no if id_no else None,
            )

        return Response({
            "session_id": session_id,
            "created_students_count": len(created_students),
            "created_students": [
                {
                    "id": s.id,
                    "chinese_name": s.chinese_name,
                    "english_name": s.english_name,
                } for s in created_students
            ],
        })


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
