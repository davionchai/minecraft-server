#!/bin/bash
echo "$CRON_SCHEDULE /usr/local/bin/python /app/main.py >> /var/log/cron.log 2>&1" > /etc/cron.d/backup-cron
crontab /etc/cron.d/backup-cron
cron -f
