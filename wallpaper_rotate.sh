#!/bin/bash
# Wallpaper rotation script — runs every 4 hours (6am-10pm)
# headline-lego theme, 2K 3:2 resolution, sets wallpaper on FHD display (desktop 3)

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

# Force dark mode for evening runs
HOUR=$(date +%H)
DARK_FLAG=""
if [ "$HOUR" -ge 18 ]; then
    DARK_FLAG="--dark-mode"
fi

echo "$(date): Run #$COUNTER — theme: $THEME" >> "$LOG"

# Cycle through wallpaper_1.png to wallpaper_10.png so you can browse recent ones
SLOT=$(( (COUNTER % 10) + 1 ))
PREV_SLOT=$(( ((COUNTER - 1) % 10 + 10) % 10 + 1 ))
WALLPAPER="$WALLPAPER_DIR/wallpaper_${SLOT}.png"
OLD_WALLPAPER="$WALLPAPER_DIR/wallpaper_${PREV_SLOT}.png"

# Generate
infographic generate \
    --theme "$THEME" \
    --aspect-ratio 3:2 \
    --resolution 1K \
    --width 1920 \
    --height 1280 \
    $DARK_FLAG \
    -o "$WALLPAPER" 2>> "$LOG"

if [ $? -ne 0 ]; then
    echo "$(date): FAILED to generate" >> "$LOG"
    exit 1
fi

# Set wallpaper on X EQUIP by display name (survives monitor reordering)
DISPLAY_NAME="X EQUIP"
osascript -e "
tell application \"System Events\"
    set targetDesktop to first desktop whose display name is \"$DISPLAY_NAME\"
    set picture of targetDesktop to \"$OLD_WALLPAPER\"
end tell
" 2>> "$LOG"
sleep 1
osascript -e "
tell application \"System Events\"
    set targetDesktop to first desktop whose display name is \"$DISPLAY_NAME\"
    set picture of targetDesktop to \"$WALLPAPER\"
end tell
" 2>> "$LOG"

echo "$(date): Wallpaper set successfully ($WALLPAPER, slot $SLOT/10)" >> "$LOG"
