from flask import Blueprint, request, jsonify, current_app
from neo4j_driver import get_driver
from dao.device import DeviceRepository
from neo4j.exceptions import ServiceUnavailable, CypherTypeError

phone_blueprint = Blueprint('phone_tracker', __name__)

@phone_blueprint.route("/api/phone_tracker", methods=['POST'])
def get_interaction():
    data = request.json
    current_app.logger.debug(f"Received data: {data}") 

    if not data:
        return jsonify({"error": "Invalid payload"}), 400

    if "devices" not in data or "interaction" not in data:
        return jsonify({"error": "Missing required keys: 'devices' and/or 'interaction'"}), 400

    try:
        device_1 = data["devices"][0]
        device_2 = data["devices"][1]
        interaction = data["interaction"]
        
        current_app.logger.debug(f"Device 1: {device_1}, Device 2: {device_2}, Interaction: {interaction}")

        if isinstance(interaction, dict):
            interaction = {k: v if isinstance(v, (int, float, str)) else None for k, v in interaction.items()}

        current_app.logger.debug(f"Processed interaction: {interaction}")


        device_repo = DeviceRepository(get_driver())
        result = device_repo.create_device_and_interaction(device_1, device_2, interaction)
        

        current_app.logger.debug(f"Database result: {result}")

        return jsonify({
            "message": "Data processed successfully",
            "device_1": device_1,
            "device_2": device_2
        }), 200

    except Exception as e:
        current_app.logger.error(f"Error processing request: {e}")
        return jsonify({"error": "Server error"}), 500



@phone_blueprint.route("/api/bluetooth_connections", methods=['GET'])
def get_bluetooth_connections():
    device_repo = DeviceRepository(get_driver())
    bluetooth_connections = device_repo.count_bluetooth_connections()

    return jsonify({'result': bluetooth_connections}), 200


@phone_blueprint.route("/api/strong_signal_devices", methods=['GET'])
def find_stronger_devices():
    data = request.args.get('signal_strength_dbm', -60)
    device_repo = DeviceRepository(get_driver())
    strong_signal_devices = device_repo.find_devices_with_signal_strength(int(data))

    return jsonify({'result': strong_signal_devices}), 200


@phone_blueprint.route("/api/device_connections", methods=['GET'])
def count_connected_devices():
    device_id = request.args.get('device_id')
    device_repo = DeviceRepository(get_driver())
    device_connections = device_repo.count_device_connections(device_id)

    return jsonify({'result': device_connections}), 200


@phone_blueprint.route("/api/direct_connection", methods=['GET'])
def check_direct_connection():
    from_device_id = request.args.get('from_device_id')
    to_device_id = request.args.get('to_device_id')
    device_repo = DeviceRepository(get_driver())
    is_direct_connection = device_repo.is_device_direct_connection(from_device_id, to_device_id)

    return jsonify({'result': is_direct_connection}), 200


@phone_blueprint.route("/api/most_recent_interaction", methods=['GET'])
def get_most_recent_interaction():
    device_id = request.args.get('device_id')
    device_repo = DeviceRepository(get_driver())
    most_recent_interaction = device_repo.find_most_recent_interaction(device_id)

    return jsonify({'result': most_recent_interaction}), 200