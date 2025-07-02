const login = {
  email: {
    input: document.getElementById("email_input"),
    regex: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
    validacion: function () {
      return this.regex.test(this.input.value);
    },
    error: "Ingrese un correo electrónico válido.",
  },
  password: {
    input: document.getElementById("password_input"),
    regex: /^[a-zA-Z0-9!@#$%^&*]{6,16}$/,
    validacion: function () {
      return this.regex.test(this.input.value);
    },
    error: "La contraseña debe tener entre 6 y 16 caracteres.",
  },
};

const form = document.querySelector(".form");

form.addEventListener("submit", (e) => {
  let isValid = true;

  // Validar email
  const emailOk = login.email.validacion();
  const emailError = document.getElementById("error_email");
  if (!emailOk) {
    emailError.style.display = "block";
    emailError.textContent = login.email.error;
    isValid = false;
  } else {
    emailError.style.display = "none";
  }

  // Validar contraseña
  const passwordOk = login.password.validacion();
  const passwordError = document.getElementById("error_password");
  if (!passwordOk) {
    passwordError.style.display = "block";
    passwordError.textContent = login.password.error;
    isValid = false;
  } else {
    passwordError.style.display = "none";
  }

  // Solo prevenir si hay errores
  if (!isValid) {
    e.preventDefault();
  }
});
