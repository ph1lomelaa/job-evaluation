"""Резолвер кириллического TTF-шрифта для ReportLab.

Встроенные шрифты ReportLab (Helvetica, Times) не содержат кириллических
глифов — без явной регистрации внешнего TTF кириллический текст в PDF
рендерится пустыми прямоугольниками. Подходящий шрифт ищем по списку
известных путей вместо вендоринга бинарника в репозиторий: прод-контейнер
ставит пакет `fonts-dejavu-core` (см. `backend/Dockerfile`), для локальной
разработки используются шрифты, уже установленные в ОС.
"""

from __future__ import annotations

import logging
import os
from functools import lru_cache

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

logger = logging.getLogger(__name__)

FONT_NAME = "PdfCyrillic"
FONT_NAME_BOLD = "PdfCyrillic-Bold"

# (путь к обычному начертанию, путь к жирному или None — тогда жирность
# эмулируется тем же файлом обычного начертания).
_CANDIDATES: list[tuple[str, str | None]] = [
    # Debian/Ubuntu — прод-контейнер, см. backend/Dockerfile (fonts-dejavu-core).
    (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ),
    # Alpine/Fedora и другие частые Linux-пути для того же пакета.
    (
        "/usr/share/fonts/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
    ),
    (
        "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    ),
    # macOS — шрифт уже установлен системой, скачивать ничего не нужно.
    ("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", None),
    # Windows.
    (r"C:\Windows\Fonts\arial.ttf", r"C:\Windows\Fonts\arialbd.ttf"),
]


@lru_cache(maxsize=1)
def register_cyrillic_font() -> tuple[str, str]:
    """Регистрирует кириллический шрифт в ReportLab (один раз за процесс —
    `pdfmetrics` хранит регистрацию в общем для процесса реестре) и
    возвращает (имя_обычного_начертания, имя_жирного_начертания)."""
    candidates = list(_CANDIDATES)
    override = os.environ.get("JEVAL_PDF_FONT_PATH")
    if override:
        candidates.insert(0, (override, os.environ.get("JEVAL_PDF_FONT_BOLD_PATH")))

    for regular_path, bold_path in candidates:
        if not regular_path or not os.path.isfile(regular_path):
            continue
        pdfmetrics.registerFont(TTFont(FONT_NAME, regular_path))
        if bold_path and os.path.isfile(bold_path):
            pdfmetrics.registerFont(TTFont(FONT_NAME_BOLD, bold_path))
        else:
            pdfmetrics.registerFont(TTFont(FONT_NAME_BOLD, regular_path))
        logger.info("PDF-экспорт: используется кириллический шрифт %s", regular_path)
        return FONT_NAME, FONT_NAME_BOLD

    raise RuntimeError(
        "Не найден TTF-шрифт с кириллицей для PDF-экспорта. В контейнере "
        "должен быть установлен пакет fonts-dejavu-core (см. backend/Dockerfile); "
        "локально путь к шрифту можно задать явно через переменную окружения "
        "JEVAL_PDF_FONT_PATH."
    )
