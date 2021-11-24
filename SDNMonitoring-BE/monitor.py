import argparse, socket, time, json, datetime, platform, psutil, requests, pprint, uuid
from socket import getservbyname, getservbyport
import os
from time import sleep
from ping3 import ping

 

# parse args
parser = argparse.ArgumentParser(description='Monitoring script to send system info to a tracking server')
parser.add_argument('-d', '--dest', default='142.250.4.138', help='API Endpoint for Monitoring Data (Defaults to http://localhost:8080/)')
parser.add_argument('-i', '--interval', default=5, type=int, help='Interval between checks (Seconds. Defaults to 5 seconds)')
parser.add_argument('-a', '--attempts', default=30, type=int, help='Attempts to send data when sending failes (Defaults to 30)')
parser.add_argument('-t', '--timeout', default=60, type=int, help='Timeout between resend attempts (Seconds. Defaults to 60. If attempts is reached script will die)')
args = parser.parse_args()

# Factor in sleep for bandwidth checking
if args.interval >= 2:
    args.interval -= 2

def main():
    # Hostname Info
    hostname = socket.gethostname()
    print("Hostname:", hostname)

    # CPU Info
    cpu_count = psutil.cpu_count()
    cpu_usage = psutil.cpu_percent(interval=1)
    print("CPU:\n\tCount:", cpu_count, "\n\tUsage:", cpu_usage)

    # Memory Info
    memory_stats = psutil.virtual_memory()
    memory_total = memory_stats.total
    memory_used = memory_stats.used
    memory_used_percent = memory_stats.percent
    print("Memory:\n\tPercent:", memory_used_percent, "\n\tTotal:", memory_total / 1e+6, "MB", "\n\tUsed:", memory_used / 1e+6, "MB")

    # Disk Info
    disk_info = psutil.disk_partitions()
    print("Disks:")
    disks = []
    for x in disk_info:
        # Try fixes issues with connected 'disk' such as CD-ROMS, Phones, etc.
        try:
            disk = {
                "name" : x.device,
                "mount_point" : x.mountpoint,
                "type" : x.fstype,
                "total_size" : psutil.disk_usage(x.mountpoint).total,
                "used_size" : psutil.disk_usage(x.mountpoint).used,
                "percent_used" : psutil.disk_usage(x.mountpoint).percent
            }

            disks.append(disk)

            print("\tDisk name",disk["name"], "\tMount Point:", disk["mount_point"], "\tType",disk["type"], "\tSize:", disk["total_size"] / 1e+9,"\tUsage:", disk["used_size"] / 1e+9, "\tPercent Used:", disk["percent_used"])
        except:
            print("")

    # Bandwidth Info
    network_stats = get_bandwidth()
    print("Network:\n\tTraffic in:",network_stats["traffic_in"] / 1e+6,"\n\tTraffic out:",network_stats["traffic_out"] / 1e+6)

    # Network Info
    nics = []
    print("NICs:")
    for name, snic_array in psutil.net_if_addrs().items():
        # Create NIC object
        nic = {
            "name": name,
            "mac": "",
            "address": "",
            "address6": "",
            "netmask": ""
        }
        # Get NiC values
        for snic in snic_array:
            if snic.family == -1:
                nic["mac"] = snic.address
            elif snic.family == 2:
                nic["address"] = snic.address
                nic["netmask"] = snic.netmask
            elif snic.family == 23:
                nic["address6"] = snic.address
        nics.append(nic)
        print("\tNIC:",nic["name"], "\tMAC:", nic["mac"], "\tIPv4 Address:",nic["address"], "\tIPv4 Subnet:", nic["netmask"], "\tIPv6 Address:", nic["address6"])

    # Platform Info
    system = {
        "name" : platform.system(),
        "version" : platform.release()
    }
    print("OS:\n\t",system["name"],system["version"])

    # Time Info
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00")
    uptime = int(time.time() - psutil.boot_time())
    print("System Uptime:\n\t",uptime)

    # System UUID
    sys_uuid = uuid.getnode()

    # Set Machine Info
    machine = {
    	"hostname" : hostname,
		"uuid" : sys_uuid,
        "system" : system,
        "uptime" : uptime,
    	"cpu_count" : cpu_count,
    	"cpu_usage" : cpu_usage,
    	"memory_total" : memory_total,
    	"memory_used" : memory_used,
    	"memory_used_percent" : memory_used_percent,
    	"drives" : disks,
    	"network_up" : network_stats["traffic_out"],
    	"network_down" : network_stats["traffic_in"],
        "network_cards": nics,
        "timestamp" : timestamp
    }


def get_bandwidth():
    # Get net in/out
    net1_out = psutil.net_io_counters().bytes_sent
    net1_in = psutil.net_io_counters().bytes_recv

    time.sleep(1)

    # Get new net in/out
    net2_out = psutil.net_io_counters().bytes_sent
    net2_in = psutil.net_io_counters().bytes_recv

    # Compare and get current speed
    if net1_in > net2_in:
        current_in = 0
    else:
        current_in = net2_in - net1_in

    if net1_out > net2_out:
        current_out = 0
    else:
        current_out = net2_out - net1_out

    network = {"traffic_in" : current_in, "traffic_out" : current_out}
    return network

def send_data(data):
    # Attempt to send data up to 30 times
    for attempt in range(args.attempts):
        try:
            # endpoint = monitoring server
            endpoint = args.dest
            response = requests.post(url = endpoint, data = data)
            print("\nPOST:")
            print("Response:", response.status_code)
            print("Headers:")
            pprint.pprint(response.headers)
            print("Content:", response.content)
            # Attempt printing response in JSON if possible
            try:
                print("JSON Content:")
                pprint.pprint(response.json())
            except:
                print("No JSON content")
            break
        except requests.exceptions.RequestException as e:
            print("\nPOST Error:\n",e)
            # Sleep 1 minute before retrying
            time.sleep(args.timeout)
    else:
        # If no connection established for attempts*timeout, kill script
        exit(0)

ip = socket.gethostbyname (socket.gethostname()) #getting ip-address of host

print("\nRunning Protocols and ports:")

for port in range(65535):      #check for all available ports

    try:
        serv = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # create a new socket
        serv.bind((ip,port)) # bind socket with address

    except:
        print('TCP        OPEN       ',port) #print open port number

    serv.close()

for port in range(65535):      #check for all available ports

    try:
        serv = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # create a new socket
        serv.bind((ip,port)) # bind socket with address

    except:
        print('UDP        OPEN       ',port,) #print open port number

    serv.close()

print("-----------------------------------------------------------------\n")
print("CPU usage, Disk usage and Memory usage:\n")

a = True;
while a:
    main()
    print("-----------------------------------------------------------------\n")
    a=False
    

print("Average Delay time between links\n")

THRESHOLD = 0.25  # 250 milliseconds is the Comcast SLA threshold.

# SET YOUR PING INTERVAL HERE, IN SECONDS
INTERVAL = 1

# WHO SHOULD WE RUN THE PING TEST AGAINST
DESTINATION = "142.250.4.138"  # "www.google.com"


# LOG TO WRITE TO WHEN PINGS TAKE LONGER THAN THE THRESHOLD SET ABOVE
i = datetime.datetime.now()
log_file = "logs/latency-tester." + i.strftime("%Y.%m.%d.%H.%M.%S") + ".log"


def write_to_file(file_to_write, message):
    os.makedirs(os.path.dirname(file_to_write), exist_ok=True)
    fh = open(file_to_write, "a")
    fh.write(message + "\n")
    fh.close()


count = 0
header = f"Pinging {DESTINATION} every {INTERVAL} secs; threshold: {THRESHOLD} secs."
print(header)
write_to_file(log_file, header)
a = True
while a:
    count += 1
    latency = ping(DESTINATION)

    # Do we want to write it to the log?
    write_log = "Yes" if latency > THRESHOLD else "No"
    line = f"Pinged {DESTINATION}; latency: {latency} secs; logging: {write_log}"
    print(line)
    write_to_file(log_file, line)
    if(count==5):
       a=False
    sleep(INTERVAL)



if __name__ == '__main__':
    main()
