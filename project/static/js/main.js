// NAVBAR
const hamburger = document.querySelector(".hamburger");
const navMenu = document.querySelector(".nav-menu");

hamburger.addEventListener("click", mobileMenu);

function mobileMenu() {
    hamburger.classList.toggle("active");
    navMenu.classList.toggle("active");
}
const navLink = document.querySelectorAll(".nav-link");

navLink.forEach(n => n.addEventListener("click", closeMenu));

function closeMenu() {
    hamburger.classList.remove("active");
    navMenu.classList.remove("active");
}

// SEARCH FORM
let searchButton = document.getElementById('search-button');
let searchForm = document.getElementById('search-form');
let searchClose = document.getElementById('search-close');

searchButton.onclick = () => {
  searchForm.classList.add('active');
}

searchClose.onclick = () => {
  searchForm.classList.remove('active');
}

// USER MANAGEMENT BUTTON
const userButton = document.querySelector('.user-btn');
const userMenu = document.querySelector('.user-menu');

userButton.onclick = () => {
  userMenu.classList.toggle('active');
}

// DROPDOWN
let dropdownBtn = document.querySelector('.menu-btn');
let menuContent = document.querySelector('.menu-content');
dropdownBtn.addEventListener('click',()=>{
    if(menuContent.style.display===""){
        menuContent.style.display="block";
    } else {
        menuContent.style.display="";
    }
})
