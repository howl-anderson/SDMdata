#!/bin/bash
# TODO: bash cannot cross platform, this file may remove later
 
gunicorn="gunicorn"
prog="sdmdata"
PROJECT_HOME="./sdmdata"
pid="/var/lock/$prog"
 
RETVAL=0
HOST="0.0.0.0"
PORT=8080
 
start() {
	echo -n $"Starting $prog:"
	cd $PROJECT_HOME
	$gunicorn --daemon -b $HOST:$PORT --pid=$pid web_server:app
	RETVAL=$?
	cd -
	echo
	[ $RETVAL -eq 0 ] && touch $pid
	return $RETVAL
}
 
stop() {
	echo -n $"Stopping $prog:"
	kill -9 `cat $pid`
	RETVAL=$?
	echo
	[ $RETVAL -eq 0 ] && rm -f $pid
	return $RETVAL
}
 
reload() {
	echo -n $"Reloading $prog:"
	kill -HUP `cat $pid`
	RETVAL=$?
	echo
	return $RETVAL
}
 
case "$1" in
	start)
		start
		;;
	stop)
		stop
		;;
	restart)
		stop
		start
		;;
	reload)
		reload
		;;
	*)
		echo "Usage: $0 {start|stop|restart|reload}"
		RETVAL=1
		;;
esac
exit $RETVAL
