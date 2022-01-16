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

// SETTINGS BOX
const toggleIcon = document.querySelector(".fa-cog");
const settingBox = document.querySelector(".setting-box");
const settingBoxToggle = document.querySelector(".setting-box-toggle");

settingBoxToggle.addEventListener("click", togglebox);

function togglebox() {
    toggleIcon.classList.toggle("fa-spin");
    settingBox.classList.toggle("open");
}

// LIGHT MODE ADN DARK MODE
const colorList = document.querySelectorAll(".mode li");
let mainColor = localStorage.getItem("color_option");
let mainFontColor = localStorage.getItem("font_color_option");
let backgroundColor = localStorage.getItem("background_color_option");

if (mainColor !== null) {
    document.documentElement.style.setProperty('--main-ele-color', localStorage.getItem(mainColor));
    document.documentElement.style.setProperty('--main-font-color', localStorage.getItem(mainFontColor));
    document.documentElement.style.setProperty('--main-bg-color', localStorage.getItem(backgroundColor));
}

colorList.forEach( li => {
    li.addEventListener("click", (e) => {
        document.documentElement.style.setProperty('--main-ele-color', e.target.dataset.color);
        document.documentElement.style.setProperty('--main-font-color', e.target.dataset.font);
        document.documentElement.style.setProperty('--main-bg-color', e.target.dataset.background);
        // LOCAL STORAGE
        localStorage.setItem(mainColor, e.target.dataset.color);
        localStorage.setItem(mainFontColor, e.target.dataset.font);
        localStorage.setItem(backgroundColor, e.target.dataset.background);
    });
});

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