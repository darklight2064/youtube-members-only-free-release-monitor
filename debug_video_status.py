#!/usr/bin/env python3
"""
Debug script to analyze video status detection logic
"""

import yt_dlp
import json
from datetime import datetime

def debug_video_status():
    playlist_url = "https://www.youtube.com/playlist?list=PLO_DkCSmTKMNMgr-JKMDV2Sw2HW59LMvc"
    
    print("🔍 DEBUG: Analyzing video status detection")
    print("=" * 70)
    
    # Step 1: Get playlist structure
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(playlist_url, download=False)
            videos = info.get('entries', [])[:3]
            
            print(f"📋 Playlist: {info.get('title')}")
            print(f"📊 Total videos: {len(info.get('entries', []))}")
            print(f"🎯 Testing first 3 videos\n")
            
            for i, video in enumerate(videos, 1):
                if not video:
                    continue
                    
                video_id = video.get('id')
                video_title = video.get('title')
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                
                print(f"🎥 Video {i}: {video_title}")
                print(f"   ID: {video_id}")
                print(f"   URL: {video_url}")
                
                # Test different extraction methods
                test_video_detailed(video_id, video_url)
                print("-" * 50)
    
    except Exception as e:
        print(f"❌ Error: {e}")

def test_video_detailed(video_id, video_url):
    """Test video with different yt-dlp configurations"""
    
    print(f"\n📋 Testing extraction methods for {video_id}:")
    
    # Method 1: Basic extraction
    print("   Method 1: Basic extraction")
    test_basic_extraction(video_url)
    
    # Method 2: With cookies simulation
    print("   Method 2: Simulate extraction with more options")
    test_enhanced_extraction(video_url)
    
    # Method 3: Extract metadata only
    print("   Method 3: Metadata only")
    test_metadata_only(video_url)

def test_basic_extraction(video_url):
    """Test basic video extraction"""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
        'skip_download': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
            if info:
                print(f"      ✅ SUCCESS: Extracted info")
                print(f"      📝 Title: {info.get('title', 'N/A')}")
                print(f"      🔓 Availability: {info.get('availability', 'N/A')}")
                print(f"      👤 Uploader: {info.get('uploader', 'N/A')}")
                print(f"      📅 Upload date: {info.get('upload_date', 'N/A')}")
                print(f"      🎬 Duration: {info.get('duration', 'N/A')}")
                print(f"      👁️ View count: {info.get('view_count', 'N/A')}")
                print(f"      🔒 Is live: {info.get('is_live', 'N/A')}")
                print(f"      📺 Live status: {info.get('live_status', 'N/A')}")
                
                # Check for member-only indicators
                member_indicators = []
                availability = info.get('availability', '').lower()
                if 'premium' in availability or 'member' in availability:
                    member_indicators.append(f"availability={availability}")
                
                title = info.get('title', '').lower()
                if '会员' in title or 'member' in title:
                    member_indicators.append(f"title contains member keywords")
                
                print(f"      🔍 Member indicators: {member_indicators if member_indicators else 'None'}")
                
                # Our current logic
                is_member_only = False  # Since we successfully extracted
                print(f"      🎯 CURRENT LOGIC: is_member_only = {is_member_only}")
                
            else:
                print(f"      ❌ FAILED: No info extracted")
                print(f"      🎯 CURRENT LOGIC: is_member_only = True")
                
    except Exception as e:
        error_msg = str(e)
        print(f"      ❌ EXCEPTION: {error_msg}")
        
        # Check for member-only keywords in error
        member_keywords = ['member', 'premium', 'subscriber', 'level']
        has_member_keywords = any(keyword in error_msg.lower() for keyword in member_keywords)
        print(f"      🔍 Error contains member keywords: {has_member_keywords}")
        print(f"      🎯 CURRENT LOGIC: is_member_only = {has_member_keywords}")

def test_enhanced_extraction(video_url):
    """Test with enhanced options"""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
        'skip_download': True,
        'extract_flat': False,
        'writeinfojson': False,
        'simulate': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
            if info:
                print(f"      ✅ Enhanced extraction successful")
                print(f"      🔓 Availability: {info.get('availability', 'N/A')}")
                print(f"      🎬 Extractors: {info.get('extractor', 'N/A')}")
            else:
                print(f"      ❌ Enhanced extraction failed")
                
    except Exception as e:
        print(f"      ❌ Enhanced extraction exception: {str(e)[:100]}...")

def test_metadata_only(video_url):
    """Test metadata-only extraction"""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
        'skip_download': True,
        'writeinfojson': False,
        'extract_flat': False,
        'playlist_items': '1',
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Try to get just the webpage
            info = ydl.extract_info(video_url, download=False)
            
            if info:
                print(f"      ✅ Metadata extraction successful")
                # Look for specific indicators
                description = info.get('description', '').lower()
                if 'member' in description or '会员' in description:
                    print(f"      🔍 Description contains member keywords")
                else:
                    print(f"      🔍 No member keywords in description")
            else:
                print(f"      ❌ Metadata extraction failed")
                
    except Exception as e:
        print(f"      ❌ Metadata extraction exception: {str(e)[:100]}...")

if __name__ == "__main__":
    debug_video_status()
    
    print("\n" + "=" * 70)
    print("🤔 ANALYSIS QUESTIONS:")
    print("1. Are we correctly identifying member-only videos?")
    print("2. What data is actually available for each video?")
    print("3. Should we change our detection logic?")
    print("4. Are there better indicators we should use?")
    print("=" * 70)