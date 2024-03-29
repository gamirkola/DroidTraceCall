from strace_utils import StraceUtils
from probe_source import *
from config.get_config import config as cfg
import requests
from bs4 import BeautifulSoup
import re
import wget
from os import path, remove

class ProbeBuilder:

    def __init__(self):
        self.script_shabang = android_shabang
        self.logging_dir = ''
        self.strace_script = ''
        self.logcat_script = ''
        self.pstree_script = ''
        self.top_script = ''
        self.tools = ''
        self.strace_utils = StraceUtils()



    def busy_box_download(self):
        download_busybox = input("Busybox must be pushed to the phone to execute some of the tools, do you want to do it now? (Y/n) ") or 'y'
        if download_busybox == 'y':
            if path.exists('../tools/busybox/busybox-armv8l'):
                remove_busybox = input('It looks like you already have a busybox bin, do you want to download it again? (y/N) ')
                if remove_busybox:
                    remove("../tools/busybox/busybox-armv8l")
                else:
                    return True
            print('Downloading the latest version of busybox...')
            busybox_binaries_url = 'https://busybox.net/downloads/binaries/'
            busybox_binaries_page = requests.get(busybox_binaries_url)
            bin_soup = BeautifulSoup(busybox_binaries_page.content, 'html.parser')
            multiarch_url = bin_soup.find_all(href=re.compile("defconfig"))
            latest_multiarch = multiarch_url[len(multiarch_url) - 1]
            wget.download(busybox_binaries_url + latest_multiarch['href'] + 'busybox-armv8l', '../tools/busybox/busybox-armv8l')
            return True

    def busybox_push(self, device):
        try:
            busybox_push = input("[+] Do you want to push the busybox executable to the phone? (Y/n): ") or 'y'
            if busybox_push == 'y':
                if cfg.probe['intermediary_folder_path'] is None:
                    print('[*] Pushing busybox to /{}/DroidTraceCall'.format(cfg.probe['probe_folder_path']))
                    device.push('../tools/busybox/busybox-armv8l', '/{}/DroidTraceCall/busybox-armv8l'.format(cfg.probe['probe_folder_path']))
                    print('[*] Making busybox bin executable...')
                    device.shell('chmod +x /{}/DroidTraceCall/busybox-armv8l'.format(cfg.probe['probe_folder_path']))
                    return True
                else:
                    print('[*] Pushing busybox to /{}/DroidTraceCall'.format(cfg.probe['intermediary_folder_path']))
                    device.push('../tools/busybox/busybox-armv8l', '/{}/DroidTraceCall/busybox-armv8l'.format(cfg.probe['intermediary_folder_path']))
                    print('[*] Making busybox bin executable...')
                    device.shell('chmod +x /{}/DroidTraceCall/busybox-armv8l'.format(cfg.probe['intermediary_folder_path']))
                    return True
        except Exception as e:
            print('Error: {}'.format(e))
            return False

    def split_strace_logs_push(self, device):
        try:
            split_logs_push = input("[+] Do you want to push the split_strace_logs executable to the phone? (Y/n): ") or 'y'
            if split_logs_push == 'y':
                if cfg.probe['intermediary_folder_path'] is None:
                    print('[*] Pushing split_strace_logs to /{}/DroidTraceCall'.format(cfg.probe['probe_folder_path']))
                    device.push('../tools/strace/split_log/split_logs', '/{}/DroidTraceCall/split_logs'.format(cfg.probe['probe_folder_path']))
                    print('[*] Making busybox bin executable...')
                    device.shell('chmod +x /{}/DroidTraceCall/split_logs'.format(cfg.probe['probe_folder_path']))
                    return True
                else:
                    print('[*] Pushing split_strace_logs to /{}/DroidTraceCall'.format(cfg.probe['intermediary_folder_path']))
                    device.push('../tools/strace/split_log/split_logs', '/{}/DroidTraceCall/split_logs'.format(cfg.probe['intermediary_folder_path']))
                    print('[*] Making busybox bin executable...')
                    device.shell('chmod +x /{}/DroidTraceCall/split_logs'.format(cfg.probe['intermediary_folder_path']))
                    return True
        except Exception as e:
            print('Error: {}'.format(e))
            return False

    def strace_build(self):
        strace_compile = input("[+] Do you want to compile the strace executable? (y/N): ")
        if strace_compile == 'y':
            self.strace_utils.compile_strace()
            return True

    def tool_to_use(self, probe_tools):
        if probe_tools:
            self.tools = probe_tools
            if '1' in probe_tools:
                self.strace_build()
                self.logging_dir = self.logging_dir + create_if_not_strace_logs_dir
            if '2' in probe_tools:
                #include logcat
                self.logging_dir = self.logging_dir + create_if_not_logcat_logs_dir
            if '3' in probe_tools:
                # include top
                self.logging_dir = self.logging_dir + create_if_not_top_logs_dir
            if '4' in probe_tools:
                # include pstree
                self.logging_dir = self.logging_dir + create_if_not_pstree_logs_dir

    def set_strace_tool(self, attaching_method, syscalls, include_pstree, strace_20sec_loop_script):
        if '2' in attaching_method:
            self.strace_script = create_package_file
            self.strace_script = self.strace_script + while_on_packages(syscalls, include_pstree, strace_20sec_loop_script)
            return True
        if '1' in attaching_method:
            self.strace_script = get_all_pids
            self.strace_script = self.strace_script + while_on_all_pids(syscalls, include_pstree, True, strace_20sec_loop_script)
            return True

    #todo add controls on failed scripts
    def probe_build(self):
        strace_window_script = False
        if '1' in self.tools:
            strace_attaching = input('[+] Do you what strace to be attached to (select 1 or 2):\n\t[1] All the processes\n\t[2] Only to the installed packages\n>')
            strace_syscalls = input('[+] Insert the syscalls you want to trace (memory,network,ipc,file), type "all" for all the calls: ' )
            strace_window =  input('[+] Do you want to run strace for a determined time (y/N)? ' )
            strace_20sec_loop = input('[+] Do you want to save strace logs every 20 seconds in different timestamped folders? (y/N)? ' )
            if strace_window == 'y':
                time = input('[+] Insert the running time in sec (e.g. 5,50...) or minutes (e.g. 5m...): ')
                strace_window_script = strace_time_window(time)
            else:
                strace_window_script = False
            if strace_20sec_loop == 'y':
                strace_20sec_loop_script = True
            else:
                strace_20sec_loop_script = False
            if strace_attaching and strace_syscalls:
                include_pstree = True if '4' in self.tools else False
                strace_set = self.set_strace_tool(strace_attaching, strace_syscalls, include_pstree, strace_20sec_loop_script)
        if '2' in self.tools:
            logcat_buffers = input('[+] Insert the buffers you want to log (radio,events,system,main), type "all" for all the buffers: ')
            logcat_format = input('[+] Insert logcat format options: ')
            self.logcat_script = logcat(logcat_buffers, logcat_format)
        if '3' in self.tools:
            seconds = input('[+] Insert top logging interval in sec (e.g. 5,50...): ')
            self.top_script = top_loop(seconds)
        if self.tools != '':
            with open('../scripts/probe/probe.sh', 'w') as probe_script:
                probe_script.write(self.script_shabang + self.logging_dir + self.logcat_script + self.strace_script +( strace_window_script if strace_window_script else '') + self.top_script)
        else:
            print('Error in generating strace script!')

    def push_tools(self, device):
        if '1' in self.tools:
            self.strace_utils.push_strace(device)
            self.split_strace_logs_push(device)
        if path.exists('../tools/busybox/busybox-armv8l'):
            self.busybox_push(device)

    def probe_start(self, device):
        if cfg.probe['intermediary_folder_path'] is None:
            device.shell("su -c 'cd /{}/DroidTraceCall && nohup ./probe.sh > /dev/null &'".format(cfg.probe['probe_folder_path']), 9999, 9999)
        else:
            print('[*] Moving DroidTraceCall folder to data...')
            try:
                device.shell('mount -o rw,remount /')
                device.root()
            except:
                print("[!] Cannot grant root permissions!")
            device.shell('cp -r /{0}/DroidTraceCall /{1}/DroidTraceCall'.format(cfg.probe['intermediary_folder_path'],cfg.probe['probe_folder_path']))
            device.shell('chmod +x /{}/DroidTraceCall/strace'.format(cfg.probe['probe_folder_path']))
            device.shell('chmod +x /{}/DroidTraceCall/probe.sh'.format(cfg.probe['probe_folder_path']))
            device.shell("su -c 'cd /{}/DroidTraceCall && nohup ./probe.sh > /dev/null &'".format(cfg.probe['probe_folder_path']), 9999, 9999)
        a = input('[*] Press q to stop the probe: ')
        if a == 'q':
            print('[*] Killing the probe...')
            device.shell('pkill -f strace')
            print('[*] Probe killed')

    def probe_push(self,device):
        #after all the tools are configured start to build the probe.
        print('[*] Initialaizing probe build steps...')
        print('[*] Making the filesystem writable...')
        device.shell('mount -o rw,remount /')
        if cfg.probe['intermediary_folder_path'] is None:
            print('[*] Pushing probe to /{}/DroidTraceCall...'.format(cfg.probe['probe_folder_path']))
            device.push('../scripts/probe/probe.sh', '/{}/DroidTraceCall/probe.sh'.format(cfg.probe['probe_folder_path']))
            print('[*] Making probe script executable...')
            device.shell('chmod +x /{}/DroidTraceCall/probe.sh'.format(cfg.probe['probe_folder_path']))
        else:
            print('[*] Pushing probe to /{}/DroidTraceCall...'.format(cfg.probe['intermediary_folder_path']))
            device.push('../scripts/probe/probe.sh', '/{}/DroidTraceCall/probe.sh'.format(cfg.probe['intermediary_folder_path']))

