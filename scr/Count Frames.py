import os
import cv2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Traverse through directories to find videos
def get_video_files_from_folders(root_folder):
    video_files = []
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.endswith(('.mp4', '.avi', '.mov', '.mkv')):  
                video_files.append(os.path.join(root, file))
    return video_files

# Step 2: Calculate frame count for each video
def calculate_frame_count(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None  # Return None if the video can't be opened
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    return frames

# Step 3: Collect video file names and frame counts
def collect_frame_data(root_folder):
    video_files = get_video_files_from_folders(root_folder)
    frame_data = {'Video Name': [], 'Frame Count': []}
    
    for video_file in video_files:
        frame_count = calculate_frame_count(video_file)
        if frame_count is not None:
            video_name = os.path.basename(video_file)  # Extract only the video file name
            frame_data['Video Name'].append(video_name)
            frame_data['Frame Count'].append(frame_count)
    
    # Convert to DataFrame
    df = pd.DataFrame(frame_data)
    return df

# Step 4: Visualize the data in a bar plot
def plot_frame_count_distribution(df,save_path):
    plt.figure(figsize=(10, 6))
    df = df.sort_values('Frame Count', ascending=False)
    sns.countplot(x=df['Frame Count'], color='skyblue')
    plt.title('Frame Count Distribution Across Videos')
    plt.tight_layout()
    plt.xticks(rotation = 90)
    # Save the plot to the specified path
    plt.savefig(save_path, dpi=300)  # Save the image with high resolution
    plt.show()
    
# Example usage:
root_folder = 'Test1'  #'linear interpolation'  
df = collect_frame_data(root_folder)
df.to_csv(f'{root_folder}.csv',index = False)

# Path to save the image
save_path = f'{root_folder}.png'

# Plotting the frame count distribution
plot_frame_count_distribution(df,save_path)
