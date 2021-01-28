#!/system/bin/sh 
if [ ! -d ./logs ];then
	mkdir logs
fi
touch package.txt
pm list packages > package.txt
input="package.txt"
while IFS= read -r line
do
  TARGET_PACKAGE=`echo $line | cut -d':' -f2`
  PID=`echo $(pidof $TARGET_PACKAGE)`
  if [ ! -z "$PID" ]; then
      ./strace -f -t -e trace=memory,network,ipc  -p $PID -s 9999 -o ./logs/$PID-$TARGET_PACKAGE.out &>/dev/null &
  fi
done < "$input"
