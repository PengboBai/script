#!/bin/bash
set -x
/etc/init.d/apache2  start
chown -R root:root /opt/phabricator
chmod 755 /opt/phabricator/hooks/phabricator-ssh-hook.sh
chown -R mysql:mysql /opt/phabricator/mysql
/etc/init.d/mysql start
source /etc/environment
phd start
/usr/sbin/sshd -f /opt/phabricator/sshd_config.phabricator
echo "apache2 status"
service apache2 status
echo "Mysql status"
service mysql status
echo "phd status"
phd status
echo "Awesome"
/bin/bash
