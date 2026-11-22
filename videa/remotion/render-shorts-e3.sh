#!/bin/bash
# vyrenderuje shorty epizody 3 do out/shorts-e3
B=/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell
mkdir -p out/shorts-e3
for id in e3-short-1-mamut e3-short-2-ledovec e3-short-3-kosti e3-short-4-venuse e3-short-5-tenisky e3-short-6-pes e3-short-7-tlupa; do
  npx remotion render src/index.ts $id out/shorts-e3/$id.mp4 --public-dir=.. \
    --browser-executable=$B --codec=h264 --crf=22 --concurrency=4 2>&1 | grep -E "rror"
  echo "HOTOVO $id"
done
echo VSE_HOTOVO
