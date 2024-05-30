import imageio.v3 as iio
import shlex
import subprocess
from os import stat
from moviepy.editor import VideoFileClip

SUPPORTED_RESOLUTION = (512, 512)
SUPPORTED_SIZE = 256 * 1024
SUPPORTED_DURATION = 3.0
CODEC = "libvpx-vp9"


def convert_webp_to_webm(files):
    for f in files:
        webm_file = f.replace(".webp", ".webm")
        print(f"Converting {f} to {webm_file}")

        try:
            frames = iio.imread(f, index=..., mode="RGBA")

            iio.imwrite(
                webm_file,
                frames,
                codec="vp9",
                plugin="pyav",
                is_batch=True,
                in_pixel_format="rgba",
                out_pixel_format="yuva420p",
            )

            with VideoFileClip(webm_file) as webm:
                ffmpeg_params = []

                # Check if webm is too lengthy
                if webm.duration > SUPPORTED_DURATION:
                    print(
                        f"{webm_file} is too lengthy ({webm.duration}). Trim it to {SUPPORTED_DURATION} seconds"
                    )
                    ffmpeg_params.append(f"-t {SUPPORTED_DURATION}")

                # Check if webm has correct resolution
                if webm.w != SUPPORTED_RESOLUTION[0] or webm.h != SUPPORTED_RESOLUTION[1]:
                    print(
                        f"{webm_file} has incorrect resolution {webm.size}. Resize it to {SUPPORTED_RESOLUTION}"
                    )
                    ffmpeg_params.append(
                        f"-vf scale={SUPPORTED_RESOLUTION[0]}:{SUPPORTED_RESOLUTION[1]}"
                    )

            rm_old_webm = lambda file: shlex.split(f"rm {file}")
            if ffmpeg_params:
                new_webm_file = webm_file[:-5] + "_0.webm"
                ffmpeg_cmd = shlex.split(
                    f"ffmpeg -y -i {webm_file} -c:v {CODEC} {' '.join(ffmpeg_params)} {new_webm_file}"
                )
                subprocess.run(ffmpeg_cmd, check=True)
                subprocess.run(rm_old_webm(webm_file))
                webm_file = new_webm_file

            # Check if webm_file has correct size
            if stat(webm_file).st_size > SUPPORTED_SIZE:
                new_webm_file = webm_file[:-5] + "_1.webm"
                print(
                    f"{webm_file} has incorrect size ({str(stat(webm_file).st_size / 1024) + ' kB'}). Compress it to {SUPPORTED_SIZE} kB"
                )
                ffmpeg_cmd = shlex.split(
                    f"ffmpeg -y -i {webm_file} -c:v {CODEC} -b:v {SUPPORTED_SIZE} {new_webm_file}"
                )
                subprocess.run(ffmpeg_cmd, check=True)
                subprocess.run(rm_old_webm(webm_file))
                webm_file = new_webm_file

        except Exception as ex:
            print(f"Error converting {f}: {ex}")


def resize_image(img):
    img.thumbnail(SUPPORTED_RESOLUTION)
    return img
