"""Минимальный DOCX-парсер на stdlib.

Парсер не интерпретирует данные и не делает выводов. Он только извлекает текст
абзацев и таблиц из Office Open XML, чтобы следующий слой мог собрать черновик.
"""

from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from typing import Optional
from zipfile import BadZipFile, ZipFile
import xml.etree.ElementTree as ET


_W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


@dataclass(frozen=True)
class ParsedBlock:
    kind: str
    text: str
    paragraph_index: Optional[int] = None
    table_index: Optional[int] = None
    row_index: Optional[int] = None
    cell_index: Optional[int] = None


@dataclass(frozen=True)
class ParsedDocument:
    text: str
    tables: list[list[list[str]]]
    blocks: list[ParsedBlock]


def extract_docx_text(data: bytes) -> ParsedDocument:
    """Извлечь текст и таблицы из `.docx`.

    Raises:
        ValueError: если файл не похож на docx или не содержит document.xml.
    """
    try:
        with ZipFile(BytesIO(data)) as zf:
            if "word/document.xml" not in zf.namelist():
                raise ValueError("Файл DOCX не содержит word/document.xml")
            root = ET.fromstring(zf.read("word/document.xml"))
    except BadZipFile as exc:
        raise ValueError("Файл не является корректным DOCX") from exc
    except ET.ParseError as exc:
        raise ValueError("Не удалось разобрать XML внутри DOCX") from exc

    blocks: list[str] = []
    tables: list[list[list[str]]] = []
    structured_blocks: list[ParsedBlock] = []
    paragraph_index = 0
    table_index = 0

    body = root.find(f"{_W}body")
    if body is None:
        return ParsedDocument(text="", tables=[], blocks=[])

    for child in body:
        if child.tag == f"{_W}p":
            text = _paragraph_text(child)
            if text:
                blocks.append(text)
                structured_blocks.append(
                    ParsedBlock(kind="paragraph", text=text, paragraph_index=paragraph_index)
                )
                paragraph_index += 1
        elif child.tag == f"{_W}tbl":
            table, table_blocks = _table_rows(child, table_index)
            if table:
                tables.append(table)
                structured_blocks.extend(table_blocks)
                blocks.append("--- TABLE ---")
                blocks.extend(" | ".join(cell for cell in row if cell) for row in table)
                blocks.append("--- END TABLE ---")
                table_index += 1

    text = "\n".join(line for line in blocks if line.strip())
    return ParsedDocument(text=text, tables=tables, blocks=structured_blocks)


def _paragraph_text(node: ET.Element) -> str:
    parts = [t.text or "" for t in node.iter(f"{_W}t")]
    return " ".join("".join(parts).split())


def _table_rows(node: ET.Element, table_index: int) -> tuple[list[list[str]], list[ParsedBlock]]:
    rows: list[list[str]] = []
    blocks: list[ParsedBlock] = []
    for tr_index, tr in enumerate(node.findall(f"{_W}tr")):
        row: list[str] = []
        for tc_index, tc in enumerate(tr.findall(f"{_W}tc")):
            cell_parts: list[str] = []
            for p in tc.findall(f"{_W}p"):
                p_text = _paragraph_text(p)
                if p_text:
                    cell_parts.append(p_text)
            cell_text = " ".join(cell_parts).strip()
            row.append(cell_text)
            if cell_text:
                blocks.append(
                    ParsedBlock(
                        kind="table_cell",
                        text=cell_text,
                        table_index=table_index,
                        row_index=tr_index,
                        cell_index=tc_index,
                    )
                )
        if any(row):
            rows.append(row)
            blocks.append(
                ParsedBlock(
                    kind="table_row",
                    text=" | ".join(cell for cell in row if cell),
                    table_index=table_index,
                    row_index=tr_index,
                )
            )
    return rows, blocks
