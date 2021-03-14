import subprocess
from pathlib import Path
from glob import glob
from tqdm.auto import tqdm


if __name__ == "__main__":
    input_dir = Path("./audio")
    output_dir = Path("./")
    input_paths = glob((input_dir / "**/*.ogg").as_posix(), recursive=True)
    for input_path in tqdm(input_paths):
        subprocess.run(
            args=[
                "ffmpeg",
                "-i",
                input_path,
                Path(input_path).relative_to(input_dir).with_suffix(".wav"),
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )
