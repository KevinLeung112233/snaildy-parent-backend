document.addEventListener('DOMContentLoaded', function () {
  flatpickr('.datetimepicker', {
    enableTime: true,
    dateFormat: "Y-m-d H:i",
    time_24hr: true,
  });
});
