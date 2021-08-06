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
        
        if [[ ! -z $PID && $PID != "" ]];then
                if [[ $PACKAGE_NAME != "" && ! -z $PACKAGE_NAME ]];then
                    ./strace -t -p $PID -s 9999 2>&1 | ./split_logs $UID-$PID-$PACKAGE_NAME &>/dev/null &
                else
                    ./strace -t -p $PID -s 9999 2>&1 | ./split_logs $UID-$PID  &>/dev/null &
                fi
            fi
    fi
done < "pids.txt"
sleep 50 && pkill -f strace && pkill -f split_logs
