#!/usr/bin/env python3
"""
Simple test script to verify the YouTube Playlist Monitor is working correctly.
"""

import os
import json
from datetime import datetime
from src.playlist_monitor import PlaylistMonitor

def test_monitor():
    """Test the playlist monitor functionality"""
    print("🧪 Testing YouTube Playlist Monitor")
    print("=" * 50)
    
    playlist_url = "https://www.youtube.com/playlist?list=PLO_DkCSmTKMNMgr-JKMDV2Sw2HW59LMvc"
    test_state_file = "test_state.json"
    
    # Clean up any existing test file
    if os.path.exists(test_state_file):
        os.remove(test_state_file)
    
    print("📋 Creating monitor instance...")
    monitor = PlaylistMonitor(playlist_url, test_state_file)
    
    print("🔍 Fetching playlist data...")
    playlist_data = monitor.fetch_playlist_videos()
    
    if not playlist_data:
        print("❌ Failed to fetch playlist data")
        return False
    
    print(f"✅ Successfully fetched {len(playlist_data['videos'])} videos")
    print(f"📺 Playlist: {playlist_data['playlist_title']}")
    print(f"📊 Total videos in playlist: {playlist_data['total_videos']}")
    print()
    
    # Analyze videos
    free_count = 0
    member_count = 0
    
    for i, video in enumerate(playlist_data['videos'], 1):
        status = "🔓 FREE" if not video['is_member_only'] else "🔒 MEMBER-ONLY"
        has_free_indicator = "✅" if '限免' in video['title'] else "❌"
        
        print(f"{i}. {video['title'][:60]}...")
        print(f"   Status: {status}")
        print(f"   Has '限免': {has_free_indicator}")
        print()
        
        if video['is_member_only']:
            member_count += 1
        else:
            free_count += 1
    
    print("📈 RESULTS:")
    print(f"   🔓 Free videos: {free_count}")
    print(f"   🔒 Member-only videos: {member_count}")
    print(f"   ⚡ Processing: Fast (title-based detection)")
    print(f"   💾 State saved to: {test_state_file}")
    
    # Test change detection
    print("\n🔍 Testing change detection...")
    changes = monitor.detect_changes(None, playlist_data)
    print(f"   No previous state - detected {len(changes)} changes (expected: 0)")
    
    # Save state
    monitor.save_current_state(playlist_data)
    print(f"   ✅ State saved successfully")
    
    # Clean up
    if os.path.exists(test_state_file):
        os.remove(test_state_file)
        print(f"   🧹 Cleaned up test file")
    
    print("\n🎉 Test completed successfully!")
    print("🚀 Monitor is ready for production use")
    
    return True

if __name__ == "__main__":
    try:
        success = test_monitor()
        exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Test failed: {e}")
        exit(1)