import cv2
import os
import numpy as np

def rotate_frame(frame, angle):
    """Rotate the image by the specified angle."""
    (h, w) = frame.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_frame = cv2.warpAffine(frame, M, (w, h))
    return rotated_frame

def augment_video(input_video_path, output_folder):
    """Augment a video with all combinations including original."""
    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        print(f"Error opening video file {input_video_path}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    base_name = os.path.splitext(os.path.basename(input_video_path))[0]
    os.makedirs(output_folder, exist_ok=True)

    # All possible combinations including original
    combinations = [
        {'flip': False, 'rotate': False, 'brightness': False},  # Original
        {'flip': True,  'rotate': False, 'brightness': False},
        {'flip': False, 'rotate': True,  'brightness': False},
        {'flip': False, 'rotate': False, 'brightness': True},
        {'flip': True,  'rotate': True,  'brightness': False},
        {'flip': True,  'rotate': False, 'brightness': True},
        {'flip': False, 'rotate': True,  'brightness': True},
        {'flip': True,  'rotate': True,  'brightness': True},
    ]

    # Generate random parameters once per video
    params = {
        'rotate_angle': np.random.uniform(-15, 15),
        'contrast': 1.2,
        'brightness_val': 15
    }

    # Create VideoWriters for all combinations
    writers = []
    for combo in combinations:
        suffix_parts = []
        if combo['flip']: suffix_parts.append('flip')
        if combo['rotate']: suffix_parts.append('rotate')
        if combo['brightness']: suffix_parts.append('brightness')
        
        if suffix_parts:
            output_name = f"{base_name}_{'_'.join(suffix_parts)}.mp4"
        else:
            output_name = f"{base_name}.mp4"  # Original video
        
        output_path = os.path.join(output_folder, output_name)
        writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
        writers.append((combo, writer))

    # Process each frame
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        for combo, writer in writers:
            augmented = frame.copy()

            # Apply flip
            if combo['flip']:
                augmented = cv2.flip(augmented, 1)

            # Apply rotation
            if combo['rotate']:
                augmented = rotate_frame(augmented, params['rotate_angle'])

            # Apply brightness
            if combo['brightness']:
                augmented = cv2.convertScaleAbs(augmented, 
                                               alpha=params['contrast'], 
                                               beta=params['brightness_val'])

            writer.write(augmented)

    # Release resources
    cap.release()
    for _, writer in writers:
        writer.release()
    print(f"Generated {len(writers)} videos in: {output_folder}")

def process_folder(input_folder, output_folder):
    """Process all videos in the input folder and its subfolders."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, dirs, files in os.walk(input_folder):
        relative_path = os.path.relpath(root, input_folder)
        output_dir = os.path.join(output_folder, relative_path)
        os.makedirs(output_dir, exist_ok=True)

        for file in files:
            if file.lower().endswith(('.mp4', '.avi', '.mov')):
                video_path = os.path.join(root, file)
                augment_video(video_path, output_dir)

# Example usage
input_folder = 'old dataset'
output_folder = 'dataset'
process_folder(input_folder, output_folder)