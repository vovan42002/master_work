import React, { useState } from "react";
import './App.css';

// Example JSON schema
const schema = {
  app: "App1",
  version: "1.0.0",
  containers: [
    {
      name: "frontend",
      env_vars: [
        {
          name: "DOMAIN",
          type: "string",
          default: "test.com",
          hint: "Please enter you domain"
        },
        {
          name: "USE_CUSTOM_LOGGER",
          type: "boolean",
          default: true,
          hint: "Enable or not"
        },
        {
          name: "LOG_LEVEL",
          type: "dropdown-list",
          values: ["debug", "info", "warning"],
          default: "info",
          hint: "Please choose logging level"
        },
      ],
    },
    {
      name: "backend",
      env_vars: [
        {
          name: "DOMAIN",
          type: "string",
          default: "test.com",
          hint: "Please enter you domain"
        }
      ]
    },
  ],
};

const DynamicForm = () => {
  const [formData, setFormData] = useState({});

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

  return (
    <div>
      <h1>{schema.app} configuration</h1>
      <h2>{schema.version}</h2>
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
      <pre>{JSON.stringify(formData, null, 2)}</pre>
    </div>
  );
};

export default DynamicForm;
