#!/bin/bash
# Wallpaper rotation script — runs every 15 minutes
# Even runs: headline theme, Odd runs: random other theme
# Sets wallpaper on 2nd monitor (LG TV)

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
THEME="headline"

echo "$(date): Run #$COUNTER — theme: $THEME" >> "$LOG"

# Alternate between two filenames so macOS sees a "new" file each time
if [ $((COUNTER % 2)) -eq 0 ]; then
    WALLPAPER="$WALLPAPER_DIR/wallpaper_a.png"
    OLD_WALLPAPER="$WALLPAPER_DIR/wallpaper_b.png"
else
    WALLPAPER="$WALLPAPER_DIR/wallpaper_b.png"
    OLD_WALLPAPER="$WALLPAPER_DIR/wallpaper_a.png"
fi

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
osascript -e "
tell application \"System Events\"
    set picture of desktop 2 to \"$WALLPAPER\"
end tell
" 2>> "$LOG"

# Clean up old wallpaper
rm -f "$OLD_WALLPAPER"

echo "$(date): Wallpaper set successfully ($WALLPAPER)" >> "$LOG"
