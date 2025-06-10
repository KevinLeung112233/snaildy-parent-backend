document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('input[name=q][autofocus]');
    if (searchInput) {
        searchInput.removeAttribute('autofocus');
    }
});
