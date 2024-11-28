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
