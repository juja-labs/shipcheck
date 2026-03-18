"""CDP DOM 추출 — DOMSnapshot + AX Tree 병합.

DOMSnapshot.captureSnapshot으로 좌표 + 속성 + computed styles를,
Accessibility.getFullAXTree로 역할 + 이름을 가져온 뒤
backendNodeId 기준으로 병합한다.
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

# captureSnapshot에 요청할 computed style 목록
COMPUTED_STYLES = ["display", "visibility", "opacity"]


@dataclass
class RawNode:
    """CDP에서 추출한 원시 노드 데이터."""

    backend_node_id: int
    tag: str  # 소문자 태그명

    # 좌표 (CSS 픽셀, 문서 기준)
    x: float = 0.0
    y: float = 0.0
    width: float = 0.0
    height: float = 0.0
    has_bounds: bool = False

    # DOM 속성
    attributes: dict[str, str] = field(default_factory=dict)

    # 접근성 (AX tree 병합 후 채워짐)
    ax_role: str | None = None
    ax_name: str | None = None
    ax_value: str | None = None
    ax_properties: dict[str, str] = field(default_factory=dict)

    # computed styles
    display: str = ""
    visibility: str = ""
    opacity: str = "1"

    # 특수 플래그
    is_contenteditable: bool = False
    is_clickable: bool = False  # DOMSnapshot의 isClickable 필드


# DOMSnapshot에서 무시할 태그
_SKIP_TAGS = frozenset(
    {"script", "style", "head", "meta", "link", "title", "noscript", "svg", "path"}
)


def _build_rare_boolean_set(data: dict | None) -> set[int]:
    """DOMSnapshot RareBooleanData → set of indices."""
    if not data:
        return set()
    return set(data.get("index", []))


async def extract_raw_tree(cdp_session) -> list[RawNode]:
    """CDP DOMSnapshot + AX Tree 병렬 호출 후 backendNodeId 기준 병합.

    Returns:
        RawNode 리스트 (필터링 전 — 모든 요소 포함).
    """
    # 두 CDP 호출을 병렬 실행
    snapshot_coro = cdp_session.send(
        "DOMSnapshot.captureSnapshot",
        {
            "computedStyles": COMPUTED_STYLES,
            "includeDOMRects": True,
            "includePaintOrder": False,
        },
    )
    ax_coro = cdp_session.send("Accessibility.getFullAXTree")

    snapshot, ax_tree = await asyncio.gather(
        snapshot_coro, ax_coro, return_exceptions=True
    )

    # CDP 실패 처리
    if isinstance(snapshot, Exception):
        logger.error("DOMSnapshot.captureSnapshot 실패: %s", snapshot)
        return []
    if isinstance(ax_tree, Exception):
        logger.warning("Accessibility.getFullAXTree 실패: %s — DOM만 사용", ax_tree)
        ax_tree = {"nodes": []}

    # --- 1. DOMSnapshot 파싱 ---
    nodes_by_id: dict[int, RawNode] = {}
    strings = snapshot.get("strings", [])

    def _str(idx: int) -> str:
        return strings[idx] if 0 <= idx < len(strings) else ""

    for document in snapshot.get("documents", []):
        dom_nodes = document.get("nodes", {})
        layout = document.get("layout", {})

        backend_ids = dom_nodes.get("backendNodeId", [])
        node_types = dom_nodes.get("nodeType", [])
        node_names = dom_nodes.get("nodeName", [])
        attributes_list = dom_nodes.get("attributes", [])
        clickable_set = _build_rare_boolean_set(dom_nodes.get("isClickable"))

        # layout nodeIndex → layout array position
        layout_node_indices = layout.get("nodeIndex", [])
        layout_bounds = layout.get("bounds", [])
        layout_styles = layout.get("styles", [])

        layout_map: dict[int, int] = {}
        for li, ni in enumerate(layout_node_indices):
            if ni not in layout_map:
                layout_map[ni] = li

        for i, bid in enumerate(backend_ids):
            # element nodes만 (nodeType 1)
            if i >= len(node_types) or node_types[i] != 1:
                continue

            tag = _str(node_names[i]).lower() if i < len(node_names) else ""
            if tag in _SKIP_TAGS:
                continue

            # 속성 파싱 (key-value 쌍)
            attrs: dict[str, str] = {}
            if i < len(attributes_list):
                attr_indices = attributes_list[i]
                for j in range(0, len(attr_indices) - 1, 2):
                    attrs[_str(attr_indices[j])] = _str(attr_indices[j + 1])

            node = RawNode(
                backend_node_id=bid,
                tag=tag,
                attributes=attrs,
                is_contenteditable=(
                    attrs.get("contenteditable", "").lower()
                    not in ("", "false", "inherit")
                ),
                is_clickable=i in clickable_set,
            )

            # 레이아웃 정보 (bounds + computed styles)
            if i in layout_map:
                li_idx = layout_map[i]
                if li_idx < len(layout_bounds):
                    b = layout_bounds[li_idx]
                    if len(b) >= 4:
                        node.x, node.y = b[0], b[1]
                        node.width, node.height = b[2], b[3]
                        node.has_bounds = True

                if li_idx < len(layout_styles):
                    style_indices = layout_styles[li_idx]
                    for si, style_name in enumerate(COMPUTED_STYLES):
                        if si < len(style_indices):
                            setattr(node, style_name, _str(style_indices[si]))

            nodes_by_id[bid] = node

    # --- 2. AX Tree 병합 ---
    for ax_node in ax_tree.get("nodes", []):
        if ax_node.get("ignored"):
            continue

        bid = ax_node.get("backendDOMNodeId")
        if bid is None or bid not in nodes_by_id:
            continue

        node = nodes_by_id[bid]

        role_obj = ax_node.get("role", {})
        if isinstance(role_obj, dict):
            node.ax_role = role_obj.get("value")

        name_obj = ax_node.get("name", {})
        if isinstance(name_obj, dict):
            node.ax_name = name_obj.get("value")

        value_obj = ax_node.get("value", {})
        if isinstance(value_obj, dict):
            node.ax_value = value_obj.get("value")

        for prop in ax_node.get("properties", []):
            prop_name = prop.get("name", "")
            prop_val = prop.get("value", {})
            if isinstance(prop_val, dict) and prop_val.get("value") is not None:
                node.ax_properties[prop_name] = str(prop_val["value"])

    return list(nodes_by_id.values())
