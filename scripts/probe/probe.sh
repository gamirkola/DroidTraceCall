#!/system/bin/sh
if [ ! -d ./strace_logs ];then
	mkdir strace_logs
fi
if [ ! -d ./logcat_logs ];then
	mkdir logcat_logs
fi
if [ ! -d ./top_logs ];then
	mkdir top_logs
fi
if [ ! -d ./pstree_logs ];then
	mkdir pstree_logs
fi
touch package.txt
pm list packages > package.txt
input="package.txt"

while IFS= read -r line
do
  TARGET_PACKAGE=`echo $line | cut -d':' -f2`
  PID=`echo $(pidof $TARGET_PACKAGE)`
  if [ ! -z "$PID" ]; then
      UID=`echo $(ps -o user= -p $PID | xargs id -u )`
      ./busybox-armv8l pstree -p > ./pstree_logs/pstree.out
      ./strace -f -t -p $PID -s 9999 -o ./strace_logs/$UID-$PID-$TARGET_PACKAGE.out &>/dev/null &
  fi
done < "$input"
end=$((SECONDS+5))

while [ $SECONDS -lt $end ]; do
    TIMESTAMP=`echo $(date +"%H_%M_%S")`
    top -m 500 -n 1 > ./top_logs/top_log_$TIMESTAMP.txt
done