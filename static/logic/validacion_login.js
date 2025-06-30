const login = {
  email: {
    input: document.getElementById("email_input"),
    regex: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
    validacion: function () {
      return (
        this.input.value.trim() !== "" && this.regex.test(this.input.value)
      );
    },
    error: "Ingrese un correo electrónico válido.",
  },
  password: {
    input: document.getElementById("password_input"),
    regex: /^[a-zA-Z0-9!@#$%^&*]{6,16}$/,
    validacion: function () {
      return (
        this.input.value.trim() !== "" && this.regex.test(this.input.value)
      );
    },
    error: "La contraseña debe tener entre 6 y 16 caracteres.",
  },
};

const form = document.querySelector(".form");

function showError(errorId, message) {
  const errorElement = document.getElementById(errorId);
  errorElement.textContent = message;
  errorElement.style.display = "block";
}

function hideError(errorId) {
  const errorElement = document.getElementById(errorId);
  errorElement.style.display = "none";
}

login.email.input.addEventListener("blur", () => {
  const emailOk = login.email.validacion();
  if (!emailOk && login.email.input.value.trim() !== "") {
    showError("error_email", login.email.error);
  } else {
    hideError("error_email");
  }
});

login.email.input.addEventListener("focus", () => {
  hideError("error_email");
});

login.password.input.addEventListener("blur", () => {
  const passwordOk = login.password.validacion();
  if (!passwordOk && login.password.input.value.trim() !== "") {
    showError("error_password", login.password.error);
  } else {
    hideError("error_password");
  }
});

login.password.input.addEventListener("focus", () => {
  hideError("error_password");
});

form.addEventListener("submit", (e) => {
  e.preventDefault();

  let isValid = true;

  const emailOk = login.email.validacion();
  if (!emailOk) {
    if (login.email.input.value.trim() === "") {
      showError("error_email", "El email es obligatorio.");
    } else {
      showError("error_email", login.email.error);
    }
    isValid = false;
  } else {
    hideError("error_email");
  }

  const passwordOk = login.password.validacion();
  if (!passwordOk) {
    if (login.password.input.value.trim() === "") {
      showError("error_password", "La contraseña es obligatoria.");
    } else {
      showError("error_password", login.password.error);
    }
    isValid = false;
  } else {
    hideError("error_password");
  }

  if (isValid) {
    form.submit();
  }
});

login.email.input.addEventListener("input", () => {
  if (login.email.input.value.trim() !== "") {
    hideError("error_email");
  }
});

login.password.input.addEventListener("input", () => {
  if (login.password.input.value.trim() !== "") {
    hideError("error_password");
  }
});
