#!/bin/bash
# Wallpaper rotation script — runs every 4 hours (6am-10pm)
# headline-lego theme, 4K resolution, sets wallpaper on 2nd monitor (LG TV)

export PATH="/opt/homebrew/bin:$PATH"

# Load API keys from environment or .env file
ENV_FILE="/Users/phobus/work/infographic/.env"
if [ -f "$ENV_FILE" ]; then
    set -a
    source "$ENV_FILE"
    set +a
fi

if [ -z "$GOOGLE_API_KEY" ] || [ -z "$NEWSAPI_KEY" ]; then
    echo "$(date): Missing GOOGLE_API_KEY or NEWSAPI_KEY. Set in environment or $ENV_FILE" >> "$LOG"
    exit 1
fi

VENV="/Users/phobus/work/infographic/.venv/bin/activate"
WALLPAPER_DIR="/Users/phobus/work/infographic"
COUNTER_FILE="/Users/phobus/work/infographic/.wallpaper_counter"
LOG="/Users/phobus/work/infographic/wallpaper_rotate.log"

source "$VENV"

# Read and increment counter
if [ -f "$COUNTER_FILE" ]; then
    COUNTER=$(cat "$COUNTER_FILE")
else
    COUNTER=0
fi
NEXT=$((COUNTER + 1))
echo "$NEXT" > "$COUNTER_FILE"

# Pick theme
THEME="headline-lego"

echo "$(date): Run #$COUNTER — theme: $THEME" >> "$LOG"

# Cycle through wallpaper_1.png to wallpaper_10.png so you can browse recent ones
SLOT=$(( (COUNTER % 10) + 1 ))
PREV_SLOT=$(( ((COUNTER - 1) % 10 + 10) % 10 + 1 ))
WALLPAPER="$WALLPAPER_DIR/wallpaper_${SLOT}.png"
OLD_WALLPAPER="$WALLPAPER_DIR/wallpaper_${PREV_SLOT}.png"

# Generate
infographic generate \
    --theme "$THEME" \
    --aspect-ratio 16:9 \
    --resolution 4K \
    --width 3840 \
    --height 2160 \
    -o "$WALLPAPER" 2>> "$LOG"

if [ $? -ne 0 ]; then
    echo "$(date): FAILED to generate" >> "$LOG"
    exit 1
fi

# Set wallpaper on 2nd monitor
# First set to a blank to force macOS to notice the change, then set the real one
osascript -e "
tell application \"System Events\"
    set picture of desktop 2 to \"$OLD_WALLPAPER\"
end tell
" 2>> "$LOG"
sleep 1
osascript -e "
tell application \"System Events\"
    set picture of desktop 2 to \"$WALLPAPER\"
end tell
" 2>> "$LOG"

echo "$(date): Wallpaper set successfully ($WALLPAPER, slot $SLOT/10)" >> "$LOG"
