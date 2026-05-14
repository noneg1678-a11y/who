import sys
import os
import warnings

# غیرفعال کردن HTTP/2 برای رفع خطای اول
os.environ["HQPORNER_USE_HTTP2"] = "false"

def main():
    if len(sys.argv) < 2:
        print("Error: No video URL provided")
        sys.exit(1)
    
    video_url = sys.argv[1]
    print(f"Starting download for: {video_url}")
    
    os.makedirs("downloaded_video", exist_ok=True)
    
    try:
        from hqporner_api.api import Client
        
        # ایجاد کلاینت با غیرفعال کردن HTTP/2
        client = Client(use_http2=False)
        print("Connected to API (HTTP/2 disabled)")
        
        print("Fetching video info...")
        video = client.get_video(video_url)
        
        print(f"Title: {video.title}")
        
        # بررسی وجود attributeها با hasattr
        if hasattr(video, 'duration'):
            print(f"Duration: {video.duration} seconds")
        
        print("Downloading video (this may take a while)...")
        video.download(output_path="downloaded_video")
        
        print("SUCCESS: Video downloaded!")
        
        # نمایش فایل دانلود شده
        for file in os.listdir("downloaded_video"):
            if file.endswith((".mp4", ".ts", ".m3u8")):
                file_path = os.path.join("downloaded_video", file)
                size = os.path.getsize(file_path) / (1024 * 1024)
                print(f"Saved file: {file} ({size:.2f} MB)")
        
        if not any(f.endswith(".mp4") for f in os.listdir("downloaded_video")):
            print("Warning: No MP4 file found. Listing all files in download directory:")
            for file in os.listdir("downloaded_video"):
                print(f"  - {file}")
                
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
