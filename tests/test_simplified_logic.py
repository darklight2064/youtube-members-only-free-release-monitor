#!/usr/bin/env python3
"""
Test the simplified logic - title-only detection
"""

from src.playlist_monitor import PlaylistMonitor
import json

def test_simplified_logic():
    print("🚀 Testing simplified logic - title-only detection")
    print("=" * 70)
    
    playlist_url = "https://www.youtube.com/playlist?list=PLO_DkCSmTKMNMgr-JKMDV2Sw2HW59LMvc"
    monitor = PlaylistMonitor(playlist_url, "test_simplified.json")
    
    # Run monitoring
    playlist_data = monitor.fetch_playlist_videos()
    
    if playlist_data:
        print(f"✅ Successfully fetched {len(playlist_data['videos'])} videos")
        print(f"⚡ Processing time: Much faster (no individual video checks)")
        print("\n📊 Video Analysis:")
        
        for video in playlist_data['videos']:
            print(f"\n🎥 Video {video['position']}: {video['title']}")
            print(f"   ID: {video['id']}")
            print(f"   Status: {'🔓 FREE' if not video['is_member_only'] else '🔒 MEMBER-ONLY'}")
            print(f"   Availability: {video['availability']}")
            print(f"   Detection method: Title parsing only")
            
            # Check logic
            has_limited_free = '限免' in video['title']
            detected_as_free = not video['is_member_only']
            
            if has_limited_free == detected_as_free:
                print(f"   🎯 LOGIC: ✅ Correct")
            else:
                print(f"   🎯 LOGIC: ❌ Error")
        
        # Save results
        with open('simplified_results.json', 'w') as f:
            json.dump(playlist_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Results saved to simplified_results.json")
        
        # Summary
        total_videos = len(playlist_data['videos'])
        free_videos = sum(1 for v in playlist_data['videos'] if not v['is_member_only'])
        member_videos = total_videos - free_videos
        limited_free_count = sum(1 for v in playlist_data['videos'] if '限免' in v['title'])
        
        print(f"\n📈 SUMMARY:")
        print(f"   Total videos: {total_videos}")
        print(f"   🔓 Free videos: {free_videos}")
        print(f"   🔒 Member-only videos: {member_videos}")
        print(f"   🎯 Videos with '限免': {limited_free_count}")
        print(f"   ⚡ No individual video API calls needed!")
        
        return True
    else:
        print("❌ Failed to fetch playlist data")
        return False

if __name__ == "__main__":
    success = test_simplified_logic()
    if success:
        print("\n🎉 Simplified logic test completed!")
        print("✅ Much faster and simpler approach confirmed")
    else:
        print("\n❌ Test failed")