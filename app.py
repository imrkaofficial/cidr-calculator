from flask import Flask, render_template, request, jsonify
import ipaddress

app = Flask(__name__)

def validate_cidr(cidr):
    try:
        ipaddress.ip_network(cidr, strict=False)
        return True
    except ValueError:
        return False

def cidr_to_range(cidr):
    try:
        network = ipaddress.ip_network(cidr, strict=False)
    except ValueError:
        return "Invalid CIDR notation"

    network_address = network.network_address
    broadcast_address = network.broadcast_address
    first_host = network_address + 1
    last_host = broadcast_address - 1

    return {
        "Network Address": str(network_address),
        "Broadcast Address": str(broadcast_address),
        "First Host Address": str(first_host),
        "Last Host Address": str(last_host),
        "Subnet Mask": str(network.netmask),
        "Number of Hosts": network.num_addresses - 2 if network.num_addresses > 2 else network.num_addresses
    }

def range_to_cidr(start_ip, end_ip):
    try:
        start = ipaddress.ip_address(start_ip)
        end = ipaddress.ip_address(end_ip)
        if start > end:
            return "Invalid IP address range"
    except ValueError:
        return "Invalid IP addresses"

    networks = ipaddress.summarize_address_range(start, end)
    return [str(network) for network in networks]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cidr-to-range', methods=['POST'])
def cidr_to_range_route():
    cidr = request.form['cidr']
    if validate_cidr(cidr):
        result = cidr_to_range(cidr)
        return jsonify(result)
    else:
        return jsonify({"error": "Invalid CIDR notation"})

@app.route('/range-to-cidr', methods=['POST'])
def range_to_cidr_route():
    start_ip = request.form['start_ip']
    end_ip = request.form['end_ip']
    result = range_to_cidr(start_ip, end_ip)
    if isinstance(result, str):
        return jsonify({"error": result})
    else:
        return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True, port=7000)
