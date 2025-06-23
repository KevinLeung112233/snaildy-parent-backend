# from django.urls import reverse
# from django_select2.forms import ModelSelect2MultipleWidget

# from student.models import Student


# class StudentWidget(ModelSelect2MultipleWidget):
#     model = Student
#     search_fields = ['chinese_name__icontains', 'english_name__icontains']

#     def get_url(self):
#         return reverse('admin:student_student_autocomplete')

#     def filter_queryset(self, term, queryset=None, **dependent_fields):
#         # You can override this to filter by dependent_fields['parent']
#         parent_id = self.data.get('user') or self.attrs.get('data-parent-id')
#         if parent_id:
#             queryset = queryset.filter(parent_id=parent_id)
#         return super().filter_queryset(term, queryset)
