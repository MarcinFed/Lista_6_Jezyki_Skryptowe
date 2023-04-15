import re
from lab_7 import SSHLogJournal
from lab_2 import RejectedPasswordSSHLogEntry, AcceptedPasswordSSHLogEntry, ErrorSSHLogEntry, OtherSSHLogEntry

VALIDATE_PATTERN = r"^[a-z_][a-z0-9_-]{0,31}$"


class SSHUser:
    def __init__(self, user_name, last_login):
        self.user_name = user_name
        self.last_login = last_login

    def validate(self):
        if not re.match(VALIDATE_PATTERN, self.user_name):
            raise ValueError("Invalid user_name")
        return True

    def __repr__(self):
        return f"SSHUser (user_name={self.user_name}, last_login={self.last_login})"


if __name__ == "__main__":
    journal = SSHLogJournal()
    first_log = AcceptedPasswordSSHLogEntry("Dec 10 09:32:20 LabSZ sshd[24680]: Accepted password for user fztu from 119.137.62.142 port 49116 ssh2")
    second_log = RejectedPasswordSSHLogEntry("Dec 10 07:07:45 LabSZ sshd[24206]: Failed password for invalid user test9 from 52.80.34.196 port 36060 ssh2")
    third_log = ErrorSSHLogEntry("Dec 10 11:03:44 LabSZ sshd[25455]: error: Received disconnect from 103.99.0.122: 14: No more user authentication methods available. [preauth]")
    fourth_log = OtherSSHLogEntry("Dec 10 07:11:42 LabSZ sshd[24224]: pam_unix(sshd:auth): check pass; user unknown")

    journal.append(first_log)
    journal.append(second_log)
    journal.append(third_log)
    journal.append(fourth_log)

    shared_list = [journal.get_log_by_index(0), journal.get_log_by_index(1), journal.get_log_by_index(2),
                   journal.get_log_by_index(3), SSHUser("test01", "01-01-2001"), SSHUser("test02", "02-02-2002")]

    for elem in shared_list:
        print(elem.validate())