import paramiko
from time import sleep
import datetime
import sys
from os.path import exists

isFile = exists ("queueInfo.csv")

if (isFile == False):
    with open ("queueInfo.csv", "w") as newFile:
        newFile.write ("Time, small8, small20, small40, medium, long, verylong, large, gpuq\n")

if len (sys.argv) != 3:
    print ("\nWARNING: Incorrect number of args passed.\n~~~~~~~~\n\nREQUIRED ARGUMENTS:\n~~~~~~~~~~~~~~~~~~~\n\nargv[0] = program\nargv[1] = username\nargv[2] = password\n\nEXAMPLE: python ./checkQueues ic34946 secretPassword\n~~~~~~~~\n")
    exit(1)

while (1):
    ip_hpce = "10.24.6.200"
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip_hpce, username = sys.argv[1], password = sys.argv[2], look_for_keys = False)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("qstat")

    now = datetime.datetime.utcnow()+datetime.timedelta(hours = 0, minutes = 0)

    nJobs_small8 = 0
    nJobs_small20 = 0
    nJobs_small40 = 0
    nJobs_medium = 0
    nJobs_long = 0
    nJobs_verylong = 0
    nJobs_large = 0
    nJobs_gpuq = 0

    for line in ssh_stdout:
        if (".hn1" in line and " R " in line and "small8" in line):
            nJobs_small8 += 1
        if (".hn1" in line and " R " in line and "small20" in line):
            nJobs_small20 += 1
        if (".hn1" in line and " R " in line and "small40" in line):
            nJobs_small40 += 1
        if (".hn1" in line and " R " in line and "medium" in line):
            nJobs_medium += 1
        if (".hn1" in line and " R " in line and "long" in line):
            nJobs_long += 1
        if (".hn1" in line and " R " in line and "verylong" in line):
            nJobs_verylong += 1
        if (".hn1" in line and " R " in line and "large" in line):
            nJobs_large += 1
        if (".hn1" in line and " R " in line and "gpuq" in line):
            nJobs_gpuq += 1

    print ("\nnJobs_small8: ", nJobs_small8, "\nnJobs_small20: ", nJobs_small20, "\nnJobs_small40: ", nJobs_small40, "\nnJobs_medium: ",  nJobs_medium, "\nnJobs_long: ", nJobs_long, "\nnJobs_verylong: ", nJobs_verylong, "\nnJobs_large: ", nJobs_large, "\nnJobs_gpuq: ", nJobs_gpuq)

    with open ("queueInfo.csv", "a") as outputFile:
        outputFile.write ("{}, {}, {}, {}, {}, {}, {}, {}, {}\n".format (now, nJobs_small8, nJobs_small20, nJobs_small40, nJobs_medium, nJobs_long, nJobs_verylong, nJobs_large, nJobs_gpuq))

    ssh.close ()

    # checks all the queues every 6 hours
    sleep (21600)