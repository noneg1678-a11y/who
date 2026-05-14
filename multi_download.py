import sys
import os
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def download_video(video_url, quality, index):
    """دانلود یک ویدیو با threading"""
    try:
        print(f"\n[ویدیو {index}] شروع دانلود: {video_url}")
        
        from hqporner_api.api import Client
        
        client = Client()
        video = client.get_video(video_url)
        
        print(f"[ویدیو {index}] عنوان: {video.title}")
        
        # ایجاد پوشه مخصوص هر ویدیو
        download_path = f"downloaded_videos/video_{index}/"
        os.makedirs(download_path, exist_ok=True)
        
        # دانلود ویدیو
        video.download(
            quality=quality,
            path=download_path
        )
        
        print(f"[ویدیو {index}] ✅ دانلود کامل شد!")
        return True, index, video.title
        
    except Exception as e:
        print(f"[ویدیو {index}] ❌ خطا: {e}")
        return False, index, str(e)

def main():
    # گرفتن لینک‌ها از environment variables
    video_urls = []
    for i in range(1, 11):
        url = os.environ.get(f'VIDEO_URL_{i}')
        if url and url.strip():
            video_urls.append((i, url.strip()))
    
    if not video_urls:
        print("خطا: هیچ لینکی وارد نشده است!")
        sys.exit(1)
    
    quality = os.environ.get('VIDEO_QUALITY', '1080')
    print(f"کیفیت انتخابی: {quality}")
    print(f"تعداد ویدیوهای برای دانلود: {len(video_urls)}")
    print("=" * 50)
    
    # دانلود همزمان با حداکثر ۳ تا ترد همزمان (برای جلوگیری از ban شدن)
    max_workers = min(3, len(video_urls))
    results = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(download_video, url, quality, idx): idx 
            for idx, url in video_urls
        }
        
        for future in as_completed(futures):
            success, idx, message = future.result()
            results.append((success, idx, message))
    
    # گزارش نهایی
    print("\n" + "=" * 50)
    print("گزارش نهایی دانلود:")
    successful = [r for r in results if r[0]]
    failed = [r for r in results if not r[0]]
    
    print(f"✅ موفق: {len(successful)} ویدیو")
    print(f"❌ ناموفق: {len(failed)} ویدیو")
    
    if failed:
        print("\nویدیوهای ناموفق:")
        for _, idx, error in failed:
            print(f"  - ویدیو {idx}: {error}")
    
    # نمایش فایل‌های دانلود شده
    print("\nفایل‌های ذخیره شده:")
    for root, dirs, files in os.walk("downloaded_videos"):
        for file in files:
            file_path = os.path.join(root, file)
            size = os.path.getsize(file_path) / (1024 * 1024)
            print(f"  {file_path} ({size:.2f} MB)")
    
    if failed:
        sys.exit(1)

if __name__ == "__main__":
    main()
