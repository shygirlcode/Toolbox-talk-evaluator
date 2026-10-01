from src.video.video_processor import VideoProcessor


video_path = "data/input/constrution video.mp4"

processor = VideoProcessor(video_path)

processor.validate()

frames = processor.sample_frames(interval_seconds=2)
resized_frames = processor.resize_frames(frames)
processor.save_frames(resized_frames)
denoised_frames = processor.reduce_noise(resized_frames)
shot_boundaries = processor.detect_shot_boundaries(denoised_frames)

print("Shot boundaries:", shot_boundaries)

print("Noise reduction completed.")

print("Sampled frames:", len(resized_frames))
print("Frames saved successfully.")
print("Original frames:", frames[0].shape)
print("Resized frames:", resized_frames[0].shape)