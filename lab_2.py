from lab_1 import SSHLogEntry
from tools import get_user_name, get_error_msg


class RejectedPasswordSSHLogEntry(SSHLogEntry):
    def __init__(self, log):
        super().__init__(log)
        self.user_name = get_user_name(self._SSHLogEntry__message)

    def validate(self):
        return "Failed password for invalid user" in self._SSHLogEntry__message


class AcceptedPasswordSSHLogEntry(SSHLogEntry):
    def __init__(self, log):
        super().__init__(log)
        self.user_name = get_user_name(self._SSHLogEntry__message)

    def validate(self):
        return "Accepted password" and "for" and "from" in self._SSHLogEntry__message


class ErrorSSHLogEntry(SSHLogEntry):
    def __init__(self, log):
        super().__init__(log)
        self.error_message = get_error_msg(self._SSHLogEntry__message)

    def validate(self):
        return "Received disconnect from" in self._SSHLogEntry__message


class OtherSSHLogEntry(SSHLogEntry):
    def __init__(self, log):
        super().__init__(log)
        self.other_message = self._SSHLogEntry__message

    def validate(self):
        return True
