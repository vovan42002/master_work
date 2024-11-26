import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

const ConfigureDeployment = () => {
    const { appName, version } = useParams(); // Extract parameters from the route
    const [schema, setSchema] = useState(null);
    const [formData, setFormData] = useState({});
    const [error, setError] = useState("");

    useEffect(() => {
        const fetchSchema = async () => {
            try {
                const response = await axios.get(`http://localhost:8002/v1/schema/${appName}/${version}`);
                setSchema(response.data);
            } catch (err) {
                console.error("Error fetching schema:", err);
                setError("Failed to load configuration schema. Please try again later.");
            }
        };

        fetchSchema();
    }, [appName, version]);

    const handleInputChange = (container, fieldName, value) => {
        setFormData((prevData) => ({
            ...prevData,
            [container]: {
                ...prevData[container],
                [fieldName]: value,
            },
        }));
    };

    const renderInput = (containerName, env) => {
        switch (env.type) {
            case "string":
                return (
                    <input
                        type="text"
                        value={formData[containerName]?.[env.name] || env.default}
                        onChange={(e) =>
                            handleInputChange(containerName, env.name, e.target.value)
                        }
                    />
                );
            case "boolean":
                return (
                    <input
                        type="checkbox"
                        checked={formData[containerName]?.[env.name] ?? env.default}
                        onChange={(e) =>
                            handleInputChange(containerName, env.name, e.target.checked)
                        }
                    />
                );
            case "dropdown-list":
                return (
                    <select
                        value={formData[containerName]?.[env.name] || env.default}
                        onChange={(e) =>
                            handleInputChange(containerName, env.name, e.target.value)
                        }
                    >
                        {env.values.map((value) => (
                            <option key={value} value={value}>
                                {value}
                            </option>
                        ))}
                    </select>
                );
            default:
                return null;
        }
    };

    if (error) {
        return <p>{error}</p>;
    }

    if (!schema) {
        return <p>Loading configuration...</p>;
    }

    return (
        <div>
            <h1>{schema.application_name} Configuration</h1>
            <h2>Version: {schema.version}</h2>
            {schema.containers.map((container) => (
                <div key={container.name}>
                    <h3>{container.name}</h3>
                    {container.env_vars &&
                        container.env_vars.map((env) => (
                            <div key={env.name}>
                                <label title={env.hint}>{env.name}</label>
                                {renderInput(container.name, env)}
                            </div>
                        ))}
                </div>
            ))}
            <h3>Preview Data</h3>
            <pre>{JSON.stringify(formData, null, 2)}</pre>
        </div>
    );
};

export default ConfigureDeployment;
