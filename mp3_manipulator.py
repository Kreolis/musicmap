import os, sys
from tinytag import TinyTag
from mutagen.easyid3 import EasyID3

file_names = []
def get_files(data_path):
    """Collecting all files to be processed"""
    for root, dirs, files in os.walk(data_path):
        for file in files:
            if file.endswith(".mp3"):
                filename = os.path.join(root, file)
                file_names.append(filename)
    return file_names

if __name__ == '__main__':
    #print ('Number of arguments:', len(sys.argv), 'arguments.')
    #print ('Argument List:', str(sys.argv))
    file_names = get_files(sys.argv[1])
    print(file_names)

    for mp3 in file_names:
        tag = TinyTag.get(mp3)
        print(tag)
