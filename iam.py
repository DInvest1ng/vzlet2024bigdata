import subprocess
import json
from datetime import datetime
import datetime as dt
import config

def write():
    process = subprocess.Popen(config.bash_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    response_data = json.loads(stdout.decode())
    with open("iam.json", "w") as f:
        json.dump(response_data, f)

def check():
    with open("iam.json", "r") as f:
        data = json.load(f).get("expiresAt")[:16]
        data = datetime.strptime(data, "%Y-%m-%dT%H:%M")

    if datetime.now().replace(second=0, microsecond=0) > data+ dt.timedelta(hours=3):
        write()

    with open("iam.json", "r") as f:
        return json.load(f).get("iamToken")