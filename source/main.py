#!/usr/bin/env python

"""
main.py
====================================
The core module of DroidTraceCall from here at the moment you can
proceed compiling strace from the source for arm64 architecture in order to be able to install it on a phone and start
a configurable probe that saves the logs as you want it to be ;)
"""

from pyfiglet import figlet_format
from adb_utils import AdbUtils
from probe_builder import ProbeBuilder


if __name__ == '__main__':
    #prints the name of the app
    print(figlet_format('D r o i d  T r a c e  C a l l', font='slant'))
    adb_utils = AdbUtils()
    probe_builder = ProbeBuilder()
    #todo check if adb is already running alse kill it
    #os.system('adb kill-server')

    connect_device = input("[+] Do you want to connect the device? (Y/n): ") or 'y'
    if connect_device == 'y':
        device = adb_utils.connect_device()

    print('[*] Granting root permissions on the device...')
    device.root()

    probe_tools = input("[+] Insert the numbers of the tools that you want to include into the probe in the following syntax (1,2...): \nTools avaiable: \n [1] Strace\n>")
    if probe_tools:
        probe_builder.tool_to_use(probe_tools)

    probe_builder.push_tools(device)
    probe_builder.probe_build()

    # probe_start = input("[+] Do you want to start the probe now? (Y/n): ") or 'y'
    # if probe_start == 'y':
    #     device.shell("su -c 'cd /data/DroidTraceCall/ && nohup ./strace_all_proc.sh > /dev/null &'", 9999, 9999)
    #     a = input('[*] Press a key to stop the probe: ')
    #     if a:
    #         device.shell('pkill -f strace')
    #
    # pull_logs = input("[+] Do you want to pull the logs? (y/n): ")
    # if pull_logs == 'y':
    #     device.pull('/data/DroidTraceCall/logs', '')