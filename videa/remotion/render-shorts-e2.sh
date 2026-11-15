#!/bin/bash
# vyrenderuje shorty epizody 2 do out/shorts-e2
B=/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell
mkdir -p out/shorts-e2
for id in e2-short-1-carodej e2-short-2-brambory e2-short-3-lazebnik e2-short-4-most e2-short-5-zabava e2-short-6-katedrala; do
  npx remotion render src/index.ts $id out/shorts-e2/$id.mp4 --public-dir=.. \
    --browser-executable=$B --codec=h264 --crf=22 --concurrency=4 2>&1 | grep -E "rror" 
  echo "HOTOVO $id"
done
echo VSE_HOTOVO
