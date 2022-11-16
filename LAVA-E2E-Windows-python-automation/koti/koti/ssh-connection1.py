import paramiko
from subprocess  import STDOUT

#command = "lavacli --uri http://admin:es3bkjwhjo04oazzl0zqhl7zfr2n8wf1eg3zl246o9gspyyi2pczdsotmufgyc00yzkjuz6o0pl28mymjz7he980artaysb7hj4h4r5tia1u2f3y3ecf94ys1ye32ns0@192.168.3.106/RPC2/ jobs submit /home/equser/koti/lava-testcases/e2e/edgeq-raptor2_e2e_gnb_cellup_board41.yaml"
command="echo hai >> /dev/nell | echo returnkoti"

# Update the next three lines with your
# server's information

host = "192.168.3.106"
username = "equser"
password = "Password$2021"

client = paramiko.client.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, username=username, password=password)
#_stdin, _stdout,_stderr = client.exec_command("lavacli --uri http://admin:es3bkjwhjo04oazzl0zqhl7zfr2n8wf1eg3zl246o9gspyyi2pczdsotmufgyc00yzkjuz6o0pl28mymjz7he980artaysb7hj4h4r5tia1u2f3y3ecf94ys1ye32ns0@192.168.3.106/RPC2/ jobs submit /home/equser/koti/lava-testcases/e2e/edgeq-raptor2_e2e_gnb_cellup_board41.yaml"")
_stdin, _stdout,_stderr = client.exec_command(command)
out = _stdout.read().decode()
print(out)
client.close()