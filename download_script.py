import sys
import os

# غیرفعال کردن HTTP/2 از طریق متغیر محیطی قبل از import کتابخانه
os.environ["HTTPX_HTTP2"] = "0"

def main():
    if len(sys.argv) < 2:
        print("Error: No video URL provided")
        sys.exit(1)
    
    video_url = sys.argv[1]
    print(f"Starting download for: {video_url}")
    
    os.makedirs("downloaded_video", exist_ok=True)
    
    try:
        from hqporner_api.api import Client
        
        # بدون هیچ پارامتری کلاینت را بساز
        client = Client()
        print("Connected to API")
        
        print("Fetching video info...")
        video = client.get_video(video_url)
        
        print(f"Title: {video.title}")
        
        # بررسی duration اگر وجود داشت
        if hasattr(video, 'duration') and video.duration:
            print(f"Duration: {video.duration} seconds")
        
        print("Downloading video...")
        video.download(output_path="downloaded_video")
        
        print("SUCCESS: Video downloaded!")
        
        # نمایش فایل دانلود شده
        files = os.listdir("downloaded_video")
        if files:
            for file in files:
                file_path = os.path.join("downloaded_video", file)
                if os.path.isfile(file_path):
                    size = os.path.getsize(file_path) / (1024 * 1024)
                    print(f"Saved: {file} ({size:.2f} MB)")
        else:
            print("Warning: No files found in download directory")
                
    except Exception as e:
        print(f"ERROR: {e}")
        # نمایش جزئیات بیشتر خطا
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
