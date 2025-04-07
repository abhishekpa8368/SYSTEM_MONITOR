import psutil

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_ram_usage():
    return psutil.virtual_memory().percent

def get_disk_usage():
    return psutil.disk_usage('/').percent

def get_network_usage():
    net_io = psutil.net_io_counters()
    return {"sent": net_io.bytes_sent, "received": net_io.bytes_recv}
