# py_vp9
Script to encode high efficiency video for web, using ffmpeg and libvpx. Manipulate `settings.yaml` instead of the CLI.

Requires ffmpeg to be installed and in your `PATH`.

### Usage

```
pip install pyyaml
python encode.py
```

## Example settings file

```
---
InputFilename: 2021-10-26_18-46-11
InputExtension: '.mp4'
OutputExtension: '.webm'
FileDir: C:/video/recordings/
FolderDir: C:/Users/Saturn/Videos/
Debug: true
SkipEncoding: false
Batch: false
Scale: true
ScaleMode: lanczos
Environment: dev
Mode: file
OutFileDir: C:/video/finished
OutFolderDir: C:/video/
OutResolution: 640x480
CRFDefault: '26'
CRF:
  - '50'
  - '30'
  - '20'
  - '12'
  - '8'

```

### Features:
- _File_: Transcode a single input video to vp9
	- Default crf: 30
- _Batch_: Transcode a single input video to multiple quality option thresholds based on settings (Batch mode)
	- Default crf values: 50, 30, 20, 12, 8 (it may be preferable to use crf 4 or lower for exceptional IQ)


### Encoding settings:
- Two-pass.
- Optional downscaling by integer with lanczos (`1280x920` -> `640x480`).
- libvpx-vp9 encoding. From the [ffmpeg docs](https://trac.ffmpeg.org/wiki/Encode/VP9):
  >libvpx-vp9 can save about 20–50% bitrate compared to libx264 (the default H.264 encoder), while retaining the same visual quality.
- Variable bitrate switch `-b:v` is set to 0, because the high quality use case prefers that image quality is not variable.
- Constant rate factor switch `-crf` is set by the user to achieve the desired consistent image quality across the length of the video. Good defaults are between 8 and 30, but more research is needed.

### Coming soon
- AV1 encoding with rav1e
- `Folder` mode: Transcode all items inside a single folder, with or without batch mode.
- `-deadline` and `-cpu-used` arguments to further optimize IQ
