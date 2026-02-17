#!/bin/bash
set -euo pipefail

CLICK_JS=$(cat /tmp/qbo_click_first_entry.js)
DELETED=0
MAX_DELETES=${1:-55}

extract_ref() {
    # Extract ref=eNN from a line like: button "Delete" [ref=e67]
    echo "$1" | sed -n 's/.*\[ref=\([^]]*\)\].*/\1/p' | head -1
}

echo "Starting deletion loop (max $MAX_DELETES)..."

for i in $(seq 1 "$MAX_DELETES"); do
    RESULT=$(agent-browser eval "$CLICK_JS" 2>/dev/null || echo "ERROR")

    if echo "$RESULT" | grep -q "DONE"; then
        echo "[$i] No more entries found. Total deleted: $DELETED"
        break
    fi

    if echo "$RESULT" | grep -q "ERROR"; then
        echo "[$i] Error: $RESULT"
        sleep 2
        continue
    fi

    echo -n "[$i] $RESULT -> "
    sleep 1.2

    # Find Delete button
    SNAPSHOT=$(agent-browser snapshot -i -C 2>/dev/null)
    DEL_LINE=$(echo "$SNAPSHOT" | grep -m1 'button "Delete"')
    DEL_REF=$(extract_ref "$DEL_LINE")
    if [ -z "$DEL_REF" ]; then
        echo "No Delete button."
        agent-browser press Escape 2>/dev/null || true
        sleep 1
        continue
    fi

    agent-browser click "@$DEL_REF" 2>/dev/null
    sleep 0.8

    # Find Yes button
    SNAPSHOT2=$(agent-browser snapshot -i 2>/dev/null)
    YES_LINE=$(echo "$SNAPSHOT2" | grep -m1 'button "Yes"')
    YES_REF=$(extract_ref "$YES_LINE")
    if [ -z "$YES_REF" ]; then
        echo "No Yes button."
        agent-browser press Escape 2>/dev/null || true
        sleep 1
        continue
    fi

    agent-browser click "@$YES_REF" 2>/dev/null
    sleep 1.5

    DELETED=$((DELETED + 1))
    echo "Deleted #$DELETED"
done

echo ""
echo "=== Done. Total deleted: $DELETED ==="
