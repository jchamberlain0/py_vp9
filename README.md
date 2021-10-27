# py_vp9

Encode high efficiency video for web, using [ffmpeg](https://ffmpeg.org/) and [libvpx](https://github.com/webmproject/libvpx).

### Features
- **File**: Transcode a video to a single vp9 video file.
	- Default crf: 30
- **Batch**: Transcode a video to multiple vp9 files, at user-defined quality thresholds. This is useful for providing users with quality options.
	- Default crf values: 50, 30, 20, 12, 8

### Get started

Install dependencies:
  ```
  sudo apt install ffmpeg
  pip install pyyaml
  ```
Modify `settings.yaml` as needed:
  ```
  FileDir: C:/video/
  ...
  ```
Encode:
  ```
  python encode.py
  ```

<br>

### Settings

| Field  | Example | Description |
| ---: | -------: | :--------- |
| `InputFileDir` | C:/video/ | Path to input video, with trailing slash. |
| `InputFilename` | 2021-10-26 | Filename of the input video without its extension. |
| `InputExtension` | .mp4 | The extension of the input video. |
| `OutFileDir` | C:/video/web/ | Output directory, with trailing slash. |
| `OutputExtension` | .webm | Container format. `.webm` is highly recommended over `.mkv` |
| `Scale` | true | Flag: Scale output. Intended for integer downscaling.
| `OutResolution` | 640x480 | String resolution in the format WIDTHxHEIGHT. Ignored when not scaling. |
| `ScaleMode` | lanczos | [Algorithm](https://ffmpeg.org/ffmpeg-scaler.html#toc-Scaler-Options) used to resample image when `Scale` is on. |
| `Batch` | false | Flag: encode multiple quality options defined in the `CRF` array. |
| `CRFDefault` | 20 | String crf value to use in single-file mode. |
| `CRF` | ['50,'30','12'] | Array of string crf values to encode in batch mode. |
| `Debug` | true | Flag: additional logging. |
| `SkipEncoding` | false | Flag: print args without executing them. |

<br>

### Encoding details
- Two-pass.
- Optional downscaling by integer with lanczos (`1280x920` -> `640x480`).
- libvpx-vp9 encoding. From the [ffmpeg docs](https://trac.ffmpeg.org/wiki/Encode/VP9):
  >libvpx-vp9 can save about 20–50% bitrate compared to libx264 (the default H.264 encoder), while retaining the same visual quality.
- Variable bitrate switch `-b:v` is set to 0, because the high quality use case prefers that image quality is not variable.
- Constant rate factor switch `-crf` is set by the user to achieve the desired consistent image quality across the length of the video. Good defaults are between 8 and 30, but more research is needed.

<br>

### Future
- Improve workflow by starting the encode without needing to copy/paste filenames. Drag & drop?
- AV1 encoding with rav1e, when it has better support
- `Folder` mode: Transcode all items inside a single folder, with or without batch mode.
- `-deadline` and `-cpu-used` arguments to further optimize IQ
