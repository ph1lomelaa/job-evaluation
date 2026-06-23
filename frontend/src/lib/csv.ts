// Экспорт табличных данных в CSV (RFC 4180) — для выгрузки реестра должностей
// в Excel. Без бэкенда: данные уже посчитаны и отрендерены на странице,
// экспортируем то же самое, без дублирования логики подсчёта баллов в Python.

// Разделитель — «;», а не «,»: в ru-RU локали Excel запятая зарезервирована
// под десятичный разделитель, и список с «,» не раскладывается по столбцам
// при обычном открытии файла.
const DELIMITER = ";";

function escapeCell(value: string | number | null | undefined): string {
  const text = value == null ? "" : String(value);
  return new RegExp(`["${DELIMITER}\n\r]`).test(text) ? `"${text.replace(/"/g, '""')}"` : text;
}

export function toCsv(headers: string[], rows: Array<Array<string | number | null | undefined>>): string {
  const lines = [headers, ...rows].map((row) => row.map(escapeCell).join(DELIMITER));
  return lines.join("\r\n");
}

export function downloadCsv(filename: string, csv: string): void {
  // BOM, чтобы Excel на Windows корректно показывал кириллицу.
  const blob = new Blob(["﻿" + csv], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}
