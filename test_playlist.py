#!/usr/bin/env python3
"""
Test script to verify yt-dlp can extract playlist data and member-only video info
"""

import yt_dlp
import json
from datetime import datetime

def test_playlist_extraction():
    playlist_url = "https://www.youtube.com/playlist?list=PLO_DkCSmTKMNMgr-JKMDV2Sw2HW59LMvc"
    
    # Configure yt-dlp options
    ydl_opts = {
        'quiet': True,
        'extract_flat': False,  # Get full video info
        'writeinfojson': False,
        'no_warnings': True,
        'ignoreerrors': True,  # Continue on errors
    }
    
    print(f"Testing playlist: {playlist_url}")
    print("=" * 60)
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("Extracting playlist info...")
            info = ydl.extract_info(playlist_url, download=False)
            
            if not info:
                print("❌ Failed to extract playlist info")
                return
            
            # Print playlist metadata
            print(f"✅ Playlist Title: {info.get('title', 'Unknown')}")
            print(f"✅ Playlist ID: {info.get('id', 'Unknown')}")
            print(f"✅ Total Videos: {len(info.get('entries', []))}")
            print()
            
            # Analyze first few videos
            videos = info.get('entries', [])
            for i, video in enumerate(videos[:5]):  # Test first 5 videos
                if video is None:
                    continue
                    
                print(f"Video {i+1}:")
                print(f"  ID: {video.get('id', 'Unknown')}")
                print(f"  Title: {video.get('title', 'Unknown')}")
                print(f"  URL: {video.get('webpage_url', 'Unknown')}")
                print(f"  Availability: {video.get('availability', 'Unknown')}")
                print(f"  Is Live: {video.get('is_live', False)}")
                
                # Check for member-only indicators
                availability = video.get('availability', '')
                live_status = video.get('live_status', '')
                
                is_member_only = (
                    availability in ['premium_only', 'subscriber_only'] or
                    'member' in availability.lower() or
                    'premium' in availability.lower()
                )
                
                print(f"  Member Only: {is_member_only}")
                print(f"  Live Status: {live_status}")
                print("-" * 40)
            
            # Save sample data for analysis
            sample_data = {
                'playlist_id': info.get('id'),
                'playlist_title': info.get('title'),
                'total_videos': len(videos),
                'extracted_at': datetime.now().isoformat(),
                'sample_videos': []
            }
            
            for video in videos[:3]:  # Save first 3 videos as sample
                if video:
                    sample_data['sample_videos'].append({
                        'id': video.get('id'),
                        'title': video.get('title'),
                        'availability': video.get('availability'),
                        'live_status': video.get('live_status'),
                        'is_live': video.get('is_live'),
                        'webpage_url': video.get('webpage_url')
                    })
            
            with open('sample_playlist_data.json', 'w') as f:
                json.dump(sample_data, f, indent=2)
            
            print(f"✅ Sample data saved to sample_playlist_data.json")
            print(f"✅ Extraction successful! Found {len(videos)} videos")
            
    except Exception as e:
        print(f"❌ Error extracting playlist: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_playlist_extraction()
    if success:
        print("\n🎉 yt-dlp successfully extracted playlist data!")
        print("✅ Ready to proceed with implementation")
    else:
        print("\n❌ yt-dlp extraction failed - need to investigate")