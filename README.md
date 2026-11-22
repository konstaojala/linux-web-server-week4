# Linux Web Server - Week 4

## Overview

This project extends my Ubuntu web server setup by adding a
second server for website backups and database replication.

The environment runs on CSC cPouta using Ubuntu, Nginx,
Python Flask, Gunicorn, MariaDB, Bash, cron, and rsync.

## Server architecture

### Server a - primary server
Public IP: 193.166.24.178

- Hosts the original website and week 2 visitor counter.
- Stores the visitor counter in MariaDB.
- Sends database changes to server b using MariaDB replication.
- Runs an hourly website backup script.

### Server b - backup and replica server
Public IP: 195.148.23.252

- Stores timestamped website backups from server a.
- Runs a MariaDB replica with read-only mode enabled.
- Displays the replicated visitor count using Flask and Gunicorn.
- Uses a separate database account with SELECT-only permissions.

## Website links

- Server a: http://193.166.24.178/
- Week 2 counter: http://193.166.24.178/week2/
- Week 3 report: http://193.166.24.178/week3/
- Week 4 read-only counter: http://195.148.23.252/viikko4/

## Automated backups

The backup script uses rsync over SSH to copy files from:

/var/www/html/

to:

/srv/backups/server-a/

Each backup is saved in a timestamped directory.

Cron schedule;

0 * * * * /usr/bin/bash /home/ubuntu/week4/backup.sh >> /home/ubuntu/week4/cron.log 2>&1

This schedules a backup every hour.

The SSH connection uses a dedicated backup user and SSH key.

Manual backup and file restoration test were completed
successfully. Automatic cron execution is checked separately.

## MariaDB Replication

Server a is the primary MariaDB server.
Server b is the replica.

Changes to the visitor counter are replicated automatically
from server a to server b.

The week 2 Flask application updates the counter on server a.

Week 4 Flask application on server b only reads the
replicated visitor count. Refreshing the Week 4 page does
not increase the count.

## Testing
- SSH connection between the servers
- Manual rsync backup
- File restoration and checksum comparison
- MariaDB replication of visitor counts
- Read-only counter display on server b
- Server b reboot
- Automatic startup of Nginx, MariaDB, and Gunicorn
- Database replication after server b reboot

## Security
- SSH access uses key authentication.
- Backup access uses a dedicated restricted account.
- MariaDB replication uses the private network.
- Database users have limited permissions.
- Database passwords and private SSH keys are not stored
  in this GitHub repository.

## Note
MariaDB replication is not a substitute for a database backup.
The hourly rsync script backs up website files, while MariaDB
replication maintains a second copy of the visitor counter.
