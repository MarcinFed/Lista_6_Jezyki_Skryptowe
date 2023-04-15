class SSHLogJournal:
    def __init__(self):
        self.ssh_log_entries = []

    def __len__(self):
        return len(self.ssh_log_entries)

    def __contains__(self, log):
        return log in self.ssh_log_entries

    def __iter__(self):
        return iter(self.ssh_log_entries)

    def append(self, log):
        if log.validate():
            self.ssh_log_entries.append(log)

    def get_logs_by_host_name(self, host_name):
        return [log for log in self.ssh_log_entries if log.host_name == host_name]

    def get_log_by_index(self, index):
        return self.ssh_log_entries[index]

    def get_logs_by_ipv4(self, ipv4_address):
        return [log for log in self.ssh_log_entries if log.get_ipv4_address() == ipv4_address]

