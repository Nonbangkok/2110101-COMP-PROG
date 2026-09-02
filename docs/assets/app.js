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
    scrim:    document.getElementById('scrim')
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
                '<svg class="nav-caret" viewBox="0 0 10 10"><polyline points="3.5,2 6.5,5 3.5,8"/></svg>' +
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
              '<svg class="nav-caret" viewBox="0 0 10 10"><polyline points="3.5,2 6.5,5 3.5,8"/></svg>' +
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
      h += '<div class="file-list">';
      p.data.forEach(function (d, i) {
        var did = 'data-' + p.code + '-' + i;
        h += '<div class="card">' +
               '<div class="card-head"><span class="name">' + esc(d.name) + '</span>' +
               '<span class="size">' + bytes(d.size) + '</span>' +
               '<span class="spacer"></span>' +
               '<a class="btn-link" href="' + esc(repoPath(d.path)) + '" target="_blank" rel="noopener">raw</a>' +
               '<button class="btn" type="button" data-copy="' + did + '">Copy</button></div>' +
               '<pre class="io" id="' + did + '">' + esc(d.text) + '</pre>' +
             '</div>';
      });
      h += '</div>';
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
    showTab(pickWorkshopTab(w));

    function tabBtn(id, label, count, disabled) {
      return '<button class="tab" type="button" role="tab" data-tab="' + id + '"' +
             (disabled ? ' disabled' : '') + ' aria-selected="false">' + label +
             '<span class="pill">' + count + '</span></button>';
    }
  }

  function renderWorkshopResources(w, resources) {
    if (!resources.length) return '<div class="empty-state">No additional files are stored for this workshop.</div>';
    var codes = resources.filter(function (r) { return r.kind === 'code'; });
    var images = resources.filter(function (r) { return r.kind === 'image'; });
    var audio = resources.filter(function (r) { return r.kind === 'audio'; });
    var other = resources.filter(function (r) { return r.kind !== 'code' && r.kind !== 'image' && r.kind !== 'audio'; });
    var h = '';
    if (codes.length) {
      h += '<section class="resource-section"><h2>Code</h2><div class="file-list">';
      codes.forEach(function (r, i) {
        var id = 'workshop-src-' + w.id + '-' + i;
        var lines = r.text.replace(/\n$/, '').split('\n');
        var gutter = lines.map(function (_, n) { return n + 1; }).join('\n');
        h += '<div class="card code-card"><div class="card-head"><span class="name">' + esc(r.name) +
             '</span><span class="size">' + lines.length + ' lines · ' + bytes(r.size) +
             '</span><span class="spacer"></span><a class="btn-link" href="' + esc(repoPath(r.path)) +
             '" target="_blank" rel="noopener">raw</a><button class="btn" type="button" data-theme-toggle title="Switch the code colours">' +
             codeThemeLabel() + '</button><button class="btn" type="button" data-copy="' + id + '">Copy</button></div>' +
             '<div class="code-wrap"><pre class="gutter" aria-hidden="true">' + gutter +
             '</pre><pre class="code"><code id="' + id + '">' + highlightPython(r.text) + '</code></pre></div></div>';
      });
      h += '</div></section>';
    }
    if (images.length) {
      h += '<section class="resource-section"><h2>Images</h2><div class="image-grid">';
      images.forEach(function (r) {
        h += '<a class="image-card" href="' + esc(repoPath(r.path)) + '" target="_blank" rel="noopener"><img src="' +
             esc(repoPath(r.path)) + '" alt="' + esc(r.name) + '" loading="lazy"><span>' + esc(r.name) + '</span></a>';
      });
      h += '</div></section>';
    }
    if (audio.length) {
      h += '<section class="resource-section"><h2>Audio</h2><div class="file-list">';
      audio.forEach(function (r) {
        h += '<div class="card media-card"><div class="card-head"><span class="name">' + esc(r.name) +
             '</span><span class="size">' + bytes(r.size) + '</span><span class="spacer"></span><a class="btn-link" href="' +
             esc(repoPath(r.path)) + '" target="_blank" rel="noopener">Open</a></div><audio controls preload="metadata" src="' +
             esc(repoPath(r.path)) + '"></audio></div>';
      });
      h += '</div></section>';
    }
    if (other.length) {
      h += '<section class="resource-section"><h2>Other files</h2><div class="file-list">';
      other.forEach(function (r) {
        h += '<div class="card"><div class="card-head"><span class="name">' + esc(r.name) +
             '</span><span class="size">' + bytes(r.size) + '</span><span class="spacer"></span><a class="btn-link" href="' +
             esc(repoPath(r.path)) + '" target="_blank" rel="noopener">Open</a><a class="btn-link" href="' +
             esc(repoPath(r.path)) + '" download>Download</a></div></div>';
      });
      h += '</div></section>';
    }
    return h;
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

  els.search.addEventListener('input', function () {
    state.query = els.search.value.trim().toLowerCase();
    renderNav();
  });

  document.addEventListener('keydown', function (ev) {
    if (ev.key === '/' && document.activeElement !== els.search) {
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
