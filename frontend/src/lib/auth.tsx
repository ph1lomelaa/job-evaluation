import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { ACTIVE_COMPANY_KEY, CSRF_TOKEN_KEY, api } from "./api";
import type { Company, User } from "./types";

interface CompanyDraft {
  name: string;
  purpose?: string;
  user_role?: string;
  organization_size?: string;
}

interface AuthState {
  loading: boolean;
  user: User | null;
  companies: Company[];
  activeCompany: Company | null;
  login: (email: string, password: string) => Promise<void>;
  register: (displayName: string, email: string, password: string) => Promise<void>;
  createCompany: (draft: CompanyDraft) => Promise<Company>;
  selectCompany: (company: Company) => void;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthState | null>(null);

function pickCompany(companies: Company[]): Company | null {
  const saved = window.localStorage.getItem(ACTIVE_COMPANY_KEY);
  return companies.find((company) => company.id === saved) ?? companies[0] ?? null;
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState<User | null>(null);
  const [companies, setCompanies] = useState<Company[]>([]);
  const [activeCompany, setActiveCompany] = useState<Company | null>(null);

  const applySession = useCallback((nextUser: User, nextCompanies: Company[]) => {
    const selected = pickCompany(nextCompanies);
    setUser(nextUser);
    setCompanies(nextCompanies);
    setActiveCompany(selected);
    if (selected) window.localStorage.setItem(ACTIVE_COMPANY_KEY, selected.id);
    else window.localStorage.removeItem(ACTIVE_COMPANY_KEY);
  }, []);

  const clearSession = useCallback(() => {
    window.localStorage.removeItem(ACTIVE_COMPANY_KEY);
    window.localStorage.removeItem(CSRF_TOKEN_KEY);
    setUser(null);
    setCompanies([]);
    setActiveCompany(null);
  }, []);

  useEffect(() => {
    api
      .me()
      .then((response) => {
        window.localStorage.setItem(CSRF_TOKEN_KEY, response.csrf_token);
        applySession(response.user, response.companies);
      })
      .catch(clearSession)
      .finally(() => setLoading(false));
  }, [applySession, clearSession]);

  async function login(email: string, password: string) {
    const response = await api.login({ email, password });
    window.localStorage.setItem(CSRF_TOKEN_KEY, response.csrf_token);
    applySession(response.user, response.companies);
  }

  async function register(displayName: string, email: string, password: string) {
    const response = await api.register({ display_name: displayName, email, password });
    window.localStorage.setItem(CSRF_TOKEN_KEY, response.csrf_token);
    applySession(response.user, response.companies);
  }

  async function createCompany(draft: CompanyDraft) {
    const company = await api.createCompany(draft);
    const nextCompanies = [...companies, company];
    setCompanies(nextCompanies);
    setActiveCompany(company);
    window.localStorage.setItem(ACTIVE_COMPANY_KEY, company.id);
    return company;
  }

  function selectCompany(company: Company) {
    setActiveCompany(company);
    window.localStorage.setItem(ACTIVE_COMPANY_KEY, company.id);
    void api.activateCompany(company.id).catch(() => undefined);
  }

  async function logout() {
    try {
      await api.logout();
    } finally {
      clearSession();
    }
  }

  const value = useMemo<AuthState>(
    () => ({
      loading,
      user,
      companies,
      activeCompany,
      login,
      register,
      createCompany,
      selectCompany,
      logout,
    }),
    [loading, user, companies, activeCompany],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthState {
  const value = useContext(AuthContext);
  if (!value) throw new Error("useAuth должен использоваться внутри AuthProvider");
  return value;
}
