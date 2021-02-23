import subprocess
from pathlib import Path
from .paths import dataset_root


subdir = "6/0"
num_threads = 4


if __name__ == "__main__":
    remote_path = dataset_root / "podcasts-audio-only-2TB" / "podcasts-audio" / subdir
    subprocess.run(
        [
            "rclone",
            "copy",
            "--progress",
            "--transfers",
            str(num_threads),
            "--checkers",
            str(num_threads),
            remote_path.as_posix(),
            "./",
        ]
    )
