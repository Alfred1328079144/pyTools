# coding=utf-8

import codecs
import copy
import io
import numpy as np
import os, struct, array
import pickle
import re
import time
import argparse
import shutil
import json
import wave

from collections import Counter
from pprint import pprint
import xml.etree.ElementTree as ET



def read_sr_alignment(lab_filename):
    with open(lab_filename, encoding='utf-8') as f:
        lines = [line.strip() for line in f]

    alignment = []
    for i in range(len(lines)):
        start, phone = lines[i].split()
        alignment.append((float(start), phone))

    return alignment

def prepare_data(wave_dir, alignment_dir, info_filename, outfilelist):
        
    # get all lab files
    lab_files = {} # {wave_id: filename}
    for root, dirs, files in os.walk(alignment_dir):
        for file in files:
            wave_id = file[:-4]
            lab_files[wave_id] = os.path.join(root, file)
    print("len(lab_files)", len(lab_files))

    # get all wave files {wave_id: filename}
    wave_files = {}
    for root, dirs, files in os.walk(wave_dir):
        for file in files:
            wave_id = file[:-4]
            wave_files[wave_id] = os.path.join(root, file)
    print("len(wave_files)", len(wave_files))

   
    overflow_cnt = 0
    exception_cnt = 0
    text = []
    for wave_id in wave_files.keys():
        if (wave_id not in lab_files.keys()):
            continue
        try:
            print("processing", wave_id)
            alignment = read_sr_alignment(lab_files[wave_id])
            
            wave_filename = wave_files[wave_id]
            print("loading wave_filename", wave_filename)
            fw = wave.open(wave_filename, 'rb')
            (nchannels, sampwidth, samplerate, nsamples, comptype, compname) = fw.getparams()
            wav_data = fw.readframes(nsamples)
            wav_len = len(wav_data)/samplerate/sampwidth
            #print(wav_len)
            fw.close()

            # remove silence at the start/end
            sbegin = 0
            sdur = 0
            maxsil_b = 0
            maxsil_e = 0
            maxsil_m = 0
            for i in range(len(alignment)):
                if (i == len(alignment) - 1):
                    if alignment[i][1] == 'sil':
                        sbegin = alignment[i][0]
                        sdur = wav_len - sbegin  
                        if (sdur > maxsil_e):
                            maxsil_e = sdur                     
                    else:
                        continue
                elif(i == 0):
                    if alignment[i][1] == 'sil':                        
                        sbegin = alignment[i][0]
                        sdur = alignment[i+1][0] - sbegin
                        if (sdur > maxsil_b):
                            maxsil_b = sdur 
                    else:
                        continue
                else:
                    if alignment[i][1] == 'sil':                        
                        sbegin = alignment[i][0]
                        sdur = alignment[i+1][0] - sbegin
                        if (sdur > maxsil_m):
                            maxsil_m = sdur 
                    else:
                        continue
            text.append(wave_id + " " + str(maxsil_b)+ " " + str(maxsil_m)+ " " + str(maxsil_e))
            if ((maxsil_b < 0.4) and (maxsil_m < 0.4) and (maxsil_e < 0.9)):
                outfilelist.append(wave_id)
        except Exception as e:
            print("Exception when processing {}, message: {}".format(wave_id, e.message))
            exception_cnt += 1
    print("overflow_cnt =", overflow_cnt, "exception_cnt ", exception_cnt)
    with codecs.open(info_filename, "w", "utf-8") as fout:
        fout.write('\n'.join(text))

def parse_args():
    parser = argparse.ArgumentParser(description='details',
                        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-wave', type=str, default="",
                        help='input 16k wave folder')
    parser.add_argument('-lab', type=str, default="",
                        help='forced alignment lab folder by SR')
    parser.add_argument('-out', type=str, default="",
                        help='output folder')
                        
    return parser

def main():
    parser = parse_args()
    args = parser.parse_args()

    if not os.path.isdir(args.wave):
        parser.print_help()
        print("The wave folder is not exist: {}".format(args.wave))
        return 
    if not os.path.isdir(args.lab):
        parser.print_help()
        print("The align lab folder is not exist: {}".format(args.lab))
        return 

    outfilelist = []

    prepare_data(args.wave, args.lab, args.out, outfilelist)

    with open(r"C:\Users\v-chzh12\Desktop\dumpFileList_NEW_silFilter.txt",  "w",encoding='utf-8') as fw:
        for item in outfilelist:
            fw.write(item + "\n")

if __name__ == "__main__":
    main()
