#!/system/bin/sh

#create package file
touch package.txt

#insert found packages inside the file
pm list packages > package.txt

#path to the file
input="package.txt"
mkdir logs

while IFS= read -r line
do
  TARGET_PACKAGE=`echo $line | cut -d':' -f2`
  PID=`echo $(pidof $TARGET_PACKAGE)`
  if [ ! -z "$PID" ]; then
	echo "PID of $TARGET_PACKAGE: "
	echo "$PID"
	./strace -f -p $PID -o ./logs/$PID.txt &
  fi
done < "$input"

