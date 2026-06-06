const topbar = document.querySelector(".topbar");

window.addEventListener("scroll", () => {
  topbar.style.boxShadow = window.scrollY > 12
    ? "0 10px 30px rgba(23, 32, 29, 0.08)"
    : "none";
});
