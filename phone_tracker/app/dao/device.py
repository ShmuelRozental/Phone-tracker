from neo4j.exceptions import ServiceUnavailable

class DeviceRepository:
    def __init__(self, driver):
        self.driver = driver

    def create_device_and_interaction(self, device_1, device_2, interaction_data):
        query = """
        MERGE (d1:Device {id: $device_1.id})
        SET d1.brand = $device_1.brand, d1.model = $device_1.model, d1.os = $device_1.os, d1.location = $device_1.location
        
        MERGE (d2:Device {id: $device_2.id})
        SET d2.brand = $device_2.brand, d2.model = $device_2.model, d2.os = $device_2.os, d2.location = $device_2.location
        
        MERGE (d1)-[r:INTERACTED_WITH]->(d2)
        SET r.method = $interaction.method, 
            r.signal_strength_dbm = $interaction.signal_strength_dbm,
            r.distance_meters = $interaction.distance_meters, 
            r.timestamp = $interaction.timestamp
        RETURN d1, d2, r
        """
        with self.driver.session() as session:
            try:
                result = session.write_transaction(
                    lambda tx: tx.run(
                        query,
                        device_1=device_1,
                        device_2=device_2,
                        interaction=interaction_data
                    )
                )
                return result.single()
            except ServiceUnavailable as e:
                raise e




    def count_bluetooth_connections(self):
        query = """
            MATCH (start:Device)
            MATCH (end:Device)
            WHERE start <> end
            MATCH path = shortestPath((start)-[:CONNECTED*]->(end))
            WHERE ALL(r IN relationships(path) WHERE r.method = 'Bluetooth')
            WITH path, length(path) as pathLength
            ORDER BY pathLength DESC
            LIMIT 1
            RETURN length(path) as length
        """
        with self.driver.session() as session:
            result = session.run(query)

            return result.single()["length"]

    def find_devices_with_signal_strength(self, signal_strength_dbm):
        query = """
            MATCH (d1:Device)-[r:CONNECTED]->(d2:Device)
            WHERE r.signal_strength_dbm > $signal_strength_dbm
            RETURN d1.id AS device_from, d2.id AS device_to, r.signal_strength_dbm AS signal_strength
        """
        with self.driver.session() as session:
            result = session.run(query, {"signal_strength_dbm": signal_strength_dbm})

            devices = []
            for record in result:
                devices.append({
                    "device_from": record["device_from"],
                    "device_to": record["device_to"],
                    "signal_strength_dbm": record["signal_strength"]
                })

        return devices

    def count_device_connections(self, device_id):
        query = """
            MATCH (d:Device)-[r:CONNECTED]-(d2:Device)
            WHERE d.id = $device_id
            RETURN COUNT(r) as connection_count
        """
        with self.driver.session() as session:
            result = session.run(query, {"device_id": device_id})

            return result.single()["connection_count"]

    def is_device_direct_connection(self, from_device_id, to_device_id):
        query = """
            MATCH (d1:Device)-[r:CONNECTED]-(d2:Device)
            WHERE d1.id = $from_device_id AND d2.id = $to_device_id
            RETURN COUNT(r) > 0 as is_connection
        """
        with self.driver.session() as session:
            result = session.run(query, {"from_device_id": from_device_id, "to_device_id": to_device_id})

            return result.single()["is_connection"]

    def find_most_recent_interaction(self, device_id):
        query = """
            MATCH (d:Device)-[r:CONNECTED]-(other:Device)
            WHERE d.id = $device_id
            RETURN other.id AS other_device_id, r.timestamp AS interaction_timestamp
            ORDER BY r.timestamp DESC
            LIMIT 1
        """
        with self.driver.session() as session:
            result = session.run(query, {"device_id": device_id})
            record = result.single()

            if record:
                return {
                    "other_device_id": record["other_device_id"],
                    "interaction_timestamp": record["interaction_timestamp"]
                }
            else:
                return None