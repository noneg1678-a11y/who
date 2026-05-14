import sys
import os
from hqporner_api.api import Client, Quality

def main():
    # دریافت آدرس ویدیو از آرگومان خط فرمان
    if len(sys.argv) < 2:
        print("Error: Please provide video URL")
        sys.exit(1)
    
    video_url = sys.argv[1]
    
    print(f"Processing video: {video_url}")
    
    # ایجاد پوشه برای ذخیره ویدیو
    output_dir = "downloaded_video"
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # ایجاد کلاینت و دریافت اطلاعات ویدیو
        print("Connecting to API...")
        client = Client()
        
        print("Fetching video information...")
        video = client.get_video(video_url)
        
        print(f"Video Title: {video.title}")
        print(f"Video Duration: {video.duration} seconds")
        print(f"Available qualities: {video.available_qualities}")
        
        # دانلود ویدیو
        print("Downloading video...")
        video.download(
            quality=Quality.BEST,
            output_path=output_dir
        )
        
        print("✅ Download completed successfully!")
        
        # لیست فایل های دانلود شده
        for filename in os.listdir(output_dir):
            if filename.endswith('.mp4'):
                file_path = os.path.join(output_dir, filename)
                file_size = os.path.getsize(file_path) / (1024 * 1024)
                print(f"Saved file: {filename} ({file_size:.2f} MB)")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
