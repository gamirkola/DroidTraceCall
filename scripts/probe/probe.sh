#!/system/bin/sh
if [ ! -d ./logcat_logs ];then
	mkdir logcat_logs
fi
logcat -b all -v  -d > ./logcat_logs/logcat_log.out
