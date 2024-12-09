export const AUTH_SERVICE_BASE_URL = "https://auth.master-work-volodymyr.com"; //"http://localhost:8003";
export const APPLICATIONS_SERVICE_BASE_URL = "https://backend.master-work-volodymyr.com"; //"http://localhost:8002";

if (!AUTH_SERVICE_BASE_URL) {
    console.warn(
        'Environment variable AUTH_SERVICE_BASE_URL is not defined. Please ensure it is set in your .env file.'
    );
}

if (!AUTH_SERVICE_BASE_URL) {
    console.warn(
        'Environment variable APPLICATIONS_SERVICE_BASE_URL is not defined. Please ensure it is set in your .env file.'
    );
}
