#! /bin/sh
# /etc/init.d/dna 

### BEGIN INIT INFO
# Provides:          dna
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Pretty DNA!
# Description:       It's lights time!
### END INIT INFO

# If you want a command to always run, put it here

# Carry out specific functions when asked to by the system
case "$1" in
  start)
    echo "Starting dna"
    # run application you want to start
    python /home/chip/hotcouture2017/dna.py &
    ;;
  stop)
    echo "Stopping dna"
    # kill application you want to stop
    killall python
    ;;
  *)
    echo "Usage: /etc/init.d/dna {start|stop}"
    exit 1
    ;;
esac

exit 0