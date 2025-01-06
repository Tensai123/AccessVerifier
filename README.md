# Access Verifier Application

This is a Flask-based access verifier application that checks whether a request is coming from an allowed IP address or host. It fetches AWS IP ranges for the specified region and checks the incoming request's `Host` header against allowed values.

## Features

- Verifies incoming requests based on their `Host` header.
- Fetches AWS IP ranges for the specified region (e.g., Europe West).
- Allows configuring AWS IP range URL and region filter via environment variables (AWS_IP_RANGES_URL and REGION_FILTER by default "https://ip-ranges.amazonaws.com/ip-ranges.json" and "eu-west-").
- Allows log level configuration via LOG_LEVEL environment variable (INFO by default).
- Allows to change interval of refreshing allowed IP addresses range via IPS_REFRESH_TIME variable (in seconds, 86400 seconds = 24 hours by default).

## Requirements

- Python 3.11
- Docker (optional, for containerization)
- Flask 2.1.1
- Requests 2.26.0
- Werkzeug 2.0.3


