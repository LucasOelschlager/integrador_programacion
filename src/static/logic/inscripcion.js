const campoNombre = document.querySelector("[name=nombre]");
const campoApellido = document.querySelector("[name=apellido]");
const campoEmail = document.querySelector("[name=email]");
const campoDireccion = document.querySelector("[name=direccion]");

const setErrors = (message, campo, isError = true) => {
    if (isError) {
      campo.classList.add("invalid");
      campo.nextElementSibling.classList.add("error");
      campo.nextElementSibling.innerText = message;
    } else {
      campo.classList.remove("invalid");
      campo.nextElementSibling.classList.remove("error");
      campo.nextElementSibling.innerText = "";
    }
  }
  const validarCampoVacio = (message, e) => {
    const campo = e.target;
    const evaluarCampo = e.target.value;
    if (evaluarCampo.trim().length === 0) {
      setErrors(message, campo);
    } else {
      setErrors("", campo, false);
    }
  }

  const validarEmail = e => {
    const campo = e.target;
    const evaluarCampo = e.target.value;
    const regex = new RegExp(/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/);
    if (evaluarCampo.trim().length > 5 && !regex.test(evaluarCampo)) {
      setErrors("Please enter a valid email", campo);
    } else {
      setErrors("", campo, false);
    }
  }
  campoNombre.addEventListener("blur", (e) => validarCampoVacio("Escriba su nombre!", e));
  campoApellido.addEventListener("blur", (e) => validarCampoVacio("Escriba su apellido!", e));
  campoEmail.addEventListener("blur", (e) => validarCampoVacio("Escriba su mail!", e));
  campoDireccion.addEventListener("blur", (e) => validarCampoVacio("Escriba su direccion!", e));
  campoMensaje.addEventListener("blur", (e) => validarCampoVacio("Escriba su mensaje!", e));

  emailField.addEventListener("input", validarEmail);
