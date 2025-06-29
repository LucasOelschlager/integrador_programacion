document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector(".form");
  const emailInput = document.getElementById("email_input");
  const passwordInput = document.getElementById("password_input");

  form.addEventListener("submit", function (e) {
    let isValid = true;

    // Validar email
    if (!emailInput.value.trim()) {
      showError("error_email", "El email es obligatorio");
      isValid = false;
    } else if (!isValidEmail(emailInput.value)) {
      showError("error_email", "Ingresa un email válido");
      isValid = false;
    } else {
      hideError("error_email");
    }

    // Validar contraseña
    if (!passwordInput.value.trim()) {
      showError("error_password", "La contraseña es obligatoria");
      isValid = false;
    } else {
      hideError("error_password");
    }

    if (!isValid) {
      e.preventDefault();
    }
  });

  function showError(errorId, message) {
    const errorElement = document.getElementById(errorId);
    errorElement.textContent = message;
    errorElement.style.display = "block";
  }

  function hideError(errorId) {
    const errorElement = document.getElementById(errorId);
    errorElement.style.display = "none";
  }

  function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }
});
