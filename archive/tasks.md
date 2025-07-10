# YouTube Playlist Monitor - Tasks

## Project Overview
Create a Python program to monitor the YouTube playlist `https://www.youtube.com/playlist?list=PLO_DkCSmTKMNMgr-JKMDV2Sw2HW59LMvc` for updates, specifically detecting when member-only videos become temporarily free, and send email notifications using Resend.

## Tasks Breakdown

### Phase 1: Research & Planning ✅
- [x] **1. Analyze YouTube playlist structure**
  - Understand how member-only videos are marked
  - Identify video metadata that indicates temporary free access
  - Document playlist API response format

- [x] **2. Choose monitoring approach**
  - **Decision: Use yt-dlp SDK** (no API key required, better member-only detection)
  - No rate limits or authentication requirements
  - Reliable metadata extraction

- [x] **3. Design system architecture**
  - Data storage for tracking playlist state
  - Monitoring frequency and scheduling
  - Notification triggers and content format

### Phase 2: Core Implementation
- [ ] **4. Set up project structure**
  - Create virtual environment
  - Install dependencies (yt-dlp, resend, schedule)
  - Set up configuration management

- [ ] **5. Implement yt-dlp playlist fetcher**
  - Create function to fetch first 3 videos from playlist using yt-dlp
  - Parse video information (title, status, availability, member-only status)
  - Handle yt-dlp errors and edge cases

- [ ] **6. Build state tracking system**
  - Design data structure to store playlist state
  - Implement comparison logic for detecting changes
  - Add persistence (JSON file for simplicity)

- [ ] **7. Implement Resend email notifications**
  - Set up Resend API integration
  - Create email templates for notifications
  - Add error handling for email delivery

### Phase 3: Monitoring & Scheduling
- [ ] **8. Add change detection logic**
  - Compare current state of first 3 videos with stored state
  - Identify newly available videos (member-only → free)
  - Filter relevant changes for notification

- [ ] **9. Implement monitoring loop**
  - Create scheduled checking mechanism using `schedule` library
  - Add configurable monitoring intervals
  - Implement graceful error handling and logging

### Phase 4: Configuration & Deployment
- [ ] **10. Create configuration system**
  - Environment variables for Resend API key
  - Configurable email recipients
  - Adjustable monitoring frequency

- [ ] **11. Add logging and monitoring**
  - Log monitoring activities with timestamps
  - Track notification history
  - Add health check capabilities

- [ ] **12. Documentation and testing**
  - Create setup instructions
  - Add usage examples
  - Test notification system end-to-end

## Technical Requirements
- **yt-dlp** for YouTube playlist data extraction
- **Resend API** for email notifications
- **JSON** for state persistence
- **schedule** library for automated monitoring
- **Python 3.8+** with virtual environment

## Configuration Needed
- Resend API key
- Email recipient addresses
- Monitoring frequency settings (default: every 30 minutes)
- Playlist URL (provided: PLO_DkCSmTKMNMgr-JKMDV2Sw2HW59LMvc)

## Success Criteria
- Detect when member-only videos become temporarily free
- Send timely email notifications with video details
- Maintain reliable monitoring without manual intervention
- Handle errors gracefully without stopping monitoring

## System Architecture Design

### Component Overview
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Scheduler     │───▶│  Playlist       │───▶│  Change         │
│   (every 30min)│    │  Fetcher        │    │  Detector       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │                        │
                              ▼                        ▼
                    ┌─────────────────┐    ┌─────────────────┐
                    │  yt-dlp         │    │  State Storage  │
                    │  Extractor      │    │  (JSON)         │
                    └─────────────────┘    └─────────────────┘
                                                      │
                                                      ▼
                                          ┌─────────────────┐
                                          │  Email          │
                                          │  Notifier       │
                                          │  (Resend)       │
                                          └─────────────────┘
```

### Data Flow
1. **Scheduler** triggers monitoring every 30 minutes
2. **Playlist Fetcher** uses yt-dlp to extract first 3 videos from playlist
3. **Change Detector** compares with stored state of these 3 videos
4. **State Storage** persists current state as JSON
5. **Email Notifier** sends alerts for member-only → free changes

### Data Structures
```python
# Video state structure
{
    "video_id": "abc123",
    "title": "Video Title",
    "url": "https://youtube.com/watch?v=abc123",
    "is_member_only": False,
    "availability": "public",
    "upload_date": "20240101",
    "last_checked": "2024-01-01T12:00:00Z"
}

# Playlist state structure
{
    "playlist_id": "PLO_DkCSmTKMNMgr-JKMDV2Sw2HW59LMvc",
    "playlist_title": "Playlist Name",
    "last_updated": "2024-01-01T12:00:00Z",
    "videos": [video_objects],
    "total_videos": 50
}
```

### Monitoring Strategy
- **Scope**: Monitor only first 3 videos in playlist (most recent uploads)
- **Frequency**: Every 30 minutes (configurable)
- **Storage**: JSON file for state persistence
- **Notifications**: Only when member-only videos become free
- **Error Handling**: Log errors, continue monitoring

### Notification Triggers
- Video status changes from `is_member_only: true` to `is_member_only: false`
- Video availability changes from "premium_only" to "public"
- New videos added to playlist (optional feature)

## yt-dlp Implementation Notes
```python
# Basic yt-dlp usage for playlist metadata
import yt_dlp

ydl_opts = {
    'quiet': True,
    'extract_flat': False,  # Get full video info
    'writeinfojson': False,
    'no_warnings': True
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(playlist_url, download=False)
    # Access video availability, titles, member-only status
```