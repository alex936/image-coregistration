import os
from pathlib import Path

import imageio


def get_file_paths(image_root_path, file_extensions=("png",)):
    image_file_paths = []

    for root, dirs, filenames in os.walk(image_root_path):
        filenames = sorted(filenames)
        for filename in filenames:
            input_path = os.path.abspath(root)
            file_path = os.path.join(input_path, filename)

            file_extension = filename.split(".")[-1]
            if file_extension.lower() in file_extensions:
                image_file_paths.append(Path(file_path))

        break

    return image_file_paths


def make_gif(folder):
    frame_paths = get_file_paths(folder)
    frame_paths = [p for p in frame_paths if (p.name != "output.png") and (p.name != "errors.png")]
    frame_paths = sorted(frame_paths, key=lambda x: int(str(x).split('_')[-1].split('.')[0]))
    gif_output_path = os.path.join(folder, "progress.gif")
    durations = [0.2] * len(frame_paths)
    durations[-1] = 2
    images = [imageio.imread(frame_path) for frame_path in frame_paths]
    imageio.mimsave(gif_output_path, images, duration=durations)


if __name__ == "__main__":
    make_gif('output')
