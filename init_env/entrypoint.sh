#!/bin/bash
/etc/init.d/apache2  start
usermod -d /opt/phabricator/mysql mysql || echo "usermod"
chown mysql:mysql /opt/phabricator/mysql
/etc/init.d/mysql start
source /etc/environment
phd start
/usr/sbin/sshd -f /opt/phabricator/sshd_config.phabricator
service apache2 status
service mysql status
phd status
echo "Awesome"
/bin/bash
