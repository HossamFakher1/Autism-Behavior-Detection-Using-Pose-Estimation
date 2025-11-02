import os
import cv2
import numpy as np
import glob as gb

def interpolate_frames(video_path, target_frame_count):
    # Open video
    cap = cv2.VideoCapture(video_path)
    frames = []

    # Read frames
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)

    cap.release()

    original_frame_count = len(frames)

    # Ensure we generate exactly target_frame_count frames
    if original_frame_count <= 1:
        return frames  # Return as is if there's 1 or no frame

    # Calculate how many interpolated frames are needed
    total_frames_needed = target_frame_count - original_frame_count
    interpolated_frames = []
    total_frames_needed_c = total_frames_needed
    if total_frames_needed > original_frame_count :
        print(f'Total frames : {original_frame_count}')
        print(f'Total frames needed: {total_frames_needed}')
    # Calculate how many new frames should be created between each pair of original frames
    num_new_frames = total_frames_needed // (original_frame_count - 1)
    
    # Append the original frames
    for i in range(original_frame_count - 1):
        interpolated_frames.append(frames[i])  # Append the current frame

        # Calculate how many interpolated frames to create between current and next frame
        if total_frames_needed_c > 0:
            # print(num_new_frames)
            # Create new frames between the current and next frame
            for j in range(num_new_frames + 1):  # +1 to include one additional frame
                # Calculate alpha for blending
                alpha = (j + 1) / (num_new_frames + 1)  # Use (j + 1) to avoid zero alpha
                # Create new frame using weighted blend
                new_frame = cv2.addWeighted(frames[i], 1 - alpha, frames[i + 1], alpha, 0)
                interpolated_frames.append(new_frame)
            total_frames_needed_c -=1

    # Append the last frame
    interpolated_frames.append(frames[-1])

    # Return only the desired number of frames
    return interpolated_frames[:target_frame_count]  # Return only the target number of frames

# Example usage
input_folder = 'Swimming Dataset'  # Change this to your input folder
output_folder = 'Test1'  # Change this to your output folder
target_frame_count = 70  # Set the desired frame count for the output videos

# Traverse directories
for folder in os.listdir(input_folder):
    for video_path in gb.glob(os.path.join(input_folder, folder, '*.mp4')):
        print(f'Processing {video_path}')

        # Interpolate frames
        interpolated_frames = interpolate_frames(video_path, target_frame_count)

        # Construct the output path
        make_folder = os.path.join(output_folder, folder)
        os.makedirs(make_folder, exist_ok=True)  # Create output folder if it doesn't exist

        # Save the processed video in the new folder with a new filename
        output_filename = f'linear interpolation{os.path.basename(video_path)}'
        output_path = os.path.join(make_folder, output_filename)

        out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), 35, (interpolated_frames[0].shape[1], interpolated_frames[0].shape[0]))
        for frame in interpolated_frames:
            out.write(frame)

        out.release()
        # print(f'Saved processed video to {output_path}')
        # print(f'Total frames saved: {len(interpolated_frames)}')
