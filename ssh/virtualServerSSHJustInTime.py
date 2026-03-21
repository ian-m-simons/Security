import os 
from datetime import datetime, timedelta
import subprocess
import random

time = datetime.now()

since = time.strftime("%Y-%m-%d %H:%M:%S")

timeout=time + timedelta(minutes=1)
print(time)
print(timeout)

data = os.popen("journalctl --since \"" + since + "\" | grep sshd | grep \"Accepted\"").read()
detected = False
command = ["sudo", "systemctl", "restart", "ssh"]
os.system("sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak")
with open("/etc/ssh/sshd_config", 'r') as file:
    lines = file.readlines()
port = str(random.randint(1025,65534))
lines[13]="port " + port + "\n"

for i in range(len(lines)):
    if "port 22" in lines[i].lower():
        lines[i] = "port "+ port+"\n"
    if "passwordauthentication " in lines[i].lower():
        lines[i] = "PasswordAuthentication no\n"
    if "pubkeyauthentication " in lines[i].lower():
        lines[i] = "PubkeyAuthentication yes\n"
    if "permitrootlogin " in lines[i].lower():
        lines[i] = "PermitRootLogin no\n"
    if "usepam " in lines[i].lower():
        lines[i] = "UsePAM no\n"
with open("/etc/ssh/sshd_config", 'w') as file:
    file.writelines(lines)

with open("/home/ian/testsshd_config", 'w') as file:
    file.writelines(lines)

try:
    subprocess.run(command, check=True)
    print("ssh opened on port " + port + " please complete login(timeout in 1 minute)")
except subprocess.CalledProcessError as e:
    print("command failed: " + str(e.stderr))

while (detected != True and time < timeout):
    data = os.popen("journalctl --since \"" + since + "\" | grep sshd | grep \"Accepted\"").read()
    if data != "":
        detected = True
    
    time = datetime.now()
command[2] = "stop"
subprocess.run(command)
if detected:
    print("login detected, SSH closed")
else:
    print("timedout, SSH closed")

os.system("sudo cp /etc/ssh/sshd_config.bak /etc/ssh/sshd_config")
os.system("sudo rm /etc/ssh/sshd_config.bak")
