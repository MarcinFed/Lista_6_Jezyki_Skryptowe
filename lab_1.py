from ipaddress import IPv4Address
from abc import ABC, abstractmethod
import re
from tools import parse_log_line, TIMESTAMP, HOST_NAME, MESSAGE, PID_NUMBER, IPV4_PATTERN


class SSHLogEntry(ABC):
    def __init__(self, log):
        prepared_log = parse_log_line(log)
        self.timestamp = prepared_log[TIMESTAMP]
        self.__message = prepared_log[MESSAGE]
        self.pid_number = prepared_log[PID_NUMBER]
        self.host_name = prepared_log[HOST_NAME] if prepared_log[HOST_NAME] else None

    def __str__(self):
        return f"[{self.timestamp}] [{self.pid_number}] [{self.host_name}] [{self.__message}]" if self.host_name else f"[{self.timestamp}] [{self.pid_number}] [{self.__message}]"

    def get_ipv4_address(self):
        match = re.search(IPV4_PATTERN, self.__message)
        return IPv4Address(match.group(0)) if match else None

    @abstractmethod
    def validate(self):
        pass

    @property
    def has_ip(self):
        return self.get_ipv4_address() is not None

    def __repr__(self):
        return f"SSHLogEntry (timestamp={self.timestamp}, host_name={self.host_name}, pid_number={self.pid_number}, message={self.__message})"

    def __eq__(self, other):
        if not isinstance(other, SSHLogEntry):
            raise TypeError("Trying to compare non SSHLogEntry object")
        return (self.timestamp, self.host_name, self.pid_number, self.__message) == (other.timestamp, other.host_name, other.pid_numberm, other.__message)

    def __lt__(self, other):
        if not isinstance(other, SSHLogEntry):
            raise TypeError("Trying to compare non SSHLogEntry object")
        return self.timestamp < other.timestamp

    def __gt__(self, other):
        if not isinstance(other, SSHLogEntry):
            raise TypeError("Trying to compare non SSHLogEntry object")
        return self.timestamp > other.timestamp

