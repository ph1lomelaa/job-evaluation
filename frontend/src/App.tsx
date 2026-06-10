import { Route, Routes } from "react-router-dom";
import { MainLayout } from "./components/Layout";
import ComparisonPage from "./pages/ComparisonPage";
import DashboardPage from "./pages/DashboardPage";
import EvaluationCardPage from "./pages/EvaluationCardPage";
import JobFormPage from "./pages/JobFormPage";

export default function App() {
  return (
    <MainLayout>
      <Routes>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/new" element={<JobFormPage />} />
        <Route path="/positions/:id" element={<EvaluationCardPage />} />
        <Route path="/compare" element={<ComparisonPage />} />
      </Routes>
    </MainLayout>
  );
}
