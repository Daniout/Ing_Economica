document.addEventListener("DOMContentLoaded", function() {
    var btnInteresSimple = document.querySelector("#btn-interes-simple");
    var submenuInteresSimple = document.querySelector("#submenu-interes-simple");

    // Ocultar el submenu al cargar la página
    submenuInteresSimple.style.display = "none";

    // Mostrar u ocultar el submenu al hacer clic en el botón
    btnInteresSimple.addEventListener("click", function() {
        if (submenuInteresSimple.style.display === "none") {
            submenuInteresSimple.style.display = "block";

        } else {
            submenuInteresSimple.style.display = "none";
        }
    });
});

