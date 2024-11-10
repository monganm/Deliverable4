document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("searchInput");
    const athleteCards = document.querySelectorAll(".athlete");

    searchInput.addEventListener("input", () => {
        const searchTerm = searchInput.value.toLowerCase();
        athleteCards.forEach(card => {
            const athleteName = card.querySelector("h3").textContent.toLowerCase();
            if (athleteName.includes(searchTerm)) {
                card.style.display = "block";
            } else {
                card.style.display = "none";
            }
        });
    });
});
