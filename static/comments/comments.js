const LOAD_DELAY_MS = 300;
const commentsState = {};  // хранит page, loading, finished, loadedIds по targetType

function loadComments(targetType) {
  if (!commentsState[targetType]) {
    commentsState[targetType] = {
      page: 1,
      loading: false,
      finished: false,
      loadedIds: new Set()
    };
  }

  const state = commentsState[targetType];
  if (state.loading || state.finished) return;

  state.loading = true;
  document.getElementById(`${targetType}-comments-loader`).classList.remove("hidden");

  const container = document.getElementById(`${targetType}-comments-container`);
  const slug = container.dataset.objectSlug;

  fetch(`/comments/${targetType}/${slug}/comments/?page=${state.page}`)
    .then(res => res.json())
    .then(data => {
        // если НЕТ комментариев — выходим
        if (!data.comments.length) {
            state.finished = true;
            state.loading = false;
            document.getElementById(`load-more-comments-${targetType}`).classList.add("hidden");
            document.getElementById(`no-more-comments-${targetType}`).classList.remove("hidden");
            document.getElementById(`${targetType}-comments-loader`).classList.add("hidden");
            return;
        }

        // есть комментарии — показываем
        setTimeout(() => {
            data.comments.forEach(c => {
            if (state.loadedIds.has(c.id)) return;
            state.loadedIds.add(c.id);

            const avatar = c.avatar ? c.avatar : `https://ui-avatars.com/api/?name=${c.author}&background=ecd5fa&color=8e44ad`;

            const block = document.createElement("div");
            block.className = "flex gap-3 border-b border-gray-200 pb-3";
            block.innerHTML = `
                <a href="/profile/${c.author}/">
                <img src="${avatar}" alt="${c.author}" class="w-10 h-10 rounded-full object-cover border" />
                </a>
                <div>
                <a href="/profile/${c.author}/" class="font-semibold hover:underline">${c.author}</a>
                <div class="text-gray-400 text-xs">${c.created_at}</div>
                <div class="mt-1 text-sm text-gray-900">${c.text}</div>
                </div>
            `;
            container.appendChild(block);
            });

            state.page++;
            state.loading = false;
            document.getElementById(`${targetType}-comments-loader`).classList.add("hidden");

            // 💥 теперь — если последняя страница, скрываем кнопку
            if (data.is_last_page) {
            state.finished = true;
            document.getElementById(`load-more-comments-${targetType}`).classList.add("hidden");
            document.getElementById(`no-more-comments-${targetType}`).classList.remove("hidden");
            }
        }, LOAD_DELAY_MS);
    })
    .catch(() => {
      state.loading = false;
      document.getElementById(`${targetType}-comments-loader`).classList.add("hidden");
    });
}

function submitComment(e, targetType) {
  e.preventDefault();

  const container = document.getElementById(`${targetType}-comments-container`);
  const slug = container.dataset.objectSlug;
  const form = document.getElementById(`commentForm-${targetType}`);
  const input = document.getElementById(`commentInput-${targetType}`);
  const text = input.value.trim();

  if (!text) return;

  const formData = new FormData();
  formData.append('text', text);

  fetch(`/comments/${targetType}/${slug}/comments/post/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
    },
    body: formData
  })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        input.value = '';
        commentsState[targetType] = null;
        container.innerHTML = '';
        loadComments(targetType);
      }
    });
}

document.addEventListener("DOMContentLoaded", () => {
  const autoBlocks = document.querySelectorAll('[data-target-type]');
  autoBlocks.forEach(el => {
    const type = el.dataset.targetType;
    loadComments(type);
  });
});

window.loadComments = loadComments;
window.submitComment = submitComment;