import subprocess
from pathlib import Path
from .paths import dataset_root


subdir = "0/L/show_0L0j6X6cf3DO1Bs0D0K4Ch"
num_threads = 4
rclone_exec = "rclone"


if __name__ == "__main__":
    remote_path = dataset_root / "podcasts-audio-only-2TB" / "podcasts-audio" / subdir
    subprocess.run(
        [
            rclone_exec,
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
