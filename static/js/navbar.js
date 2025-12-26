document.addEventListener("DOMContentLoaded", function () {
    const dropdown = document.getElementById("navbarDropdown");

    if (dropdown) {
        dropdown.addEventListener("shown.bs.dropdown", function () {
            window.scrollBy({
                top: 180,
                behavior: "smooth"
            });
        });
    }
});
