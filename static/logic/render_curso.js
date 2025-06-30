const cards_container = document.querySelector(".container");
let element;
cards_container.addEventListener("click", (e) => {
  const focus = e.target;
  if (focus.classList.contains("button")) {
    element = focus.parentElement;
    renderCurso(element.id);
  }
});
