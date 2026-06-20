import { Link } from "react-router-dom";
import { Button, Card } from "../components/ui";

export default function NotFoundPage() {
  return (
    <div className="min-h-[70vh] p-6">
      <div className="mx-auto flex min-h-[70vh] max-w-3xl items-center justify-center">
        <Card className="w-full max-w-2xl p-8">
          <div className="text-xs uppercase tracking-wide text-muted">404</div>
          <h1 className="mt-3 text-[28px]">Страница не найдена</h1>
          <p className="mt-3 text-sm leading-7 text-muted">
            Похоже, адрес устарел или страницы с таким путём нет в текущем рабочем пространстве.
          </p>
          <div className="mt-6 flex flex-wrap gap-3">
            <Link to="/">
              <Button>На главную</Button>
            </Link>
          </div>
        </Card>
      </div>
    </div>
  );
}

