#RyomenKingsfall


#import statements
import argparse
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

# Function to parse port input
def parse_ports(s):
    parts = s.split(',')
    ports = set()
    for p in parts:
        if '-' in p:
            lo, hi = p.split('-', 1)
            ports.update(range(int(lo), int(hi) + 1))
        else:
            ports.add(int(p))
    return sorted(p for p in ports if 1 <= p <= 65535)

def scan_port(host, port, timeout):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            if sock.connect_ex((host, port)) == 0:
                try:
                    svc = socket.getservbyport(port)
                except OSError:
                    svc = ''
                return port, True, svc
    except Exception:
        pass
    return port, False, ''

def main():
    parser = argparse.ArgumentParser(description="Basic TCP port scanner")
    parser.add_argument("host", help="Target hostname or IP")
    parser.add_argument("-p", "--ports", default="1-1024",
                        help="Ports (e.g. 22,80,443 or 1-1024). Default: 1-1024")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Number of worker threads")
    parser.add_argument("--timeout", type=float, default=1.0, help="Socket timeout in seconds")
    args = parser.parse_args()

    try:
        addr = socket.gethostbyname(args.host)
    except socket.gaierror:
        print(f"Cannot resolve host: {args.host}")
        return

    ports = parse_ports(args.ports)
    print(f"Scanning {args.host} ({addr}) {len(ports)} ports with {args.threads} threads...")

    open_ports = []
    with ThreadPoolExecutor(max_workers=args.threads) as ex:
        futures = {ex.submit(scan_port, addr, p, args.timeout): p for p in ports}
        for fut in as_completed(futures):
            port, is_open, svc = fut.result()
            if is_open:
                open_ports.append((port, svc))
                svc_txt = f"/{svc}" if svc else ""
                print(f"{port} open{svc_txt}")

    if not open_ports:
        print("No open ports found.")

if __name__ == "__main__":
    main()