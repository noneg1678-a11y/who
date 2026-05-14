import sys
import os

def main():
    if len(sys.argv) < 2:
        print("Error: No video URL provided")
        sys.exit(1)
    
    video_url = sys.argv[1]
    print(f"Starting download for: {video_url}")
    
    os.makedirs("downloaded_video", exist_ok=True)
    
    try:
        from hqporner_api.api import Client
        
        client = Client()
        print("Connected to API")
        
        print("Fetching video info...")
        video = client.get_video(video_url)
        
        print(f"Title: {video.title}")
        print(f"Duration: {video.length}")
        print(f"Available qualities: {video.video_qualities}")
        print(f"Pornstars: {', '.join(video.pornstars) if video.pornstars else 'N/A'}")
        print(f"Tags: {', '.join(video.tags[:5])}...")
        
        print("\nStarting download...")
        # استفاده از پارامترهای صحیح متد download
        video.download(
            quality='1080',  # یا '720' یا '360'
            path='downloaded_video/'
        )
        
        print("\nSUCCESS: Video downloaded!")
        
        # نمایش فایل دانلود شده
        for file in os.listdir("downloaded_video"):
            file_path = os.path.join("downloaded_video", file)
            if os.path.isfile(file_path):
                size = os.path.getsize(file_path) / (1024 * 1024)
                print(f"Saved: {file} ({size:.2f} MB)")
                
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
