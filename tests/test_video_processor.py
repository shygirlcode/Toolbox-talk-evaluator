import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.video.video_processor import VideoProcessor


class TestVideoProcessor(unittest.TestCase):

    def test_supported_video_file(self):
        with TemporaryDirectory() as temp_dir:
            video_path = Path(temp_dir) / "test.mp4"
            video_path.touch()

            processor = VideoProcessor(video_path)

            self.assertTrue(processor.validate())


if __name__ == "__main__":
    unittest.main()

