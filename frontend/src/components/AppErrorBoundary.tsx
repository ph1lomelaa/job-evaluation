import { Component, type ReactNode } from "react";
import { Button, Card } from "./ui";

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  message: string;
}

export class AppErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false, message: "" };

  static getDerivedStateFromError(error: unknown): State {
    return {
      hasError: true,
      message: error instanceof Error ? error.message : String(error),
    };
  }

  componentDidCatch(error: unknown) {
    // eslint-disable-next-line no-console
    console.error("AppErrorBoundary caught an error:", error);
  }

  render() {
    if (!this.state.hasError) return this.props.children;

    return (
      <div className="min-h-screen bg-bg p-6">
        <div className="mx-auto flex min-h-[70vh] max-w-3xl items-center justify-center">
          <Card className="w-full max-w-2xl p-8">
            <div className="text-xs uppercase tracking-wide text-muted">Ошибка приложения</div>
            <h1 className="mt-3 text-[28px]">Страница не смогла загрузиться</h1>
            <p className="mt-3 text-sm leading-7 text-muted">
              Это не должно останавливать работу интерфейса. Обновите страницу или вернитесь на
              главную.
            </p>
            <div className="mt-4 rounded-xl border border-[rgb(var(--row-divider))] bg-[rgb(var(--field-bg))] p-4 text-sm text-muted">
              {this.state.message}
            </div>
            <div className="mt-6 flex flex-wrap gap-3">
              <Button onClick={() => window.location.assign("/")}>На главную</Button>
              <Button variant="secondary" onClick={() => window.location.reload()}>
                Перезагрузить
              </Button>
            </div>
          </Card>
        </div>
      </div>
    );
  }
}
