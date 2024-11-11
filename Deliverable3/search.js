document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("searchInput");
    const athleteCards = document.querySelectorAll(".athlete");

    searchInput.addEventListener("input", () => {
        const searchTerm = searchInput.value.toLowerCase();
        athleteCards.forEach(card => {
            const athleteName = card.querySelector("h3").textContent.toLowerCase();
            if (athleteName.includes(searchTerm)) {
                card.style.display = ""; // Reset to default display style
            } else {
                card.style.display = "none"; // Hide if no match
            }
        });
    });
});
