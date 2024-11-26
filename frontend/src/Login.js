import React, { useState } from "react";
import axios from "axios";
import Cookies from "js-cookie";
import { useNavigate } from "react-router-dom";
import "./Login.css"; // Import the styles
import { REACT_APP_AUTH_SERVICE_BASE_URL } from "./env.js"

const Login = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();

        try {
            const url = `${REACT_APP_AUTH_SERVICE_BASE_URL}/v1/token`;
            const data = new URLSearchParams({ username, password });

            const response = await axios.post(url, data, {
                headers: {
                    Accept: "application/json",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            });

            // Save the token in a cookie
            Cookies.set("authToken", response.data.token, { secure: true });
            Cookies.set("username", username, { secure: true });

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
