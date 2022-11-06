from analysis.music_analyser import music_analyiser


if __name__ == '__main__':
    processor = music_analyiser(sys.argv[1])
    #print ('Number of arguments:', len(sys.argv), 'arguments.')
    #print ('Argument List:', str(sys.argv))
    processor.get_files()
    #processor.run()
    processor.run(extract_features=True)
    #processor.save_glob_sidecar()


    