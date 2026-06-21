// Кэш справочника уровней факторов с backend (один фетч на сессию вкладки).
// Раньше тексты уровней были захардкожены отдельно в mapping.ts и расходились
// со справочником агента (jeval/reference/levels.py) — теперь один источник.

import { api } from "./api";
import type { FactorLevelReference, FactorLevelRules } from "./types";
import { useFetch } from "./useFetch";

let cached: Promise<FactorLevelReference> | null = null;

function loadFactorLevelReference(): Promise<FactorLevelReference> {
  if (!cached) {
    cached = api.getFactorLevels().catch((error: unknown) => {
      cached = null; // дать следующему вызову повторить попытку
      throw error;
    });
  }
  return cached;
}

export function useFactorLevelReference() {
  return useFetch(loadFactorLevelReference, []);
}

let cachedRules: Promise<FactorLevelRules> | null = null;

function loadFactorLevelRules(): Promise<FactorLevelRules> {
  if (!cachedRules) {
    cachedRules = api.getFactorLevelRules().catch((error: unknown) => {
      cachedRules = null;
      throw error;
    });
  }
  return cachedRules;
}

export function useFactorLevelRules() {
  return useFetch(loadFactorLevelRules, []);
}
