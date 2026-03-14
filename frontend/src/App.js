import { BrowserRouter, Routes, Route } from 'react-router-dom';
import AppLayout from './layouts/AppLayout.jsx';
import HomePage from './pages/HomePage.jsx';
import JournalPage from './pages/JournalPage.jsx';
import SessionsPage from './pages/SessionsPage.jsx';
import ExercisesPage from './pages/ExercisesPage.jsx';
import ProgressPage from './pages/ProgressPage.jsx';

function App() {
  return (
    <BrowserRouter>
      <AppLayout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/journal" element={<JournalPage />} />
          <Route path="/sessions" element={<SessionsPage />} />
          <Route path="/exercises" element={<ExercisesPage />} />
          <Route path="/progress" element={<ProgressPage />} />
        </Routes>
      </AppLayout>
    </BrowserRouter>
  );
}

export default App;