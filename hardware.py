
devices = {
    "bedroom_light": False,
    "living_room_light": False,
    "fan": False
}


def execute_command(command):

    device = command.get("device")
    action = command.get("action")

    if device not in devices:
        return {
            "success": False,
            "error": "Unknown device"
        }

    if action == "turn_on":
        devices[device] = True

    elif action == "turn_off":
        devices[device] = False

    elif action == "get_status":
        pass

    else:
        return {
            "success": False,
            "error": "Invalid action"
        }

    return {
        "success": True,
        "device": device,
        "action": action,
        "status": "ON" if devices[device] else "OFF"
    }


def get_all_devices():
    return {
        device: "ON" if status else "OFF"
        for device, status in devices.items()
    }
