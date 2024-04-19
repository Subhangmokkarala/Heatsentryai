import asyncio
from bleak import BleakScanner, BleakClient

# Define the notification message
notification_message = "Hello from Python!"

async def send_notification(device_address, message):
    try:
        async with BleakClient(device_address) as client:
            await client.connect()
            await client.write_gatt_char(0x0001, message.encode(), response=True)
            await client.disconnect()
            print(f"Notification sent to {device_address}: {message}")
    except Exception as e:
        print(f"Error sending notification to {device_address}: {e}")

async def discover_and_send_notifications(message):
    scanner = BleakScanner()

    async def scan_callback(device, advertisement_data):
        if device.name:
            devices.append(device)  # Store discovered devices in the list
            print(f"Discovered device: {device.name} ({device.address})")

    devices = []  # List to store discovered devices
    scanner.register_detection_callback(scan_callback)
    
    try:
        await scanner.start()
        print("Scanning for BLE devices...")
        await asyncio.sleep(10)  # Scan for 10 seconds
    except Exception as e:
        print(f"Error during scanning: {e}")
    finally:
        await scanner.stop()

    # Print the list of discovered devices
    print("\nList of Discovered Devices:")
    for device in devices:
        print(f"{device.name} ({device.address})")

if __name__ == "__main__":
    asyncio.run(discover_and_send_notifications(notification_message))
