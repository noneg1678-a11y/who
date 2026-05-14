import sys
import os

os.environ["HTTPX_HTTP2"] = "0"

def main():
    if len(sys.argv) < 2:
        print("Usage: python inspect_video.py <video_url>")
        sys.exit(1)
    
    video_url = sys.argv[1]
    print(f"Inspecting: {video_url}\n")
    print("=" * 60)
    
    try:
        from hqporner_api.api import Client
        
        client = Client()
        video = client.get_video(video_url)
        
        # نمایش همه attribute های موجود
        print("\n📋 ALL ATTRIBUTES AND METHODS:")
        print("=" * 60)
        
        all_attrs = dir(video)
        
        # جدا کردن attribute های خصوصی و معمولی
        public_attrs = [attr for attr in all_attrs if not attr.startswith('_')]
        private_attrs = [attr for attr in all_attrs if attr.startswith('_') and not attr.startswith('__')]
        magic_methods = [attr for attr in all_attrs if attr.startswith('__') and attr.endswith('__')]
        
        print(f"\n🔹 Public attributes/methods ({len(public_attrs)} items):")
        for attr in public_attrs:
            try:
                value = getattr(video, attr)
                if not callable(value):
                    print(f"   • {attr}: {type(value).__name__} = {value}")
                else:
                    print(f"   • {attr}() -> method")
            except:
                print(f"   • {attr} -> (unable to access)")
        
        print(f"\n🔸 Private attributes ({len(private_attrs)} items):")
        for attr in private_attrs[:10]:  # فقط 10 تا اول رو نشون بده
            print(f"   • {attr}")
        if len(private_attrs) > 10:
            print(f"   ... and {len(private_attrs) - 10} more")
        
        print("\n" + "=" * 60)
        print("\n📊 VIDEO INFORMATION:")
        print("=" * 60)
        
        # تلاش برای دریافت اطلاعات متداول
        common_attrs = ['title', 'duration', 'views', 'rating', 'tags', 
                       'uploader', 'upload_date', 'description', 'thumbnail',
                       'url', 'video_url', 'download_url', 'qualities', 
                       'available_qualities', 'formats']
        
        for attr in common_attrs:
            if hasattr(video, attr):
                value = getattr(video, attr)
                if not callable(value):
                    print(f"   {attr}: {value}")
        
        print("\n" + "=" * 60)
        print("\n🎯 TRYING TO GET DOWNLOAD INFO:")
        print("=" * 60)
        
        # بررسی متدهای دانلود
        if hasattr(video, 'download'):
            print("✓ download() method exists")
            import inspect
            sig = inspect.signature(video.download)
            print(f"   download{ sig }")
        
        # بررسی کیفیت‌های موجود
        if hasattr(video, 'qualities'):
            print(f"   qualities: {video.qualities}")
        if hasattr(video, 'available_qualities'):
            print(f"   available_qualities: {video.available_qualities}")
        if hasattr(video, 'formats'):
            print(f"   formats: {video.formats}")
        
        # بررسی دیکشنری داخلی
        if hasattr(video, '__dict__'):
            print(f"\n   Internal __dict__:")
            for key, value in video.__dict__.items():
                if not callable(value):
                    print(f"      {key}: {value}")
                
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
