# -*- coding: utf-8 -*-

import numpy as np
import os
from glob import glob

def npytotxt(melfolder, prefix, step):
    melfolder = os.path.abspath(melfolder)
    meltxtfile = os.path.join(os.path.dirname(melfolder), prefix + '_' + step + '_' + os.path.basename(melfolder) + ".txt")
    with open(meltxtfile, 'w', encoding='utf-8') as f:
        melfiles = []
        for melfile in glob(os.path.join(melfolder, "**", "out_*.npy"), recursive=True):
            melfiles.append(melfile)
        
        def getindex(x):
            a = os.path.basename(x)
            a = a[a.find('out_') + len('out_') : -4]
            return int(a)
            
        melfiles = sorted(melfiles, key = lambda x : getindex(x))
        print(melfiles)
        for melfile in melfiles:
            mel = np.load(melfile)
            mel = (mel + 4.0) / 8.0
            mel = mel.reshape(-1).tolist()
            mel = [str(x) for x in mel]
            f.write(' '.join(mel) + '\n')

if __name__ == '__main__':
    import sys
    folder = sys.argv[1]
    prefix = sys.argv[2]
    step = sys.argv[3]
    npytotxt(folder, prefix, step)
