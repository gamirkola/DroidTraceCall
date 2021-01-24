#!/usr/bin/env python

"""
main.py
====================================
The core module of DroidTraceCall from here at the moment you can
proceed compiling strace from the source for arm64 architecture in order to be able to install it on a phone and start
a configurable probe that saves the logs as you want it to be ;)
"""

from pyfiglet import figlet_format
import subprocess
from adb_utils import AdbUtils


if __name__ == '__main__':
    #prints the name of the app
    print(figlet_format('D r o i d  T r a c e  C a l l', font='slant'))
    adb_utils = AdbUtils()
    #todo check if adb is already running alse kill it
    #os.system('adb kill-server')

    strace_compile = input("[+] Do you want to compile the strace executable? (y/N): ")
    if strace_compile == 'y':
        # launch strace compile script
        subprocess.run('./compile_strace_aarch64.sh', shell=True, cwd='./scripts/strace/')

    device = adb_utils.connect_device()

    print('[*] Granting root permissions on the device...')
    device.root()

    strace_push = input("[+] Do you want to push the strace executable to the phone? (y/N): ")
    if strace_push == 'y':
        print('[*] Pushing strace to /data/DroidTraceCall/')
        device.push('./tools/strace/strace', '/data/DroidTraceCall/strace')
        print('[*] Making strace bin executable...')
        device.shell('chmod +x /data/DroidTraceCall/strace')

    probe_push = input("[+] Do you want to push the probe to the device? (Y/n): ") or 'y'
    if probe_push == 'y':
        #after all the tools are configured start to build the probe.
        print('[*] Initialaizing probe build steps...')
        print('[*] Making the filesystem writable...')
        device.shell('mount -o rw,remount /')
        #at the moment only the strace test probe is pushed
        print('[*] Pushing probe to the device...')
        device.push('./scripts/probe/strace_all_proc.sh', '/data/DroidTraceCall/strace_all_proc.sh')
        print('[*] Making probe script executable...')
        device.shell('chmod +x /data/DroidTraceCall/strace_all_proc.sh')

    probe_start = input("[+] Do you want to start the probe now? (Y/n): ") or 'y'
    if probe_start == 'y':
        device.shell("su -c 'cd /data/DroidTraceCall/ && nohup ./strace_all_proc.sh > /dev/null &'", 9999, 9999)
        a = input('[*] Press a key to stop the probe: ')
        if a:
            device.shell('pkill -f strace')

    pull_logs = input("[+] Do you want to pull the logs? (y/n): ")
    if pull_logs == 'y':
        device.pull('/data/DroiTraceCall/logs.gz', 'logs.gz')