from ipaddress import IPv4Address
from abc import ABC, abstractmethod
import re
import datetime

TIMESTAMP = "timestamp"
HOST_NAME = "host_name"
PID_NUMBER = "pid_number"
MESSAGE = "message"
TIMESTAMP_MATCH = 1
HOST_NAME_MATCH = 2
PID_NUMBER_MATCH = 4
MESSAGE_MATCH = 5
LOG_PATTERN = r"^(\w{3}\s\d{1,2}\s\d{2}:\d{2}:\d{2})\s(\S+)\s(\S+)\[(\d+)\]:\s(.*)$"
IPV4_PATTERN = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
TIMESTAMP_FORMAT = "%b %d %H:%M:%S"
TYPE_ERROR_MESSAGE = "Trying to compare non SSHLogEntry object"
MATCHING_EXCEPTION_MESSAGE = "No match in log line!"


class SSHLogEntry(ABC):
    def __init__(self, log):
        prepared_log = self.parse_log_line(log)
        self.timestamp = prepared_log[TIMESTAMP]
        self._message = prepared_log[MESSAGE]
        self.pid_number = prepared_log[PID_NUMBER]
        self.host_name = prepared_log[HOST_NAME] if prepared_log[HOST_NAME] else None

    def parse_log_line(log):
        try:
            match = re.match(LOG_PATTERN, log)
            if not match:
                return {}
            return {
                TIMESTAMP: datetime.datetime.strptime(match.group(TIMESTAMP_MATCH), TIMESTAMP_FORMAT),
                HOST_NAME: match.group(HOST_NAME_MATCH),
                PID_NUMBER: match.group(PID_NUMBER_MATCH),
                MESSAGE: match.group(MESSAGE_MATCH),
            }
        except Exception:
            raise Exception(MATCHING_EXCEPTION_MESSAGE)

    def __str__(self):
        return f"[{self.timestamp}] [{self.pid_number}] [{self.host_name}] [{self._message}]" if self.host_name else f"[{self.timestamp}] [{self.pid_number}] [{self._message}]"

    def get_ipv4_address(self):
        match = re.search(IPV4_PATTERN, self._message)
        return IPv4Address(match.group(0)) if match else None

    @abstractmethod
    def validate(self):
        pass

    @property
    def has_ip(self):
        return self.get_ipv4_address() is not None

    def __repr__(self):
        return f"SSHLogEntry (timestamp={self.timestamp}, host_name={self.host_name}, pid_number={self.pid_number}, message={self._message})"

    def __eq__(self, other):
        if not isinstance(other, SSHLogEntry):
            raise TypeError(TYPE_ERROR_MESSAGE)
        return (self.timestamp, self.host_name, self.pid_number, self._message) == (other.timestamp, other.host_name, other.pid_number, other._message)

    def __lt__(self, other):
        if not isinstance(other, SSHLogEntry):
            raise TypeError(TYPE_ERROR_MESSAGE)
        return self.timestamp < other.timestamp

    def __gt__(self, other):
        if not isinstance(other, SSHLogEntry):
            raise TypeError(TYPE_ERROR_MESSAGE)
        return self.timestamp > other.timestamp

