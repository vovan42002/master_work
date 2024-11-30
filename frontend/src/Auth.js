import axios from "axios";
import { AUTH_SERVICE_BASE_URL } from "./env.js";

export const refreshAuthToken = async (navigate) => {
    const refreshToken = localStorage.getItem("refresh_token");

    // Check if refresh_token exists
    if (!refreshToken) {
        console.error("No refresh token available. Redirecting to login.");
        if (navigate) navigate("/"); // Redirect if `navigate` function is available
        return null;
    }

    try {
        const response = await axios.post(
            `${AUTH_SERVICE_BASE_URL}/v1/refresh_token`,
            new URLSearchParams({ refresh_token: refreshToken }),
            {
                headers: {
                    Authorization: "Bearer " + refreshToken,
                },
            }
        );

        const { token } = response.data;

        // Update tokens in local storage
        localStorage.setItem("token", token);

        return token;
    } catch (err) {
        // Handle 401 errors specifically
        if (err.response && (err.response.status === 401 || err.response.status === 403)) {
            console.error("Refresh token invalid or expired. Redirecting to login.");
            if (navigate) navigate("/");
        } else {
            console.error("Error refreshing token:", err);
        }

        return null;
    }
};
