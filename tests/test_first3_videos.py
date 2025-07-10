#!/usr/bin/env python3
"""
Test monitoring only the first 3 videos from the playlist
"""

import yt_dlp
import json
from datetime import datetime

def test_first3_videos():
    playlist_url = "https://www.youtube.com/playlist?list=PLO_DkCSmTKMNMgr-JKMDV2Sw2HW59LMvc"
    
    # First get playlist structure with flat extraction
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'no_warnings': True,
    }
    
    print(f"Testing first 3 videos monitoring from: {playlist_url}")
    print("=" * 70)
    
    try:
        # Step 1: Get playlist structure
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("📋 Extracting playlist structure...")
            info = ydl.extract_info(playlist_url, download=False)
            
            if not info:
                print("❌ Failed to extract playlist info")
                return False
            
            print(f"✅ Playlist: {info.get('title', 'Unknown')}")
            print(f"✅ Total Videos: {len(info.get('entries', []))}")
            
            # Get first 3 videos
            videos = info.get('entries', [])[:3]
            print(f"✅ Monitoring first 3 videos")
            print()
            
            # Step 2: Check each of the first 3 videos individually
            monitored_videos = []
            
            for i, video in enumerate(videos, 1):
                if not video:
                    continue
                    
                video_id = video.get('id')
                video_title = video.get('title')
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                
                print(f"🔍 Video {i}: {video_title}")
                print(f"   ID: {video_id}")
                
                # Check video status
                video_status = check_video_status(video_id, video_url)
                monitored_videos.append({
                    'position': i,
                    'id': video_id,
                    'title': video_title,
                    'url': video_url,
                    **video_status
                })
                
                print(f"   Status: {'🔒 Member-only' if video_status['is_member_only'] else '🔓 Public/Free'}")
                if video_status.get('error_message'):
                    print(f"   Note: {video_status['error_message'][:80]}...")
                print()
            
            # Step 3: Save monitoring data
            monitoring_data = {
                'playlist_id': info.get('id'),
                'playlist_title': info.get('title'),
                'monitored_at': datetime.now().isoformat(),
                'videos': monitored_videos
            }
            
            with open('first3_monitoring.json', 'w') as f:
                json.dump(monitoring_data, f, indent=2)
            
            print("💾 Monitoring data saved to first3_monitoring.json")
            print(f"✅ Successfully monitored {len(monitored_videos)} videos")
            
            # Summary
            member_only_count = sum(1 for v in monitored_videos if v['is_member_only'])
            free_count = len(monitored_videos) - member_only_count
            
            print(f"\n📊 Summary:")
            print(f"   🔒 Member-only videos: {member_only_count}")
            print(f"   🔓 Free/Public videos: {free_count}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_video_status(video_id, video_url):
    """Check individual video for member-only status"""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
        'skip_download': True,
    }
    
    status = {
        'is_member_only': False,
        'availability': 'unknown',
        'error_message': None,
        'checked_at': datetime.now().isoformat()
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
            if info:
                # Successfully extracted - likely public or free
                status['is_member_only'] = False
                status['availability'] = info.get('availability', 'public')
            else:
                # Could not extract - might be member-only
                status['is_member_only'] = True
                status['availability'] = 'member_only'
                
    except Exception as e:
        error_msg = str(e)
        if any(keyword in error_msg.lower() for keyword in ['member', 'premium', 'subscriber']):
            status['is_member_only'] = True
            status['availability'] = 'member_only'
            status['error_message'] = error_msg
        else:
            status['error_message'] = error_msg
    
    return status

if __name__ == "__main__":
    success = test_first3_videos()
    if success:
        print("\n🎉 First 3 videos monitoring test successful!")
        print("✅ Ready to implement the monitoring system")
    else:
        print("\n❌ Test failed - need to investigate")