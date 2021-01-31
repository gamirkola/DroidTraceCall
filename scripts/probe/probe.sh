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
  UID=`echo dumpsys package $TARGET_PACKAGE | grep userId | tr -d '\n'`
  PID=`echo $(pidof $TARGET_PACKAGE)`
  if [ ! -z "$PID" ]; then
      ./strace -f -t -p $PID -s 9999 -o ./logs/$PID-$UID-$TARGET_PACKAGE.out &>/dev/null &
  fi
done < "$input"
