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
        if device.name and ("Android" in device.name or "Microsoft" in device.name):
            await send_notification(device.address, message)

    scanner.register_detection_callback(scan_callback)
    await scanner.start()
    await asyncio.sleep(10)  # Scan for 10 seconds
    await scanner.stop()

if __name__ == "__main__":
    asyncio.run(discover_and_send_notifications(notification_message))
