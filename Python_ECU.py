import can
import time
import csv

# Configuration
can_interface = 'vector'  # Use 'vector' for Vector interfaces
duration = 1.0  # Duration to collect data in seconds (increased for testing)
output_file = 'ecu_data.csv'

# Initialize CAN bus
bus = can.interface.Bus(channel='0', bustype='vector')  # '0' is typically the channel for VN1630

# Function to collect data
def collect_data(duration):
    start_time = time.time()
    collected_data = []

    while time.time() - start_time < duration:
        try:
            print("Waiting for CAN messages...")
            message = bus.recv(timeout=0.01)  # 10 ms timeout for faster processing
            if message is not None:
                # Keep timestamp in original format and convert others to hex
                timestamp = message.timestamp  # Keep timestamp as is
                arbitration_id_hex = format(message.arbitration_id, 'x')
                data_hex = message.data.hex()
                dlc = message.dlc  # Data Length Code
                message_type = 'Extended' if message.is_extended_id else 'Standard'  # Message Type

                collected_data.append((timestamp, arbitration_id_hex, data_hex, dlc, message_type))
                print(f"Received message: Timestamp={timestamp}, ID={arbitration_id_hex}, Data={data_hex}, DLC={dlc}, Type={message_type}")
        except can.CanError as e:
            print(f"CAN error: {e}")
        except Exception as e:
            print(f"Error receiving message: {e}")

    return collected_data

# Write collected data to CSV
def write_to_csv(data, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Arbitration ID (hex)', 'Data (hex)', 'DLC', 'Message Type'])
        writer.writerows(data)

# Main function
def main():
    print("Starting data collection...")
    try:
        data = collect_data(duration)
    except Exception as e:
        print(f"An error occurred during data collection: {e}")
    finally:
        bus.shutdown()  # Ensure the bus is shut down properly
        print("CAN bus shut down.")

    print("Data collection completed.")
    write_to_csv(data, output_file)
    print(f"Data saved to {output_file}")

if __name__ == "__main__":
    main()