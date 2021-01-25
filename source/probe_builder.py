from strace_utils import StraceUtils
import os

script_dir = os.path.dirname(os.path.realpath('__file__'))
# rel_path = "scripts/probe.sh"
# abs_probe_path = os.path.join(script_dir, rel_path)

class ProbeBuilder:

    def __init__(self):
        self.script_shabang = '#!/system/bin/sh \n'
        self.logging_dir = '#create logs dir if it does not exist\n\tif [ ! -d ./logs ];then\n\tmkdir logs\nfi\n'
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
            self.probe_script = '#create package file\ntouch package.txt\n#insert found packages inside the file\npm list packages > package.txt\n#path to the file\ninput="package.txt" '
            self.probe_script = self.probe_script + """\nwhile IFS= read -r line
do
  TARGET_PACKAGE=`echo $line | cut -d':' -f2`
  PID=`echo $(pidof $TARGET_PACKAGE)`
  if [ ! -z "$PID" ]; then
      ./strace -f -t -e trace=""" + syscalls + """  -p $PID -s 9999 -o ./logs/$PID-$TARGET_PACKAGE.out &>/dev/null &
  fi
done < "$input"
            """
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
                    with open(os.path.join(script_dir, 'scripts/probe/probe.sh'), 'w') as probe_script:
                        probe_script.write(self.script_shabang + self.logging_dir + self.probe_script)

    def push_tools(self, device):
        if '1' in self.tools:
            self.strace_utils.push_strace(device)

