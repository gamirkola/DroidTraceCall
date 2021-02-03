#!/system/bin/sh
if [ ! -d ./strace_logs ];then
	mkdir strace_logs
fi
if [ ! -d ./logcat_logs ];then
	mkdir logcat_logs
fi
logcat -b all -v uid -d > ./logcat_logs/logcat_log.out
touch package.txt
pm list packages > package.txt
input="package.txt"

while IFS= read -r line
do
  TARGET_PACKAGE=`echo $line | cut -d':' -f2`
  PID=`echo $(pidof $TARGET_PACKAGE)`
  if [ ! -z "$PID" ]; then
      UID=`echo $(ps -o user= -p $PID | xargs id -u )`
      ./strace -f -t -p $PID -s 9999 -o ./strace_logs/$PID-$UID-$TARGET_PACKAGE.out &>/dev/null &
  fi
done < "$input"
sleep 50 && pkill -f strace