# AccessVerifier
To improve security, AccessVerifier implements IP address restrictions to ensure that only requests originating from the allowed AWS IP ranges in the Europe West region are processed.

You can use this variables for configuration:
- AWS_IP_RANGES_URL - Where to take allowed IP ranges from ([https://ip-ranges.amazonaws.com/ip-ranges.json](https://ip-ranges.amazonaws.com/ip-ranges.json) by default)
- REGION_FILTER - Region of IP to be allowed (eu-west- by default)
- IPS_REFRESH_TIME - How often it will refresh IP list in seconds (24 hours = 86400 seconds by default)

You can as well overwrite starting command if you want to change any parameter of gunicorn.
