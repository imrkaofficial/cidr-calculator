import ipaddress

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
        "Network Address": network_address,
        "Broadcast Address": broadcast_address,
        "First Host Address": first_host,
        "Last Host Address": last_host,
        "Subnet Mask": network.netmask,
        "Number of Hosts": network.num_addresses - 2
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

if __name__ == "__main__":
    print("Choose an option:")
    print("1. Convert CIDR to IP address range")
    print("2. Convert IP address range to CIDR")
    choice = input("Enter choice (1 or 2): ")

    if choice == '1':
        cidr_input = input("Enter CIDR notation (e.g., 192.168.1.0/24): ")
        
        if validate_cidr(cidr_input):
            result = cidr_to_range(cidr_input)
            if isinstance(result, str):
                print(result)
            else:
                for key, value in result.items():
                    print(f"{key}: {value}")
        else:
            print(f"{cidr_input} is not a valid CIDR notation. Please enter a valid CIDR.")

    elif choice == '2':
        start_ip = input("Enter the start IP address: ")
        end_ip = input("Enter the end IP address: ")
        result = range_to_cidr(start_ip, end_ip)
        if isinstance(result, str):
            print(result)
        else:
            print("CIDR notation(s):")
            for cidr in result:
                print(cidr)
    else:
        print("Invalid choice. Please enter 1 or 2.")
