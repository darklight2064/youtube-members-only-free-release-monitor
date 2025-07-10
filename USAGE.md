# Quick Usage Guide

## Setup (One-time)

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Create configuration:**
   ```bash
   cp .env.example .env
   # Edit .env with your Resend API key and email settings
   ```

3. **Test email setup:**
   ```bash
   uv run main.py --mode test-email
   ```

## Daily Usage

**Check for free videos:**
```bash
uv run main.py
```

That's it! The program will:
- ✅ Check the first 3 videos in the playlist
- ✅ Detect videos with '限免' (limited-time free)
- ✅ Send email if member-only videos became free
- ✅ Exit automatically

## Advanced Usage

**Run a simple test:**
```bash
uv run tests/run_test.py
```

**Continuous monitoring (optional):**
```bash
uv run main.py --mode monitor
```

**Schedule with cron (recommended):**
```bash
# Check every 30 minutes
*/30 * * * * cd /path/to/youtube-monitor && uv run main.py
```

## Files

- `playlist_state.json` - Tracks video status between runs
- `monitor.log` - Log file with timestamps
- `.env` - Your private configuration (don't share!)

## How it Works

1. Fetches playlist structure using yt-dlp
2. Checks first 3 video titles for '限免' keyword
3. Compares with previous state
4. Sends beautiful HTML email via Resend if changes detected
5. Saves new state for next run

Simple and effective! 🎉