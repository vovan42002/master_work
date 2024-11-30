import React, { useState, useEffect } from "react";
import axios from "axios";
import "./styles/VersionModal.css";
import { APPLICATIONS_SERVICE_BASE_URL } from "./env.js"

const VersionModal = ({ appName, onClose, onSelect }) => {
    const [versions, setVersions] = useState([]);
    const [error, setError] = useState("");
    const [isLoading, setIsLoading] = useState(true); // Added loading state

    useEffect(() => {
        const fetchVersions = async () => {
            try {
                const response = await axios.get(
                    `${APPLICATIONS_SERVICE_BASE_URL}/v1/applications/${appName}/versions`,
                    { headers: { Accept: "application/json" } }
                );
                setVersions(response.data.versions);
            } catch (err) {
                console.error("Error fetching versions:", err);
                setError("Failed to load versions. Please try again later.");
            } finally {
                setIsLoading(false);
            }
        };

        fetchVersions();
    }, [appName]);

    return (
        <div className="modal-backdrop" role="dialog" aria-labelledby="modal-title">
            <div className="modal">
                <header className="modal-header">
                    <h2 id="modal-title">Select Version for {appName}</h2>
                </header>
                <main className="modal-content">
                    {error ? (
                        <p className="error" role="alert">
                            {error}
                        </p>
                    ) : isLoading ? (
                        <p>Loading versions...</p>
                    ) : (
                        <ul className="version-list">
                            {versions.map((version) => (
                                <li key={version} className="version-item">
                                    <button
                                        className="version-button"
                                        onClick={() => onSelect(version)}
                                    >
                                        {version}
                                    </button>
                                </li>
                            ))}
                        </ul>
                    )}
                </main>
                <footer className="modal-footer">
                    <button
                        onClick={onClose}
                        className="close-button"
                        aria-label="Close version selection modal"
                    >
                        Cancel
                    </button>
                </footer>
            </div>
        </div>
    );
};

export default VersionModal;
