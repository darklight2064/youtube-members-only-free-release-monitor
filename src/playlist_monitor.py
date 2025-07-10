#!/usr/bin/env python3
"""
YouTube Playlist Monitor - Core monitoring functionality
"""

import yt_dlp
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import logging

class PlaylistMonitor:
    def __init__(self, playlist_url: str, state_file: str = "playlist_state.json"):
        self.playlist_url = playlist_url
        self.state_file = state_file
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        """Set up logging for the monitor"""
        logger = logging.getLogger("playlist_monitor")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def fetch_playlist_videos(self) -> Optional[Dict]:
        """Fetch first 3 videos from playlist using yt-dlp"""
        ydl_opts = {
            'quiet': True,
            'extract_flat': True,
            'no_warnings': True,
        }
        
        try:
            self.logger.info(f"Fetching playlist: {self.playlist_url}")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.playlist_url, download=False)
                
                if not info:
                    self.logger.error("Failed to extract playlist info")
                    return None
                
                # Get first 3 videos only
                videos = info.get('entries', [])[:3]
                
                playlist_data = {
                    'playlist_id': info.get('id'),
                    'playlist_title': info.get('title'),
                    'total_videos': len(info.get('entries', [])),
                    'monitored_at': datetime.now().isoformat(),
                    'videos': []
                }
                
                # Process each video using only title information
                for i, video in enumerate(videos, 1):
                    if not video:
                        continue
                        
                    video_id = video.get('id')
                    video_title = video.get('title')
                    video_url = f"https://www.youtube.com/watch?v={video_id}"
                    
                    self.logger.info(f"Processing video {i}: {video_title}")
                    
                    # Determine status based on title only
                    if '限免' in video_title:
                        is_member_only = False
                        availability = 'limited_free'
                        self.logger.info(f"Video {video_id}: Detected as limited-time free from title")
                    else:
                        is_member_only = True
                        availability = 'member_only'
                        self.logger.info(f"Video {video_id}: Assumed member-only (no '限免' in title)")
                    
                    playlist_data['videos'].append({
                        'position': i,
                        'id': video_id,
                        'title': video_title,
                        'url': video_url,
                        'is_member_only': is_member_only,
                        'availability': availability,
                        'error_message': None,
                        'checked_at': datetime.now().isoformat()
                    })
                
                self.logger.info(f"Successfully fetched {len(playlist_data['videos'])} videos")
                return playlist_data
                
        except Exception as e:
            self.logger.error(f"Error fetching playlist: {e}")
            return None
    
    
    def load_previous_state(self) -> Optional[Dict]:
        """Load previous monitoring state from file"""
        if not os.path.exists(self.state_file):
            self.logger.info("No previous state file found")
            return None
            
        try:
            with open(self.state_file, 'r') as f:
                data = json.load(f)
                self.logger.info(f"Loaded previous state with {len(data.get('videos', []))} videos")
                return data
        except Exception as e:
            self.logger.error(f"Error loading previous state: {e}")
            return None
    
    def save_current_state(self, playlist_data: Dict) -> bool:
        """Save current monitoring state to file"""
        try:
            with open(self.state_file, 'w') as f:
                json.dump(playlist_data, f, indent=2)
            self.logger.info(f"Saved current state to {self.state_file}")
            return True
        except Exception as e:
            self.logger.error(f"Error saving state: {e}")
            return False
    
    def detect_changes(self, previous_state: Dict, current_state: Dict) -> List[Dict]:
        """Detect videos that changed from member-only to free"""
        changes = []
        
        if not previous_state or not current_state:
            self.logger.info("No previous state to compare - skipping change detection")
            return changes
        
        # Create lookup for previous videos
        prev_videos = {v['id']: v for v in previous_state.get('videos', [])}
        curr_videos = {v['id']: v for v in current_state.get('videos', [])}
        
        for video_id, curr_video in curr_videos.items():
            prev_video = prev_videos.get(video_id)
            
            if not prev_video:
                # New video detected - check if it's free
                self.logger.info(f"New video detected: {curr_video['title']}")
                if not curr_video['is_member_only']:
                    change = {
                        'type': 'new_free_video',
                        'video_id': video_id,
                        'title': curr_video['title'],
                        'url': curr_video['url'],
                        'previous_status': 'not_existed',
                        'current_status': curr_video['availability'],
                        'detected_at': datetime.now().isoformat()
                    }
                    changes.append(change)
                    self.logger.info(f"🎉 New free video detected: {curr_video['title']}")
                continue
            
            # Check for member-only → free change
            if (prev_video['is_member_only'] and not curr_video['is_member_only']):
                change = {
                    'type': 'member_to_free',
                    'video_id': video_id,
                    'title': curr_video['title'],
                    'url': curr_video['url'],
                    'previous_status': prev_video['availability'],
                    'current_status': curr_video['availability'],
                    'detected_at': datetime.now().isoformat()
                }
                changes.append(change)
                self.logger.info(f"🎉 Video became free: {curr_video['title']}")
        
        self.logger.info(f"Detected {len(changes)} changes")
        return changes
    
    def monitor_once(self) -> List[Dict]:
        """Perform one monitoring cycle and return any changes"""
        self.logger.info("Starting monitoring cycle")
        
        # Fetch current state
        current_state = self.fetch_playlist_videos()
        if not current_state:
            self.logger.error("Failed to fetch current playlist state")
            return []
        
        # Load previous state
        previous_state = self.load_previous_state()
        
        # Detect changes
        changes = self.detect_changes(previous_state, current_state)
        
        # Save current state
        self.save_current_state(current_state)
        
        self.logger.info("Monitoring cycle completed")
        return changes

if __name__ == "__main__":
    # Test the monitor
    playlist_url = "https://www.youtube.com/playlist?list=PLO_DkCSmTKMNMgr-JKMDV2Sw2HW59LMvc"
    monitor = PlaylistMonitor(playlist_url)
    
    changes = monitor.monitor_once()
    if changes:
        print(f"🎉 Found {len(changes)} changes!")
        for change in changes:
            print(f"  - {change['title']} became free")
    else:
        print("📊 No changes detected")