export const AUTH_SERVICE_BASE_URL = "https://auth.master-work-volodymyr.com";
export const APPLICATIONS_SERVICE_BASE_URL = "https://backend.master-work-volodymyr.com";

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
