#!/system/bin/sh
if [ ! -d ./strace_logs ];then
	mkdir strace_logs
fi
if [ ! -d ./pstree_logs ];then
	mkdir pstree_logs
fi
get_all_pids(){
    ALL_PIDS=()
    first_line=0
    ps -A -o pid > pids.txt
    while IFS= read -r line
    do
        if [[ $first_line -eq 1 && $line != "" ]];then
            ALL_PIDS+=("$line")
        else
            first_line=1
        fi
    done < "pids.txt"
}
get_all_pids

for PID in "${ALL_PIDS[@]}"
do
  if [ ! -z "$PID" ]; then
      UID=`echo $(ps -o user= -p $PID | xargs id -u )`
      ./busybox-armv8l pstree -p > ./pstree_logs/pstree.out
      ./strace -f -t -p $PID -s 9999 -o ./strace_logs/$UID-$PID.out &>/dev/null &
  fi
done
