#!/bin/bash

FILE=$1
DOC_ID=${2:-$(basename "$FILE")}

if [ -z "$FILE" ] || [ ! -f "$FILE" ]; then
    echo "Usage: $0 <filename> [doc_id]"
    echo "Example: $0 document.txt my_doc"
    exit 1
fi

CONTENT=$(cat "$FILE" | sed 's/\\/\\\\/g' | sed 's/"/\\"/g' | sed ':a;N;$!ba;s/\n/\\n/g')

curl -X POST "http://localhost:8000/ingest" \
  -H "Content-Type: application/json" \
  -d "{\"doc_id\": \"$DOC_ID\", \"text\": \"$CONTENT\"}"

echo ""
echo "Ingested: $FILE as $DOC_ID"