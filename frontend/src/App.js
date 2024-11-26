import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import './App.css';
import Login from "./Login";
import Applications from "./Applications";
import ConfigureDeployment from "./ConfigureDeployment";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/applications" element={<Applications />} />
        <Route path="/applications/my/configure/:appName/:version" element={<ConfigureDeployment />} />
      </Routes>
    </Router>
  );
}

export default App;
