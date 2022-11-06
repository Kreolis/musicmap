import sys, os
import argparse
from halo import Halo
from graph.graph import run_path_plotter

parser = argparse.ArgumentParser(description="musicmap mental health music tagger")

parser.add_argument('-t', '--tags', dest="tags", 
                    action='store_true',
                    help="Get all possible tags")

parser.add_argument('-p', '--path', dest="path",
                    type=str,  
                    help="path to files")

parser.add_argument('-l', '--hops', dest="hops",
                    type=int,  
                    help="playlist length",
                    default=10)

parser.add_argument('-s', '--start', dest="start",
                    type=str,  
                    help="playlist start tag",
                    default="Mellow")

parser.add_argument('-e', '--end', dest="end",
                    type=str,  
                    help="playlist end tag",
                    default="party")

# getting all provided arguments
args = parser.parse_args(sys.argv[1:])

if __name__ == '__main__':
    if args.tags:
        print(['rock','pop','alternative',
        'indie','electronic','female vocalists',
        'dance','00s','alternative rock',
        'jazz','beautiful','metal','chillout',
        'male vocalists','classic rock','soul',
        'indie rock','Mellow','electronica','80s',
        'folk','90s','chill','instrumental','punk',
        'oldies','blues','hard rock','ambient',
        'acoustic','experimental','female vocalist',
        'guitar','Hip-Hop','70s','party','country',
        'easy listening','sexy','catchy','funk',
        'electro','heavy metal','Progressive rock',
        '60s','rnb','indie pop','sad','House','happy'])
        exit()
    from analysis.music_analyser import music_analyiser

    file_folder = args.path
    processor = music_analyiser(file_folder)
    #print ('Number of arguments:', len(sys.argv), 'arguments.')
    #print ('Argument List:', str(sys.argv))
    processor.get_files()
    #processor.run()
    processor.run(extract_features=True)
    #processor.save_glob_sidecar()

    spinner = Halo(text='calculating graph', spinner='dots')
    spinner.start() 
    run_path_plotter(os.path.dirname(os.path.abspath(__file__)), args.hops, args.start, args.end)
    spinner.stop() 
