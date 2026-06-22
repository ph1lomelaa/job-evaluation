import { FormEvent, useMemo, useState } from "react";
import { useLocation } from "react-router-dom";
import { API_BASE_URL, ApiError } from "../lib/api";
import { useAuth } from "../lib/auth";

const AUTH_MESSAGES: Record<string, string> = {
  access_denied: "Ваш Gmail не добавлен в список доступа. Обратитесь к администратору.",
  google_state: "Не удалось подтвердить OAuth-сессию. Попробуйте войти ещё раз.",
  google_403: "Google-аккаунт не подходит для входа в систему.",
  google_503: "Вход через Google временно недоступен.",
  google_conflict: "Этот Gmail уже связан с другим аккаунтом.",
};

export default function AuthPage() {
  const registrationEnabled = import.meta.env.VITE_REGISTRATION_ENABLED !== "false";
  const location = useLocation();
  const { login, register } = useAuth();
  const [isRegistration, setIsRegistration] = useState(false);
  const [displayName, setDisplayName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [formError, setFormError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const authError = useMemo(() => {
    const params = new URLSearchParams(location.search);
    const value = params.get("auth_error");
    return value ? AUTH_MESSAGES[value] ?? "Не удалось выполнить вход." : null;
  }, [location.search]);

  function startGoogleLogin() {
    window.location.assign(`${API_BASE_URL}/api/auth/google/start`);
  }

  async function submitCredentials(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    setFormError(null);
    try {
      if (isRegistration) await register(displayName.trim(), email.trim(), password);
      else await login(email.trim(), password);
    } catch (error) {
      setFormError(error instanceof ApiError ? error.message : "Не удалось выполнить вход.");
    } finally {
      setSubmitting(false);
    }
  }

  function switchMode() {
    setIsRegistration((value) => !value);
    setFormError(null);
  }

  return (
    <main className="auth-shell min-h-screen lg:grid lg:grid-cols-[minmax(0,1.08fr)_minmax(480px,0.92fr)]">
      <section className="auth-hero relative flex min-h-[46vh] flex-col overflow-hidden border-b border-[#e3dfd8] px-6 py-7 sm:px-10 lg:min-h-screen lg:border-b-0 lg:border-r lg:px-[clamp(40px,5vw,84px)] lg:py-10">
        <div className="relative z-10 my-auto max-w-[760px] py-14 lg:py-20">
          <h1 className="font-display text-[48px] font-medium leading-[0.91] tracking-[-2.2px] text-[#211f1d] sm:text-[68px] lg:text-[clamp(58px,5.2vw,88px)]">
            Решения по ролям.
            <br />
            На основе фактов.
          </h1>
          <p className="mt-7 max-w-[610px] text-base leading-7 text-[#716d67] sm:text-lg">
            Единое рабочее пространство для описания должностей, экспертной оценки по факторам и прозрачного согласования грейдов.
          </p>

          <div className="auth-preview mt-10 max-w-[590px] rounded-[22px] border border-[#ded9d2] bg-white/90 p-5 sm:p-6">
            <div className="flex items-center justify-between border-b border-[#ebe7e1] pb-4 text-xs font-semibold">
              <span>Карточка оценки</span>
              <span className="rounded-full bg-[#f7e8ea] px-3 py-1 text-[#7a2636]">готово к комитету</span>
            </div>
            <div className="grid grid-cols-3 gap-3 pt-5">
              {[["Знания", "350"], ["Решение задач", "152"], ["Ответственность", "200"]].map(([label, score]) => (
                <div key={label}>
                  <div className="text-xs leading-4 text-[#8a857e]">{label}</div>
                  <div className="mt-1 font-sans text-3xl font-medium text-[#282522]">{score}</div>
                </div>
              ))}
            </div>
            <div className="mt-5 flex items-end justify-between rounded-2xl bg-[#faf0f1] px-4 py-3">
              <span className="text-xs leading-5 text-[#736d79]">Итоговая оценка<br />и согласованный грейд</span>
              <span className="font-sans text-4xl font-medium text-[#7a2636]">702 · G14</span>
            </div>
          </div>
        </div>

        <p className="relative z-10 hidden text-xs text-[#96918a] lg:block">Методология оценки должностей · защищённый доступ</p>
      </section>

      <section className="flex min-h-[54vh] items-center bg-white px-6 py-14 sm:px-10 lg:min-h-screen lg:px-[clamp(52px,7vw,118px)]">
        <div className="mx-auto w-full max-w-[520px]">
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[#8a857e]">Личный кабинет</p>
          <h2 className="mt-3 font-display text-[44px] font-medium leading-none tracking-[-1.4px] text-[#211f1d] sm:text-[52px]">
            {isRegistration ? "Создать аккаунт" : "Вход в систему"}
          </h2>
          <p className="mt-3 text-[15px] leading-6 text-[#77736e]">
            {isRegistration ? "Зарегистрируйтесь для начала работы." : "Продолжите работу с оценками и грейдами."}
          </p>

          {(authError || formError) && (
            <div role="alert" className="mt-7 rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm leading-6 text-red-700">
              {formError ?? authError}
            </div>
          )}

          <form className="mt-8 space-y-5" onSubmit={submitCredentials}>
            {isRegistration && (
              <label className="block text-sm font-medium text-[#45413d]">
                Имя
                <input className="auth-field mt-2" type="text" autoComplete="name" value={displayName} onChange={(event) => setDisplayName(event.target.value)} required />
              </label>
            )}
            <label className="block text-sm font-medium text-[#45413d]">
              Email
              <input className="auth-field mt-2" type="email" autoComplete="email" value={email} onChange={(event) => setEmail(event.target.value)} required />
            </label>
            <label className="block text-sm font-medium text-[#45413d]">
              Пароль
              <input className="auth-field mt-2" type="password" minLength={8} autoComplete={isRegistration ? "new-password" : "current-password"} value={password} onChange={(event) => setPassword(event.target.value)} required />
            </label>
            <button disabled={submitting} className="min-h-[58px] w-full rounded-[14px] bg-[#252527] px-5 text-base font-medium text-white transition-colors hover:bg-[#151516] disabled:cursor-wait disabled:opacity-60">
              {submitting ? "Подождите…" : isRegistration ? "Зарегистрироваться" : "Войти"}
            </button>
          </form>

          <div className="my-6 flex items-center gap-4 text-xs uppercase tracking-[0.14em] text-[#aaa59e] before:h-px before:flex-1 before:bg-[#e8e4de] after:h-px after:flex-1 after:bg-[#e8e4de]">или</div>

          <button type="button" onClick={startGoogleLogin} className="flex min-h-[58px] w-full items-center justify-center gap-3 rounded-[14px] border border-[#dcd8d2] bg-white px-5 text-base font-medium text-[#373330] transition-colors hover:bg-[#faf9f7]">
            <GoogleMark />
            Войти через Google
          </button>

          {registrationEnabled && (
            <p className="mt-7 text-center text-sm text-[#77736e]">
              {isRegistration ? "Уже есть аккаунт?" : "Нет аккаунта?"}{" "}
              <button type="button" onClick={switchMode} className="font-medium text-[#8c2d3f] hover:text-[#5c1822]">
                {isRegistration ? "Войти" : "Регистрация"}
              </button>
            </p>
          )}
        </div>
      </section>
    </main>
  );
}

function GoogleMark() {
  return (
    <svg aria-hidden="true" viewBox="0 0 24 24" className="h-5 w-5">
      <path fill="#4285F4" d="M21.6 12.2c0-.7-.1-1.4-.2-2H12v3.8h5.4a4.6 4.6 0 0 1-2 3v2.5h3.2c1.9-1.8 3-4.3 3-7.3Z" />
      <path fill="#34A853" d="M12 22c2.7 0 5-.9 6.6-2.4l-3.2-2.5c-.9.6-2 1-3.4 1a5.8 5.8 0 0 1-5.5-4H3.2v2.6A10 10 0 0 0 12 22Z" />
      <path fill="#FBBC05" d="M6.5 14.1a6 6 0 0 1 0-4.2V7.3H3.2a10 10 0 0 0 0 9.4l3.3-2.6Z" />
      <path fill="#EA4335" d="M12 5.9c1.5 0 2.8.5 3.8 1.5l2.9-2.8A9.7 9.7 0 0 0 3.2 7.3l3.3 2.6A5.8 5.8 0 0 1 12 6Z" />
    </svg>
  );
}
