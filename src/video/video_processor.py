from pathlib import Path
import cv2


class VideoProcessor:
    """Handles toolbox talk video input."""

    SUPPORTED_FORMATS = {".mp4", ".avi", ".mov", ".mkv"}

    def __init__(self, video_path):
        self.video_path = Path(video_path)

    def validate(self):
        """Check whether the video exists and uses a supported format."""

        if not self.video_path.exists():
            raise FileNotFoundError(
                f"Video file not found: {self.video_path}"
            )

        if self.video_path.suffix.lower() not in self.SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported video format: {self.video_path.suffix}"
            )

        return True

    def open_video(self):
        """Open the video using OpenCV."""

        video = cv2.VideoCapture(str(self.video_path))

        if not video.isOpened():
            raise ValueError("Could not open the video.")

        return video
    def sample_frames(self, interval_seconds=2):
        """Sample one frame at a fixed time interval."""

        video = self.open_video()

        fps = video.get(cv2.CAP_PROP_FPS)

        if fps <= 0:
            video.release()
            raise ValueError("Could not determine video FPS.")

        frame_interval = int(fps * interval_seconds)

        frames = []
        frame_number = 0

        while True:
            success, frame = video.read()

            if not success:
                break

            if frame_number % frame_interval == 0:
                frames.append(frame)

            frame_number += 1

        video.release()

        return frames
    def save_frames(self, frames, output_dir="data/output"):
        """Save sampled frames as image files."""

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        for index, frame in enumerate(frames):
            filename = output_path / f"sampled_frame_{index:03d}.jpg"
            cv2.imwrite(str(filename), frame)

    def resize_frames(self, frames, width=1920, height=1080):
        """Resize frames to a standard resolution."""

        resized_frames = []

        for frame in frames:
            resized_frame = cv2.resize(frame, (width, height))
            resized_frames.append(resized_frame)

        return resized_frames  
    
    def reduce_noise(self, frames):
        """Reduce visual noise in video frames."""

        denoised_frames = []

        for frame in frames:
            denoised_frame = cv2.GaussianBlur(frame, (5, 5), 0)
            denoised_frames.append(denoised_frame)

        return denoised_frames 
    
    def detect_shot_boundaries(self, frames, threshold=50):
        """Detect major visual changes between consecutive frames."""

        boundaries = []

        for i in range(1, len(frames)):
            difference = cv2.absdiff(frames[i - 1], frames[i])
            average_difference = difference.mean()

            if average_difference > threshold:
                boundaries.append(i)

        return boundaries     
    
    
   