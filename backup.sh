
#!/usr/bin/env bash

# Week 4 - Website backup from server a to server b

TIMESTAMP=$(date -u +%Y-%m-%d_%H-%M-%S)

SOURCE="/var/www/html/"
DESTINATION="backupuser@192.168.1.157"
REMOTE_DIR="/srv/backups/server-a/$TIMESTAMP"

KEY="/home/ubuntu/.ssh/week4_backup_key"
LOG="/home/ubuntu/week4/backup.log"

# Create a new timestamped backup directory on Server B
if ssh -i "$KEY" -o BatchMode=yes -o IdentitiesOnly=yes \
    "$DESTINATION" "mkdir -m 700 '$REMOTE_DIR'" &&
   rsync -a --no-owner --no-group --no-perms \
    -e "ssh -i $KEY -o BatchMode=yes -o IdentitiesOnly=yes" \
    "$SOURCE" "$DESTINATION:$REMOTE_DIR/"; then

    echo "$TIMESTAMP SUCCESS" | tee -a "$LOG"

else
    echo "$TIMESTAMP FAILED" | tee -a "$LOG"
    exit 1
fi
