document.addEventListener("DOMContentLoaded", function () {
    const stars = document.querySelectorAll("#star-rating .star");
    const animeId = document.querySelector("[data-anime-id]").dataset.animeId;
    const ratingValue = document.getElementById("user-rating-value");
    const ratingResponse = document.getElementById("rating-response");
  
    stars.forEach((star, index) => {
      star.addEventListener("mouseover", () => highlightStars(index + 1));
      star.addEventListener("mouseout", resetStars);
      star.addEventListener("click", () => {
        const score = index + 1;
        fetch("/ratings/rate/", {
          method: "POST",
          headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/x-www-form-urlencoded",
          },
          body: `anime_id=${animeId}&score=${score}`,
        })
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            ratingValue.textContent = `${data.score} / 10`;
            ratingResponse.classList.remove("hidden");
            setTimeout(() => ratingResponse.classList.add("hidden"), 2000);
          }
        });
      });
    });
  
    function highlightStars(score) {
      stars.forEach((s, i) => {
        s.classList.toggle("text-yellow-400", i < score);
        s.classList.toggle("text-gray-300", i >= score);
      });
    }
  
    function resetStars() {
      const current = parseInt(ratingValue.textContent);
      stars.forEach((s, i) => {
        s.classList.toggle("text-yellow-400", i < current);
        s.classList.toggle("text-gray-300", i >= current);
      });
    }
  
    resetStars();
  
    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.startsWith(name + "=")) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
});
  