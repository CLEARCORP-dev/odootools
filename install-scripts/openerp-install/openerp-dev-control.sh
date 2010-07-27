#!/bin/bash

function proc_ctl {
	gksudo service $1 $2
}

case $2 in
server)
	case $3 in
	start)
		gksudo service openerp-server-$1 start
		;;
	stop)
		gksudo service openerp-server-$1 stop
		;;
	restart)
		gksudo service openerp-server-$1 restart
		;;
	esac
	;;
web)
	case $3 in
	start)
		gksudo service openerp-web-$1 start
		;;
	stop)
		gksudo service openerp-web-$1 stop
		;;
	restart)
		gksudo service openerp-web-$1 restart
		;;
	esac
	;;
all)
	case $3 in
	start)
		gksudo service openerp-server-$1 start
		gksudo service openerp-web-$1 start
		;;
	stop)
		gksudo service openerp-server-$1 stop
		gksudo service openerp-web-$1 stop
		;;
	restart)
		gksudo service openerp-server-$1 restart
		gksudo service openerp-web-$1 restart
		;;
	esac
	;;
apache)
	case $2 in
	start)
		gksudo service apache2 start
		;;
	stop)
		gksudo service apache2 stop
		;;
	restart)
		gksudo service apache2 restart
		;;
	esac
	;;
postgresql)
	case $2 in
	start)
		gksudo service postgresql-8.4 start
		;;
	stop)
		gksudo service postgresql-8.4 stop
		;;
	restart)
		gksudo service postgresql-8.4 restart
		;;
	esac
	;;
esac
