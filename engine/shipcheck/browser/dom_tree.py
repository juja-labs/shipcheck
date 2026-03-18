"""DOM 트리 필터링 + 직렬화.

RawNode 리스트를 받아 가시성/인터랙티브 필터를 적용하고,
LLM이 읽을 인덱스 기반 텍스트와 selector_map을 생성한다.

직렬화 형식 예시:
  [0] button "Create a free form"
  [1] textbox "Email" placeholder="Enter email"
  [2] link "Sign in" href="/login"
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

from .cdp_dom import RawNode

logger = logging.getLogger(__name__)

# 인터랙티브로 간주하는 AX role
INTERACTIVE_ROLES = frozenset({
    "button", "link", "textbox", "searchbox", "combobox",
    "checkbox", "radio", "tab", "menuitem", "menuitemcheckbox",
    "menuitemradio", "option", "switch", "slider", "spinbutton",
    "treeitem",
})

# AX role 없어도 인터랙티브로 간주하는 태그
INTERACTIVE_TAGS = frozenset({
    "input", "textarea", "select", "button", "a",
})

# 직렬화에 포함할 HTML 속성
INCLUDE_ATTRS = (
    "placeholder", "href", "type", "name",
    "aria-label", "aria-expanded", "aria-checked",
    "required", "disabled", "readonly",
)


@dataclass
class SerializedTree:
    """직렬화 결과."""

    text: str  # LLM에 전달할 텍스트
    selector_map: dict[int, int]  # index → backendNodeId
    interactive_count: int
    text_length: int


def filter_and_serialize(
    nodes: list[RawNode],
    scroll_y: float,
    viewport: dict[str, int],
    viewport_margin: float = 300.0,
) -> SerializedTree:
    """RawNode 리스트 → 필터링 → 인덱스 할당 → 직렬화.

    Args:
        nodes: extract_raw_tree()의 반환값
        scroll_y: 현재 스크롤 위치 (window.scrollY)
        viewport: {"width": 1280, "height": 720}
        viewport_margin: 뷰포트 밖 허용 여유 (px)
    """
    vh = viewport.get("height", 720)
    vw = viewport.get("width", 1280)

    visible_top = scroll_y - viewport_margin
    visible_bottom = scroll_y + vh + viewport_margin

    interactive: list[RawNode] = []

    for node in nodes:
        if not _is_visible(node):
            continue
        if not _in_viewport(node, visible_top, visible_bottom, vw, viewport_margin):
            continue
        if not _is_interactive(node):
            continue
        if not _has_name_or_is_input(node):
            continue
        interactive.append(node)

    # 페이지 순서대로 정렬 (위→아래, 좌→우)
    interactive.sort(key=lambda n: (n.y, n.x))

    # 인덱스 할당 + 직렬화
    lines: list[str] = []
    selector_map: dict[int, int] = {}

    for idx, node in enumerate(interactive):
        selector_map[idx] = node.backend_node_id
        lines.append(_serialize_node(idx, node))

    text = "\n".join(lines)

    return SerializedTree(
        text=text,
        selector_map=selector_map,
        interactive_count=len(interactive),
        text_length=len(text),
    )


# -------------------------------------------------------------------
# 필터 함수들
# -------------------------------------------------------------------


def _is_visible(node: RawNode) -> bool:
    """CSS 가시성 + 레이아웃 존재 확인."""
    if not node.has_bounds:
        return False
    if node.width < 1 or node.height < 1:
        return False
    if node.display.lower() == "none":
        return False
    if node.visibility.lower() == "hidden":
        return False
    try:
        if float(node.opacity) <= 0:
            return False
    except (ValueError, TypeError):
        pass
    return True


def _in_viewport(
    node: RawNode,
    visible_top: float,
    visible_bottom: float,
    viewport_width: float,
    margin: float,
) -> bool:
    """뷰포트 + margin 안에 있는지 확인. bounds는 문서 좌표."""
    if node.y + node.height < visible_top:
        return False
    if node.y > visible_bottom:
        return False
    if node.x + node.width < -margin:
        return False
    if node.x > viewport_width + margin:
        return False
    return True


def _is_interactive(node: RawNode) -> bool:
    """인터랙티브 요소인지 확인."""
    if node.ax_role and node.ax_role.lower() in INTERACTIVE_ROLES:
        return True
    if node.tag in INTERACTIVE_TAGS:
        return True
    if node.is_contenteditable:
        return True
    if node.is_clickable and node.tag in ("div", "span", "li", "td", "img"):
        return True
    return False


def _has_name_or_is_input(node: RawNode) -> bool:
    """이름이 있거나 폼 요소인지 확인 (이름 없는 generic 요소 제외)."""
    if node.ax_name and node.ax_name.strip():
        return True
    if node.tag in ("input", "textarea", "select"):
        return True
    if node.is_contenteditable:
        return True
    # is_clickable인 div/span 등은 이름 없어도 포함
    if node.is_clickable:
        return True
    return False


# -------------------------------------------------------------------
# 직렬화
# -------------------------------------------------------------------


def _serialize_node(idx: int, node: RawNode) -> str:
    """단일 노드 → '[idx] role "name" attr=val' 형태 문자열."""
    role = node.ax_role or node.tag
    name = _truncate(node.ax_name or "", 80)

    line = f"[{idx}] {role}"
    if name:
        line += f' "{name}"'

    # 주요 HTML 속성
    attr_parts: list[str] = []
    for attr in INCLUDE_ATTRS:
        val = node.attributes.get(attr)
        if val:
            attr_parts.append(f'{attr}="{_truncate(val, 40)}"')

    # 현재 입력값 (input 요소의 값 표시)
    if node.ax_value and node.tag in ("input", "textarea", "select"):
        attr_parts.append(f'value="{_truncate(node.ax_value, 30)}"')

    # AX 속성 (checked, expanded 등)
    for prop_name in ("checked", "expanded", "disabled", "required"):
        val = node.ax_properties.get(prop_name)
        if val and val.lower() not in ("false", "0"):
            attr_parts.append(f"{prop_name}={val}")

    if node.is_contenteditable and role not in ("textbox", "searchbox"):
        attr_parts.append("contenteditable")

    if attr_parts:
        line += " " + " ".join(attr_parts)

    return line


def _truncate(s: str, max_len: int) -> str:
    if len(s) <= max_len:
        return s
    return s[: max_len - 3] + "..."
