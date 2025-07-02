const register = {
  nombre: {
    input: document.getElementById("nombre_input"),
    regex:
      /^([A-Za-zÑñÁáÉéÍíÓóÚú]+[\'\-]{0,1}[A-Za-zÑñÁáÉéÍíÓóÚú]+)(\s+([A-Za-zÑñÁáÉéÍíÓóÚú]+[\'\-]{0,1}[A-Za-zÑñÁáÉéÍíÓóÚú]+))*$/,
    validacion: function () {
      return this.regex.test(this.input.value);
    },
    error: "Ingrese un nombre válido (solo letras y espacios).",
  },
  apellido: {
    input: document.getElementById("apellido_input"),
    regex:
      /^([A-Za-zÑñÁáÉéÍíÓóÚú]+[\'\-]{0,1}[A-Za-zÑñÁáÉéÍíÓóÚú]+)(\s+([A-Za-zÑñÁáÉéÍíÓóÚú]+[\'\-]{0,1}[A-Za-zÑñÁáÉéÍíÓóÚú]+))*$/,
    validacion: function () {
      return this.regex.test(this.input.value);
    },
    error: "Ingrese un apellido válido (solo letras y espacios).",
  },
  email: {
    input: document.getElementById("email_input"),
    regex: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
    validacion: function () {
      return this.regex.test(this.input.value);
    },
    error: "Ingrese un correo electrónico válido.",
  },
  confirmEmail: {
    input: document.getElementById("email_inputConfirm"),
    validacion: function () {
      return this.input.value === register.email.input.value;
    },
    error: "Los correos electrónicos no coinciden.",
  },
  password: {
    input: document.getElementById("password_input"),
    regex: /^[a-zA-Z0-9!@#$%^&*]{6,16}$/,
    validacion: function () {
      return this.regex.test(this.input.value);
    },
    error: "La contraseña debe tener entre 6 y 16 caracteres.",
  },
  confirmPassword: {
    input: document.getElementById("password_inputConfirm"),
    validacion: function () {
      return this.input.value === register.password.input.value;
    },
    error: "Las contraseñas no coinciden.",
  },
  documento: {
    input: document.getElementById("dni_input"),
    regex: /^[0-9]*$/,
    validacion: function () {
      return this.regex.test(this.input.value);
    },
    error: "Ingrese solo números para el documento.",
  },
};

const form = document.querySelector(".form");
form.addEventListener("submit", (e) => {
  e.preventDefault();

  // Validar todos los campos usando el objeto register
  let isValid = true;

  // Validar nombre
  const nameOk = register.nombre.validacion();
  const nameError = document.getElementById("error_nombre");
  if (!nameOk) {
    nameError.style.display = "block";
    nameError.textContent = register.nombre.error;
    isValid = false;
  } else {
    nameError.style.display = "none";
  }

  // Validar apellido
  const apellidoOk = register.apellido.validacion();
  const apellidoError = document.getElementById("error_apellido");
  if (!apellidoOk) {
    apellidoError.style.display = "block";
    apellidoError.textContent = register.apellido.error;
    isValid = false;
  } else {
    apellidoError.style.display = "none";
  }

  // Validar email
  const emailOk = register.email.validacion();
  const emailError = document.getElementById("error_email");
  if (!emailOk) {
    emailError.style.display = "block";
    emailError.textContent = register.email.error;
    isValid = false;
  } else {
    emailError.style.display = "none";
  }

  // Validar confirmación de email
  const confirmEmailOk = register.confirmEmail.validacion();
  const confirmEmailError = document.getElementById("error_emailConfirm");
  if (!confirmEmailOk) {
    confirmEmailError.style.display = "block";
    confirmEmailError.textContent = register.confirmEmail.error;
    isValid = false;
  } else {
    confirmEmailError.style.display = "none";
  }

  // Validar contraseña
  const passwordOk = register.password.validacion();
  const passwordError = document.getElementById("error_password");
  if (!passwordOk) {
    passwordError.style.display = "block";
    passwordError.textContent = register.password.error;
    isValid = false;
  } else {
    passwordError.style.display = "none";
  }

  // Validar confirmación de contraseña
  const confirmPasswordOk = register.confirmPassword.validacion();
  const confirmPasswordError = document.getElementById("error_passwordConfirm");
  if (!confirmPasswordOk) {
    confirmPasswordError.style.display = "block";
    confirmPasswordError.textContent = register.confirmPassword.error;
    isValid = false;
  } else {
    confirmPasswordError.style.display = "none";
  }

  // Validar documento
  const documentoOk = register.documento.validacion();
  const documentoError = document.getElementById("error_dni");
  if (!documentoOk || register.documento.input.value.length < 8) {
    documentoError.style.display = "block";
    documentoError.textContent = register.documento.error;
    isValid = false;
  } else {
    documentoError.style.display = "none";
  }

  if (!isValid) {
    e.preventDefault();
  }

  // Si todo es válido, enviar el formulario
  if (isValid) {
    form.submit();
  }

  register.nombre.input.addEventListener("blur", () =>
    register.nombre.input.validacion()
  );
  register.nombre.input.addEventListener("focus", () =>
    register.nombre.input.validacion()
  );
});
