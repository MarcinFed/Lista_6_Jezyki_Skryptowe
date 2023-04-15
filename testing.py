from lab_2 import OtherSSHLogEntry, ErrorSSHLogEntry, AcceptedPasswordSSHLogEntry, RejectedPasswordSSHLogEntry
from lab_1 import SSHLogEntry
from lab_7 import SSHLogJournal
from ipaddress import IPv4Address

if __name__ == "__main__":
    journal = SSHLogJournal()
    first_log = AcceptedPasswordSSHLogEntry(
        "Dec 10 09:32:20 LabSZ sshd[24680]: Accepted password for user fztu from 119.137.62.142 port 49116 ssh2")
    second_log = RejectedPasswordSSHLogEntry(
        "Dec 10 07:07:45 LabSZ sshd[24206]: Failed password for invalid user test9 from 52.80.34.196 port 36060 ssh2")
    third_log = ErrorSSHLogEntry(
        "Dec 10 11:03:44 LabSZ sshd[25455]: error: Received disconnect from 103.99.0.122: 14: No more user authentication methods available. [preauth]")
    fourth_log = OtherSSHLogEntry("Dec 10 07:11:42 LabSZ sshd[24224]: pam_unix(sshd:auth): check pass; user unknown")

    journal.append(first_log)
    journal.append(second_log)
    journal.append(third_log)
    journal.append(fourth_log)

    print(journal.get_log_by_index(0))
    print(journal.get_logs_by_ipv4(IPv4Address("103.99.0.122")))
    print(journal.get_logs_by_host_name("LabSZ"))

    print(journal.get_log_by_index(0).__gt__(journal.get_log_by_index(1)))
    print(journal.get_log_by_index(0).__eq__(journal.get_log_by_index(1)))
    print(journal.get_log_by_index(0).__eq__(journal.get_log_by_index(0)))
    print(journal.get_log_by_index(0).__lt__(journal.get_log_by_index(1)))
    print(journal.get_log_by_index(0).has_ip)
    print(journal.get_log_by_index(3).has_ip)