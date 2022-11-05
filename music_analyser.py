import os, sys
import numpy as np
import tqdm
from musicnn.extractor import extractor

from typing import TypedDict, List

class analysis_data(TypedDict):
    filename: str
    taggram: List[float]
    tags: List[str]
    features: List[str]
    toptags: List[str]

class music_analyiser:
    def __init__(self, fielpath: str) -> None:
        self.files = []
        self.filepath = fielpath

    def get_files(self):
        """Collecting all files to be processed"""
        for root, dirs, files in os.walk(self.filepath):
            for file in files:
                if file.endswith(".mp3"):
                    data = analysis_data()
                    data["filename"] = os.path.join(root, file)
                    self.files.append(data)
                    #np.append(self.files, data)
        
        print("Got", len(self.files), "files")

    def run(self, export_sidecar: bool = True):
        """Run musicnn analysis on files"""
        for data in tqdm.tqdm(self.files):
            filepath = data["filename"]
            print("Analysing ", filepath)
            data["taggram"], data["tags"], data["features"] = extractor(filepath, model='MTT_musicnn', extract_features=True)
            # converting to numpy array
            #data["vector"] = []
            #for entry in vector:
            #    data["vector"].append(entry.eval().numpy())
            #data["vector"] = data["vector"].numpy()
            
            self.get_top_tags(data)
            
            if export_sidecar:
                self.save_sidecar(data)

    def get_top_tags(self, data: analysis_data, topN: int=3, print_tags: bool=True):
        
        tags_likelihood_mean = np.mean(data["taggram"], axis=0)

        #if print_tags:
        #    print('[' + file_name + '] Top' + str(topN) + ' tags: ')

        #if save_tags:
        #    to = open(save_tags, 'a')   
        #    to.write(file_name + ',' + model + ',input_length=' + str(input_length) + ',input_overlap=' + str(input_overlap)) 

        topN_tags = []
        for tag_index in tags_likelihood_mean.argsort()[-topN:][::-1]:
            topN_tags.append(data["tags"][tag_index])

            if print_tags:
                print(' - ' + data["tags"][tag_index])
        
        data["toptags"] = topN_tags
        return topN_tags
    
    def save_sidecar(self, data: analysis_data):
        base=os.path.basename(data["filename"])
        sidecar_name = os.path.splitext(base)[0] + ".npy"
        sidecar_path = os.path.join(self.filepath, sidecar_name)
        np.save(sidecar_path, data)
        

    def save_sidecars(self):
        for data in self.files:
            self.save_sidecar(data)

    def save_glob_sidecar(self):
        np.save("global_outputs.npy", self.files)


if __name__ == '__main__':
    processor = music_analyiser(sys.argv[1])
    #print ('Number of arguments:', len(sys.argv), 'arguments.')
    #print ('Argument List:', str(sys.argv))
    processor.get_files()
    processor.run()
    processor.save_glob_sidecar()
