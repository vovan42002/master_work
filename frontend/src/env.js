export const REACT_APP_AUTH_SERVICE_BASE_URL = "http://localhost:8003";
export const REACT_APP_APPLICATIONS_SERVICE_BASE_URL = "http://localhost:8002";

if (!REACT_APP_AUTH_SERVICE_BASE_URL) {
    console.warn(
        'Environment variable REACT_APP_AUTH_SERVICE_BASE_URL is not defined. Please ensure it is set in your .env file.'
    );
}

if (!REACT_APP_AUTH_SERVICE_BASE_URL) {
    console.warn(
        'Environment variable REACT_APP_APPLICATIONS_SERVICE_BASE_URL is not defined. Please ensure it is set in your .env file.'
    );
}
