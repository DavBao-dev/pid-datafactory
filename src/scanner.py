from pathlib import Path
import json
import re

KEYWORD_SUFFIX = [
    "symbol",
    "P&ID",
    "ISA",
    "ISO",
    "CAD",
    "SVG",
    "DWG",
    "engineering symbol",
    "piping symbol",
    "line drawing"
]


class DatasetScanner:

    def __init__(self, dataset_path: str):

        self.dataset = Path(dataset_path)

    def scan(self):

        folders = [f for f in self.dataset.iterdir() if f.is_dir()]

        print(f"\nFound {len(folders)} classes\n")

        for folder in folders:

            self.process(folder)

    def process(self, folder: Path):

        print(f"Scanning {folder.name}")

        # create folders

        for name in [
            "reference",
            "raw",
            "crop",
            "clean",
            "final",
            "cache"
        ]:

            (folder / name).mkdir(exist_ok=True)

        sample = self.find_sample(folder)

        if sample is None:

            print("   sample image not found")

            return

        metadata = {

            "class": folder.name,

            "sample": str(sample.name),

            "downloaded": 0,

            "accepted": 0,

            "keywords": self.generate_keywords(folder.name)

        }

        with open(folder / "metadata.json", "w", encoding="utf8") as f:

            json.dump(metadata, f, indent=4)

        print("   metadata created")

    def find_sample(self, folder):

        exts = [
            "*.png",
            "*.jpg",
            "*.jpeg",
            "*.bmp",
            "*.webp"
        ]

        for ext in exts:

            files = list(folder.glob(ext))

            if len(files):

                return files[0]

        ref = folder / "reference"

        if ref.exists():

            for ext in exts:

                files = list(ref.glob(ext))

                if len(files):

                    return files[0]

        return None

    def split_name(self, name):

        return re.sub(r'(?<!^)(?=[A-Z])', ' ', name)

    def generate_keywords(self, classname):

        classname = self.split_name(classname)

        keywords = []

        for suffix in KEYWORD_SUFFIX:

            keywords.append(f"{classname} {suffix}")

        return keywords
