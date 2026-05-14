name: Download multiple Videos from HQPorner

on:
  workflow_dispatch:
    inputs:
      video_url_1:
        description: 'آدرس ویدیو 1 را وارد کنید'
        required: true
        type: string
      video_url_2:
        description: 'آدرس ویدیو 2 را وارد کنید'
        required: true
        type: string
      video_url_3:
        description: 'آدرس ویدیو 3 را وارد کنید'
        required: true
        type: string
      video_url_4:
        description: 'آدرس ویدیو 4 را وارد کنید'
        required: true
        type: string
      video_url_5:
        description: 'آدرس ویدیو 5 را وارد کنید'
        required: true
        type: string
      video_url_6:
        description: 'آدرس ویدیو 6 را وارد کنید'
        required: true
        type: string
      video_url_7:
        description: 'آدرس ویدیو 7 را وارد کنید'
        required: true
        type: string
      video_url_8:
        description: 'آدرس ویدیو 8 را وارد کنید'
        required: true
        type: string
      video_url_9:
        description: 'آدرس ویدیو 9 را وارد کنید'
        required: true
        type: string
      video_url_10:
        description: 'آدرس ویدیو 10 را وارد کنید'
        required: true
        type: string
      quality:
        description: 'کیفیت (360, 720, 1080)'
        required: false
        default: '1080'
        type: choice
        options:
          - '1080'
          - '720'
          - '360'

jobs:
  download:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      
      - name: Install hqporner-api
        run: pip install hqporner-api
      
      - name: Run multi-download script
        run: python multi_download.py
        env:
          VIDEO_URL_1: ${{ github.event.inputs.video_url_1 }}
          VIDEO_URL_2: ${{ github.event.inputs.video_url_2 }}
          VIDEO_URL_3: ${{ github.event.inputs.video_url_3 }}
          VIDEO_URL_4: ${{ github.event.inputs.video_url_4 }}
          VIDEO_URL_5: ${{ github.event.inputs.video_url_5 }}
          VIDEO_URL_6: ${{ github.event.inputs.video_url_6 }}
          VIDEO_URL_7: ${{ github.event.inputs.video_url_7 }}
          VIDEO_URL_8: ${{ github.event.inputs.video_url_8 }}
          VIDEO_URL_9: ${{ github.event.inputs.video_url_9 }}
          VIDEO_URL_10: ${{ github.event.inputs.video_url_10 }}
          VIDEO_QUALITY: ${{ github.event.inputs.quality }}
      
      - uses: actions/upload-artifact@v4
        with:
          name: downloaded-videos
          path: downloaded_videos/
          retention-days: 7
