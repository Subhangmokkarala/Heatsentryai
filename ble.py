import bluetooth

def send_notification(device_address, message):
    try:
        socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        socket.connect((device_address, 1))
        socket.send(message)
        socket.close()
        print(f"Notification sent to {device_address}: {message}")
    except Exception as e:
        print(f"Error sending notification to {device_address}: {e}")

def send_notifications(message):
    nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True, lookup_class=True)
    for addr, name, _ in nearby_devices:
        if "Android" in name or "Microsoft" in name:
            send_notification(addr, message)

if __name__ == "__main__":
    message = "Hello from Python!"
    send_notifications(message)
