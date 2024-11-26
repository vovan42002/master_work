import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Cookies from "js-cookie";
import axios from "axios";
import "./Applications.css";
import { REACT_APP_APPLICATIONS_SERVICE_BASE_URL } from "./env";
import VersionModal from "./VersionModal";

const Applications = () => {
    const navigate = useNavigate();
    const [applications, setApplications] = useState([]);
    const [myapplications, setMyApplications] = useState([]);
    const [error, setError] = useState("");
    const [selectedApp, setSelectedApp] = useState(null);

    useEffect(() => {
        const token = Cookies.get("authToken");
        if (!token) {
            navigate("/");
            return;
        }

        const fetchApplications = async () => {
            try {
                const response = await axios.get(`${REACT_APP_APPLICATIONS_SERVICE_BASE_URL}/v1/applications`, {
                    headers: {
                        Accept: "application/json",
                    },
                });
                setApplications(response.data.applications);
            } catch (err) {
                console.error("Error fetching applications:", err);
                setError("Failed to load applications. Please try again later.");
            }
        };

        const fetchMyApplications = async () => {
            try {
                const response = await axios.get(`${REACT_APP_APPLICATIONS_SERVICE_BASE_URL}/v1/applications/my`, {
                    headers: {
                        Accept: "application/json",
                    },
                });
                setMyApplications(response.data.applications);
            } catch (err) {
                console.error("Error fetching applications:", err);
                setError("Failed to load applications. Please try again later.");
            }
        };

        fetchApplications();
        fetchMyApplications();
    }, [navigate]);

    const handleDeploy = (appName) => {
        console.log(`Deploy button clicked for ${appName}`);
    };

    const handleConfigure = (appName) => {
        setSelectedApp(appName); // Open the modal with the selected app name
    };

    const handleVersionSelect = (version) => {
        navigate(`/applications/my/configure/${selectedApp}/${version}`);
        setSelectedApp(null); // Close the modal
    };

    return (
        <div className="container">
            <h1 className="header">All Applications</h1>
            {error && <p className="error">{error}</p>}
            <ul className="list">
                {applications.map((app, index) => (
                    <li key={index} className="list-item">
                        <span className="app-name">{app}</span>
                        <button className="deploy-button" onClick={() => handleDeploy(app)}>
                            Deploy
                        </button>
                    </li>
                ))}
            </ul>
            <h1 className="header">My Applications</h1>
            {error && <p className="error">{error}</p>}
            <ul className="list">
                {myapplications.map((app, index) => (
                    <li key={index} className="list-item">
                        <span className="app-name">{app}</span>
                        <button className="deploy-button" onClick={() => handleConfigure(app)}>
                            Configure
                        </button>
                    </li>
                ))}
            </ul>
            {selectedApp && (
                <VersionModal
                    appName={selectedApp}
                    onClose={() => setSelectedApp(null)} // Close the modal
                    onSelect={handleVersionSelect} // Handle version selection
                />
            )}
        </div>
    );
};

export default Applications;
