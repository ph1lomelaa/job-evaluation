import { motion, AnimatePresence } from "framer-motion";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../lib/auth";
import { cn } from "../lib/cn";

const PURPOSES = [
  { value: "job-evaluation", label: "Оценка должностей", note: "Создание JE-досье и расчёт грейдов" },
  { value: "grade-calibration", label: "Калибровка грейдов", note: "Сравнение ролей и подготовка к комитету" },
  { value: "methodology", label: "Методология", note: "Единые стандарты оценки для команды" },
];

const ROLES = [
  { value: "hr-cb", label: "HR / C&B" },
  { value: "evaluator", label: "Эксперт по оценке" },
  { value: "manager", label: "Руководитель" },
  { value: "consultant", label: "Консультант" },
];

const SIZES = [
  { value: "1-50", label: "До 50 сотрудников" },
  { value: "51-250", label: "51–250" },
  { value: "251-1000", label: "251–1 000" },
  { value: "1000+", label: "Более 1 000" },
];

export default function OnboardingPage() {
  const navigate = useNavigate();
  const { user, companies, createCompany } = useAuth();
  const adding = companies.length > 0;
  const [step, setStep] = useState(0);
  const [purpose, setPurpose] = useState("");
  const [role, setRole] = useState("");
  const [size, setSize] = useState("");
  const [name, setName] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const selected = [purpose, role, size, name.trim()][step];

  async function continueFlow() {
    if (!selected) return;
    if (step < 3) {
      setStep((value) => value + 1);
      return;
    }
    setBusy(true);
    setError(null);
    try {
      await createCompany({
        name: name.trim(),
        purpose,
        user_role: role,
        organization_size: size,
      });
      navigate("/", { replace: true });
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : String(reason));
    } finally {
      setBusy(false);
    }
  }

  const firstName = user?.display_name.split(" ")[0] || "";
  const headings = [
    "Для чего вы будете использовать Hay Eval?",
    "Какая у вас роль в процессе оценки?",
    "Какой размер вашей организации?",
    "Как называется компания?",
  ];

  return (
    <div className="auth-shell min-h-screen px-5 py-10 sm:py-16">
      <main className="mx-auto flex min-h-[calc(100vh-128px)] max-w-[980px] flex-col justify-center">
        <div className="text-center">
          <div className="mx-auto mb-6 grid h-11 w-11 place-items-center rounded-xl bg-accent font-semibold text-white">H</div>
          <h1 className="font-display text-[44px] font-normal leading-tight tracking-[-1.5px] sm:text-[64px]">
            {adding ? "Добавим новую компанию" : `Добро пожаловать, ${firstName}!`}
          </h1>
          <p className="mt-3 text-lg text-muted">
            {adding ? "Настройка займёт меньше минуты." : "Несколько вопросов — и можно начинать работу."}
          </p>
        </div>

        <section className="mx-auto mt-10 w-full max-w-[840px] rounded-[34px] border border-black/10 bg-white p-6 shadow-[0_6px_0_rgba(42,34,25,0.04),0_18px_60px_rgba(42,34,25,0.07)] sm:p-12">
          <div className="flex gap-2" aria-label={`Шаг ${step + 1} из 4`}>
            {[0, 1, 2, 3].map((index) => (
              <div
                key={index}
                className={cn(
                  "h-2 flex-1 rounded-full transition-colors",
                  index <= step ? "bg-accent" : "bg-[#dedede]",
                )}
              />
            ))}
          </div>

          <div className="mt-10 min-h-[210px]">
            <AnimatePresence mode="wait">
              <motion.div
                key={step}
                initial={{ opacity: 0, x: 16 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -16 }}
                transition={{ duration: 0.18 }}
              >
                <h2 className="text-[26px] font-medium tracking-[-0.4px]">{headings[step]}</h2>

                {step === 0 && (
                  <div className="mt-7 grid gap-3 sm:grid-cols-3">
                    {PURPOSES.map((option) => (
                      <OptionButton
                        key={option.value}
                        active={purpose === option.value}
                        onClick={() => setPurpose(option.value)}
                        label={option.label}
                        note={option.note}
                      />
                    ))}
                  </div>
                )}
                {step === 1 && (
                  <div className="mt-7 flex flex-wrap gap-3">
                    {ROLES.map((option) => (
                      <Choice key={option.value} active={role === option.value} onClick={() => setRole(option.value)}>
                        {option.label}
                      </Choice>
                    ))}
                  </div>
                )}
                {step === 2 && (
                  <div className="mt-7 flex flex-wrap gap-3">
                    {SIZES.map((option) => (
                      <Choice key={option.value} active={size === option.value} onClick={() => setSize(option.value)}>
                        {option.label}
                      </Choice>
                    ))}
                  </div>
                )}
                {step === 3 && (
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
                )}
              </motion.div>
            </AnimatePresence>
          </div>

          {error && <div className="mb-4 rounded-xl bg-red-50 px-4 py-3 text-sm text-red-700">{error}</div>}

          <div className="mt-7 flex items-center gap-3">
            {(step > 0 || adding) && (
              <button
                type="button"
                onClick={() => (step > 0 ? setStep((value) => value - 1) : navigate("/"))}
                className="min-h-[56px] rounded-xl border border-black/15 px-6 text-sm font-medium hover:bg-[#f8f6f2]"
              >
                {step > 0 ? "Назад" : "Отмена"}
              </button>
            )}
            <button
              type="button"
              disabled={!selected || busy}
              onClick={() => void continueFlow()}
              className="min-h-[56px] flex-1 rounded-xl bg-accent px-6 text-base font-medium text-white transition hover:bg-[#6d3eaa] disabled:cursor-not-allowed disabled:opacity-40"
            >
              {busy ? "Создаём пространство…" : step === 3 ? "Создать компанию" : "Продолжить"}
            </button>
          </div>
        </section>
      </main>
    </div>
  );
}

function Choice({ active, onClick, children }: { active: boolean; onClick: () => void; children: string }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={cn(
        "rounded-xl border px-6 py-3.5 text-base transition",
        active ? "border-accent bg-accent text-white" : "border-black/15 bg-white hover:border-accent/60",
      )}
    >
      {children}
    </button>
  );
}

function OptionButton({ active, onClick, label, note }: { active: boolean; onClick: () => void; label: string; note: string }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={cn(
        "min-h-[122px] rounded-2xl border p-5 text-left transition",
        active ? "border-accent bg-[#f5effb] ring-1 ring-accent" : "border-black/15 hover:border-accent/60",
      )}
    >
      <span className="block text-base font-medium">{label}</span>
      <span className="mt-2 block text-sm leading-5 text-muted">{note}</span>
    </button>
  );
}
