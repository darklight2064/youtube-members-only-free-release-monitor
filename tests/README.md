# Test Files

This directory contains development and testing scripts used during the development of the YouTube Playlist Monitor.

## Test Scripts

### Core Functionality Tests
- `test_playlist.py` - Initial playlist data extraction test
- `test_flat_extraction.py` - Flat playlist extraction test
- `test_first3_videos.py` - First 3 videos monitoring test
- `test_updated_logic.py` - Title-based detection logic test
- `test_simplified_logic.py` - Simplified title-only logic test

### Debug Scripts
- `debug_video_status.py` - Detailed video status analysis

## Usage

These scripts were used during development to test and validate the monitoring logic. They are kept for reference but are not needed for normal operation of the YouTube Playlist Monitor.

To run the main application, use:
```bash
cd .. && uv run main.py
```