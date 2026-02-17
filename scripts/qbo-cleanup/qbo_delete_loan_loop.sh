#!/bin/bash
set -euo pipefail

CLICK_JS=$(cat /tmp/qbo_click_first_entry.js)
DELETED=0
MAX_DELETES=${1:-510}
EMPTY_PAGES=0

extract_ref() {
    echo "$1" | sed -n 's/.*\[ref=\([^]]*\)\].*/\1/p' | head -1
}

echo "Starting Shopify Capital Loan deletion loop (max $MAX_DELETES)..."

for i in $(seq 1 "$MAX_DELETES"); do
    RESULT=$(agent-browser eval "$CLICK_JS" 2>/dev/null || echo "ERROR")

    if echo "$RESULT" | grep -q "DONE"; then
        EMPTY_PAGES=$((EMPTY_PAGES + 1))
        if [ $EMPTY_PAGES -ge 3 ]; then
            echo "[$i] Empty page x3. Account empty. Total deleted: $DELETED"
            break
        fi
        echo "[$i] Empty page #$EMPTY_PAGES. Refreshing..."
        agent-browser open "https://qbo.intuit.com/app/register?accountId=1150040012" 2>/dev/null
        sleep 3
        continue
    fi

    EMPTY_PAGES=0

    if echo "$RESULT" | grep -q "ERROR"; then
        echo "[$i] Error: $RESULT"
        sleep 2
        continue
    fi

    echo -n "[$i] $RESULT -> "
    sleep 1.2

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

    # Progress report every 50
    if [ $((DELETED % 50)) -eq 0 ]; then
        echo "=== PROGRESS: $DELETED deleted so far ==="
    fi
done

echo ""
echo "=== COMPLETE. Total deleted: $DELETED ==="
