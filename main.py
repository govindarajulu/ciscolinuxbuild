#!/usr/bin/python2
import paramiko
import sys

cmd = "cd /mnt/archkvm/svn/rxhash/palo_enic_linux_esx_main/sa/src/palo/drivers/enic/linux/ 2>&1;\
       echo FAILED > /tmp/govind_enicbuildstatus 2>&1;\
       make -f Makefile.outer 2>&1 && echo SUCCESS > /tmp/govind_enicbuildstatus 2>&1;\
       cat /tmp/govind_enicbuildstatus"

table = [ ["10.106.186.201", "root", "root", cmd, "rhel 6.2"],
	  ["10.106.186.200", "root", "root", cmd, "rhel 6.3"],
	  ["10.106.186.199", "root", "root", cmd, "rhel 6.1"],
	  ["10.106.186.195", "root", "root", cmd, "rhel 6.4"],
	  ["10.106.186.194", "root", "root", cmd, "rhel 5.9"],
	  ["10.106.186.193", "root", "root", cmd, "sles 11 sp2"],
	  ["10.106.186.192", "root", "root", cmd, "sles 11 sp3"],
	  ["10.106.186.191", "root", "root", cmd, "rhel 7.0"],
	  ["10.106.186.197", "root", "root", cmd, "OVM sdk 3.2.1"],
	  ["10.106.186.198", "root", "root", cmd, "OVM sdk 3.1.1"]
	  ]

def ssh_action(client):
	f = open(client[0]+".log", "w")
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(client[0], username=client[1], password=client[2])
	sys.stdout.write(client[0] + " " + client[4] + " : ")
	sys.stdout.flush()
	stdin, stdout, stderr = ssh.exec_command(client[3])
	for i in stdout.readlines():
		f.write(i)
	stdin, stdout, stderr = ssh.exec_command("cat /tmp/govind_enicbuildstatus")
	print stdout.readlines()[0]
	ssh.close()
	f.close()

for entry in table:
	ssh_action(entry)
