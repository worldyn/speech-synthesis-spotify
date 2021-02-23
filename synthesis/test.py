from pathlib import Path


print(Path.cwd())
print(list(Path("./audio").iterdir()))
