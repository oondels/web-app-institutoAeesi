window.addEventListener("DOMContentLoaded", () => {
  const activePage = window.location.pathname;
  const navLinks = document.querySelectorAll("nav a").forEach((link) => {
    if (link.href.includes(`${activePage}`)) {
      link.classList.add("active");
    }
  });

  var menuButton = document.getElementById("menuButton");
  function navBar() {
    var x = document.getElementById("topNav");
    if (x.className === "nav-bar") {
      x.className += " responsive";
    } else {
      x.className = "nav-bar";
    }
  }
  menuButton.addEventListener("click", navBar);
});
