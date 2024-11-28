from flask import Blueprint, request, jsonify, current_app
from neo4j_driver import get_driver
from dao.device import DeviceRepository



phone_blueprint = Blueprint('phone_tracker', __name__)


@phone_blueprint.route("/api/phone_tracker", methods=['POST'])
def get_interaction():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid payload"}), 400
    

    if isinstance(data, list):
        try:

            device_1 = data[0]
            device_2 = data[1]
            interaction = data[2]
            device_repo = DeviceRepository(get_driver())

            result = device_repo.create_device_and_interaction(device_1, device_2, interaction)
            return jsonify({
                "message": "Data processed successfully",
                "device_1": device_1,
                "device_2": device_2
            }), 200

        except IndexError as e:
            return jsonify({"error": "Devices list is incomplete"}), 400
    else:
        return jsonify({"error": "Invalid data format, expected a list"}), 400




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