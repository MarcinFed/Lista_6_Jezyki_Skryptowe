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
USER_NAME_PATTERN =  r"(?<=user )\w+"
ERROR_PATTERN = r"error: (.+?) \["
IPV4_PATTERN = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
TIMESTAMP_FORMAT = "%b %d %H:%M:%S"


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
        raise Exception("No match in log line!")


def get_user_name(message):
    return re.findall(USER_NAME_PATTERN, message)[0]


def get_error_msg(message):
    return re.findall(ERROR_PATTERN, message)[0]
