import json
import random
from datetime import datetime
import pytz
import hashlib
import sys

class SHAUtils(object):
    @staticmethod
    def sha_string(string):
        """
        Hashes the provided string using the SHA-256 algorithm.
        :param string: String to hash.
        :type string: string
        :return: SHA-256 hashed string.
        :rtype: string
        """
        return hashlib.sha256(string.encode("utf-8")).hexdigest()

    @classmethod
    def stringify_dict(cls, d):
        """
        Converts a dict to a JSON string.
        Dictionaries with the same (key, value) pairs are guaranteed to serialize to the same string,
        irrespective of the order in which the keys were added.
        :param d: Dictionary to convert to JSON.
        :type d: dict
        :return: JSON serialization of the given dict.
        :rtype: string
        """
        return json.dumps(d, sort_keys=True)

    @classmethod
    def sha_dict(cls, d):
        """
        Hashes the provided dict using the SHA-256 algorithm.
        :param d: Dictionary to hash.
        :type d: dict
        :return: SHA-256 hashed dict.
        :rtype: string
        """
        return cls.sha_string(cls.stringify_dict(d))


if (len(sys.argv) != 2):
    print ("Usage python enron_json_to_message.py path_to_data")
    exit(1)

f = open(sys.argv[1])

msgs = []
i = 0

for ln in f:
    message = json.loads(ln)
    sender = message["sender"]
    text = message["text"]
    subject = message["subject"]

    lines = text.split("\n")
    lines = lines[0:5]
    text = "\n".join(lines)
    
    msgs.append(
        {
            "MessageID" : "{}".format(SHAUtils.sha_string(str(text))),
            "Text" : str(text),
            "CreationDateTimeUTC" : pytz.utc.localize(datetime.utcnow()).isoformat(timespec="microseconds"),
            "Labels" : [],
            "SequenceNumber" : i
        }
    )
    i += 1

print (json.dumps(msgs, ensure_ascii=True, indent=2))




