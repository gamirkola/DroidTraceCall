#todo insert logging dirs as configs
#shabangs
android_shabang = '#!/system/bin/sh\n'
bash_shabang = '#!/bin/bash \n'
#strace options
create_if_not_strace_logs_dir = 'if [ ! -d ./strace_logs ];then\n\tmkdir strace_logs\nfi\n'
create_package_file = 'touch package.txt\npm list packages > package.txt\ninput="package.txt"\n'
while_on_packages = lambda syscalls, pstree:"""\nwhile IFS= read -r line
do
  TARGET_PACKAGE=`echo $line | cut -d':' -f2`
  PID=`echo $(pidof $TARGET_PACKAGE)`
  if [ ! -z "$PID" ]; then
      UID=`echo $(ps -o user= -p $PID | xargs id -u )`
      """ + getPsTree(pstree) + """
      """ + getAllStrace(syscalls) + """
  fi
done < "$input"
"""
while_on_all_pids = lambda syscalls, pstree, all_pids:"""\nfor PID in "${ALL_PIDS[@]}"
do
  if [ ! -z "$PID" ]; then
      UID=`echo $(ps -o user= -p $PID | xargs id -u )`
      """ + getPsTree(pstree) + """
      """ + getAllStrace(syscalls, all_pids) + """
  fi
done
"""
strace_time_window = lambda time: 'sleep ' + time + ' && pkill -f strace\n'
# todo make logcat configurable per each app
#logcat options
create_if_not_logcat_logs_dir = 'if [ ! -d ./logcat_logs ];then\n\tmkdir logcat_logs\nfi\n'
logcat = lambda buffers,format: 'logcat -b ' + buffers + ' -v ' + format + ' -d > ./logcat_logs/logcat_log.out\n'

#todo end logcat pid loop
logcat_pid_loop = lambda seconds:"""end=$((SECONDS+"""+ seconds +"""))

while [ $SECONDS -lt $end ]; do
    TIMESTAMP=`echo $(date +"%H_%M_%S")`
    logcat | grep $PID
done"""

#top options
create_if_not_top_logs_dir = 'if [ ! -d ./top_logs ];then\n\tmkdir top_logs\nfi\n'
#to be implemented
# top_per_app = lambda top: ''
# todo make top lines configurable and also packages
global_top = 'top -m 500 -n 1 > ./top_logs/top_log_$TIMESTAMP.txt'
top_loop = lambda seconds:"""end=$((SECONDS+"""+ seconds +"""))

while [ $SECONDS -lt $end ]; do
    TIMESTAMP=`echo $(date +"%H_%M_%S")`
    """+ global_top +"""
done"""

#pstree with busybox
create_if_not_pstree_logs_dir = 'if [ ! -d ./pstree_logs ];then\n\tmkdir pstree_logs\nfi\n'

def getEnterAsChar():
    # you can use \\n too
    return "\n".encode("unicode_escape").decode("utf-8")

#little work around for makins trace traceall the system calls
def getAllStrace(syscalls, all_pids):
    if all_pids:
        if syscalls == 'all':
            return './strace -f -t -p $PID -s 9999 -o ./strace_logs/$UID-$PID.out &>/dev/null &'
        else:
            return './strace -f -t -e trace=' + syscalls + ' -p $PID -s 9999 -o ./strace_logs/$UID-$PID.out &>/dev/null &'
    else:
        if syscalls == 'all':
            return './strace -f -t -p $PID -s 9999 -o ./strace_logs/$UID-$PID-$TARGET_PACKAGE.out &>/dev/null &'
        else:
            return './strace -f -t -e trace=' + syscalls + ' -p $PID -s 9999 -o ./strace_logs/$UID-$PID-$TARGET_PACKAGE.out &>/dev/null &'

def getPsTree(pstree):
    if(pstree):
        return './busybox-armv8l pstree -p > ./pstree_logs/pstree.out'
    else:
        return ''

get_all_pids = """get_all_pids(){
    ALL_PIDS=()
    first_line=0
    ps -A -o pid > pids.txt
    while IFS= read -r line
    do
        if [[ $first_line -eq 1 && $line != "" ]];then
            ALL_PIDS+=("$line")
        else
            first_line=1
        fi
    done < "pids.txt"
}
get_all_pids
"""

get_package_pids="""get_package_pids(){
    pm list packages > packages.txt
    PACKAGE_PIDS=()    
    while read -r line
    do
      TARGET_PACKAGE=`echo $line | cut -d':' -f2`
      PID=`echo $(pidof $TARGET_PACKAGE)`
      if [[ $PID != "" ]];then
        PACKAGE_PIDS+=("$PID")
      fi
    done < "packages.txt"
}
get_package_pids
"""
