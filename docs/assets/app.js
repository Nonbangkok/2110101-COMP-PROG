/* -------------------------------------------------------------------
   2110101 Computer Programming — problem browser
   Data comes from assets/data.js (window.CP_DATA).
------------------------------------------------------------------- */

(function () {
  'use strict';

  var DATA = window.CP_DATA || { topics: [], problems: [], workshops: [] };
  var BY_CODE = {};
  DATA.problems.forEach(function (p) { BY_CODE[p.code] = p; });
  var BY_WORKSHOP = {};
  (DATA.workshops || []).forEach(function (w) { BY_WORKSHOP[w.id] = w; });

  var els = {
    search:   document.getElementById('search'),
    nav:      document.getElementById('nav'),
    navEmpty: document.getElementById('navEmpty'),
    welcome:  document.getElementById('welcome'),
    detail:   document.getElementById('detail'),
    statRow:  document.getElementById('statRow'),
    topstats: document.getElementById('topstats'),
    menuBtn:  document.getElementById('menuBtn'),
    scrim:    document.getElementById('scrim'),
    themeBtn: document.getElementById('themeBtn')
  };

  var state = { code: null, kind: 'problem', tab: 'problem', set: 'examplesets', query: '' };

  /* ------------------------------------------------------- helpers */

  function esc(s) {
    return String(s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function bytes(n) {
    if (n == null) return '';
    if (n < 1024) return n + ' B';
    if (n < 1024 * 1024) return (n / 1024).toFixed(n < 10240 ? 1 : 0) + ' KB';
    return (n / 1048576).toFixed(1) + ' MB';
  }

  function plural(n, one, many) {
    return n + ' ' + (n === 1 ? one : (many || one + 's'));
  }

  // Path from docs/ up to the repository root.
  function repoPath(p) { return '../' + p; }

  // Paths emitted beneath docs/ are already relative to this page.
  function docsPath(p) { return p; }

  /* -------------------------------------------- python highlighting */

  var PY_KW = /^(False|None|True|and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield|match|case)$/;
  var PY_BI = /^(abs|all|any|bin|bool|chr|dict|divmod|enumerate|eval|exec|filter|float|format|frozenset|getattr|hex|input|int|isinstance|iter|len|list|map|max|min|next|object|oct|open|ord|pow|print|range|repr|reversed|round|set|setattr|slice|sorted|str|sum|super|tuple|type|zip|self)$/;

  function highlightPython(src) {
    var out = '';
    var i = 0;
    var n = src.length;

    while (i < n) {
      var c = src[i];

      // comment
      if (c === '#') {
        var j = src.indexOf('\n', i);
        if (j < 0) j = n;
        out += '<span class="tok-com">' + esc(src.slice(i, j)) + '</span>';
        i = j;
        continue;
      }

      // string (triple or single quoted, with prefix letters)
      if (c === '"' || c === "'") {
        var quote = c;
        var triple = src.substr(i, 3) === quote + quote + quote;
        var end;
        if (triple) {
          end = src.indexOf(quote + quote + quote, i + 3);
          end = end < 0 ? n : end + 3;
        } else {
          end = i + 1;
          while (end < n && src[end] !== quote && src[end] !== '\n') {
            if (src[end] === '\\') end++;
            end++;
          }
          end = Math.min(end + 1, n);
        }
        out += '<span class="tok-str">' + esc(src.slice(i, end)) + '</span>';
        i = end;
        continue;
      }

      // number
      if (/[0-9]/.test(c) && !/[A-Za-z_]/.test(src[i - 1] || '')) {
        var k = i;
        while (k < n && /[0-9a-fA-FxXoObB_.eE+\-jJ]/.test(src[k])) {
          if (/[+\-]/.test(src[k]) && !/[eE]/.test(src[k - 1])) break;
          k++;
        }
        out += '<span class="tok-num">' + esc(src.slice(i, k)) + '</span>';
        i = k;
        continue;
      }

      // word
      if (/[A-Za-z_]/.test(c)) {
        var w = i;
        while (w < n && /[A-Za-z0-9_]/.test(src[w])) w++;
        var word = src.slice(i, w);
        var cls = '';
        if (PY_KW.test(word)) cls = 'tok-kw';
        else if (src[w] === '(') cls = 'tok-fn';
        else if (PY_BI.test(word)) cls = 'tok-bi';
        out += cls ? '<span class="' + cls + '">' + esc(word) + '</span>' : esc(word);
        i = w;
        continue;
      }

      out += esc(c);
      i++;
    }
    return out;
  }

  /* ------------------------------------------------------- drawer */
  /* On phones the problem list is a drawer over the content. */

  var MOBILE = window.matchMedia('(max-width: 760px)');

  function isMobile() { return MOBILE.matches; }

  function setNav(open) {
    document.body.classList.toggle('nav-open', open);
    els.menuBtn.setAttribute('aria-expanded', String(open));
    els.scrim.hidden = !open;
  }

  function closeNav() { if (document.body.classList.contains('nav-open')) setNav(false); }

  /* --------------------------------------------------- code theme */

  function pageTheme() {
    return document.documentElement.getAttribute('data-theme') || 'light';
  }

  function syncPageThemeButton() {
    var dark = pageTheme() === 'dark';
    els.themeBtn.textContent = dark ? 'Light mode' : 'Dark mode';
    els.themeBtn.setAttribute('aria-label', dark ? 'Switch to light mode' : 'Switch to dark mode');
    els.themeBtn.setAttribute('aria-pressed', String(dark));
  }

  function togglePageTheme() {
    var next = pageTheme() === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    try { localStorage.setItem('cp-page-theme', next); } catch (e) { /* ignore */ }
    syncPageThemeButton();
  }

  (function restorePageTheme() {
    var saved = null;
    try { saved = localStorage.getItem('cp-page-theme'); } catch (e) { /* ignore */ }
    document.documentElement.setAttribute('data-theme', saved === 'dark' ? 'dark' : 'light');
    syncPageThemeButton();
  })();

  function codeTheme() {
    return document.documentElement.getAttribute('data-code-theme') || 'light';
  }

  function codeThemeLabel() {
    return codeTheme() === 'dark' ? 'Light code' : 'Dark code';
  }

  function toggleCodeTheme() {
    var next = codeTheme() === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-code-theme', next);
    try { localStorage.setItem('cp-code-theme', next); } catch (e) { /* ignore */ }
    els.detail.querySelectorAll('[data-theme-toggle]').forEach(function (b) {
      b.textContent = codeThemeLabel();
    });
  }

  (function restoreCodeTheme() {
    var saved = null;
    try { saved = localStorage.getItem('cp-code-theme'); } catch (e) { /* ignore */ }
    document.documentElement.setAttribute('data-code-theme', saved === 'dark' ? 'dark' : 'light');
  })();

  /* ------------------------------------------------------ copy btn */

  function onCopyClick(ev) {
    var btn = ev.target.closest('[data-copy]');
    if (!btn) return;
    var src = document.getElementById(btn.getAttribute('data-copy'));
    if (!src) return;
    var text = src.textContent;
    var done = function () {
      var old = btn.textContent;
      btn.textContent = 'Copied';
      btn.classList.add('copied');
      setTimeout(function () {
        btn.textContent = old;
        btn.classList.remove('copied');
      }, 1400);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, fallback);
    } else {
      fallback();
    }
    function fallback() {
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand('copy'); done(); } catch (e) { /* ignore */ }
      document.body.removeChild(ta);
    }
  }

  /* --------------------------------------------------------- icons */
  /* Lucide icons (lucide.dev, ISC licence), inlined so the site needs no CDN. */

  var FILE_BODY = '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/>';
  var ICONS = {
    'chevron-right': '<path d="m9 18 6-6-6-6"/>',
    'x': '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    'folder': '<path d="M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z"/>',
    'folder-open': '<path d="m6 14 1.5-2.9A2 2 0 0 1 9.24 10H20a2 2 0 0 1 1.94 2.5l-1.54 6a2 2 0 0 1-1.95 1.5H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h3.9a2 2 0 0 1 1.69.9l.81 1.2a2 2 0 0 0 1.67.9H18a2 2 0 0 1 2 2v2"/>',
    'file': FILE_BODY,
    'file-code': FILE_BODY + '<path d="m10 13-2 2 2 2"/><path d="m14 17 2-2-2-2"/>',
    'file-text': FILE_BODY + '<path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/>',
    'image': '<rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>',
    'music': '<path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/>',
    'film': '<rect width="18" height="18" x="3" y="3" rx="2"/><path d="M7 3v18"/><path d="M3 7.5h4"/><path d="M3 12h18"/><path d="M3 16.5h4"/><path d="M17 3v18"/><path d="M17 7.5h4"/><path d="M17 16.5h4"/>',
    'panel-left-close': '<rect width="18" height="18" x="3" y="3" rx="2"/><path d="M9 3v18"/><path d="m16 15-3-3 3-3"/>',
    'panel-left-open': '<rect width="18" height="18" x="3" y="3" rx="2"/><path d="M9 3v18"/><path d="m14 9 3 3-3 3"/>',
    'chevrons-up-down': '<path d="m7 15 5 5 5-5"/><path d="m7 9 5-5 5 5"/>',
    'chevrons-down-up': '<path d="m7 20 5-5 5 5"/><path d="m7 4 5 5 5-5"/>',
    'download': '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/><path d="M12 15V3"/>',
    'search': '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>'
  };

  function icon(name, cls) {
    return '<svg class="icon' + (cls ? ' ' + cls : '') + '" viewBox="0 0 24 24" aria-hidden="true">' + ICONS[name] + '</svg>';
  }

  /* ------------------------------------------------------ explorer */
  /* A VS Code-style file explorer used by the Data files and Resources tabs. */

  var ex = null;

  // Sidebar width and visibility are remembered across pages and visits.
  var EX_MIN = 160, EX_DEFAULT = 260;
  var exPrefs = { width: EX_DEFAULT, hidden: false };
  try {
    var savedEx = JSON.parse(localStorage.getItem('cp-explorer') || '{}');
    if (typeof savedEx.width === 'number') exPrefs.width = savedEx.width;
    exPrefs.hidden = savedEx.hidden === true;
  } catch (e) { /* ignore */ }

  function exSavePrefs() {
    try { localStorage.setItem('cp-explorer', JSON.stringify(exPrefs)); } catch (e) { /* ignore */ }
  }

  // CSS also caps the width so the file view always keeps room; see .explorer.
  function exApplyWidth(host, width) {
    var max = host.clientWidth ? Math.max(EX_MIN, Math.min(640, host.clientWidth - 240)) : 640;
    exPrefs.width = Math.round(Math.max(EX_MIN, Math.min(max, width)));
    host.style.setProperty('--ex-side-w', exPrefs.width + 'px');
    var handle = host.querySelector('.ex-resize');
    if (handle) handle.setAttribute('aria-valuenow', exPrefs.width);
  }

  // True when every folder below the root is expanded.
  function exAllOpen(n) {
    return Object.keys(n.dirs).every(function (k) { return ex.open[n.dirs[k].path] && exAllOpen(n.dirs[k]); });
  }

  function fileIcon(f) {
    if (f.kind === 'code') return 'file-code';
    if (f.kind === 'image') return 'image';
    if (f.kind === 'audio') return 'music';
    if (f.kind === 'video') return 'film';
    if (f.kind === 'text' || /\.(txt|csv|json|md|in|out)$/i.test(f.name)) return 'file-text';
    return 'file';
  }

  function explorerShell() { return '<div class="explorer" id="explorer"></div>'; }

  function exInit(rootPath, list) {
    var root = { name: rootPath.split('/').pop(), path: rootPath, dirs: {}, files: [] };
    var byPath = {};
    list.forEach(function (item) {
      var parts = item.path.slice(rootPath.length + 1).split('/');
      var node = root;
      for (var i = 0; i < parts.length - 1; i++) {
        var key = parts[i];
        node = node.dirs[key] = node.dirs[key] ||
          { name: key, path: node.path + '/' + key, dirs: {}, files: [] };
      }
      var f = { name: parts[parts.length - 1], path: item.path, size: item.size,
                kind: item.kind, text: item.text, trunc: item.trunc };
      node.files.push(f);
      byPath[f.path] = f;
    });
    ex = { root: root, byPath: byPath, open: {}, tabs: [], preview: null, active: null, filter: '' };
    ex.open[root.path] = true;
    Object.keys(root.dirs).forEach(function (k) { ex.open[root.dirs[k].path] = true; });
    var first = list.filter(function (f) { return f.kind === 'code'; })[0] || list[0];
    if (first) exOpenFile(first.path, false);
    exRender();
  }

  function exCount(n) {
    return Object.keys(n.dirs).reduce(function (c, k) { return c + exCount(n.dirs[k]); }, n.files.length);
  }

  function exHit(name) { return !ex.filter || name.toLowerCase().indexOf(ex.filter) >= 0; }

  function exHasHit(n) {
    return n.files.some(function (f) { return exHit(f.name); }) ||
           Object.keys(n.dirs).some(function (k) { return exHasHit(n.dirs[k]); });
  }

  function exFindDir(path, n) {
    n = n || ex.root;
    if (n.path === path) return n;
    for (var k in n.dirs) { var hit = exFindDir(path, n.dirs[k]); if (hit) return hit; }
    return null;
  }

  function exSortedDirs(n) { return Object.keys(n.dirs).sort(function (a, b) { return a.localeCompare(b); }); }
  function exSortedFiles(n) { return n.files.slice().sort(function (a, b) { return a.name.localeCompare(b.name); }); }

  function exGuides(depth) {
    var h = '';
    for (var g = 0; g < depth; g++) h += '<span class="ex-guide" style="left:' + (17 + g * 14) + 'px"></span>';
    return h;
  }

  function exRows(n, depth) {
    var open = ex.open[n.path] || !!ex.filter;
    var h = '<button type="button" class="ex-row is-folder' + (ex.active === 'dir:' + n.path ? ' active' : '') +
            '" style="--d:' + depth + '" data-ex-dir="' + esc(n.path) + '" aria-expanded="' + open + '">' +
            exGuides(depth) + icon('chevron-right', 'ex-chev' + (open ? ' open' : '')) +
            icon(open ? 'folder-open' : 'folder', 'ex-ico') +
            '<span class="ex-label">' + esc(n.name) + '</span><span class="ex-count">' + exCount(n) + '</span></button>';
    if (!open) return h;
    exSortedDirs(n).forEach(function (k) { if (exHasHit(n.dirs[k])) h += exRows(n.dirs[k], depth + 1); });
    exSortedFiles(n).forEach(function (f) {
      if (!exHit(f.name)) return;
      h += '<button type="button" class="ex-row' + (ex.active === f.path ? ' active' : '') +
           '" style="--d:' + (depth + 1) + '" data-ex-file="' + esc(f.path) + '" title="' + esc(f.path) + '">' +
           exGuides(depth + 1) + '<span class="ex-chev-space"></span>' + icon(fileIcon(f), 'ex-ico ex-ico-' + fileIcon(f)) +
           '<span class="ex-label">' + esc(f.name) + '</span></button>';
    });
    return h;
  }

  function exOpenFile(path, pin) {
    if (ex.tabs.indexOf(path) < 0) {
      var at = ex.preview ? ex.tabs.indexOf(ex.preview) : -1;
      if (!pin && at >= 0) ex.tabs[at] = path;
      else ex.tabs.push(path);
      ex.preview = pin ? (ex.preview === path ? null : ex.preview) : path;
    } else if (pin && ex.preview === path) {
      ex.preview = null;
    }
    ex.active = path;
  }

  function exView() {
    if (!ex.active) return '<div class="ex-empty">Select a file in the explorer to open it.</div>';
    if (ex.active.indexOf('dir:') === 0) {
      var d = exFindDir(ex.active.slice(4));
      var items = exSortedDirs(d).map(function (k) {
        return '<button type="button" class="ex-tile" data-ex-enter="' + esc(d.dirs[k].path) + '">' +
               '<span class="ex-tile-art">' + icon('folder', 'ex-tile-ico') + '</span><span>' + esc(k) + '</span></button>';
      }).concat(exSortedFiles(d).map(function (f) {
        var art = f.kind === 'image'
          ? '<img src="' + esc(repoPath(f.path)) + '" alt="" loading="lazy">'
          : icon(fileIcon(f), 'ex-tile-ico');
        return '<button type="button" class="ex-tile" data-ex-file="' + esc(f.path) + '">' +
               '<span class="ex-tile-art">' + art + '</span><span>' + esc(f.name) + '</span></button>';
      }));
      return items.length ? '<div class="ex-grid">' + items.join('') + '</div>'
                          : '<div class="ex-empty">This folder is empty.</div>';
    }
    var f = ex.byPath[ex.active];
    var note = f.trunc ? '<div class="trunc-note">Preview only — ' + bytes(f.size) + ' in full. Use Raw to open the whole file.</div>' : '';
    if (f.kind === 'code' && f.text != null) {
      var lines = f.text.replace(/\n$/, '').split('\n');
      return note + '<div class="code-wrap"><pre class="gutter" aria-hidden="true">' +
             lines.map(function (_, i) { return i + 1; }).join('\n') +
             '</pre><pre class="code"><code id="ex-src">' + highlightPython(f.text) + '</code></pre></div>';
    }
    if (f.kind === 'image') {
      return '<div class="ex-media"><img src="' + esc(repoPath(f.path)) + '" alt="' + esc(f.name) + '">' +
             '<span class="ex-media-meta">' + esc(f.name) + ' · ' + bytes(f.size) + '</span></div>';
    }
    if (f.kind === 'audio' || f.kind === 'video') {
      var tag = f.kind === 'audio' ? 'audio' : 'video';
      return '<div class="ex-media">' + (tag === 'audio' ? icon('music', 'ex-media-ico') : '') +
             '<' + tag + ' controls preload="metadata" src="' + esc(repoPath(f.path)) + '"></' + tag + '>' +
             '<span class="ex-media-meta">' + esc(f.name) + ' · ' + bytes(f.size) + '</span></div>';
    }
    if (f.text != null) return note + '<pre class="io ex-text" id="ex-src">' + esc(f.text) + '</pre>';
    return '<div class="ex-empty">' + icon(fileIcon(f), 'ex-empty-ico') +
           '<span>There is no preview for this file (' + bytes(f.size) + ').</span>' +
           '<a class="btn-link" href="' + esc(repoPath(f.path)) + '" download>' + icon('download') + ' Download</a></div>';
  }

  function exRender() {
    var host = document.getElementById('explorer');
    if (!host || !ex) return;
    var filterFocused = document.activeElement && document.activeElement.classList.contains('ex-filter');
    var treeScroll = host.querySelector('.ex-tree');
    treeScroll = treeScroll ? treeScroll.scrollTop : 0;

    var isDir = ex.active && ex.active.indexOf('dir:') === 0;
    var f = ex.active && !isDir ? ex.byPath[ex.active] : null;
    var activePath = isDir ? ex.active.slice(4) : ex.active;
    var crumbs = activePath
      ? ex.root.name + activePath.slice(ex.root.path.length)
      : '';
    var crumbHtml = crumbs.split('/').filter(Boolean).map(function (s) { return '<span>' + esc(s) + '</span>'; })
      .join(icon('chevron-right', 'ex-crumb-sep'));

    var tools = '';
    if (f) {
      tools += '<span class="ex-size">' + bytes(f.size) + '</span>';
      if (f.kind === 'code' && f.text != null) {
        tools += '<button class="btn" type="button" data-theme-toggle title="Switch the code colours">' + codeThemeLabel() + '</button>';
      }
      tools += '<a class="btn-link" href="' + esc(repoPath(f.path)) + '" target="_blank" rel="noopener">Raw</a>';
      if (f.text != null) tools += '<button class="btn" type="button" data-copy="ex-src">Copy</button>';
    }

    var hasDirs = Object.keys(ex.root.dirs).length > 0;
    var allOpen = hasDirs && exAllOpen(ex.root);
    var foldTool = hasDirs
      ? '<button type="button" class="ex-tool" data-ex-act="' + (allOpen ? 'collapse' : 'expand') + '" title="' +
        (allOpen ? 'Collapse all folders' : 'Expand all folders') + '" aria-label="' +
        (allOpen ? 'Collapse all folders' : 'Expand all folders') + '">' + icon(allOpen ? 'chevrons-down-up' : 'chevrons-up-down') + '</button>'
      : '';

    host.classList.toggle('side-hidden', exPrefs.hidden);
    host.innerHTML =
      '<aside class="ex-side">' +
        '<div class="ex-side-head"><span>Explorer</span><span class="spacer"></span>' + foldTool +
          '<button type="button" class="ex-tool" data-ex-act="hide" title="Hide the explorer" aria-label="Hide the explorer">' + icon('panel-left-close') + '</button>' +
        '</div>' +
        '<label class="ex-filter-wrap">' + icon('search', 'ex-filter-ico') +
          '<input class="ex-filter" type="search" placeholder="Filter files" aria-label="Filter files" value="' + esc(ex.filter) + '"></label>' +
        '<div class="ex-tree" role="tree">' + exRows(ex.root, 0) + '</div>' +
        '<div class="ex-side-foot">' + plural(exCount(ex.root), 'file') + '</div>' +
        '<div class="ex-resize" role="separator" tabindex="0" aria-orientation="vertical" aria-label="Resize the explorer" ' +
          'aria-valuemin="' + EX_MIN + '" title="Drag to resize · double-click to reset"></div>' +
      '</aside>' +
      '<div class="ex-main">' +
        '<div class="ex-tabs" role="tablist">' +
          (exPrefs.hidden ? '<button type="button" class="ex-show" data-ex-act="show" title="Show the explorer" aria-label="Show the explorer">' +
            icon('panel-left-open') + '<span>Explorer</span></button>' : '') +
          ex.tabs.map(function (path) {
          var t = ex.byPath[path];
          return '<div class="ex-tab' + (path === ex.active ? ' active' : '') + (path === ex.preview ? ' is-preview' : '') + '">' +
                 '<button type="button" class="ex-tab-open" data-ex-tab="' + esc(path) + '" title="' + esc(path) + '">' +
                 icon(fileIcon(t), 'ex-ico ex-ico-' + fileIcon(t)) + '<span>' + esc(t.name) + '</span></button>' +
                 '<button type="button" class="ex-tab-close" data-ex-close="' + esc(path) + '" aria-label="Close ' + esc(t.name) + '">' + icon('x') + '</button></div>';
        }).join('') + '</div>' +
        '<div class="ex-bar"><span class="ex-crumbs">' + crumbHtml + '</span><span class="spacer"></span>' + tools + '</div>' +
        '<div class="ex-view">' + exView() + '</div>' +
      '</div>';

    host.style.setProperty('--ex-side-w', exPrefs.width + 'px');
    host.querySelector('.ex-resize').setAttribute('aria-valuenow', exPrefs.width);
    host.querySelector('.ex-tree').scrollTop = treeScroll;
    if (filterFocused) {
      var input = host.querySelector('.ex-filter');
      input.focus();
      input.setSelectionRange(input.value.length, input.value.length);
    }
  }

  function exClick(ev) {
    if (!ex || !ev.target.closest('#explorer')) return false;
    var el;
    if ((el = ev.target.closest('[data-ex-close]'))) {
      var path = el.dataset.exClose, at = ex.tabs.indexOf(path);
      ex.tabs.splice(at, 1);
      if (ex.preview === path) ex.preview = null;
      if (ex.active === path) ex.active = ex.tabs[Math.min(at, ex.tabs.length - 1)] || null;
    } else if ((el = ev.target.closest('[data-ex-tab]'))) {
      ex.active = el.dataset.exTab;
    } else if ((el = ev.target.closest('[data-ex-act="hide"], [data-ex-act="show"]'))) {
      exPrefs.hidden = el.dataset.exAct === 'hide';
      exSavePrefs();
      exRender();
      var focusTo = document.querySelector(exPrefs.hidden ? '#explorer .ex-show' : '#explorer [data-ex-act="hide"]');
      if (focusTo) focusTo.focus();
      return true;
    } else if ((el = ev.target.closest('[data-ex-act]'))) {
      var expand = el.dataset.exAct === 'expand';
      (function walk(n) { ex.open[n.path] = expand; for (var k in n.dirs) walk(n.dirs[k]); })(ex.root);
      ex.open[ex.root.path] = true;
    } else if ((el = ev.target.closest('[data-ex-dir]'))) {
      var dir = el.dataset.exDir;
      ex.open[dir] = !ex.open[dir];
      ex.active = 'dir:' + dir;
    } else if ((el = ev.target.closest('[data-ex-enter]'))) {
      ex.open[el.dataset.exEnter] = true;
      ex.active = 'dir:' + el.dataset.exEnter;
    } else if ((el = ev.target.closest('[data-ex-file]'))) {
      exOpenFile(el.dataset.exFile, false);
    } else {
      return false;
    }
    exRender();
    return true;
  }

  /* ----------------------------------------------------- sidebar */

  function matches(p, q) {
    if (!q) return true;
    return (p.code + ' ' + p.title).toLowerCase().indexOf(q) >= 0;
  }

  function markMatch(text, q) {
    if (!q) return esc(text);
    var idx = text.toLowerCase().indexOf(q);
    if (idx < 0) return esc(text);
    return esc(text.slice(0, idx)) + '<mark>' + esc(text.slice(idx, idx + q.length)) +
           '</mark>' + esc(text.slice(idx + q.length));
  }

  function renderNav() {
    var q = state.query;
    var html = '';
    var shown = 0;

    DATA.topics.forEach(function (t) {
      var list = DATA.problems.filter(function (p) {
        return p.topic === t.id && matches(p, q);
      });
      if (!list.length) return;
      shown += list.length;

      var hasActive = state.kind === 'problem' && list.some(function (p) { return p.code === state.code; });
      var open = q ? true : (hasActive || state.openTopics && state.openTopics[t.id]);

      html += '<div class="nav-group' + (open ? ' open' : '') + '" data-topic="' + esc(t.id) + '">';
      html += '<button class="nav-head" type="button">' +
                icon('chevron-right', 'nav-caret') +
                '<span class="nav-key">' + esc(t.key) + '</span>' +
                '<span>' + esc(t.label) + '</span>' +
                '<span class="nav-count">' + list.length + '</span>' +
              '</button>';
      html += '<div class="nav-list">';
      list.forEach(function (p) {
        html += '<a class="nav-item' + (state.kind === 'problem' && p.code === state.code ? ' active' : '') +
                '" href="#' + esc(p.code) + '">' +
                  '<span class="ni-code">' + markMatch(p.code, q) + '</span>' +
                  '<span class="ni-title">' + markMatch(p.title, q) + '</span>' +
                '</a>';
      });
      html += '</div></div>';
    });

    var workshops = (DATA.workshops || []).filter(function (w) {
      return !q || (w.id + ' ' + w.title).toLowerCase().indexOf(q) >= 0;
    });
    if (workshops.length) {
      shown += workshops.length;
      var workshopOpen = q || state.kind === 'workshop' || (state.openTopics && state.openTopics.workshops);
      html += '<div class="nav-group' + (workshopOpen ? ' open' : '') + '" data-topic="workshops">';
      html += '<button class="nav-head" type="button">' +
              icon('chevron-right', 'nav-caret') +
              '<span class="nav-key">WS</span><span>Workshops</span>' +
              '<span class="nav-count">' + workshops.length + '</span></button><div class="nav-list">';
      workshops.forEach(function (w) {
        html += '<a class="nav-item' + (state.kind === 'workshop' && w.id === state.code ? ' active' : '') +
                '" href="#workshop/' + encodeURIComponent(w.id) + '">' +
                '<span class="ni-code">' + markMatch(w.id, q) + '</span>' +
                '<span class="ni-title">' + markMatch(w.title, q) + '</span></a>';
      });
      html += '</div></div>';
    }

    els.nav.innerHTML = html;
    els.navEmpty.hidden = shown > 0;
  }

  /* ------------------------------------------------------ welcome */

  function renderStats() {
    var nProblems = DATA.problems.length;
    var nEx = 0, nTs = 0, nPdf = 0;
    DATA.problems.forEach(function (p) {
      nEx += p.nExample;
      nTs += p.nTest;
      if (p.pdf) nPdf++;
    });

    els.statRow.innerHTML =
      stat(nProblems, 'problems') +
      stat(DATA.topics.length, 'topics') +
      stat(nEx + nTs, 'test cases') +
      stat(nPdf, 'statements');

    els.topstats.textContent = nProblems + ' problems · ' + (nEx + nTs) + ' test cases';

    function stat(v, label) {
      return '<div class="stat"><b>' + v + '</b><span>' + label + '</span></div>';
    }
  }

  /* ------------------------------------------------------- detail */

  function ioBlock(part, id, path, label) {
    var head = '<div class="case-label">' + label +
               '<span class="spacer"></span>' +
               (part ? '<span class="size">' + bytes(part.size) + '</span>' : '') +
               (part ? '<button class="btn" type="button" data-copy="' + id + '">Copy</button>' : '') +
               '</div>';
    if (!part) {
      return '<div class="case-col">' + head +
             '<pre class="io"></pre></div>';
    }
    var body = '<pre class="io" id="' + id + '">' + esc(part.text) + '</pre>';
    var note = part.trunc
      ? '<div class="trunc-note">Preview only — ' + bytes(part.size) +
        ' in total. <a href="' + esc(repoPath(path)) + '" target="_blank" rel="noopener">Open the full file</a></div>'
      : '';
    return '<div class="case-col">' + head + body + note + '</div>';
  }

  function renderCases(p, setName) {
    var cases = (p.sets && p.sets[setName]) || [];
    if (!cases.length) {
      return '<div class="empty-state">This problem has no ' +
             (setName === 'examplesets' ? 'example' : 'test set') + ' cases.</div>';
    }
    return cases.map(function (c) {
      var base = p.code + '-' + setName + '-' + c.n;
      return '<div class="case">' +
        '<div class="case-head">' +
          '<span class="case-n">#' + c.n + '</span>' +
          '<span class="spacer"></span>' +
          '<a class="btn-link" href="' + esc(repoPath(c.inPath)) + '" target="_blank" rel="noopener">raw input</a>' +
          '<a class="btn-link" href="' + esc(repoPath(c.outPath)) + '" target="_blank" rel="noopener">raw output</a>' +
        '</div>' +
        '<div class="case-body">' +
          ioBlock(c['in'], base + '-in', c.inPath, 'Input') +
          ioBlock(c.out, base + '-out', c.outPath, 'Expected output') +
        '</div>' +
      '</div>';
    }).join('');
  }

  function renderDetail(p) {
    var topic = DATA.topics.filter(function (t) { return t.id === p.topic; })[0] || { label: p.topic, key: '' };
    var nCases = p.nExample + p.nTest;

    var h = '';
    h += '<div class="detail-head">';
    h += '<div class="crumb">' + esc(topic.key) + ' &nbsp;/&nbsp; ' + esc(topic.label) + '</div>';
    h += '<div class="detail-title"><h1>' + esc(p.title) + '</h1>' +
         '<span class="detail-code">' + esc(p.code) + '</span></div>';
    h += '<div class="meta-row">' +
           '<span>' + plural(nCases, 'test case') + '</span><span class="dot">·</span>' +
           '<span>' + p.nExample + ' example, ' + p.nTest + ' in the test set</span>' +
           (p.data.length ? '<span class="dot">·</span><span>' + plural(p.data.length, 'data file') + '</span>' : '') +
           (p.py ? '<span class="dot">·</span><a href="' + esc(repoPath(p.py)) + '" target="_blank" rel="noopener">source file</a>' : '') +
         '</div>';
    h += '</div>';

    h += '<div class="tabs" role="tablist">' +
      tabBtn('problem', 'Statement', null, !p.pdf) +
      tabBtn('solution', 'Solution', null, !p.source) +
      tabBtn('cases', 'Test cases', nCases, !nCases) +
      tabBtn('files', 'Data files', p.data.length, !p.data.length) +
      '</div>';

    /* statement */
    h += '<div class="panel" data-panel="problem">';
    if (p.pdf) {
      h += '<div class="panel-bar">' +
             '<span class="panel-bar-name">' + esc(p.code) + '.pdf</span>' +
             '<span class="spacer"></span>' +
             '<a class="btn-link" href="' + esc(repoPath(p.pdf)) + '" target="_blank" rel="noopener">Open in a new tab</a>' +
             '<a class="btn-link" href="' + esc(repoPath(p.pdf)) + '" download>Download</a>' +
           '</div>';
      h += '<iframe class="pdf-frame" src="' + esc(repoPath(p.pdf)) + '" title="Problem statement"></iframe>';
      h += '<p class="note pdf-fallback">If the statement does not appear above, your browser cannot display PDFs inline — open it in a new tab instead.</p>';
    } else {
      h += '<div class="empty-state">No PDF statement is stored for this problem.</div>';
    }
    h += '</div>';

    /* solution */
    h += '<div class="panel" data-panel="solution" hidden>';
    if (p.source) {
      var sid = 'src-' + p.code;
      var lines = p.source.replace(/\n$/, '').split('\n');
      var gutter = lines.map(function (_, i) { return i + 1; }).join('\n');
      h += '<div class="card code-card">' +
             '<div class="card-head"><span class="name">' + esc(p.code) + '.py</span>' +
             '<span class="size">' + lines.length + ' lines · ' + bytes(p.source.length) + '</span>' +
             '<span class="spacer"></span>' +
             '<button class="btn" type="button" data-theme-toggle title="Switch the code colours">' + codeThemeLabel() + '</button>' +
             '<button class="btn" type="button" data-copy="' + sid + '">Copy</button></div>' +
             '<div class="code-wrap">' +
               '<pre class="gutter" aria-hidden="true">' + gutter + '</pre>' +
               '<pre class="code"><code id="' + sid + '">' + highlightPython(p.source) + '</code></pre>' +
             '</div>' +
           '</div>';
    } else {
      h += '<div class="empty-state">No solution file for this problem.</div>';
    }
    h += '</div>';

    /* cases */
    h += '<div class="panel" data-panel="cases" hidden>';
    h += '<div class="seg" role="tablist">' +
           '<button type="button" data-set="examplesets" aria-selected="' + (state.set === 'examplesets') + '">Example · ' + p.nExample + '</button>' +
           '<button type="button" data-set="testsets" aria-selected="' + (state.set === 'testsets') + '">Test set · ' + p.nTest + '</button>' +
         '</div>';
    h += '<div id="caseHost">' + renderCases(p, state.set) + '</div>';
    h += '</div>';

    /* data files */
    h += '<div class="panel" data-panel="files" hidden>';
    if (p.data.length) {
      h += '<p class="note">This problem reads from files. The grader writes these into the working directory before it runs your program.</p>';
      h += explorerShell();
    } else {
      h += '<div class="empty-state">This problem does not use any data files.</div>';
    }
    h += '</div>';

    var idx = DATA.problems.indexOf(p);
    var prev = idx > 0 ? DATA.problems[idx - 1] : null;
    var next = idx < DATA.problems.length - 1 ? DATA.problems[idx + 1] : null;
    h += '<nav class="pager">' +
      (prev ? '<a class="pager-link" href="#' + esc(prev.code) + '"><span>Previous</span><b>' + esc(prev.code) + '</b></a>'
            : '<span class="pager-link is-off"></span>') +
      (next ? '<a class="pager-link right" href="#' + esc(next.code) + '"><span>Next</span><b>' + esc(next.code) + '</b></a>'
            : '<span class="pager-link is-off"></span>') +
      '</nav>';

    els.detail.innerHTML = h;
    els.detail.hidden = false;
    els.welcome.hidden = true;

    if (p.data.length) {
      exInit(p.dir, p.data.map(function (d) {
        return { path: d.path, size: d.size, kind: 'text', text: d.text, trunc: d.trunc };
      }));
    }
    showTab(pickTab(p));

    function tabBtn(id, label, count, disabled) {
      return '<button class="tab" type="button" role="tab" data-tab="' + id + '"' +
             (disabled ? ' disabled' : '') + ' aria-selected="false">' + label +
             (count != null ? '<span class="pill">' + count + '</span>' : '') + '</button>';
    }
  }

  function renderWorkshop(w) {
    var slideCount = w.slides.length;
    var notebookCount = w.notebooks.length;
    var resources = w.resources || [];
    var resourceCount = resources.length;
    var h = '<div class="detail-head"><div class="crumb">WS &nbsp;/&nbsp; Workshops</div>' +
            '<div class="detail-title"><h1>' + esc(w.title) + '</h1>' +
            '<span class="detail-code">' + esc(w.id) + '</span></div><div class="meta-row">' +
            '<span>' + plural(slideCount, 'slide deck') + '</span><span class="dot">·</span>' +
            '<span>' + plural(notebookCount, 'notebook') + '</span><span class="dot">·</span>' +
            '<span>' + plural(resourceCount, 'resource') + '</span></div></div>';
    h += '<div class="tabs" role="tablist">' +
      tabBtn('slides', 'Slides', slideCount, !slideCount) +
      tabBtn('notebooks', 'Notebook', notebookCount, !notebookCount) +
      tabBtn('resources', 'Resources', resourceCount, !resourceCount) + '</div>';

    h += '<div class="panel" data-panel="slides">';
    if (slideCount) {
      w.slides.forEach(function (slide) {
        h += '<div class="panel-bar"><span class="panel-bar-name">' + esc(slide.name) +
             '</span><span class="spacer"></span><a class="btn-link" href="' + esc(repoPath(slide.path)) +
             '" target="_blank" rel="noopener">Open in a new tab</a><a class="btn-link" href="' +
             esc(repoPath(slide.path)) + '" download>Download</a></div>' +
             '<iframe class="pdf-frame" src="' + esc(repoPath(slide.path)) + '" title="' + esc(slide.name) + '"></iframe>';
      });
    } else h += '<div class="empty-state">No slide deck is stored for this workshop.</div>';
    h += '</div>';

    h += '<div class="panel" data-panel="notebooks" hidden>';
    if (notebookCount) {
      w.notebooks.forEach(function (notebook) {
        h += '<div class="panel-bar"><span class="panel-bar-name">' + esc(notebook.name) +
             '</span><span class="spacer"></span><a class="btn-link" href="' + esc(docsPath(notebook.html)) +
             '" target="_blank" rel="noopener">Open in a new tab</a><a class="btn-link" href="' +
             esc(repoPath(notebook.path)) + '" download>Download .ipynb</a></div>' +
             '<iframe class="notebook-frame" src="' + esc(docsPath(notebook.html)) + '" title="' + esc(notebook.name) + '"></iframe>';
      });
    } else h += '<div class="empty-state">No notebook is stored for this workshop.</div>';
    h += '</div>';

    h += '<div class="panel" data-panel="resources" hidden>' + renderWorkshopResources(w, resources) + '</div>';

    els.detail.innerHTML = h;
    els.detail.hidden = false;
    els.welcome.hidden = true;
    if (resources.length) {
      var r0 = resources[0];
      exInit(r0.path.slice(0, r0.path.length - r0.name.length - 1), resources);
    }
    showTab(pickWorkshopTab(w));

    function tabBtn(id, label, count, disabled) {
      return '<button class="tab" type="button" role="tab" data-tab="' + id + '"' +
             (disabled ? ' disabled' : '') + ' aria-selected="false">' + label +
             '<span class="pill">' + count + '</span></button>';
    }
  }

  function renderWorkshopResources(w, resources) {
    if (!resources.length) return '<div class="empty-state">No additional files are stored for this workshop.</div>';
    return explorerShell();
  }

  function pickTab(p) {
    var order = [state.tab, 'problem', 'solution', 'cases', 'files'];
    for (var i = 0; i < order.length; i++) {
      var t = order[i];
      if (t === 'problem' && p.pdf) return t;
      if (t === 'solution' && p.source) return t;
      if (t === 'cases' && (p.nExample + p.nTest)) return t;
      if (t === 'files' && p.data.length) return t;
    }
    return 'problem';
  }

  function pickWorkshopTab(w) {
    var resources = w.resources || [];
    if (state.tab === 'slides' && w.slides.length) return 'slides';
    if (state.tab === 'notebooks' && w.notebooks.length) return 'notebooks';
    if (state.tab === 'resources' && resources.length) return 'resources';
    if (w.slides.length) return 'slides';
    if (w.notebooks.length) return 'notebooks';
    return 'resources';
  }

  function showTab(name) {
    state.tab = name;
    els.detail.querySelectorAll('.tab').forEach(function (b) {
      b.setAttribute('aria-selected', String(b.dataset.tab === name));
    });
    els.detail.querySelectorAll('.panel').forEach(function (pane) {
      pane.hidden = pane.dataset.panel !== name;
    });
  }

  /* -------------------------------------------------------- routing */

  function syncPlaceholder() {
    els.search.placeholder = isMobile() ? 'Search problems…' : 'Search problems…  ( / )';
  }

  function select(code, push) {
    var p = BY_CODE[code];
    if (!p) return;
    state.code = code;
    state.kind = 'problem';
    if (push && location.hash !== '#' + code) location.hash = code;
    renderDetail(p);
    renderNav();
    closeNav();
    if (isMobile()) window.scrollTo(0, 0);
    else els.main.scrollTop = 0;
    var active = els.nav.querySelector('.nav-item.active');
    if (active && active.scrollIntoView) {
      active.scrollIntoView({ block: 'nearest' });
    }
  }

  function selectWorkshop(id, push) {
    var w = BY_WORKSHOP[id];
    if (!w) return;
    state.code = id;
    state.kind = 'workshop';
    if (push && location.hash !== '#workshop/' + encodeURIComponent(id)) location.hash = 'workshop/' + encodeURIComponent(id);
    renderWorkshop(w);
    renderNav();
    closeNav();
    if (isMobile()) window.scrollTo(0, 0);
    else els.main.scrollTop = 0;
  }
  els.main = document.getElementById('main');

  function showWelcome() {
    state.code = null;
    state.kind = 'problem';
    els.detail.hidden = true;
    els.welcome.hidden = false;
    renderNav();
  }

  function fromHash() {
    var code = decodeURIComponent((location.hash || '').replace(/^#/, ''));
    if (code.indexOf('workshop/') === 0 && BY_WORKSHOP[code.slice(9)]) selectWorkshop(code.slice(9), false);
    else if (code && BY_CODE[code]) select(code, false);
    else showWelcome();
  }

  /* --------------------------------------------------------- events */

  els.menuBtn.addEventListener('click', function () {
    setNav(!document.body.classList.contains('nav-open'));
  });
  els.themeBtn.addEventListener('click', togglePageTheme);
  els.scrim.addEventListener('click', closeNav);

  MOBILE.addEventListener('change', function (e) { if (!e.matches) closeNav(); });

  els.nav.addEventListener('click', function (ev) {
    var head = ev.target.closest('.nav-head');
    if (head) {
      var group = head.parentNode;
      group.classList.toggle('open');
      state.openTopics = state.openTopics || {};
      state.openTopics[group.dataset.topic] = group.classList.contains('open');
      return;
    }
    if (ev.target.closest('.nav-item')) closeNav();
  });

  els.detail.addEventListener('click', function (ev) {
    if (exClick(ev)) return;
    var tab = ev.target.closest('.tab');
    if (tab && !tab.disabled) { showTab(tab.dataset.tab); return; }

    var seg = ev.target.closest('[data-set]');
    if (seg) {
      state.set = seg.dataset.set;
      els.detail.querySelectorAll('[data-set]').forEach(function (b) {
        b.setAttribute('aria-selected', String(b.dataset.set === state.set));
      });
      document.getElementById('caseHost').innerHTML = renderCases(BY_CODE[state.code], state.set);
      return;
    }

    if (ev.target.closest('[data-theme-toggle]')) { toggleCodeTheme(); return; }

    onCopyClick(ev);
  });

  els.detail.addEventListener('pointerdown', function (ev) {
    var handle = ev.target.closest('.ex-resize');
    if (!handle || ev.button !== 0) return;
    ev.preventDefault();
    var host = handle.closest('#explorer');
    var left = host.getBoundingClientRect().left;
    handle.setPointerCapture(ev.pointerId);
    host.classList.add('resizing');
    function move(e) { exApplyWidth(host, e.clientX - left); }
    function up() {
      handle.removeEventListener('pointermove', move);
      handle.removeEventListener('pointerup', up);
      handle.removeEventListener('pointercancel', up);
      host.classList.remove('resizing');
      exSavePrefs();
    }
    handle.addEventListener('pointermove', move);
    handle.addEventListener('pointerup', up);
    handle.addEventListener('pointercancel', up);
  });

  els.detail.addEventListener('keydown', function (ev) {
    var handle = ev.target.closest && ev.target.closest('.ex-resize');
    if (!handle) return;
    var step = ev.shiftKey ? 64 : 16;
    var host = handle.closest('#explorer');
    if (ev.key === 'ArrowLeft') exApplyWidth(host, exPrefs.width - step);
    else if (ev.key === 'ArrowRight') exApplyWidth(host, exPrefs.width + step);
    else if (ev.key === 'Home') exApplyWidth(host, EX_DEFAULT);
    else return;
    ev.preventDefault();
    exSavePrefs();
  });

  els.detail.addEventListener('dblclick', function (ev) {
    var resetHandle = ev.target.closest('.ex-resize');
    if (resetHandle) {
      exApplyWidth(resetHandle.closest('#explorer'), EX_DEFAULT);
      exSavePrefs();
      return;
    }
    var file = ex && ev.target.closest('#explorer [data-ex-file], #explorer [data-ex-tab]');
    if (!file) return;
    exOpenFile(file.dataset.exFile || file.dataset.exTab, true);
    exRender();
  });

  els.detail.addEventListener('input', function (ev) {
    if (!ex || !ev.target.matches('.ex-filter')) return;
    ex.filter = ev.target.value.trim().toLowerCase();
    exRender();
  });

  els.search.addEventListener('input', function () {
    state.query = els.search.value.trim().toLowerCase();
    renderNav();
  });

  document.addEventListener('keydown', function (ev) {
    if (ev.key === '/' && !/^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName)) {
      ev.preventDefault();
      els.search.focus();
      els.search.select();
    } else if (ev.key === 'Escape' && document.body.classList.contains('nav-open')) {
      closeNav();
    } else if (ev.key === 'Escape' && document.activeElement === els.search) {
      els.search.value = '';
      state.query = '';
      renderNav();
      els.search.blur();
    }
  });

  window.addEventListener('hashchange', fromHash);

  /* ----------------------------------------------------------- init */

  renderStats();
  syncPlaceholder();
  MOBILE.addEventListener('change', syncPlaceholder);
  fromHash();
})();
