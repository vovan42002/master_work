import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./styles/Applications.css"
import { APPLICATIONS_SERVICE_BASE_URL } from "./env";
import VersionModal from "./VersionModal";

const Applications = () => {
    const navigate = useNavigate();
    const [applications, setApplications] = useState([]);
    const [myapplications, setMyApplications] = useState([]);
    const [error, setError] = useState("");
    const [selectedApp, setSelectedApp] = useState(null);
    const [selectedVersion, setSelectedVersion] = useState(null);

    useEffect(() => {
        const token = localStorage.getItem("token");
        if (!token) {
            navigate("/");
            return;
        }

        const fetchApplications = async () => {
            try {
                const response = await axios.get(`${APPLICATIONS_SERVICE_BASE_URL}/v1/applications`, {
                    headers: { Accept: "application/json" },
                });
                setApplications(response.data.applications);
            } catch (err) {
                console.error("Error fetching applications:", err);
                setError("Failed to load all available applications. Please try again later.");
            }
        };

        const fetchMyApplications = async () => {
            try {
                const response = await axios.get(`${APPLICATIONS_SERVICE_BASE_URL}/v1/deployments/my`, {
                    headers: {
                        Accept: "application/json",
                        Authorization: "Bearer " + localStorage.token,
                    },
                });
                setMyApplications(response.data.deployments);
            } catch (err) {
                console.error("Error fetching user applications:", err);
                setError("Failed to load user applications. Please try again later.");
            }
        };

        fetchApplications();
        fetchMyApplications();
    }, [navigate]);

    const handleDeploy = (appName) => {
        console.log(`Deploy button clicked for ${appName}`);
        setSelectedApp(appName); // Open the modal with the selected app name
    };

    const handleConfigure = (app) => {
        console.log(`Configure button clicked for ${app.application_name} with ID ${app.deployment_id}`);
        navigate(`/applications/my/configure/${app.application_name}/${app.version}`, {
            state: { deployment_id: app.deployment_id },
        }); // Navigate to the ConfigureDeployment route
    };

    const handleVersionSelect = (version) => {
        console.log(`Version selected: ${version}`);
        setSelectedVersion(version);
        handleDeployVersion(selectedApp, version); // Trigger the deployment logic
        setSelectedApp(null); // Close the modal
    };

    const handleDeployVersion = async (appName, version) => {
        const username = localStorage.getItem("username"); // Assuming username is stored in localStorage
        try {
            await axios.post(
                `${APPLICATIONS_SERVICE_BASE_URL}/v1/deployments`,
                {
                    application_name: appName,
                    version: version,
                    username: username,
                    parameters: {}, // Add parameters if required
                },
                {
                    headers: {
                        Accept: "application/json",
                        "Content-Type": "application/json",
                        Authorization: "Bearer " + localStorage.getItem("token"),
                    },
                }
            );

            // Fetch the updated deployments
            const response = await axios.get(`${APPLICATIONS_SERVICE_BASE_URL}/v1/deployments/my`, {
                headers: {
                    Accept: "application/json",
                    Authorization: "Bearer " + localStorage.token,
                },
            });
            setMyApplications(response.data.deployments); // Update the table with the new data
        } catch (error) {
            console.error("Error deploying application or fetching updates:", error);
            setError("Deployment failed. Please try again.");
        }
    };

    const handleDelete = async (deploymentId) => {
        try {
            await axios.delete(`${APPLICATIONS_SERVICE_BASE_URL}/v1/deployments/${deploymentId}`, {
                headers: {
                    Accept: "application/json",
                    Authorization: "Bearer " + localStorage.token,
                },
            });

            // Fetch updated deployments after deletion
            const response = await axios.get(`${APPLICATIONS_SERVICE_BASE_URL}/v1/deployments/my`, {
                headers: {
                    Accept: "application/json",
                    Authorization: "Bearer " + localStorage.token,
                },
            });
            setMyApplications(response.data.deployments);
        } catch (err) {
            console.error("Error deleting deployment:", err);
            setError("Failed to delete deployment. Please try again.");
        }
    };

    return (
        <div className="root_container">
            <div className="frame">
                <h1 className="header">All Applications</h1>
                {error && <p className="error">{error}</p>}
                <div className="scrollable-content">
                    <ul className="list">
                        {applications.map((app, index) => (
                            <li key={index} className="list-item">
                                <span className="app-name">{app}</span>
                                <button className="add-to-my-button" onClick={() => handleDeploy(app)}>
                                    Add to My
                                </button>
                            </li>
                        ))}
                    </ul>
                </div>
            </div>

            <div className="frame">
                <h1 className="header">My Applications</h1>
                {error && <p className="error">{error}</p>}
                <div className="scrollable-content">
                    <table className="my-applications-table">
                        <thead>
                            <tr>
                                <th>Application</th>
                                <th>Version</th>
                                <th>Deployment ID</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {myapplications.map((app, index) => (
                                <tr key={index}>
                                    <td>{app.application_name}</td>
                                    <td>{app.version}</td>
                                    <td>{app.deployment_id}</td>
                                    <td>
                                        <button
                                            className="configure-button"
                                            onClick={() => handleConfigure(app)}
                                        >
                                            Configure
                                        </button>
                                        <button
                                            className="delete-button"
                                            onClick={() => handleDelete(app.deployment_id)}
                                        >
                                            Delete
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
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
