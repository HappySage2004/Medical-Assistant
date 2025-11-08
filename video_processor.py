import cv2
import os
from datetime import datetime
from moviepy import VideoFileClip

def extract_video_context(video_path, client:str, num_frames=5):
    """
    Extracts N evenly spaced frames and the full audio track from a video file.
    Returns (frame_paths, audio_path)
    """
    # --- 1. Create output folder (absolute path) ---
    base_dir = os.path.join(os.getcwd(), f"{client}_video")
    os.makedirs(base_dir, exist_ok=True)

    # create a subfolder per video for uniqueness
    folder_name = f"{os.path.splitext(os.path.basename(video_path))[0]}_{datetime.now().strftime('%H%M%S')}"
    temp_dir = os.path.join(base_dir, folder_name)
    os.makedirs(temp_dir, exist_ok=True)

    # --- 1. Extract frames ---
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_indices = [int(i * total_frames / num_frames) for i in range(num_frames)]
    frame_paths = []

    for idx in frame_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if not ret:
            continue
        frame_path = os.path.join(temp_dir, f"frame_{idx}.jpg")
        cv2.imwrite(frame_path, frame)
        frame_paths.append(frame_path)

    cap.release()

    # --- 2. Extract audio ---
    clip = VideoFileClip(video_path)
    audio_path = None
    if clip.audio is not None:
        audio_path = os.path.join(temp_dir, "audio.wav")
        clip.audio.write_audiofile(audio_path, logger=None)
    else:
        print(f"[INFO] No audio track found in '{video_path}'. Skipping audio extraction.")

    clip.close()

    return frame_paths, audio_path

if __name__ == "__main__":
    frames, audio = extract_video_context("videos/video2.mp4")
    print(frames, audio)