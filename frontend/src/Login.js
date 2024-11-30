import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./styles/Login.css"; // Import the styles
import { AUTH_SERVICE_BASE_URL } from "./env.js";

const Login = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    // Trigger token refresh when accessing the Login page
    useEffect(() => {
        const checkTokens = async () => {
            if (localStorage.getItem("refresh_token") && localStorage.getItem("token")) {
                navigate("/applications"); // Redirect if token refresh is successful
            }
        };
        checkTokens();
    }, [navigate]);

    const handleLogin = async (e) => {
        e.preventDefault();

        try {
            const url = `${AUTH_SERVICE_BASE_URL}/v1/token`;
            const data = new URLSearchParams({ username, password });

            const response = await axios.post(url, data, {
                headers: {
                    Accept: "application/json",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            });

            // Save the token in local storage
            localStorage.setItem("token", response.data.token);
            localStorage.setItem("refresh_token", response.data.refresh_token);
            localStorage.setItem("username", username);

            // Redirect to the welcome page
            navigate("/applications");
        } catch (err) {
            setError("Invalid credentials. Please try again.");
        }
    };

    return (
        <div className="login-container">
            <form className="login-form" onSubmit={handleLogin}>
                <h1>Login</h1>
                <div>
                    <label>Username</label>
                    <input
                        type="email"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>Password</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                <button type="submit">Login</button>
                {error && <p>{error}</p>}
            </form>
        </div>
    );
};

export default Login;
