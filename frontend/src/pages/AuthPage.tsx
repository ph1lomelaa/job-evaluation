import { useMemo } from "react";
import { useLocation } from "react-router-dom";
import { API_BASE_URL } from "../lib/api";

const AUTH_MESSAGES: Record<string, string> = {
  access_denied: "Ваш Gmail не добавлен в allowlist. Обратитесь к администратору.",
  google_state: "Не удалось подтвердить OAuth-сессию. Попробуйте войти ещё раз.",
  google_403: "Google-аккаунт не подходит для входа в систему.",
  google_503: "Google login временно недоступен.",
  google_conflict: "Этот Gmail уже связан с другим аккаунтом.",
};

export default function AuthPage() {
  const location = useLocation();
  const authError = useMemo(() => {
    const params = new URLSearchParams(location.search);
    const value = params.get("auth_error");
    return value ? AUTH_MESSAGES[value] ?? "Не удалось выполнить вход." : null;
  }, [location.search]);

  function startGoogleLogin() {
    window.location.assign(`${API_BASE_URL}/api/auth/google/start`);
  }

  return (
    <main className="auth-shell min-h-screen w-full bg-white px-6 py-10 sm:px-10 sm:py-16">
      <section className="mx-auto flex min-h-[calc(100vh-80px)] max-w-[640px] flex-col justify-center">
        <div className="mb-8 flex items-center gap-3 text-sm font-medium text-[#34312e]">
          <span className="grid h-10 w-10 place-items-center rounded-full border border-[#7c4dba]/45" aria-hidden="true">
            <span className="flex items-end gap-[3px]">
              <span className="h-2 w-[3px] rounded-full bg-[#7c4dba]/45" />
              <span className="h-4 w-[3px] rounded-full bg-[#7c4dba]" />
              <span className="h-3 w-[3px] rounded-full bg-[#7c4dba]/70" />
            </span>
          </span>
          <span>Оценка должностей</span>
        </div>

        <h1 className="font-display text-[44px] font-medium leading-[0.95] tracking-[-1.8px] text-[#211f1d] sm:text-[64px]">
          Вход через Google.
          <br />
          Только для разрешённых Gmail.
        </h1>
        <p className="mt-6 max-w-[540px] text-base leading-7 text-[#77736e] sm:text-lg">
          Сначала администратор добавляет Gmail в allowlist. После этого вход открывается через
          Google OAuth и система сразу выдаёт роль.
        </p>

        {authError && (
          <div className="mt-8 rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
            {authError}
          </div>
        )}

        <div className="mt-10 rounded-[22px] border border-[#ded9d2] bg-white p-6 shadow-[0_6px_0_rgba(42,34,25,0.04),0_18px_60px_rgba(42,34,25,0.07)]">
          <button
            type="button"
            onClick={startGoogleLogin}
            className="min-h-[58px] w-full rounded-[14px] bg-[#252527] px-5 text-base font-medium text-white transition-colors hover:bg-[#151516]"
          >
            Войти через Google
          </button>
          <p className="mt-4 text-sm leading-6 text-[#817d77]">
            Если Gmail не добавлен администратором, вход будет отклонён.
          </p>
        </div>
      </section>
    </main>
  );
}

