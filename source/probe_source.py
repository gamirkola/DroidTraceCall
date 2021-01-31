android_shabang = '#!/system/bin/sh \n'
bash_shabang = '#!/bin/bash \n'
create_if_not_logs_dir = 'if [ ! -d ./logs ];then\n\tmkdir logs\nfi\n'
create_package_file = 'touch package.txt\npm list packages > package.txt\ninput="package.txt"'
#todo escape \n from uid
while_on_packages = lambda syscalls:"""\nwhile IFS= read -r line
do
  TARGET_PACKAGE=`echo $line | cut -d':' -f2`
  UID=`echo $(dumpsys package $TARGET_PACKAGE | grep userId | tr -d '\n')`
  PID=`echo $(pidof $TARGET_PACKAGE)`
  if [ ! -z "$PID" ]; then
      """ + getAllStrace(syscalls) + """
  fi
done < "$input"
"""




#little work arounf for makins trace traceall the system calls
def getAllStrace(syscalls):
    if syscalls == 'all':
        return './strace -f -t -p $PID -s 9999 -o ./logs/$PID-$UID-$TARGET_PACKAGE.out &>/dev/null &'
    else:
        return './strace -f -t -e trace=' + syscalls + ' -p $PID -s 9999 -o ./logs/$PID-$UID-$TARGET_PACKAGE.out &>/dev/null &'