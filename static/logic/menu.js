const menuIcon = document.querySelector(".ri-menu-line");
const menuDesplegable = document.querySelector(".menu-desplegable");
const closeMenu = document.querySelector(".close-menu");

console.log("Menu icon:", menuIcon);

menuIcon.addEventListener("click", () => {
  menuDesplegable.classList.toggle("visible");
});

if (closeMenu) {
  closeMenu.addEventListener("click", () => {
    menuDesplegable.classList.remove("visible");
  });
}

document.querySelectorAll(".menu-desplegable-list a").forEach((link) => {
  link.addEventListener("click", () => {
    menuDesplegable.classList.remove("visible");
  });
});
