import os
from musicnn.extractor import extractor

class music_analyiser:
    def __init__(self) -> None:
        self.files = []

    def get_files(self, data_path):
        """Collecting all files to be processed"""
        for root, dirs, files in os.walk(data_path):
            for file in files:
                if file.endswith(".mp3"):
                    self.files.append(os.path.join(root, file))

    def run(self):
        """Run musicnn analysis on files"""
        for file_name in self.files:
            taggram, tags, features = extractor(file_name, model='MTT_musicnn', extract_features=True)
