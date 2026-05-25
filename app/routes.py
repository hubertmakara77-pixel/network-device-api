from flask import Blueprint, request, jsonify
from .database import db
from .models import Device

# Blueprint is a "section" in our API. All paths here will start with /api
api = Blueprint('api', __name__)

# --- 1. ADDING A DEVICE (POST) ---
@api.route('/devices', methods=['POST'])
def add_device():
    # We retrieve JSON data from the query
    data = request.get_json()
    
    # Simple validation - we check whether the user has provided the required information
    if not data or 'hostname' not in data or 'ip_address' not in data:
        return jsonify({'error': 'Missing required data: hostname and ip_address'}), 400

    # We create a new object
    new_device = Device(
        hostname=data['hostname'],
        ip_address=data['ip_address'],
        snmp_community=data.get('snmp_community', 'public'), # by default 'public'
        port=data.get('port', 161)                           # by default 161
    )

    try:
        db.session.add(new_device) # Add to "queue"
        db.session.commit()        # Confirm and save to database file
        return jsonify({'message': 'Device added!', 'id': new_device.id}), 201
    except Exception as e:
        db.session.rollback()      # In case of error, undo changes
        return jsonify({'error': 'The IP address probably already exists in the database.'}), 400


# --- 2. GETTING THE DEVICE LIST (GET) ---
@api.route('/devices', methods=['GET'])
def get_devices():

    devices = Device.query.all() 
    
    # We create an empty list and pack the device data into it
    result = []
    for d in devices:
        result.append({
            'id': d.id,
            'hostname': d.hostname,
            'ip_address': d.ip_address,
            'snmp_community': d.snmp_community,
            'port': d.port
        })
        
    return jsonify(result), 200
# --- 3. DOWNLOADING ONE DEVICE (GET) ---
@api.route('/devices/<int:id>', methods=['GET'])
def get_device(id):
    # get_or_404 is a great function - if a router with the given ID does not exist,
    # The API will automatically return a 404 (Not Found) error
    device = Device.query.get_or_404(id)
    
    return jsonify({
        'id': device.id,
        'hostname': device.hostname,
        'ip_address': device.ip_address,
        'snmp_community': device.snmp_community,
        'port': device.port
    }), 200

# --- 4. DEVICE UPDATE (PUT) ---
@api.route('/devices/<int:id>', methods=['PUT'])
def update_device(id):
    device = Device.query.get_or_404(id)
    data = request.get_json()
    
    # We only update the fields that were sent in the query
    if 'hostname' in data:
        device.hostname = data['hostname']
    if 'ip_address' in data:
        device.ip_address = data['ip_address']
    if 'snmp_community' in data:
        device.snmp_community = data['snmp_community']
    if 'port' in data:
        device.port = data['port']
        
    db.session.commit() # We save changes to the database
    return jsonify({'message': f'Device {id} updated!'}), 200

# --- 5. DELETE DEVICE ---
@api.route('/devices/<int:id>', methods=['DELETE'])
def delete_device(id):
    device = Device.query.get_or_404(id)
    
    db.session.delete(device) # Delete
    db.session.commit()       # We confirm the change
    return jsonify({'message': f'Device {id} removed from the database!'}), 200