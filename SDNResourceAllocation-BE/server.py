class Server:
    def __init__(self, cpuCores, RAM, ip):
        super().__init__()
        self.cpuCores = cpuCores
        self.RAM = RAM
        self.ip = ip