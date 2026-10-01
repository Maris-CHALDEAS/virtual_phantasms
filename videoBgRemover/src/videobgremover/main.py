#!/usr/bin/env python3

import onnxruntime
onnxruntime.preload_dlls()

from rembg import remove, new_session
from PIL import Image
import cv2
import os
import re


def remove_background(input_path, output_path) -> None:
    session = new_session("u2net")
    input_image = Image.open(input_path)
    output_image = remove(input_image, session=session)

    output_image.save(output_path, "PNG")

    print(f"Success! saved {output_path}")

def frames_from_video(input_path, output_dir) -> None:
    vid = cv2.VideoCapture(input_path)

    count, success = 0, True
    while success:
        success, image = vid.read()
        if success:
            cv2.imwrite(f"{output_dir}/frame_{count}.png", image)
            count += 1
    vid.release()


def frame_bg_remove(input_dir, output_dir):

    images = [img for img in os.listdir(input_dir) if img.endswith((".png", ".jpg", "jpeg"))]

    count = 0
    for image in images:
        image_path = os.path.join(input_dir, image)
        output_path = f"{output_dir}/frame_{count}"
        remove_background(image_path, output_path)
        count += 1

    print("INFO: Frames background removed")

def video_from_frames(input_dir, output_dir, fps=60):

    images = [img for img in os.listdir(input_dir) ]


    images.sort(key=lambda f: int(re.sub(r'\D', '', f)))

    print(len(images))

    first_image_path = os.path.join(input_dir, images[0])

    print(first_image_path)
    frame = cv2.imread(first_image_path)

    height, width, _ = frame.shape

    size = (width, height)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_dir, fourcc, fps, size)

    for image in images:
        image_path = os.path.join(input_dir, image)
        video.write(cv2.imread(image_path))
        print("INFO: Vidoe is being written")

    video.release()
    print("INFO: Vidoe have been written")

if __name__ == "__main__":
    # remove_background("../input/input.jpg", "../output.png")
    # frames_from_video("../input/miku.mp4", "../output/miku")
    # frame_bg_remove("../output/miku/", "../output/miku_bg")
    # video_from_frames("../output/miku_bg", "../output_v/miku")
    video_from_frames("../output/miku_bg", "../output_v/miku/miku.mp4", 20)
