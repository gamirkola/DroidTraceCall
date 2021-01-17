#!/system/bin/sh

#create package file
touch package.txt

#insert found packages inside the file
pm list packages > package.txt

#path to the file
input="package.txt"

#create logs dir if it does not exist
if [ ! -d ./logs ];then
  mkdir logs
fi

#read the file and start strace on each of package found
while IFS= read -r line
do
  TARGET_PACKAGE=`echo $line | cut -d':' -f2`
  PID=`echo $(pidof $TARGET_PACKAGE)`
  if [ ! -z "$PID" ]; then
#	  echo "PID of $TARGET_PACKAGE: "
#	  echo "$PID"
	  ./strace -f -p $PID -s9999 -o ./logs/$PID-$TARGET_PACKAGE.txt &>/dev/null &
  fi
done < "$input"

