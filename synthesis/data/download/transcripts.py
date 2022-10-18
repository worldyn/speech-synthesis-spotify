import subprocess
import tarfile
from pathlib import Path
from .paths import dataset_root


filename = "podcasts-transcripts-6to7.tar.gz"
rclone_exec = "rclone"


if __name__ == "__main__":
    remote_path = dataset_root / "podcasts-no-audio-13GB" / filename
    subprocess.run(
        [
            rclone_exec,
            "copy",
            "--progress",
            remote_path.as_posix(),
            "./",
        ]
    )
    print("Extracting tar archive, this will take a few minutes")
    with tarfile.open(filename, "r:gz") as tarball:
        
        import os
        
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(tarball)
    Path(filename).unlink()  # remove the archive to save space
    local_path = Path("./spotify-podcasts-2020/podcasts-transcripts")
    for subdir in local_path.iterdir():
        subdir.rename(subdir.name)  # move to top level
    local_path.rmdir()
    local_path.parent.rmdir()
