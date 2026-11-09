#!/bin/bash
# vyrenderuje všechny shorty do out/shorts
B=/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell
mkdir -p out/shorts
for id in short-1-auto short-2-karta short-3-zachod short-4-bacily short-5-mlcet; do
  npx remotion render src/index.ts $id out/shorts/$id.mp4 --public-dir=../01-praha-1926 \
    --browser-executable=$B --codec=h264 --crf=20 --concurrency=4 2>&1 | grep -E "Encoded|Error|error" 
  echo "HOTOVO $id"
done
echo VSE_HOTOVO
