/* ==========================================================================
   JAVASCRIPT MASTER STUDY DOCUMENTATION — COMPLETE BOOK (CHAPTERS 01 - 40)
   INTERACTIVE APPLICATION SCRIPT (js/app.js)
   ========================================================================== */

function toggleChapterMenu() {
  const menu = document.getElementById('chapterDropdownMenu');
  const backdrop = document.getElementById('chapterMenuBackdrop');
  const btn = document.getElementById('chapterDropdownBtn');
  const searchInput = document.getElementById('chapterSearchInput');
  const isOpen = menu && menu.classList.contains('active');
  
  if (isOpen) {
    closeChapterMenu();
  } else if (menu && backdrop && btn) {
    menu.classList.add('active');
    backdrop.classList.add('active');
    btn.setAttribute('aria-expanded', 'true');
    if (searchInput) {
      setTimeout(() => searchInput.focus(), 60);
    }
  }
}

function closeChapterMenu() {
  const menu = document.getElementById('chapterDropdownMenu');
  const backdrop = document.getElementById('chapterMenuBackdrop');
  const btn = document.getElementById('chapterDropdownBtn');
  if (menu) menu.classList.remove('active');
  if (backdrop) backdrop.classList.remove('active');
  if (btn) btn.setAttribute('aria-expanded', 'false');
}

function selectChapter(chId) {
  closeChapterMenu();
}

function filterChapters(query) {
  const q = query.trim().toLowerCase();
  const items = document.querySelectorAll('.chapter-menu-item');
  let matched = 0;
  items.forEach(item => {
    const data = item.getAttribute('data-title') || '';
    if (!q || data.includes(q)) {
      item.style.display = 'flex';
      matched++;
    } else {
      item.style.display = 'none';
    }
  });
  
  let noResults = document.getElementById('chapterMenuNoResults');
  if (matched === 0) {
    if (!noResults) {
      noResults = document.createElement('div');
      noResults.id = 'chapterMenuNoResults';
      noResults.className = 'chapter-menu-no-results';
      noResults.textContent = 'No matching chapters found';
      const list = document.getElementById('chapterMenuList');
      if (list) list.appendChild(noResults);
    }
    noResults.style.display = 'block';
  } else if (noResults) {
    noResults.style.display = 'none';
  }
}

// Close on Escape key
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') {
    closeChapterMenu();
  }
});
