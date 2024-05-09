var flashMessage = "{{get_flashed_messages()}}";
window.addEventListener("DOMContentLoaded", () => {
  if (flashMessage.length === 2) {
    document.getElementById("flash").style.display = "none";
    console.log("hellas");
  } else {
    document.getElementById("flash").style.display = "";
  }
});

const activePage = window.location.pathname;
const navLinks = document.querySelectorAll("nav a").forEach((link) => {
  if (link.href.includes(`${activePage}`)) {
    link.classList.add("active");
  }
});

window.addEventListener("DOMContentLoaded", () => {
  var menuButton = document.getElementById("menuButton");
  console.log("hello");
  function navBar() {
    var x = document.getElementById("topNav");
    if (x.className === "nav-bar") {
      x.className += " responsive";
    } else {
      x.className = "nav-bar";
    }
    console.log("hello");
  }

  menuButton.addEventListener("click", navBar);
});
