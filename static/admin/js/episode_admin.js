document.addEventListener('DOMContentLoaded', function () {
    const animeSelect = document.querySelector('select[name="anime"]');
    const seasonSelect = document.querySelector('select[name="season"]');
  
    if (!animeSelect || !seasonSelect) return;
  
    animeSelect.addEventListener('change', function () {
      const animeId = this.value;
      seasonSelect.innerHTML = '<option value="">Загрузка...</option>';
  
      fetch(`/anime/get-seasons/?anime_id=${animeId}`)
        .then(response => response.json())
        .then(data => {
          seasonSelect.innerHTML = '<option value="">Выберите сезон</option>';
          data.seasons.forEach(season => {
            const option = document.createElement('option');
            option.value = season.id;
            option.textContent = season.title;
            seasonSelect.appendChild(option);
          });
        });
    });
  });
  