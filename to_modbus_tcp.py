# --- Import Libraries ---
import time # Library for time
import paho.mqtt.client as mqtt # Library for MQTT
import json # Library for JSON format
from pymodbus.client import ModbusTcpClient # Modbus TCP client
from pymodbus.exceptions import ModbusIOException # Exception for Modbus

# --- MQTT Setup ---
MQTT_BROKER = 'broker.emqx.io'  # MQTT broker address
MQTT_PORT = 1883                # Default MQTT broker port
MQTT_TOPIC = 'data/test1' # MQTT topic to publish data

# --- Modbus Server Configuration ---
MODBUS_SERVER_IP = "192.168.0.7"  # Modbus TCP server IP
MODBUS_PORT = 502                 # Modbus TCP port (default)


# --- MQTT Functions ---
def connect_mqtt():
    """
    Create and connect to the MQTT broker with auto-reconnect.
    """
    client = mqtt.Client() # creating a new MQTT client object from the paho-mqtt library

    # Callback for when MQTT connection is lost
    def on_disconnect(client, userdata, rc): #callback function in the paho-mqtt library
        print("MQTT disconnected. Trying to reconnect...")
        while True:
            try:
                client.reconnect()  # Attempt to reconnect
                print("Reconnected to MQTT broker.")
                break
            except Exception as e:
                print(f"Reconnect failed: {e}. Retrying in 5s...")
                time.sleep(5)

    # Attach callback
    client.on_disconnect = on_disconnect

    # Try to connect to broker
    try:
        client.connect(MQTT_BROKER, MQTT_PORT)
        client.loop_start()  # Start MQTT loop in background
        print("Connected to MQTT broker.")
    except Exception as e:
        print(f"Failed to connect to MQTT broker: {e}")
        time.sleep(5)
        return connect_mqtt()  # Retry until success

    return client


def send_data(client, data):
    """
    Publish data to the MQTT broker in JSON format.
    :param client: MQTT client object
    :param data: list of Modbus register values
    """
    if len(data) < 2:
        print("Not enough data from Modbus to send.")
        return

    # Format payload (example: temperature & humidity)
    payload = {
        'temperature': data[0],
        'humidity': data[1],
        'time': time.strftime("%Y-%m-%d %H:%M:%S"),  # Current timestamp
    }

    # Publish to broker
    try:
        client.publish(MQTT_TOPIC, json.dumps(payload))
        print(f"Data sent: {payload}")
    except Exception as e:
        print(f"Failed to send data via MQTT: {e}")


# --- Modbus Functions ---
def connect_modbus():
    """
    Create and connect a Modbus client with retry logic.
    """
    while True:
        client = ModbusTcpClient(MODBUS_SERVER_IP, port=MODBUS_PORT)
        if client.connect():
            print("Connected to Modbus server.")
            return client
        else:
            print("Failed to connect to Modbus server. Retrying in 5s...")
            time.sleep(5)


# --- Main Loop ---
def main():
    # Initial connections
    modbus_client = connect_modbus()
    mqtt_client = connect_mqtt()

    try:
        while True:
            try:
                # Read 2 registers starting from address 1
                address = 1
                count = 2
                response = modbus_client.read_input_registers(address=address, count=count)

                # If read failed → reconnect Modbus
                if response is None or response.isError():
                    print("Failed to read input registers. Reconnecting Modbus...")
                    modbus_client.close()
                    modbus_client = connect_modbus()
                else:
                    # If successful → send data to MQTT
                    send_data(mqtt_client, response.registers)

            except ModbusIOException as e:
                # Handle Modbus communication error
                print(f"Modbus IO Error: {e}. Reconnecting...")
                modbus_client.close()
                modbus_client = connect_modbus()

            # Delay before next read
            time.sleep(5)

    except KeyboardInterrupt:
        # Graceful stop if user presses CTRL+C
        print("Program interrupted by user.")

    finally:
        # Clean up connections safely
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        modbus_client.close()
        print("Connections closed.")


# --- Run only if executed directly ---
if __name__ == '__main__':
    main()