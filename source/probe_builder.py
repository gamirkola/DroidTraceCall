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
            strace_attaching = input('[+] Do you what strace to be attached to (select 1 or 2):\n [1] All the processes\n[2] Only to the installed packages\n>')
            strace_syscalls = input('[+] Insert the syscalls you want to trace (memory,network,ipc,file), type "all" for all the calls: ' )
            if strace_attaching and strace_syscalls:
                strace_set = self.set_strace_tool(strace_attaching, strace_syscalls)
                if strace_set:
                    with open('../scripts/probe/probe.sh', 'w') as probe_script:
                        probe_script.write(self.script_shabang + self.logging_dir + self.probe_script)

    def push_tools(self, device):
        if '1' in self.tools:
            self.strace_utils.push_strace(device)

    def probe_start(self, device):
        device.shell("su -c 'cd /data/{}/DroidTraceCall && nohup ./strace_all_proc.sh > /dev/null &'".format(cfg.probe['probe_folder_path']), 9999, 9999)
        a = input('[*] Press Enter to stop the probe: ')
        if a:
            device.shell('pkill -f strace')

