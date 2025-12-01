import { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from "react-router-dom";
import PredictTrend from "./components/PredictTrend";
import StockSummaryPage from "./pages/StockSummaryPage";
import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";
import './App.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    setIsAuthenticated(!!token);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    setIsAuthenticated(false);
    window.location.href = "/login";
  };

  return (
    <Router>
      <nav style={{ padding: "1rem", textAlign: "center" }}>
        <Link to="/signup" style={{ marginRight: "1rem" }}>Signup</Link>

        {isAuthenticated ? (
          <>
            <Link to="/predict-trend" style={{ marginRight: "1rem" }}>Predict Trend</Link>
            <Link to="/stock-summary" style={{ marginRight: "1rem" }}>Stock Summary</Link>
            <button onClick={handleLogout}>Logout</button>
          </>
        ) : (
          <Link to="/login">Login</Link>
        )}
      </nav>
      <Routes>
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/predict-trend" element={<PredictTrend />} />
        <Route path="/stock-summary" element={<StockSummaryPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/" element={<h1>Welcome to the Stock App</h1>} />
      </Routes>
    </Router>
  );
}

export default App;
