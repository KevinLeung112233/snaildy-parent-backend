(function($) {
    $(document).ready(function() {
        function toggleTimeSlotInline() {
            if ($('#id_need_timeslot').is(':checked')) {
                $('.inline-group.timeslot-inline').show();
            } else {
                $('.inline-group.timeslot-inline').hide();
            }
        }

        // Initial toggle on page load
        toggleTimeSlotInline();

        // Toggle on checkbox change
        $('#id_need_timeslot').change(function() {
            toggleTimeSlotInline();
        });
    });
})(django.jQuery);
