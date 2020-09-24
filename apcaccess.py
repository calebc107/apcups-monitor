import subprocess
import time

def poll():
    command = "apcaccess"
    command = command.split(' ')
    proc = subprocess.Popen(command,stdout=subprocess.PIPE)
    lines=proc.stdout.readlines() #output.split('\n')
    lines = [line.decode("utf-8").split(":",1) for line in lines]
    status_dict = {key.strip():value.strip() for key,value in lines}
    return status_dict

def watch(onBattCallback):
    while True:
        status = poll()
        secs_on_batt = float(status['TIMEONBAT'].split(' ')[0])
        if secs_on_batt > 0:
            onBattCallback()
        time.sleep(1)
