(function($) {
  $(document).ready(function() {
    var $userSelect = $('#id_user');
    var $studentsSelect = $('#id_students');
    var $serviceSelect = $('#id_service');
    var $timeSlotSelect = $('#id_time_slot');
    var lastUserId = null;
    var lastServiceId = null;

    function updateStudents(userId) {
      console.log('updateStudents called with userId:', userId);
      if (!userId) {
        $studentsSelect.val(null).trigger('change');
        $studentsSelect.prop('disabled', true);
        return;
      }
      $studentsSelect.prop('disabled', false);

      $.ajax({
        url: '/admin/booking/booking/get-students-by-parent/',
        data: { parent_id: userId },
        dataType: 'json',
        success: function(data) {
          var selectedValues = $studentsSelect.val() || [];  // get currently selected student IDs

          $studentsSelect.empty();
          if (data.students && data.students.length > 0) {
            $.each(data.students, function(i, student) {
              var option = new Option(student.name, student.id, false, false);
              $studentsSelect.append(option);
            });

            // Re-select previously selected students if they still exist in the new options
            $studentsSelect.val(selectedValues.filter(function(val) {
              return data.students.some(function(student) { return student.id === val; });
            }));

            $studentsSelect.prop('disabled', false);
          } else {
            $studentsSelect.append(new Option('No students available', '', false, false));
            $studentsSelect.prop('disabled', true);
          }
          $studentsSelect.trigger('change');
        },
        error: function() {
          $studentsSelect.empty();
          $studentsSelect.append(new Option('Failed to load students', '', false, false));
          $studentsSelect.prop('disabled', true);
          $studentsSelect.trigger('change');
        }
      });
    }

    function updateTimeSlots(serviceId) {
      console.log('updateTimeSlots called with serviceId:', serviceId);
      if (!serviceId) {
        $timeSlotSelect.val(null).trigger('change');
        $timeSlotSelect.prop('disabled', true);
        return;
      }
      $timeSlotSelect.prop('disabled', false);

      $.ajax({
        url: '/admin/booking/booking/get-timeslots/',
        data: { service: serviceId },
        dataType: 'json',
        success: function(data) {
          var selectedValue = $timeSlotSelect.val();

          $timeSlotSelect.empty();
          if (data.timeslots && data.timeslots.length > 0) {
            $.each(data.timeslots, function(i, ts) {
              var option = new Option(ts.display, ts.id, false, false);
              $timeSlotSelect.append(option);
            });

            // Re-select previously selected time slot if still available
            if (selectedValue && data.timeslots.some(ts => ts.id == selectedValue)) {
              $timeSlotSelect.val(selectedValue);
            } else {
              $timeSlotSelect.val(null);
            }

            $timeSlotSelect.prop('disabled', false);
          } else {
            $timeSlotSelect.append(new Option('No timeslots available', '', false, false));
            $timeSlotSelect.prop('disabled', true);
          }
          $timeSlotSelect.trigger('change');
        },
        error: function() {
          $timeSlotSelect.empty();
          $timeSlotSelect.append(new Option('Failed to load timeslots', '', false, false));
          $timeSlotSelect.prop('disabled', true);
          $timeSlotSelect.trigger('change');
        }
      });
    }

    // Polling function to check for user selection changes
    function pollUserChange() {
      var currentUserId = $userSelect.val();
      if (currentUserId !== lastUserId) {
        console.log('User changed from', lastUserId, 'to', currentUserId);
        lastUserId = currentUserId;
        updateStudents(currentUserId);
      }
    }

    // Polling function to check for service selection changes
    function pollServiceChange() {
      var currentServiceId = $serviceSelect.val();
      if (currentServiceId !== lastServiceId) {
        console.log('Service changed from', lastServiceId, 'to', currentServiceId);
        lastServiceId = currentServiceId;
        updateTimeSlots(currentServiceId);
      }
    }

    // Initial load
    lastUserId = $userSelect.val();
    if (lastUserId) {
      updateStudents(lastUserId);
    } else {
      $studentsSelect.prop('disabled', true);
    }

    lastServiceId = $serviceSelect.val();
    if (lastServiceId) {
      updateTimeSlots(lastServiceId);
    } else {
      $timeSlotSelect.prop('disabled', true);
    }

    // Start polling every 500ms
    setInterval(pollUserChange, 500);
    setInterval(pollServiceChange, 500);
  });
})(django.jQuery);
