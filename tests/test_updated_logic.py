#!/usr/bin/env python3
"""
Test the updated detection logic with '限免' title parsing
"""

from src.playlist_monitor import PlaylistMonitor
import json

def test_updated_logic():
    print("🧪 Testing updated detection logic with '限免' title parsing")
    print("=" * 70)
    
    playlist_url = "https://www.youtube.com/playlist?list=PLO_DkCSmTKMNMgr-JKMDV2Sw2HW59LMvc"
    monitor = PlaylistMonitor(playlist_url, "test_state.json")
    
    # Run monitoring
    playlist_data = monitor.fetch_playlist_videos()
    
    if playlist_data:
        print(f"✅ Successfully fetched {len(playlist_data['videos'])} videos")
        print("\n📊 Video Analysis:")
        
        for video in playlist_data['videos']:
            print(f"\n🎥 Video {video['position']}: {video['title']}")
            print(f"   ID: {video['id']}")
            print(f"   Status: {'🔓 FREE' if not video['is_member_only'] else '🔒 MEMBER-ONLY'}")
            print(f"   Availability: {video['availability']}")
            print(f"   Title contains '限免': {'✅' if '限免' in video['title'] else '❌'}")
            
            # Check if logic worked correctly
            has_limited_free = '限免' in video['title']
            detected_as_free = not video['is_member_only']
            
            if has_limited_free and detected_as_free:
                print(f"   🎯 LOGIC: ✅ Correctly detected as free from title")
            elif has_limited_free and not detected_as_free:
                print(f"   🎯 LOGIC: ❌ Should be free but marked as member-only")
            elif not has_limited_free and not detected_as_free:
                print(f"   🎯 LOGIC: ✅ Correctly detected as member-only")
            else:
                print(f"   🎯 LOGIC: ⚠️ Unexpected state")
        
        # Save for manual inspection
        with open('test_detection_results.json', 'w') as f:
            json.dump(playlist_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Results saved to test_detection_results.json")
        
        # Summary
        total_videos = len(playlist_data['videos'])
        free_videos = sum(1 for v in playlist_data['videos'] if not v['is_member_only'])
        member_videos = total_videos - free_videos
        
        print(f"\n📈 SUMMARY:")
        print(f"   Total videos: {total_videos}")
        print(f"   🔓 Free videos: {free_videos}")
        print(f"   🔒 Member-only videos: {member_videos}")
        
        # Check for '限免' detection
        limited_free_count = sum(1 for v in playlist_data['videos'] if '限免' in v['title'])
        print(f"   🎯 Videos with '限免' in title: {limited_free_count}")
        
        return True
    else:
        print("❌ Failed to fetch playlist data")
        return False

if __name__ == "__main__":
    success = test_updated_logic()
    if success:
        print("\n🎉 Test completed successfully!")
    else:
        print("\n❌ Test failed")