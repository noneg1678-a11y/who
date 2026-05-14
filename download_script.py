import sys
import os

def main():
    # گرفتن آدرس ویدیو از ورودی
    if len(sys.argv) < 2:
        print("Error: No video URL provided")
        sys.exit(1)
    
    video_url = sys.argv[1]
    print(f"Starting download for: {video_url}")
    
    # ایجاد پوشه برای ذخیره
    os.makedirs("downloaded_video", exist_ok=True)
    
    try:
        from hqporner_api.api import Client
        
        print("Connecting to API...")
        client = Client()
        
        print("Fetching video info...")
        video = client.get_video(video_url)
        
        print(f"Title: {video.title}")
        
        # نمایش کیفیت‌های موجود
        print("Available qualities:", video.available_qualities)
        
        print("Downloading...")
        # بدون指定 کیفیت، پیش‌فرض بهترین کیفیت را می‌گیرد
        video.download(output_path="downloaded_video")
        
        print("SUCCESS: Video downloaded!")
        
        # نمایش اطلاعات فایل دانلود شده
        for file in os.listdir("downloaded_video"):
            if file.endswith(".mp4"):
                size = os.path.getsize(f"downloaded_video/{file}") / (1024 * 1024)
                print(f"File: {file} ({size:.2f} MB)")
                
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
