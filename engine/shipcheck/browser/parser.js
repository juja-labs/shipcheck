/* =========================================================================
 *  DOM "stripper" — keeps empty controls **and** guarantees unique
 *  parser-semantic-id values by appending numeric suffixes
 * ========================================================================= */

const parse = () => {
  /* ---------- globals --------------------------------------------------- */
  const BLACKLISTED_TAGS = new Set([
    'script', 'style', 'link', 'meta', 'noscript', 'template',
    'iframe', 'svg', 'canvas', 'picture', 'video', 'audio',
    'object', 'embed'
  ]);

  const ALLOWED_ATTR = new Set([
    'id', 'type', 'name', 'value', 'placeholder',
    'checked', 'disabled', 'readonly', 'required', 'maxlength',
    'min', 'max', 'step', 'role', 'tabindex', 'alt', 'title',
    'for', 'action', 'method', 'contenteditable', 'selected',
    'multiple', 'autocomplete'
  ]);

  const PRESERVE_EMPTY_TAGS = new Set([
    'input', 'select', 'textarea', 'button', 'img', 'head', 'title', 'form'
  ]);

  const USED_SEMANTIC_IDS = new Set();

  /* ---------- helpers -------------------------------------------------- */
  const copyAllowed = (src, dst) => {
    for (const a of src.attributes) {
      if (
        ALLOWED_ATTR.has(a.name) ||
        a.name.startsWith('aria-') ||
        a.name.startsWith('parser-')
      ) {
        dst.setAttribute(a.name, a.value);
      }
    }
  };

  const slug = (t) =>
    t.toLowerCase().replace(/\s+/g, ' ').trim()
      .replace(/[^\w]+/g, '_').replace(/^_+|_+$/g, '').slice(0, 20);

  const uniqueName = (base) => {
    let name = base || 'item';
    if (!USED_SEMANTIC_IDS.has(name)) {
      USED_SEMANTIC_IDS.add(name);
      return name;
    }
    let i = 1;
    while (USED_SEMANTIC_IDS.has(name + i)) i++;
    USED_SEMANTIC_IDS.add(name + i);
    return name + i;
  };

  const isEmpty = (el) => {
    if (PRESERVE_EMPTY_TAGS.has(el.tagName.toLowerCase())) return false;
    for (const n of el.childNodes) {
      if (n.nodeType === 3 && n.textContent.trim()) return false;
      if (n.nodeType === 1 && !isEmpty(n)) return false;
    }
    return true;
  };

  const isVisible = (el) => {
    const style = window.getComputedStyle(el);
    const hidden =
      style.display === 'none' ||
      style.visibility === 'hidden' ||
      parseFloat(style.opacity) === 0;

    const zeroSize = el.offsetWidth === 0 && el.offsetHeight === 0;

    const rect = el.getBoundingClientRect();
    const scrollLeft = window.scrollX || document.documentElement.scrollLeft;
    const right = rect.right;
    const top = rect.top;
    const outOfPort = (right + scrollLeft < 0);

    let belowPortNotScrollable = false;
    if (top > window.innerHeight && !(document.documentElement.scrollHeight > window.innerHeight)) {
      let hasScrollableAncestor = false;
      for (let p = el?.parentElement; p; p = p.parentElement) {
        const cs = getComputedStyle(p);
        const canScrollY = /(auto|scroll)/.test(cs.overflowY) && p.scrollHeight > p.clientHeight;
        if (canScrollY) { hasScrollableAncestor = true; break; }
      }
      belowPortNotScrollable = !hasScrollableAncestor;
    }
    if (hidden || zeroSize || outOfPort || belowPortNotScrollable) return false;
    return true;
  };

  const replaceElement = (el, newTag, child) => {
    const r = document.createElement(newTag);
    for (const a of el.attributes) r.setAttribute(a.name, a.value);
    copyAllowed(child, r);
    r.innerHTML = child.innerHTML;
    return r;
  };

  const pullUpChild = (parent, child) => {
    copyAllowed(child, parent);
    parent.innerHTML = child.innerHTML;
  };

  const flatten = (el) => {
    while (el.children.length === 1) {
      const child = el.children[0];
      const p = el.tagName.toLowerCase();
      const c = child.tagName.toLowerCase();
      if (p !== 'div' && c !== 'div') break;
      el = (p === 'div' && c !== 'div')
        ? replaceElement(el, child.tagName, child)
        : (pullUpChild(el, child), el);
    }
    return el;
  };

  /* ---------- clear parser-* attrs before run -------------------------- */
  (() => {
    const clearParserAttrs = (el) => {
      if (!el || !el.attributes) return;
      for (const a of Array.from(el.attributes)) {
        if (a.name.startsWith('parser-')) el.removeAttribute(a.name);
      }
    };

    // Clear on <html> itself first
    clearParserAttrs(document.documentElement);

    // Walk every element efficiently and clear any parser-* attrs
    const walker = document.createTreeWalker(document, NodeFilter.SHOW_ELEMENT);
    let node = walker.currentNode;
    while (node) {
      clearParserAttrs(node);
      node = walker.nextNode();
    }
  })();


  /* ==================================================================== */
  function automaticStripElement(original, parentName = '', parentIsClickable = false) {
    if (!original || original.nodeType !== 1) return null;
    const tag = original.tagName.toLowerCase();
    if (BLACKLISTED_TAGS.has(tag)) return null;
    if (!isVisible(original)) return null;

    let clone = document.createElement(original.tagName);
    copyAllowed(original, clone);

    const computedStyle = window.getComputedStyle(original);
    if (computedStyle.pointerEvents !== 'auto') {
      clone.setAttribute('parser-pointer-events', computedStyle.pointerEvents);
    }
    if (document.activeElement === original) {
      clone.setAttribute('parser-is-focused', 'true');
    }

    const isDisabled = original.disabled ||
      original.hasAttribute('disabled') ||
      computedStyle.pointerEvents === 'none';

    const probablyClickable = (() => {
      if (['button', 'select', 'summary', 'area', 'input'].includes(tag)) return true;
      if (tag === 'a' && original.hasAttribute('href')) return true;
      if (original.hasAttribute('onclick')) return true;
      const r = original.getAttribute('role');
      if (['button', 'link', 'checkbox', 'radio', 'option'].includes(r)) return true;
      return computedStyle.cursor === 'pointer';
    })();

    const isClickable = !parentIsClickable && probablyClickable && !isDisabled;

    let thisName = '';
    if (isClickable) {
      const base = slug((original.innerText || '').trim() ||
        original.getAttribute('title') ||
        original.getAttribute('placeholder') ||
        tag);
      thisName = uniqueName(parentName ? `${parentName}.${base}` : base);
      for (const e of [clone, original]) {
        e.setAttribute('parser-semantic-id', thisName);
        e.setAttribute('parser-clickable', 'true');
      }
    }

    if (original.closest('[parser-maybe-hoverable="true"]')) {
      clone.setAttribute('parser-maybe-hoverable', 'true');
      original.setAttribute('parser-maybe-hoverable', 'true');
    }

    if (tag === 'input' || tag === 'textarea' || original.hasAttribute('contenteditable')) {
      const t = original.getAttribute('type') || 'text';
      const inputIsDisabled = original.disabled || original.readOnly;
      if (!inputIsDisabled && !thisName) {
        const base = slug((original.getAttribute('placeholder') ||
          original.getAttribute('name') ||
          original.value || '').trim() || tag);
        thisName = uniqueName(parentName ? `${parentName}.${base}` : base);
      }
      if (!inputIsDisabled && thisName) {
        clone.setAttribute('parser-semantic-id', thisName);
        clone.setAttribute('value', original.value || '');
        clone.setAttribute('parser-input-disabled', 'false');
        clone.setAttribute('parser-can-edit', !original.readOnly ? 'true' : 'false');
        original.setAttribute('parser-semantic-id', thisName);
      }
      if (!inputIsDisabled && thisName && t === 'number') {
        clone.setAttribute('parser-numeric-value', original.valueAsNumber || '');
      }
      if (!inputIsDisabled && thisName && original.selectionStart !== undefined) {
        clone.setAttribute('parser-selection-start', original.selectionStart);
        clone.setAttribute('parser-selection-end', original.selectionEnd);
      }
    }

    if (tag === 'select') {
      const selectIsDisabled = original.disabled || original.hasAttribute('disabled');
      if (!selectIsDisabled) {
        if (!thisName) {
          const base = slug((original.getAttribute('name') || tag));
          thisName = uniqueName(parentName ? `${parentName}.${base}` : base);
        }
        clone.setAttribute('parser-semantic-id', thisName);
        clone.setAttribute('parser-value', original.value);
        clone.setAttribute('parser-selected-index', original.selectedIndex);
        clone.setAttribute('parser-has-multiple', original.multiple ? 'true' : 'false');
        const selectedOptions = Array.from(original.selectedOptions).map(opt => opt.value).join(',');
        clone.setAttribute('parser-selected-values', selectedOptions);
        original.setAttribute('parser-semantic-id', thisName);
        for (const opt of original.querySelectorAll('option')) {
          const o = document.createElement('option');
          o.textContent = opt.textContent.trim();
          o.setAttribute('value', opt.value);
          o.setAttribute('parser-selected', opt.selected ? 'true' : 'false');
          const optName = uniqueName(`${thisName}.${slug(opt.textContent)}`);
          o.setAttribute('parser-semantic-id', optName);
          opt.setAttribute('parser-semantic-id', optName);
          clone.appendChild(o);
        }
      }
    }

    for (const child of original.children) {
      const cleaned = automaticStripElement(
        child,
        thisName || parentName,
        parentIsClickable || isClickable
      );
      if (cleaned && (!isEmpty(cleaned))) {
        clone.appendChild(cleaned);
      }
    }

    for (const n of original.childNodes) {
      if (n.nodeType === 3 && n.textContent.trim()) {
        clone.appendChild(document.createTextNode(n.textContent.trim()));
      }
    }

    clone = flatten(clone);
    for (let i = clone.children.length - 1; i >= 0; i--) {
      const c = clone.children[i];
      if (!PRESERVE_EMPTY_TAGS.has(c.tagName.toLowerCase()) && isEmpty(c)) {
        clone.removeChild(c);
      }
    }

    return clone;
  }

  const result = automaticStripElement(document.documentElement);

  /* ---------- 뷰포트 필터링 ----------------------------------------- */
  // 원본 DOM에서 뷰포트 내 요소를 판별 (파싱된 클론이 아닌 원본 기준)
  const vh = window.innerHeight;
  const vw = window.innerWidth;
  const MARGIN = 50; // 뷰포트 경계 약간 여유

  const isInViewport = (semanticId) => {
    const orig = document.querySelector(`[parser-semantic-id="${semanticId}"]`);
    if (!orig) return false;
    const r = orig.getBoundingClientRect();
    return r.bottom > -MARGIN && r.top < vh + MARGIN
        && r.right > -MARGIN && r.left < vw + MARGIN;
  };

  // 전체 요소 (스크롤 전체 페이지)
  const allClickable = Array.from(result.querySelectorAll('[parser-clickable="true"]'))
    .map(el => el.getAttribute('parser-semantic-id'));
  const allInput = Array.from(result.querySelectorAll('input[parser-semantic-id], textarea[parser-semantic-id], [contenteditable][parser-semantic-id]'));
  const allSelect = Array.from(result.querySelectorAll('select[parser-semantic-id]'));
  const allHoverable = Array.from(result.querySelectorAll('[parser-maybe-hoverable="true"]'))
    .map(el => el.getAttribute('parser-semantic-id'));

  // 뷰포트 내 요소만 필터
  const vpClickable = allClickable.filter(isInViewport);
  const vpInput = allInput
    .map(el => ({
      id: el.getAttribute('parser-semantic-id'),
      disabled: el.hasAttribute('parser-input-disabled'),
      type: el.getAttribute('type') || (el.tagName.toLowerCase() === 'textarea' ? 'textarea' : 'contenteditable'),
      value: el.value || el.textContent,
      canEdit: el.getAttribute('parser-can-edit') === 'true',
      isFocused: el.getAttribute('parser-is-focused') === 'true'
    }))
    .filter(e => isInViewport(e.id));
  const vpSelect = allSelect
    .map(el => ({
      id: el.getAttribute('parser-semantic-id'),
      value: el.value,
      selectedIndex: el.selectedIndex,
      multiple: el.multiple,
      selectedValues: Array.from(el.selectedOptions).map(opt => opt.value)
    }))
    .filter(e => isInViewport(e.id));

  // 뷰포트 내 텍스트 길이 추정
  const vpTextLen = (() => {
    let len = 0;
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    let node;
    while (node = walker.nextNode()) {
      const parent = node.parentElement;
      if (!parent) continue;
      const r = parent.getBoundingClientRect();
      if (r.bottom > 0 && r.top < vh && r.right > 0 && r.left < vw) {
        len += (node.textContent || '').trim().length;
      }
    }
    return len;
  })();

  // 스크롤 위치 정보
  const scrollY = window.scrollY || document.documentElement.scrollTop;
  const scrollMax = document.documentElement.scrollHeight - vh;
  const scrollRatio = scrollMax > 0 ? scrollY / scrollMax : 0;

  return {
    html: result.outerHTML,
    // 뷰포트 기준 (에이전트가 "지금 보는" 것)
    clickable_elements: vpClickable,
    input_elements: vpInput,
    select_elements: vpSelect,
    hoverable_elements: allHoverable.filter(isInViewport),
    // 뷰포트 메타데이터
    viewport_element_count: vpClickable.length + vpInput.length + vpSelect.length,
    viewport_text_length: vpTextLen,
    // 전체 페이지 메타데이터 (맥락용)
    total_clickable_count: allClickable.length,
    total_input_count: allInput.length,
    total_select_count: allSelect.length,
    // 스크롤 상태
    scroll_y: scrollY,
    scroll_ratio: Math.round(scrollRatio * 100) / 100,
    scroll_max: scrollMax,
    page_height: document.documentElement.scrollHeight,
    viewport_height: vh,
  };
}

parse();
