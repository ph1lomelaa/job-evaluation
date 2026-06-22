import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../lib/auth";

export default function OnboardingPage() {
  const navigate = useNavigate();
  const { user, companies, createCompany } = useAuth();
  const adding = companies.length > 0;
  const [name, setName] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function continueFlow() {
    if (!name.trim()) return;
    setBusy(true);
    setError(null);
    try {
      await createCompany({ name: name.trim() });
      navigate("/", { replace: true });
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : String(reason));
    } finally {
      setBusy(false);
    }
  }

  const firstName = user?.display_name.split(" ")[0] || "";

  return (
    <div className="auth-shell min-h-screen px-5 py-10 sm:py-16">
      <main className="mx-auto flex min-h-[calc(100vh-128px)] max-w-[980px] flex-col justify-center">
        <div className="text-center">
          <h1 className="font-display text-[44px] font-normal leading-tight tracking-[-1.5px] sm:text-[64px]">
            {adding ? "Добавим новую компанию" : `Добро пожаловать, ${firstName}!`}
          </h1>
          <p className="mt-3 text-lg text-muted">
            {adding ? "Настройка займёт меньше минуты." : "Один вопрос — и можно начинать работу."}
          </p>
        </div>

        <section className="mx-auto mt-10 w-full max-w-[840px] rounded-[34px] border border-black/10 bg-white p-6 shadow-[0_6px_0_rgba(42,34,25,0.04),0_18px_60px_rgba(42,34,25,0.07)] sm:p-12">
          <h2 className="text-[26px] font-medium tracking-[-0.4px]">Как называется компания?</h2>

          <div className="mt-7 max-w-xl">
            <label className="block text-sm font-medium" htmlFor="company-name">Название рабочего пространства</label>
            <input
              id="company-name"
              autoFocus
              className="field mt-2 min-h-[56px] text-base"
              value={name}
              maxLength={160}
              onChange={(event) => setName(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === "Enter") void continueFlow();
              }}
              placeholder="Например, АО «Компания»"
            />
            <p className="mt-3 text-sm text-muted">Должности, оценки и формы этой компании будут храниться отдельно.</p>
          </div>

          {error && <div className="mb-4 mt-6 rounded-xl bg-red-50 px-4 py-3 text-sm text-red-700">{error}</div>}

          <div className="mt-7 flex items-center gap-3">
            {adding && (
              <button
                type="button"
                onClick={() => navigate("/")}
                className="min-h-[56px] rounded-xl border border-black/15 px-6 text-sm font-medium hover:bg-[#f8f6f2]"
              >
                Отмена
              </button>
            )}
            <button
              type="button"
              disabled={!name.trim() || busy}
              onClick={() => void continueFlow()}
              className="min-h-[56px] flex-1 rounded-xl bg-accent px-6 text-base font-medium text-white transition hover:bg-accent-soft disabled:cursor-not-allowed disabled:opacity-40"
            >
              {busy ? "Создаём пространство…" : "Создать компанию"}
            </button>
          </div>
        </section>
      </main>
    </div>
  );
}
