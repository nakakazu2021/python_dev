## 注意事項
exe化　dll必要
 * libzbar-64.dll
 * libiconv.dll
 * opencv_videoio_ffmpeg480_64.dll

```
pyinstaller main.py --onefile -add-binary=".\dll\libzbar-64.dll;." --add-binary=".\dll\libiconv.dll;." --add-binary=".\dll\opencv_videoio_ffmpeg480_64.dll;."
```
