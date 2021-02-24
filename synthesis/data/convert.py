from pathlib import Path
from glob import glob
import soundfile as sf
from tqdm.auto import tqdm


if __name__ == "__main__":
    input_dir = Path("./audio")
    output_dir = Path("./")
    input_paths = glob((input_dir / "**/*.ogg").as_posix(), recursive=True)
    for input_path in tqdm(input_paths):
        data, samplerate = sf.read(input_path)
        output_path = output_dir / Path(input_path).relative_to(input_dir).with_suffix(
            ".wav"
        )
        output_path.parent.mkdir(exist_ok=True)
        sf.write(output_path, data, samplerate)
