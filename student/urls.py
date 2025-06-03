from django.urls import path
from .views import BindStudentView, GetAllBindedStudentTokensView
from django.urls import path


urlpatterns = [
    path('bind-student/', BindStudentView.as_view(), name='bind_student'),
    path('get-all-binded-student-tokens/', GetAllBindedStudentTokensView.as_view(),
         name='get-student-tokens'),
]
