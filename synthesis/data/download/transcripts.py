import subprocess
import tarfile
from pathlib import Path
from .paths import dataset_root


filename = "podcasts-transcripts-6to7.tar.gz"


if __name__ == "__main__":
    remote_path = dataset_root / "podcasts-no-audio-13GB" / filename
    subprocess.run(
        [
            "rclone",
            "copy",
            "--progress",
            remote_path.as_posix(),
            "./",
        ]
    )
    print("Extracting tar archive, this will take a few minutes")
    with tarfile.open(filename, "r:gz") as tarball:
        tarball.extractall()
    Path(filename).unlink()  # remove the archive to save space
    local_path = Path("./spotify-podcasts-2020/podcasts-transcripts")
    for subdir in local_path.iterdir():
        subdir.rename(subdir.name)  # move to top level
    local_path.rmdir()
    local_path.parent.rmdir()
