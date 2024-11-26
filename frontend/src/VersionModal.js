import React, { useState, useEffect } from "react";
import axios from "axios";
import "./VersionModal.css";

const VersionModal = ({ appName, onClose, onSelect }) => {
    const [versions, setVersions] = useState([]);
    const [error, setError] = useState("");

    useEffect(() => {
        const fetchVersions = async () => {
            try {
                const response = await axios.get(`http://localhost:8002/v1/applications/${appName}/versions`, {
                    headers: { Accept: "application/json" },
                });
                setVersions(response.data.versions);
            } catch (err) {
                console.error("Error fetching versions:", err);
                setError("Failed to load versions. Please try again later.");
            }
        };

        fetchVersions();
    }, [appName]);

    return (
        <div className="modal-backdrop">
            <div className="modal">
                <h2>Select Version for {appName}</h2>
                {error && <p className="error">{error}</p>}
                {versions.length > 0 ? (
                    <ul>
                        {versions.map((version) => (
                            <li key={version}>
                                <button onClick={() => onSelect(version)}>{version}</button>
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p>Loading versions...</p>
                )}
                <button onClick={onClose} className="close-button">Cancel</button>
            </div>
        </div>
    );
};

export default VersionModal;
