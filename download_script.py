import sys
import os
import random
import string
import zipfile
from pathlib import Path

def create_random_folder():
    """ایجاد پوشه با نام رندوم 5 رقمی"""
    random_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    folder_path = random_name
    os.makedirs(folder_path, exist_ok=True)
    print(f"Created folder: {folder_path}")
    return folder_path

def split_file(file_path, chunk_size_mb=90):
    """
    تقسیم فایل به چند قسمت
    خروجی: file.zip.001, file.zip.002, ...
    """
    chunk_size = chunk_size_mb * 1024 * 1024  # تبدیل به بایت
    file_size = os.path.getsize(file_path)
    
    if file_size <= chunk_size:
        print(f"File size ({file_size/(1024*1024):.2f} MB) is less than {chunk_size_mb} MB, no splitting needed")
        return [file_path]
    
    print(f"Splitting {file_size/(1024*1024):.2f} MB into {chunk_size_mb} MB chunks...")
    
    # نام فایل‌های خروجی
    base_name = file_path + ".part"
    
    parts = []
    with open(file_path, 'rb') as f:
        part_num = 1
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            
            part_name = f"{base_name}{part_num:03d}"
            parts.append(part_name)
            
            with open(part_name, 'wb') as part_file:
                part_file.write(chunk)
            
            print(f"  Created: {part_name} ({len(chunk)/(1024*1024):.2f} MB)")
            part_num += 1
    
    # حذف فایل اصلی
    os.remove(file_path)
    print(f"Removed original file: {file_path}")
    
    return parts

def create_split_zip(folder_path, video_file):
    """
    ایجاد فایل زیپ و سپس اسپلیت کردن آن
    """
    zip_path = os.path.join(folder_path, "video.zip")
    
    # ساخت فایل زیپ
    print(f"Creating zip file: {zip_path}")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(video_file, os.path.basename(video_file))
    
    # حذف فایل اصلی ویدیو
    os.remove(video_file)
    print(f"Removed original video file")
    
    # چک کردن سایز زیپ
    zip_size = os.path.getsize(zip_path)
    print(f"Zip size: {zip_size/(1024*1024):.2f} MB")
    
    if zip_size > 90 * 1024 * 1024:
        print("Zip is larger than 90MB, splitting...")
        # اسپلیت کردن فایل زیپ
        parts = split_file(zip_path, 90)
        
        # تغییر نام فایل‌ها به فرمت دلخواه
        new_parts = []
        for i, part in enumerate(parts):
            if i == 0:
                new_name = os.path.join(folder_path, "video.zip")
            else:
                new_name = os.path.join(folder_path, f"video.z{i:02d}")
            
            os.rename(part, new_name)
            new_parts.append(new_name)
            print(f"  Renamed to: {os.path.basename(new_name)}")
        
        return new_parts
    else:
        return [zip_path]

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
        
        video_file = os.path.join(output_folder, downloaded_files[0])
        print(f"\nDownloaded: {video_file}")
        file_size = os.path.getsize(video_file) / (1024 * 1024)
        print(f"File size: {file_size:.2f} MB")
        
        # ایجاد زیپ و اسپلیت کردن
        print("\n" + "="*50)
        print("Creating zip and splitting if needed...")
        print("="*50)
        
        final_files = create_split_zip(output_folder, video_file)
        
        print("\n" + "="*50)
        print("DOWNLOAD COMPLETE!")
        print("="*50)
        print(f"Output folder: {output_folder}/")
        print("Files created:")
        for f in final_files:
            size = os.path.getsize(f) / (1024 * 1024)
            print(f"  - {os.path.basename(f)} ({size:.2f} MB)")
        
        # ذخیره نام پوشه در فایل برای استفاده بعدی
        with open('last_folder.txt', 'w') as f:
            f.write(output_folder)
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
