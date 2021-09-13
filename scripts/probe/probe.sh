#!/system/bin/sh
if [ ! -d ./strace_logs ];then
    mkdir strace_logs
fi
touch packages.txt
pm list packages > packages.txt

while IFS= read -r line
do
  TARGET_PACKAGE=`echo $line | cut -d':' -f2`
  PID=`echo $(pidof $TARGET_PACKAGE)`
  if [ ! -z "$PID" ]; then
      UID=`echo $(ps -o user= -p $PID | xargs id -u )`
      
      if [[ ! -z $PID && $PID != "" ]];then
                    ./strace -f -t -p $PID -s 9999 2>&1 | ./split_logs $UID-$PID-$TARGET_PACKAGE &>/dev/null &
                fi
  fi
done < "packages.txt"
