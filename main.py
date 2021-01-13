#!/usr/bin/env python

import os
from pyfiglet import figlet_format
import subprocess
strace_repo = 'https://github.com/strace/strace'
strace_dir = 'tools/strace/strace_repo/'

if __name__ == '__main__':

    #prints the name of the app
    f = figlet_format('D r o i d  T r a c e  C a l l', font='slant')
    print(f)


    strace_compile = input("[+] Do you want to compile the strace executable? (y/n): ")
    if strace_compile == 'y':
        #launch strace compile script
        subprocess.call('./scripts/strace/compile_strace_64bit.sh')




    see_connected_devices = input("[+] Do you want to verify if there are device connected? (y/n): ")
    if see_connected_devices == 'y':
        os.system('adb devices')
