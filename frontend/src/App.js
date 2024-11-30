import React, { useEffect } from "react";
import { BrowserRouter as Router, Route, Routes, useNavigate } from "react-router-dom";
import './App.css';
import Login from "./Login";
import Applications from "./Applications";
import ConfigureDeployment from "./ConfigureDeployment";
import { refreshAuthToken } from "./Auth.js";

function App() {
  const navigate = useNavigate(); // Use navigate for redirection

  useEffect(() => {
    const refreshTokenOnPageLoad = async () => {
      try {
        await refreshAuthToken();
      } catch (error) {
        if (error.response?.status === 401 || error.response?.status === 403) {
          // Redirect to login if refresh token is invalid
          navigate("/");
        }
      }
    };

    // Trigger refresh token on page load
    refreshTokenOnPageLoad();

    // Set up a periodic token refresh every 15 minutes
    const intervalId = setInterval(() => {
      refreshAuthToken().catch((error) => {
        if (error.response?.status === 401 || error.response?.status === 403) {
          navigate("/");
        }
      });
    }, 15 * 60 * 1000); // 15 minutes in milliseconds

    // Clean up the interval when the component unmounts
    return () => clearInterval(intervalId);
  }, [navigate]);

  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/applications" element={<Applications />} />
      <Route path="/applications/my/configure/:appName/:version" element={<ConfigureDeployment />} />
    </Routes>
  );
}

export default function AppWrapper() {
  return (
    <Router>
      <App />
    </Router>
  );
}
