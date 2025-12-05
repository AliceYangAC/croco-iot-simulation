import os
import time
import random
from azure.iot.device import IoTHubDeviceClient, Message
from dotenv import load_dotenv

# Explicitly load the .env file from this folder
BASE_DIR = os.path.dirname(__file__)
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))

# Load connection strings from environment variables
TUSK_CONN_STR = os.getenv("TUSK_CONN_STR")
BRUTUS_CONN_STR = os.getenv("BRUTUS_CONN_STR")
MIFFY_CONN_STR = os.getenv("MIFFY_CONN_STR")

# Define locations and their connection strings
locations ={"Tusk": TUSK_CONN_STR, "Brutus": BRUTUS_CONN_STR, "Miffy": MIFFY_CONN_STR}

# Function to generate random telemetry data
def get_telemetry(croc):
    return {
        "heartrate": random.uniform(1, 40),
        "iq": random.uniform(80, 120),
        "steps_taken": random.uniform(0, 15000),
        "hp": random.uniform(0, 100),
        "kill_count": random.uniform(0, 200),
        "body_temperature": random.uniform(28.0, 40.0),
        "blood_pressure": str(random.uniform(80.0, 180.0)) + "/" + str(random.uniform(40.0, 120.0)),
        "weight": random.uniform(120.0, 750.0),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
        "gender": random.choice(["Male", "Female", "Non-binary"]),
        "name": croc
    }

# Main function to send telemetry data
def main():
    print("Sending telemetry of 3 devices to IoT Hub...")
    
    # Create IoT Hub device clients for each location
    clients = {croc: IoTHubDeviceClient.create_from_connection_string(conn_str)
               for croc, conn_str in locations.items()}
    try:
        # True loop to send telemetry data every 10 seconds
        while True:
            # Send telemetry data for each location
            for croc, client in clients.items():
                telemetry = get_telemetry(croc)
                message = Message(str(telemetry))
                client.send_message(message)
            # Wait for 10 seconds before sending the next batch
            time.sleep(10)
    except KeyboardInterrupt:
        print("Stopped sending messages.")
    finally:
        # Disconnect all clients
        for client in clients.values():
            client.disconnect()
if __name__ == "__main__":
    main()