import React from "react";

/**
 * Renders the appropriate input based on the environment variable type.
 *
 * @param {string} containerName - The name of the container.
 * @param {Object} env - The environment variable object.
 * @param {Object} formData - The current form data state.
 * @param {Function} handleInputChange - Function to handle input changes.
 */
const renderInput = (containerName, env, formData, handleInputChange) => {
    switch (env.type) {
        case "string":
            return (
                <input
                    className="input-text"
                    type="text"
                    value={formData[containerName]?.[env.name] || env.default}
                    onChange={(e) => handleInputChange(containerName, env.name, e.target.value)}
                />
            );
        case "boolean":
            return (
                <input
                    className="input-checkbox"
                    type="checkbox"
                    checked={formData[containerName]?.[env.name] ?? env.default}
                    onChange={(e) => handleInputChange(containerName, env.name, e.target.checked)}
                />
            );
        case "dropdown-list":
            return (
                <select
                    className="input-dropdown"
                    value={formData[containerName]?.[env.name] || env.default}
                    onChange={(e) => handleInputChange(containerName, env.name, e.target.value)}
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

export default renderInput;
