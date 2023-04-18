from lab_1 import SSHLogEntry
import re

FAILED_PASSWORD = "Failed password for invalid user"
ACCEPTED_PASSWORD = "Accepted password"
FOR = "for"
FROM = "from"
RECEIVED_DISCONNECT = "Received disconnect from"
USER_NAME_PATTERN = r"(?<=user )\w+"
ERROR_PATTERN = r"error: (.+?) \["


def get_user_name(message):
    try:
        return re.findall(USER_NAME_PATTERN, message)[0]
    except Exception:
        raise IndexError("No user_name in message")


def get_error_msg(message):
    return re.findall(ERROR_PATTERN, message)[0]


class RejectedPasswordSSHLogEntry(SSHLogEntry):
    def __init__(self, log):
        super().__init__(log)
        self.user_name = get_user_name(self._message)

    def validate(self):
        return FAILED_PASSWORD in self._message


class AcceptedPasswordSSHLogEntry(SSHLogEntry):
    def __init__(self, log):
        super().__init__(log)
        self.user_name = get_user_name(self._message)

    def validate(self):
        return ACCEPTED_PASSWORD and FOR and FROM in self._message


class ErrorSSHLogEntry(SSHLogEntry):
    def __init__(self, log):
        super().__init__(log)
        self.error_message = get_error_msg(self._message)

    def validate(self):
        return RECEIVED_DISCONNECT in self._message


class OtherSSHLogEntry(SSHLogEntry):
    def __init__(self, log):
        super().__init__(log)
        self.other_message = self._message

    def validate(self):
        return True
