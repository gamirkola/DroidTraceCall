#!/usr/bin/env python

import os
from pathlib import Path
from pyfiglet import figlet_format
import subprocess
from adb_shell.adb_device import AdbDeviceUsb, AdbDeviceTcp
from adb_shell.auth.sign_pythonrsa import PythonRSASigner


# Load the public and private keys
def adb_key():
    custom_path = input('[+] Do you want to insert a custom adb key path (y/n)?')
    if custom_path == 'y':
        path = input('[*] Insert the adb key file path: ')
        if path:
            adbkey = path
        else:
            print('[*] Path invalid')
    if custom_path == 'n':
        adbkey = str(Path.home()) + '/.android/adbkey'
    print('[*] Adb key path: ' + adbkey)
    if not os.path.exists(adbkey):
        print('[!] Error retrieving the file')
        exit(1)
    with open(adbkey) as f:
        priv = f.read()
    with open(adbkey + '.pub') as f:
        pub = f.read()
    return PythonRSASigner(pub, priv)

# define the function blocks
def tcp():
    #get adb key
    signer = adb_key()
     # Connect
    ip = input('[+] Insert the device IP:')
    device = AdbDeviceTcp(ip, 5555, default_transport_timeout_s=9.)
    device.connect(rsa_keys=[signer], auth_timeout_s=0.1)
    # Send a shell command
    if device.available:
        print('[*] Device connected!')
        return device
    else:
        print('[!] Error in connecting the device')
        return False

def usb():
    #get adb key
    signer = adb_key()
    # Connect via USB
    device = AdbDeviceUsb()
    device.connect(rsa_keys=[signer], auth_timeout_s=0.1)
    if device.available:
        print('[*] Device connected!')
        return device
    else:
        print('[!] Error in connecting the device')
        return False

# connection options
conn_options = {1: tcp, 2: usb}


if __name__ == '__main__':
    #prints the name of the app
    print(figlet_format('D r o i d  T r a c e  C a l l', font='slant'))
    #todo check if adb is already running alse kill it
    # os.system('adb kill-server')

    strace_compile = input("[+] Do you want to compile the strace executable? (y/n): ")
    if strace_compile == 'y':
        # launch strace compile script
        subprocess.run('./compile_strace_aarch64.sh', shell=True, cwd='./scripts/strace/')

    connect_device = input("[+] Do you want to connect the device? (y/n): ")
    if connect_device == 'y':

        print("[!] Please select \"Always allow from this computer\" in the adb dialog!")
        conn_type = input("[+] Select ADB connection method: \n\t[1] TCP \n\t[2] USB \n")
        if conn_type:
            connect = conn_options.get(int(conn_type), '[!] Invalid option')
            if isinstance(connect, str):
                print(connect)
            else:
                device = connect()

    strace_push = input("[+] Do you want to push the strace executable to the phone? (y/n): ")
    if strace_push == 'y':
        print('[*] Granting root permissions on the device...')
        device.root()
        print('[*] Pushing strace to /data/DroidTraceCall/')
        device.push('./tools/strace/strace', '/data/DroidTraceCall/strace')
        print('[*] Making strace bin executable...')
        device.shell('chmod +x /data/DroidTraceCall/strace')


    probe_push = input("[+] Do you want to push the probe to the device? (y/n): ")
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

    probe_start = input("[+] Do you want to start the probe now? (y/n): ")
    if probe_start == 'y':
        device.shell('./data/DroidTraceCall/strace_all_proc.sh')

