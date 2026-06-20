import { Navigate, Route, Routes, useLocation } from "react-router-dom";
import { MainLayout } from "./components/Layout";
import { useAuth } from "./lib/auth";
import AssessmentSheetPage from "./pages/AssessmentSheetPage";
import AuthPage from "./pages/AuthPage";
import CalculatorPage from "./pages/CalculatorPage";
import AdminAccessPage from "./pages/AdminAccessPage";
import ComparisonPage from "./pages/ComparisonPage";
import DashboardPage from "./pages/DashboardPage";
import EvaluationCardPage from "./pages/EvaluationCardPage";
import FormLinksPage from "./pages/FormLinksPage";
import GradeTablePage from "./pages/GradeTablePage";
import GuidePage from "./pages/GuidePage";
import JobFormPage from "./pages/JobFormPage";
import OnboardingPage from "./pages/OnboardingPage";
import NotFoundPage from "./pages/NotFoundPage";
import PublicFormPage from "./pages/PublicFormPage";

export default function App() {
  return (
    <Routes>
      <Route path="/fill/:token" element={<PublicFormPage />} />
      <Route path="*" element={<PrivateApplication />} />
    </Routes>
  );
}

function PrivateApplication() {
  const { loading, user, companies, activeCompany } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div className="auth-shell grid min-h-screen place-items-center">
        <div className="grid h-12 w-12 animate-pulse place-items-center rounded-2xl bg-accent font-semibold text-white">H</div>
      </div>
    );
  }
  if (!user) return <AuthPage />;
  if (companies.length === 0) return <OnboardingPage />;
  if (location.pathname === "/onboarding") return <OnboardingPage />;
  if (!activeCompany) return <Navigate to="/onboarding" replace />;

  return (
    <MainLayout key={activeCompany.id}>
      <Routes>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/assessment-sheet" element={<AssessmentSheetPage />} />
        <Route path="/grades" element={<GradeTablePage />} />
        <Route path="/calculator" element={<CalculatorPage />} />
        <Route path="/admin" element={<AdminAccessPage />} />
        <Route path="/new" element={<JobFormPage />} />
        <Route path="/positions/:id/edit" element={<JobFormPage />} />
        <Route path="/positions/:id" element={<EvaluationCardPage />} />
        <Route path="/compare" element={<ComparisonPage />} />
        <Route path="/guide" element={<GuidePage />} />
        <Route path="/forms" element={<FormLinksPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </MainLayout>
  );
}
