#!/system/bin/sh

trim(){
    local var="$*"
    # remove leading whitespace characters
    var="${var#"${var%%[![:space:]]*}"}"
    # remove trailing whitespace characters
    var="${var%"${var##*[![:space:]]}"}"
    printf '%s' "$var"
}

if [ ! -d ./strace_logs ];then
	mkdir strace_logs
fi
ps -A -o pid > pids.txt
first_line=0
while IFS= read -r line
do
    if [[ $first_line -eq 1 && $line != "" && ! -z $line ]];then
        PID=$(echo $line | tr -d ' ')
        echo "piddo $PID"
        UID=`echo $(ps -o user= -p $PID | xargs id -u )`
        echo "pid and uid $PID $UID"
        ./strace -f -t -p $PID -s 9999 -o ./strace_logs/$UID-$PID.out &>/dev/null &
    else
        first_line=1
    fi
done < "pids.txt"
