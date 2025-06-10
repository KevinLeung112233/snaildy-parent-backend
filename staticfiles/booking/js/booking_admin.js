(function($) {
    // CSRF token setup
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        xhrFields: { withCredentials: true },
        headers: { "X-CSRFToken": csrftoken }
    });

    $(document).ready(function() {
        $('#id_service').change(function() {
            var serviceId = $(this).val();
            var timeslotUrl = window.location.pathname + 'get-timeslots/';
            console.log("Timeslot URL:", timeslotUrl);

            if (!serviceId) {
                $('#id_time_slot').empty();
                return;
            }

            $.ajax({
                url: timeslotUrl,
                data: { 'service': serviceId },
                success: function(data) {
                    var timeSlotSelect = $('#id_time_slot');
                    timeSlotSelect.empty();

                    if (!data || !data.timeslots) {
                        console.error("Invalid AJAX response:", data);
                        alert('取得時段失敗，請稍後再試。');
                        return;
                    }
                    
                    if (data.timeslots.length === 0) {
                        timeSlotSelect.append($('<option></option>').text('無可用時段').attr('value', ''));
                    } else {
                        $.each(data.timeslots, function(index, timeslot) {
                            timeSlotSelect.append(
                                $('<option></option>')
                                    .attr('value', timeslot.id)
                                    .attr('data-service-id', timeslot.service_id)
                                    .text(timeslot.display)
                            );
                        });
                    }
                },
                error: function(xhr, status, error) {
                    console.error("AJAX Error:", status, error);
                    alert('取得時段失敗，請稍後再試。');
                }
            });
        });

        // Auto-fill service when time_slot changes
        $('#id_time_slot').change(function() {
            var selectedOption = $(this).find('option:selected');
            var serviceId = selectedOption.data('service-id');
            if (serviceId) {
                $('#id_service').val(serviceId).trigger('change');
            }
        });
    });
})(django.jQuery);
