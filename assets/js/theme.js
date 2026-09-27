// 테마 토글 — 저장값이 없으면 시스템 설정을 따른다.
(function () {
  var root = document.documentElement;

  function current() {
    var t = root.getAttribute('data-theme');
    if (t === 'dark' || t === 'light') return t;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function apply(theme) {
    root.setAttribute('data-theme', theme);
    try { localStorage.setItem('theme', theme); } catch (e) {}
    document.querySelectorAll('.theme-toggle').forEach(function (btn) {
      btn.setAttribute('aria-pressed', theme === 'dark' ? 'true' : 'false');
    });
  }

  document.querySelectorAll('.theme-toggle').forEach(function (btn) {
    btn.setAttribute('aria-pressed', current() === 'dark' ? 'true' : 'false');
    btn.addEventListener('click', function () {
      apply(current() === 'dark' ? 'light' : 'dark');
    });
  });
})();

// 인쇄 버튼 — 브라우저 인쇄 대화상자를 연다.
// 여기서 여는 것과 Ctrl+P 로 여는 것이 같은 결과여야 한다(print.css 가 둘 다 담당).
(function () {
  document.querySelectorAll('.print-btn').forEach(function (btn) {
    btn.addEventListener('click', function () { window.print(); });
  });
})();
