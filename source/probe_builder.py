from strace_utils import StraceUtils
from probe_source import android_shabang, create_if_not_logs_dir, create_package_file, while_on_packages
from config.get_config import config as cfg

class ProbeBuilder:

    def __init__(self):
        self.script_shabang = android_shabang
        self.logging_dir = create_if_not_logs_dir
        self.probe_script = ''
        self.tools = ''
        self.strace_utils = StraceUtils()


    def strace_build(self):
        strace_compile = input("[+] Do you want to compile the strace executable? (y/N): ")
        if strace_compile == 'y':
            self.strace_utils.compile_strace()
            return True

    def tool_to_use(self, probe_tools):
        #at the moment only strace is implemented
        if probe_tools:
            self.tools = probe_tools
            if '1' in probe_tools:
                self.strace_build()
                return True

    def set_strace_tool(self, attaching_method, syscalls):
        if '2' in attaching_method:
            self.probe_script = create_package_file
            self.probe_script = self.probe_script + while_on_packages(syscalls)
            return True
        if '1' in attaching_method:
            return 'not implemented yet'

    def probe_build(self):
        if '1' in self.tools:
            strace_attaching = input('[+] Do you what strace to be attached to (select 1 or 2):\n\t[1] All the processes\n\t[2] Only to the installed packages\n>')
            strace_syscalls = input('[+] Insert the syscalls you want to trace (memory,network,ipc,file), type "all" for all the calls: ' )
            if strace_attaching and strace_syscalls:
                strace_set = self.set_strace_tool(strace_attaching, strace_syscalls)
                if strace_set:
                    with open('../scripts/probe/probe.sh', 'w') as probe_script:
                        probe_script.write(self.script_shabang + self.logging_dir + self.probe_script)

    def push_tools(self, device):
        if '1' in self.tools:
            self.strace_utils.push_strace(device)
    #todo verufy how to work with sd card dir
    def probe_start(self, device):
        if cfg.probe['intermediary_folder_path'] is None:
            device.shell("su -c 'cd /{}/DroidTraceCall && nohup ./probe.sh > /dev/null &'".format(cfg.probe['probe_folder_path']), 9999, 9999)
        else:
            print('[*] Moving DroidTraceCall folder to data...')
            device.shell('cp -r /{0}/DroidTraceCall /{1}/DroidTraceCall'.format(cfg.probe['intermediary_folder_path'],cfg.probe['probe_folder_path']))
            device.shell('chmod +x /{}/DroidTraceCall/strace'.format(cfg.probe['probe_folder_path']))
            device.shell('chmod +x /{}/DroidTraceCall/probe.sh'.format(cfg.probe['probe_folder_path']))
            device.shell("su -c 'cd /{}/DroidTraceCall && nohup ./probe.sh > /dev/null &'".format(cfg.probe['probe_folder_path']), 9999, 9999)
        a = input('[*] Press Enter to stop the probe: ')
        if a:
            device.shell('pkill -f strace')

    def probe_push(self,device):
        #after all the tools are configured start to build the probe.
        print('[*] Initialaizing probe build steps...')
        print('[*] Making the filesystem writable...')
        device.shell('mount -o rw,remount /')
        if cfg.probe['intermediary_folder_path'] is None:
            # at the moment only the strace test probe is pushed
            print('[*] Pushing probe to /{}/DroidTraceCall...'.format(cfg.probe['probe_folder_path']))
            device.push('../scripts/probe/probe.sh', '/{}/DroidTraceCall/probe.sh'.format(cfg.probe['probe_folder_path']))
            print('[*] Making probe script executable...')
            device.shell('chmod +x /{}/DroidTraceCall/probe.sh'.format(cfg.probe['probe_folder_path']))
        else:
            # at the moment only the strace test probe is pushed
            print('[*] Pushing probe to /{}/DroidTraceCall...'.format(cfg.probe['intermediary_folder_path']))
            device.push('../scripts/probe/probe.sh', '/{}/DroidTraceCall/probe.sh'.format(cfg.probe['intermediary_folder_path']))

