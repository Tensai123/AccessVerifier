from flask import Flask, request, jsonify
import os
import requests
import threading
import time
import logging

app = Flask(__name__)

log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
numeric_level = getattr(logging, log_level, logging.INFO)
logging.basicConfig(
    level=numeric_level,
    format='%(asctime)s - %(levelname)s - %(message)s',
)
app.logger.info(f"Logging level set to {log_level}")

# URL to fetch IP ranges for AWS Europe West
# AWS_IP_RANGES_URL = os.getenv("AWS_IP_RANGES_URL")
# REGION_FILTER = os.getenv("REGION_FILTER")

AWS_IP_RANGES_URL = "https://ip-ranges.amazonaws.com/ip-ranges.json"
REGION_FILTER = "eu-west-"

# Function to refresh allowed IPs
def refresh_allowed_ips():
    global allowed_ips
    while True:
        try:
            response = requests.get(AWS_IP_RANGES_URL)
            response.raise_for_status()
            data = response.json()
            
            # Extract the IP ranges for the selected region (AWS Europe West)
            new_allowed_ips = set()
            for prefix in data.get("prefixes", []):
                if prefix.get("region", "").startswith(REGION_FILTER):
                    new_allowed_ips.add(prefix.get("ip_prefix"))

            allowed_ips = new_allowed_ips
            app.logger.info(f"Updated allowed IPs: {allowed_ips}")
        except Exception as e:
            app.logger.error(f"Failed to update IP ranges: {e}")
        
        # time.sleep(int(os.getenv("IPS_REFRESH_TIME")))
        time.sleep(86400)

# Endpoint to verify access
@app.route("/verify", methods=["POST"])
def verify():
    app.logger.debug(f"Incoming request: {request}")
    client_host = request.remote_addr

    if any(ip_in_range(client_host, allowed_range) for allowed_range in allowed_ips):
        app.logger.debug(f"IP {client_host} allowed")
        return "OK", 200
    else:
        app.logger.warning(f"IP {client_host} not allowed")
        return "Unauthorized", 401

# Helper function to check if an IP is within a given range
from ipaddress import ip_network, ip_address
def ip_in_range(ip, range):
    try:
        return ip_address(ip) in ip_network(range)
    except ValueError:
        return False
    
# Start a background thread to refresh allowed IPs
threading.Thread(target=refresh_allowed_ips, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000) 