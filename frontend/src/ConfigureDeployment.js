import React, { useState, useEffect } from "react";
import { useParams, useLocation, useNavigate } from "react-router-dom";
import axios from "axios";
import "./styles/ConfigureDeployment.css";
import { APPLICATIONS_SERVICE_BASE_URL } from "./env.js";
import renderInput from "./utils/RenderInputSchema.js";
import VersionModal from "./VersionModal.js";

const ConfigureDeployment = () => {
    const { appName, version } = useParams();
    const location = useLocation();
    const navigate = useNavigate();
    const deploymentId = location.state?.deployment_id;

    const [schema, setSchema] = useState(null);
    const [deployment, setDeploymentParameters] = useState(null);
    const [formData, setFormData] = useState({});
    const [error, setError] = useState("");
    const [successMessage, setSuccessMessage] = useState("");
    const [deploymentStatus, setDeploymentStatus] = useState(null);
    const [initialDeploymentStatus, setInitialDeploymentStatus] = useState(null);
    const [deploymentInfo, setDeploymentInfo] = useState(null);
    const [isDeploying, setIsDeploying] = useState(false);
    const [isOpenedVersionSelection, setIsOpenedVersionSelection] = useState(false);

    useEffect(() => {
        const fetchSchema = async () => {
            try {
                const response = await axios.get(
                    `${APPLICATIONS_SERVICE_BASE_URL}/v1/schema/${appName}/${version}`, {
                    headers: {
                        Accept: "application/json",
                        Authorization: "Bearer " + localStorage.token,
                    }
                });
                setSchema(response.data);

                const initialFormData = {};
                response.data.containers.forEach((container) => {
                    initialFormData[container.name] = {};
                    container.env_vars.forEach((env) => {
                        initialFormData[container.name][env.name] = env.default || ""; // Default or empty
                    });
                });
                setFormData(initialFormData);
            } catch (err) {
                console.error("Error fetching schema:", err);
                setError("Failed to load configuration schema. Please try again later.");
            }
        };

        const fetchDeploymentParameters = async () => {
            try {
                const response = await axios.get(
                    `${APPLICATIONS_SERVICE_BASE_URL}/v1/deployments/${deploymentId}`,
                    {
                        headers: {
                            Authorization: "Bearer " + localStorage.getItem("token"),
                        },
                    }
                );
                const params = response.data.parameters || {};

                if (Object.keys(params).length > 0) {
                    const initialFormData = {};

                    Object.entries(params).forEach(([containerName, envVars]) => {
                        initialFormData[containerName] = {};
                        Object.entries(envVars).forEach(([envName, value]) => {
                            initialFormData[containerName][envName] = value || ""; // Use value or empty
                        });
                    });

                    setFormData(initialFormData);
                }
            } catch (err) {
                console.error("Error fetching deployment parameters:", err);
                setError("Failed to load deployment parameters. Please try again later.");
            }
        };

        fetchSchema();
        fetchDeploymentParameters();
    }, [appName, version]);

    const handleInputChange = (container, fieldName, value) => {
        setFormData((prevData) => ({
            ...prevData,
            [container]: {
                ...prevData[container],
                [fieldName]: value, // Allow empty values
            },
        }));
    };

    const handleDeploy = async () => {
        try {
            await axios.put(`${APPLICATIONS_SERVICE_BASE_URL}/v1/deployments/${deploymentId}`,
                {
                    version: version,
                    parameters: formData,
                },
                {
                    headers: {
                        Accept: "application/json",
                        Authorization: "Bearer " + localStorage.getItem("token"),
                    },
                });

            await axios.post(
                `${APPLICATIONS_SERVICE_BASE_URL}/v1/deployments/${deploymentId}/deploy`,
                {
                    application_name: schema.application_name,
                    version: version,
                    parameters: formData,
                },
                {
                    headers: {
                        Accept: "application/json",
                        Authorization: "Bearer " + localStorage.getItem("token"),
                    },
                }
            );

            setSuccessMessage("Deployment started successfully!");
            setIsDeploying(true);
        } catch (err) {
            console.error("Error during deployment:", err);
            setError("Deployment failed. Please try again later.");
        }
    };

    useEffect(() => {
        const updateStatusOnStart = async () => {
            try {
                const response = await axios.get(
                    `${APPLICATIONS_SERVICE_BASE_URL}/v1/deployments/${deploymentId}/status`,
                    {
                        headers: {
                            Authorization: "Bearer " + localStorage.getItem("token"),
                        },
                    }
                );
                const { status } = response.data;

                setInitialDeploymentStatus(status);
            } catch (err) {
                console.error("Error fetching deployment status:", err);
            }
        };
        updateStatusOnStart();
    }, [deploymentId]);

    useEffect(() => {
        let interval;
        if (isDeploying) {
            interval = setInterval(async () => {
                try {
                    const response = await axios.get(
                        `${APPLICATIONS_SERVICE_BASE_URL}/v1/deployments/${deploymentId}/status`,
                        {
                            headers: {
                                Authorization: "Bearer " + localStorage.getItem("token"),
                            },
                        }
                    );
                    const { status, info } = response.data;

                    setDeploymentStatus(status);
                    if (status === "failed" || status === "success") {
                        setDeploymentInfo(info);
                        setIsDeploying(false);
                        clearInterval(interval);
                    }
                } catch (err) {
                    console.error("Error fetching deployment status:", err);
                }
            }, 2000);
        }
        return () => clearInterval(interval);
    }, [isDeploying, deploymentId]);

    const handleVersionSelect = (selectedVersion) => {
        setIsOpenedVersionSelection(false);
        navigate(`/applications/my/configure/${appName}/${selectedVersion}`, {
            state: { deployment_id: deploymentId },
        });
    };

    const onClose = () => {
        navigate(`/applications`);
    };

    const handleModalClose = () => {
        setIsOpenedVersionSelection(false);
    };

    const formatMessage = (message) => {
        if (!message) return "";
        return message.replace(/\n/g, "<br>");
    };

    if (isDeploying) {
        return (
            <div className="loading-container">
                <div className="loading-animation"></div>
                <p>Deployment in process... Please wait.</p>
            </div>
        );
    }

    if (deploymentStatus && deploymentStatus !== "in_process" && deploymentStatus !== "null") {
        return (
            <div className="deployment-info">
                <h1>
                    Deployment status: {deploymentStatus === "success" ? "Successful" : "Failed"}
                </h1>
                <h3>
                    {deploymentInfo.msg}
                </h3>
                <h4>
                    Details:
                </h4>
                <pre>
                    <div
                        dangerouslySetInnerHTML={{
                            __html: formatMessage(deploymentInfo.stderr),
                        }}
                    />
                </pre>
                <button onClick={onClose} className="close-button">
                    Close
                </button>
            </div>
        );
    }

    if (error) {
        return <p className="error">{error}</p>;
    }

    if (!schema) {
        return <p className="loading">Loading configuration...</p>;
    }

    return (
        <div className="configure-container">
            <header className="header">
                <h1>{schema.application_name} Configuration</h1>
                <h2>Version: {schema.version}</h2>
                <h2>Last deployment status: {initialDeploymentStatus}</h2>
                <button className="add-to-my-button" onClick={() => setIsOpenedVersionSelection(true)}>
                    Choose another version
                </button>
                {isOpenedVersionSelection && (
                    <VersionModal
                        appName={appName}
                        onClose={handleModalClose}
                        onSelect={handleVersionSelect}
                    />
                )}
            </header>
            <main className="main-content">
                <div className="scrollable-config">
                    {schema.containers.map((container) => (
                        <section key={container.name} className="container-section">
                            <h3>{container.name}</h3>
                            <div className="env-vars">
                                {container.env_vars?.map((env) => (
                                    <div key={env.name} className="env-item">
                                        <label title={env.hint} className="env-label">
                                            {env.name}
                                        </label>
                                        {renderInput(container.name, env, formData, handleInputChange)}
                                    </div>
                                ))}
                            </div>
                        </section>
                    ))}
                </div>
                <button className="deploy-button" onClick={handleDeploy}>
                    Start Deploy
                </button>
                {successMessage && <p className="success">{successMessage}</p>}
            </main>
        </div>
    );
};

export default ConfigureDeployment;
