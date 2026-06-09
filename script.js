const navbar = document.querySelector(".navbar");

window.addEventListener("scroll", function () {

    if (window.scrollY > 100) {
        navbar.classList.add("sticky");
    } else {
        navbar.classList.remove("sticky");
    }

});
const themeBtn = document.getElementById("themeBtn");
const body = document.body;

themeBtn.addEventListener("click", function(){

    body.classList.toggle("dark-mode");

});
const hiddenElements = document.querySelectorAll(".hidden");

const observer = new IntersectionObserver(function(entries){

    entries.forEach(function(entry){

        if(entry.isIntersecting){

            entry.target.classList.add("show");

        }

    });

});

hiddenElements.forEach(function(element){

    observer.observe(element);

});
 