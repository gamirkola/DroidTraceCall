#!/usr/bin/env python

import os
from pyfiglet import figlet_format
import subprocess


if __name__ == '__main__':

    #prints the name of the app
    f = figlet_format('D r o i d  T r a c e  C a l l', font='slant')
    print(f)

    see_connected_devices = input("[+] Do you want to verify if there are device connected? (y/n): ")
    if see_connected_devices == 'y':
        os.system('adb devices')
        print("[!] Please select \"Always allow from this computer\" in the adb dialog!")

    strace_compile = input("[+] Do you want to compile the strace executable? (y/n): ")
    if strace_compile == 'y':
        #launch strace compile script
        subprocess.run('./compile_strace_aarch64.sh', shell=True, cwd='./scripts/strace/')

    strace_push = input("[+] Do you want to push the strace executable to the phone? (y/n): ")
    if strace_push == 'y':
        #launch strace compile script
        print('[*] Gaining root permissions...')
        os.system('adb root')
        print('[*] Pushing strace to /data/DroidTraceCall/')
        os.system('adb push ./tools/strace/strace /data/DroidTraceCall/strace')


