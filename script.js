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
document.addEventListener("DOMContentLoaded", () => {
    const filterButtons = document.querySelectorAll(".filter-btn");
    const projectCards = document.querySelectorAll(".project-card-item");
    const currentCountDisplay = document.getElementById("current-count");
    const totalCountDisplay = document.getElementById("total-count");

    // Set initial overall total project count
    totalCountDisplay.textContent = projectCards.length;

    filterButtons.forEach(button => {
        button.addEventListener("click", () => {
            // Remove active style from previous button, apply to clicked one
            document.querySelector(".filter-btn.active").classList.remove("active");
            button.classList.add("active");

            const selectedFilter = button.getAttribute("data-filter");
            let visibleCount = 0;

            projectCards.forEach(card => {
                const cardCategory = card.getAttribute("data-category");

                // Determine eligibility based on 'all' or specific classification match
                if (selectedFilter === "all" || cardCategory === selectedFilter) {
                    // Step 1: Remove structural display hidden tags
                    card.classList.remove("hide-completely");
                    // Step 2: Use a slight timeout to trigger the CSS opacity fade animation
                    setTimeout(() => {
                        card.classList.remove("fade-out");
                    }, 50);
                    visibleCount++;
                } else {
                    // Step 1: Fade out elements smoothly
                    card.classList.add("fade-out");
                    // Step 2: Hide structurally completely after the CSS opacity fade ends (400ms match)
                    setTimeout(() => {
                        card.classList.add("hide-completely");
                    }, 400);
                }
            });

            // Dynamically update the count output metric UI element
            currentCountDisplay.textContent = visibleCount;
        });
    });
});

async function loadGitHubProjects() {

    try {

        const response = await fetch("data/projects.json");
        const repos = await response.json();

        const container = document.getElementById("github-projects-list");

        // Clear any previous content
        container.innerHTML = "";

        repos.forEach(repo => {

            container.innerHTML += `
                <div class="repo-item">

                    <a href="${repo.url}" target="_blank">
                        📁 ${repo.name}
                    </a>

                    <span>${repo.language || "Unknown"}</span>

                </div>
            `;

        });

    }

    catch(error){

        console.error("Unable to load GitHub projects:", error);

    }

}

loadGitHubProjects();