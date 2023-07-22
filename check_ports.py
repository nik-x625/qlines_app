import subprocess

def get_open_ports():
    try:
        netstat_output = subprocess.check_output(['netstat', '-tulpen']).decode('utf-8')
        lines = netstat_output.split('\n')[2:]  # Skip the header lines
        open_ports = set()

        for line in lines:
            parts = line.split()
            if len(parts) >= 4 and parts[0] == 'tcp':
                addr = parts[3]
                ip, port = addr.split(':')
                open_ports.add((ip, int(port)))

        return open_ports
    except subprocess.CalledProcessError as e:
        print(f"Error executing 'netstat' command: {e}")
        return set()

if __name__ == "__main__":
    # List of expected IP and port pairs
    expected_ips_and_ports = [
        ("0.0.0.0", 9092, 'kafka'),
        #("0.0.0.0", 35833, 'kafka'),
        ("0.0.0.0", 2181, 'kafka'),
        #("0.0.0.0", 42283, 'kafka'),
        ("0.0.0.0", 7010, 'clickhouse'),
        ("0.0.0.0", 9000, 'clickhouse'),
        ("0.0.0.0", 9004, 'clickhouse'),
        ("0.0.0.0", 9005, 'clickhouse'),
        ("0.0.0.0", 9009, 'clickhouse'),
        ("127.0.0.1", 27017, 'mongodb'),
        ("127.0.0.1", 6379, 'redis'),
        ("0.0.0.0", 5000, 'qlines'),
        ("127.0.0.1", 1883, 'mosquitto'),
        
        #("8.8.8.8", 53),
        # Add more IP and port pairs as needed
    ]

    open_ports = get_open_ports()

    for ip, port, process in expected_ips_and_ports:
        if (ip, port) in open_ports:
            print(f"Port {port} is open on {ip}.")
        else:
            print(f"Port {port} is closed or unreachable on {ip}. The missing process: {process}")
