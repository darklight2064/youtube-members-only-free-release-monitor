#!/usr/bin/env python3
"""
Test using extract_flat to get playlist structure without downloading video details
"""

import yt_dlp
import json
from datetime import datetime

def test_flat_extraction():
    playlist_url = "https://www.youtube.com/playlist?list=PLO_DkCSmTKMNMgr-JKMDV2Sw2HW59LMvc"
    
    # Use extract_flat to get basic info without full video metadata
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,  # Only get basic playlist structure
        'no_warnings': True,
    }
    
    print(f"Testing flat extraction: {playlist_url}")
    print("=" * 60)
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("Extracting playlist structure...")
            info = ydl.extract_info(playlist_url, download=False)
            
            if not info:
                print("❌ Failed to extract playlist info")
                return False
            
            print(f"✅ Playlist Title: {info.get('title', 'Unknown')}")
            print(f"✅ Playlist ID: {info.get('id', 'Unknown')}")
            print(f"✅ Total Videos: {len(info.get('entries', []))}")
            print()
            
            # Show first 10 video IDs and titles
            videos = info.get('entries', [])
            print("Video structure (flat extraction):")
            for i, video in enumerate(videos[:10]):
                if video:
                    print(f"  {i+1}. {video.get('id', 'Unknown')} - {video.get('title', 'Unknown')}")
            
            print("\n✅ Flat extraction successful!")
            print("📝 Note: We can get video IDs, then check individual videos for member-only status")
            
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_single_video_check():
    """Test checking a single video for member-only status"""
    
    # From the error messages, we know these are member-only videos
    test_video_ids = ["8Dcop5ewKrI", "JDTmSUQWch4"]
    
    print("\nTesting individual video status check:")
    print("=" * 60)
    
    for video_id in test_video_ids:
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'ignoreerrors': True,
            'skip_download': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"Checking video: {video_id}")
                info = ydl.extract_info(video_url, download=False)
                
                if info:
                    print(f"  ✅ Title: {info.get('title', 'Unknown')}")
                    print(f"  ✅ Availability: {info.get('availability', 'Unknown')}")
                    is_member_only = info.get('availability') in ['premium_only', 'subscriber_only']
                    print(f"  ✅ Member Only: {is_member_only}")
                else:
                    print(f"  ❌ Could not extract info (likely member-only)")
                    
        except Exception as e:
            error_msg = str(e)
            if "members-only" in error_msg or "member" in error_msg.lower():
                print(f"  ✅ Detected as member-only: {video_id}")
            else:
                print(f"  ❌ Error: {e}")
        
        print()

if __name__ == "__main__":
    success = test_flat_extraction()
    if success:
        test_single_video_check()
        print("\n🎉 Strategy confirmed:")
        print("1. Use extract_flat=True to get playlist structure")
        print("2. Check individual videos for member-only status") 
        print("3. Catch exceptions to detect member-only videos")