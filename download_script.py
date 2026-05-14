import sys
import os
import random
import string
import zipfile
import subprocess

def create_random_folder():
    """ایجاد پوشه با نام رندوم 5 رقمی"""
    random_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    folder_path = random_name
    os.makedirs(folder_path, exist_ok=True)
    print(f"Created folder: {folder_path}")
    return folder_path

def main():
    if len(sys.argv) < 2:
        print("Error: No video URL provided")
        sys.exit(1)
    
    video_url = sys.argv[1]
    quality = os.environ.get('VIDEO_QUALITY', '1080')
    
    print(f"Starting download for: {video_url}")
    print(f"Quality: {quality}")
    
    try:
        from hqporner_api.api import Client
        
        # ایجاد پوشه رندوم
        output_folder = create_random_folder()
        
        client = Client()
        print("Connected to API")
        
        print("Fetching video info...")
        video = client.get_video(video_url)
        
        print(f"Title: {video.title}")
        print(f"Duration: {video.length}")
        print(f"Available qualities: {video.video_qualities}")
        
        # دانلود ویدیو
        print("\nDownloading video...")
        video.download(
            quality=quality,
            path=f'{output_folder}/'
        )
        
        # پیدا کردن فایل دانلود شده
        downloaded_files = [f for f in os.listdir(output_folder) if f.endswith('.mp4')]
        
        if not downloaded_files:
            print("ERROR: No video file found after download")
            sys.exit(1)
        
        video_file = downloaded_files[0]
        video_path = os.path.join(output_folder, video_file)
        
        # گرفتن سایز فایل به مگابایت (مثل کد dl2)
        FILE_SIZE = os.path.getsize(video_path)
        FILE_SIZE_MB = FILE_SIZE // (1024 * 1024)
        print(f"File size: {FILE_SIZE_MB} MB")
        
        # ساخت نام رندوم 5 کاراکتری (مثل کد dl2)
        RAND5 = ''.join(random.choices(string.ascii_lowercase, k=5))
        ZIP_NAME = f"{video_file}_{RAND5}.zip"
        
        print(f"ZIP name: {ZIP_NAME}")
        
        # رفتن به پوشه مقصد (مثل کد dl2 که cd می‌کرد)
        original_dir = os.getcwd()
        os.chdir(output_folder)
        
        # زیپ کردن با متد مثل کد dl2
        if FILE_SIZE_MB > 95:
            print("File larger than 95MB, splitting into parts...")
            cmd = f'zip -s 95m "{ZIP_NAME}" "{video_file}"'
            os.system(cmd)
            os.remove(video_file)
            print("File split into parts")
        else:
            print("File smaller than 95MB, zipping without split...")
            cmd = f'zip "{ZIP_NAME}" "{video_file}"'
            os.system(cmd)
            os.remove(video_file)
        
        # برگشت به پوشه اصلی
        os.chdir(original_dir)
        
        print(f"\nSaved to: {output_folder}/{ZIP_NAME}")
        print("Files in folder:")
        os.system(f'ls -la "{output_folder}"')
        
        # ذخیره نام پوشه برای آپلود (مثل کد dl2)
        with open('last_folder.txt', 'w') as f:
            f.write(output_folder)
        
        print("\n" + "="*50)
        print("DOWNLOAD COMPLETE!")
        print("="*50)
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
