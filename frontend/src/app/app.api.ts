// Central API base for frontend services.
// For local development, point directly to the API Gateway so requests work
// even when the Angular dev server runs on a non-standard port.
// The gateway in this workspace listens on http://127.0.0.1:8002 and forwards
// /api/* to the appropriate backend services.
// For immediate local testing point directly to the auth service (port 8000).
// If you prefer the API Gateway route, change this to 'http://127.0.0.1:8002/api' once the
// gateway is running and stable.
export const BASE_API = 'http://127.0.0.1:8000/api';
