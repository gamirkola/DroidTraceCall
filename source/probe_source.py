#todo insert logging dirs as configs
android_shabang = '#!/system/bin/sh\n'
bash_shabang = '#!/bin/bash \n'
create_if_not_strace_logs_dir = 'if [ ! -d ./strace_logs ];then\n\tmkdir strace_logs\nfi\n'
create_package_file = 'touch package.txt\npm list packages > package.txt\ninput="package.txt"\n'
while_on_packages = lambda syscalls:"""\nwhile IFS= read -r line
do
  TARGET_PACKAGE=`echo $line | cut -d':' -f2`
  PID=`echo $(pidof $TARGET_PACKAGE)`
  if [ ! -z "$PID" ]; then
      UID=`echo $(ps -o user= -p $PID | xargs id -u )`
      """ + getAllStrace(syscalls) + """
  fi
done < "$input"
"""

strace_time_window = lambda time: 'sleep ' + time + ' && pkill -f strace'

create_if_not_logcat_logs_dir = 'if [ ! -d ./logcat_logs ];then\n\tmkdir logcat_logs\nfi\n'
logcat = lambda buffers,format: 'logcat -b ' + buffers + ' -v ' + format + ' -d > ./logcat_logs/logcat_log.out\n'


def getEnterAsChar():
    # you can use \\n too
    return "\n".encode("unicode_escape").decode("utf-8")

#little work arounf for makins trace traceall the system calls
def getAllStrace(syscalls):
    if syscalls == 'all':
        return './strace -f -t -p $PID -s 9999 -o ./strace_logs/$PID-$UID-$TARGET_PACKAGE.out &>/dev/null &'
    else:
        return './strace -f -t -e trace=' + syscalls + ' -p $PID -s 9999 -o ./strace_logs/$PID-$UID-$TARGET_PACKAGE.out &>/dev/null &'