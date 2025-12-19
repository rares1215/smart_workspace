import { BrowserRouter, Routes, Route } from "react-router-dom";
import ProtectedRoute from "./api/ProtectedRoute";
import LoginPage from "./pages/Login";
import RegisterPage from "./pages/Register";
import { Documents } from "./pages/Documents";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login/" element={<LoginPage />} />
        <Route path="/register/" element={<RegisterPage />} />
        <Route path="/documents/" element={
          <ProtectedRoute>
            <Documents />
          </ProtectedRoute>
        } />
      </Routes>
    </BrowserRouter>
  )
}

export default App
