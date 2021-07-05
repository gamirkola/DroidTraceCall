#!/system/bin/sh
if [ ! -d ./strace_logs ];then
	mkdir strace_logs
fi
ps -A -o pid | tr -d "PID" > pids.txt
while IFS= read -r line
do
    if [[ $line != "" && ! -z $line ]];then
        PID=`echo $(echo $line | tr -d " ")`
        UID=`echo $(ps -o user= -p $PID | xargs id -u )`
        PACKAGE_NAME=`echo $(pm list packages -3 -U | grep -w $UID | cut -d':' -f2 | cut -d' ' -f1)`
        ./strace -t -p $PID -s 9999 -o ./strace_logs/$UID-$PID-$PACKAGE_NAME.out &>/dev/null &
    fi
done < "pids.txt"
