from django.urls import path
from .views import BindStudentView, GetAllBindedStudentTokensView, StudentAutocomplete
from django.urls import path
from .views import StudentCreateAPIView


urlpatterns = [
    path('bind-student/', BindStudentView.as_view(), name='bind_student'),
    path('get-all-binded-student-tokens/', GetAllBindedStudentTokensView.as_view(),
         name='get-student-tokens'),
    path('add/', StudentCreateAPIView.as_view(), name='student-add'),
    # path(
    #     'student/autocomplete/',
    #     StudentAutocomplete.as_view(),
    #     name='student_student_autocomplete'
    # ),
]
