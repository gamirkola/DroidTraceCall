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
from config.get_config import config as cfg

if __name__ == '__main__':
    #prints the name of the app
    print(figlet_format('D r o i d  T r a c e  C a l l', font='slant'))
    adb_utils = AdbUtils()
    probe_builder = ProbeBuilder()
    device = False
    #todo check if adb is already running alse kill it
    #os.system('adb kill-server')

    connect_device = input("[+] Do you want to connect the device? (Y/n): ") or 'y'
    if connect_device == 'y':
        device = adb_utils.connect_device()

    probe_tools = input("[+] Insert the numbers of the tools that you want to include into the probe in the following syntax (1,2...): \nTools avaiable: \n\t[1] Strace\n\t[2] Logcat\n\t[3] Top\n>")
    if probe_tools:
        probe_builder.tool_to_use(probe_tools)
        probe_builder.probe_build()

    if device:
        #first phone configs
        print('[*] Granting root permissions on the device...')
        try:
            device.root()
        except:
            print("[!] Cannot grant root permissions!")
        print('[*] Creating probe folder...')
        if cfg.probe['intermediary_folder_path'] is None:
            device.shell('mkdir /{}/DroidTraceCall'.format(cfg.probe['probe_folder_path']))
        else:
            device.shell('mkdir /{}/DroidTraceCall'.format(cfg.probe['intermediary_folder_path']))

    if device:
        probe_builder.push_tools(device)

        probe_push = input("[+] Do you want to push the probe to the device? (Y/n): ") or 'y'
        if probe_push == 'y':
            probe_builder.probe_push(device)

        probe_start = input("[+] Do you want to start the probe now? (Y/n): ") or 'y'
        if probe_start == 'y':
            probe_builder.probe_start(device)

        # pull_logs = input("[+] Do you want to pull the logs? (y/n): ")
        # if pull_logs == 'y':
        #     device.pull('/data/DroidTraceCall/logs', '')