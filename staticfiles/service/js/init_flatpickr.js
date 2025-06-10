document.addEventListener('DOMContentLoaded', function() {
    // Initialize flatpickr on all inputs with class 'datetimepicker'
    flatpickr(".datetimepicker", {
        enableTime: true,
        dateFormat: "Y-m-d H:i",
        time_24hr: true,
        plugins: [new confirmDatePlugin({})]  // Optional: confirm date plugin
    });
});
