android_shabang = '#!/system/bin/sh \n'
bash_shabang = '#!/bin/bash \n'
create_if_not_logs_dir = 'if [ ! -d ./logs ];then\n\tmkdir logs\nfi\n'
create_package_file = 'touch package.txt\npm list packages > package.txt\ninput="package.txt"'
while_on_packages = lambda syscalls: """\nwhile IFS= read -r line
do
  TARGET_PACKAGE=`echo $line | cut -d':' -f2`
  PID=`echo $(pidof $TARGET_PACKAGE)`
  if [ ! -z "$PID" ]; then
      ./strace -f -t -e trace=""" + syscalls + """  -p $PID -s 9999 -o ./logs/$PID-$TARGET_PACKAGE.out &>/dev/null &
  fi
done < "$input"
"""