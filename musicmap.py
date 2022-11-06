import sys
from analysis.music_analyser import music_analyiser
from graph.graph import run_path_plotter

if __name__ == '__main__':
    file_folder = sys.argv[1]
    processor = music_analyiser(file_folder)
    #print ('Number of arguments:', len(sys.argv), 'arguments.')
    #print ('Argument List:', str(sys.argv))
    processor.get_files()
    #processor.run()
    processor.run(extract_features=True)
    #processor.save_glob_sidecar()

    run_path_plotter(file_folder)
