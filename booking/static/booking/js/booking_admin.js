(function($) {
//   $(document).ready(function() {
//     var $userSelect = $('#id_user');
//     var $studentsSelect = $('#id_students');

//     function updateStudentDropdown(userId) {
//       if (!userId) {
//         // Clear selection and disable the field
//         $studentsSelect.val(null).trigger('change');
//         $studentsSelect.prop('disabled', true);
//         return;
//       }

//       $studentsSelect.prop('disabled', false);

//       // Fetch students via AJAX
//       $.ajax({
//         url: '/admin/booking/booking/get-students-by-parent/',
//         data: { parent_id: userId },
//         dataType: 'json',
//         success: function(data) {
//           // Get currently selected student IDs to preserve selection
//           var selected = $studentsSelect.val() || [];

//           // Clear existing options but keep the widget intact
//           $studentsSelect.empty();

//           // Add new options
//           $.each(data.students, function(index, student) {
//             var option = new Option(student.name, student.id, false, selected.includes(student.id.toString()));
//             $studentsSelect.append(option);
//           });

//           // Trigger change to update Select2
//           $studentsSelect.trigger('change');
//         },
//         error: function() {
//           // On error, clear options and disable
//           $studentsSelect.empty().val(null).trigger('change');
//           $studentsSelect.prop('disabled', true);
//         }
//       });
//     }

//     // Listen for user selection changes
//     $userSelect.on('select2:select change', function() {
//       var userId = $(this).val();
//       updateStudentDropdown(userId);
//     });

//     // On page load, initialize students dropdown if user preselected
//     var initialUserId = $userSelect.val();
//     if (initialUserId) {
//       updateStudentDropdown(initialUserId);
//     } else {
//       $studentsSelect.prop('disabled', true);
//     }
//   });
})(django.jQuery);
