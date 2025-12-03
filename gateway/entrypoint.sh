#!/bin/bash

# Start Nginx in the background
nginx

echo "--- 🛡️  Nginx Auto-Reloader Started (Timestamp Mode) ---"

# Store the initial timestamp of the block file
LAST_MOD=$(stat -c %Y /etc/nginx/conf.d/block.conf 2>/dev/null || echo 0)

while true; do
    # Check the current timestamp
    CURRENT_MOD=$(stat -c %Y /etc/nginx/conf.d/block.conf 2>/dev/null || echo 0)

    if [ "$CURRENT_MOD" != "$LAST_MOD" ]; then
        echo "🔄 Detected change in block.conf! Reloading..."
        nginx -s reload
        LAST_MOD=$CURRENT_MOD
    fi
    
    sleep 2
done