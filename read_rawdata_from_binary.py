# coding=utf-8
# Copyright 2018 The Tensor2Tensor Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import tensorflow as tf
from shutil import copyfile
import argparse
import numpy as np
flags = tf.flags
FLAGS = flags.FLAGS

def merge_npy2npz(output_dir):
  npylist = os.listdir(output_dir)
  encdec_dict = {}
  out_dict = {}
  for npy in npylist:
    if npy.find('encdec_') != -1:
      id = npy.replace("encdec_", "").replace(".npy", "")
      try:
        encdec_dict[id] = np.load(os.path.join(output_dir, npy))
      except:
        print("Error: Missing " + id + ".npy in encdec_attn_weights.npz")

    if npy.find('out_') != -1:
      id = npy.replace("out_", "").replace(".npy", "")
      try:
        out_dict[id] = np.load(os.path.join(output_dir, npy))
      except:
        print("Error: Missing " + id + ".npy in outputs.npz")

  np.savez(os.path.join(output_dir, 'encdec_attn_weights.npz'), **encdec_dict)
  np.savez(os.path.join(output_dir, 'outputs.npz'), **out_dict)

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--output-path',
        dest='outputdir',
        default=None)
    parser.add_argument(
        '--input-path',
        dest='inputdir',
        default=None)
    parser.add_argument(
        '--locale_filter',
        dest='locale_filter',
        default=None)
    parser.add_argument('--phillyarg', default='')

    args, _ = parser.parse_known_args()
    return args

def read_and_decode(filename_queue, random_crop=False, random_clip=False, shuffle_batch=True, locale_filter=None):
  reader = tf.TFRecordReader()
  _, serialized_example = reader.read(filename_queue)
  if locale_filter:
    features = tf.parse_single_example(
     serialized_example,
     features={
        "phones": tf.VarLenFeature(tf.int64),
        "mel_lens": tf.VarLenFeature(tf.float32),
        "mel_data": tf.VarLenFeature(tf.float32),
        "utt_id": tf.VarLenFeature(tf.int64),
        "spk_id": tf.VarLenFeature(tf.int64),
        "style_id": tf.VarLenFeature(tf.int64),
        "raw_transcript": tf.FixedLenFeature([], tf.string),
        "encdec_attn": tf.VarLenFeature(tf.float32),
        "locale_id": tf.VarLenFeature(tf.int64),
     })
  else:
    features = tf.parse_single_example(
     serialized_example,
     features={
        "phones": tf.VarLenFeature(tf.int64),
        "mel_lens": tf.VarLenFeature(tf.float32),
        "mel_data": tf.VarLenFeature(tf.float32),
        "utt_id": tf.VarLenFeature(tf.int64),
        "spk_id": tf.VarLenFeature(tf.int64),
        "style_id": tf.VarLenFeature(tf.int64),
        "raw_transcript": tf.FixedLenFeature([], tf.string),
        "encdec_attn": tf.VarLenFeature(tf.float32),
     })

  label = features['mel_data']
  enc = features['encdec_attn']
  ph = features['phones']
  spk = features['spk_id']
  style = features['style_id']
  utt = features['utt_id']

  if locale_filter:
    locale = features['locale_id']
    return [label, enc, ph, spk, style, utt, locale]
  else:
    return [label, enc, ph, spk, style, utt]

def main(_):
  from scipy import misc
  import tensorflow as tf
  import numpy as np
  import scipy.io as sio
  import os
  import json
  arr = get_arguments()
  flist = []
  input_folder = arr.inputdir
  output_dir = arr.outputdir
  for file in os.listdir(input_folder):
    if "train" in file:
      if arr.locale_filter:
        if arr.locale_filter in file:
          flist.append(os.path.join(input_folder, file))
      else:
        flist.append(os.path.join(input_folder, file))

  filename_queue = tf.train.string_input_producer(flist,
                          num_epochs=1, shuffle=False)
  readrus = read_and_decode(filename_queue, locale_filter=arr.locale_filter)

  init_op = tf.group(tf.global_variables_initializer(),
            tf.local_variables_initializer())

  if os.path.isdir(output_dir) == False:
    os.makedirs(output_dir, exist_ok=True)
  fp = open(os.path.join(output_dir, 'metadata_phone.csv'), 'w', encoding='utf-8')
  if arr.locale_filter:
    fp.write("|Unnamed: 0|style_id|wav|speaker_id|locale_id|txt2|phone|phone2|phone_words\n")
  else:
    fp.write("|Unnamed: 0|style_id|wav|speaker_id|txt2|phone|phone2|phone_words\n")
  with tf.Session() as sess:
    sess.run(init_op)
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(coord=coord)
    fphone = json.load(open(os.path.join(input_folder, 'phone_set.json'), encoding='utf-8'))
    fp_rev = {}
    cnt = 0
    if '<EOS>' in fphone:
      for k in fphone:
        fp_rev[str(cnt)] = k
        cnt += 1
    else:
      fp_rev['0'] = '<pad>'
      fp_rev['1'] = '<EOS>'
      for k in fphone:
        fp_rev[str(cnt + 2)] = k
        cnt += 1
    cnt = 0
    i = 0
    try:
      while True:
        if arr.locale_filter:
          mel, encatt, phone, spk_id, style_id, utt_id, locale_id = sess.run(readrus)
        else:
          mel, encatt, phone, spk_id, style_id, utt_id = sess.run(readrus)
        print ('batch' + str(i) + ': ')
        speaker_input = str(spk_id[1][0])
        speaker_name = ""
        if int(speaker_input)==1:
            speaker_name = "Laura"
        if int(speaker_input)==2:
            speaker_name = "Mila"
        if int(speaker_input)==3:
            speaker_name = "Paola"
        if int(speaker_input)==4:
            speaker_name = "Raul"
        if int(speaker_input)==5:
            speaker_name = "Sabina"
        if int(speaker_input)==6:
            speaker_name = "Teresa"
        if int(speaker_input)==7:
            speaker_name = "LionBridgeLuis"
        if int(speaker_input)==8:
            speaker_name = "SDIAnaliz"
        if int(speaker_input)==9:
            speaker_name = "SDIJessica"
        if int(speaker_input)==10:
            speaker_name = "SpeechOceanF53"
        if int(speaker_input)==11:
            speaker_name = "SpeechOceanM04"
        print(speaker_name)
        import pdb
        mel = mel[1]
        mels = []
        for mm in mel:
          mels.append(str(mm))
        strm = ' '.join(mels)
        encatt = encatt[1]
        mel_l = int(len(mel) / 80)
        mel = np.reshape(mel, [mel_l, 80])
        enc_l = int(len(encatt) / mel_l)
        encatt = np.reshape(encatt, [mel_l, enc_l])

        np.save(os.path.join(output_dir, speaker_name+ "_" + str(i) + '.npy'), mel)
        np.save(os.path.join(output_dir, "encdec_" + str(i) + '.npy'), encatt)
        phone_list = []
        for pp in phone[1]:
          phone_list.append(str(pp))
        phone_line = ' '.join(phone_list)
        ps = []
        for pp in phone_line.split()[:-2]:
          rawphone = fp_rev[pp]
          if arr.locale_filter:
            rawphone = rawphone.replace(arr.locale_filter + '_', '')
          ps.append(rawphone)

        style_input = '0'
        speaker_input = '0'
        if len(style_id) > 0 and len(style_id[0]) > 0:
          style_input = str(style_id[1][0])
        if len(spk_id) > 0 and len(spk_id[0]) > 0:
          speaker_input = str(spk_id[1][0])
        ps = ' '.join(ps)
        if arr.locale_filter:
          fp.write(str(cnt) + "|" + str(cnt) + "|" + style_input + "|" + speaker_name + "_"+ str(cnt) + "|" + speaker_input + "|" + locale_input + "|" + ps + "|" + ps + "|" + ps + "|" + ps + "\n")
        else:
          fp.write(str(cnt) + "|" + str(cnt) + "|" + style_input + "|" + speaker_name + "_"+ str(cnt) + "|" + speaker_input + "|" + ps + "|" + ps + "|" + ps + "|" + ps + "\n")
        cnt += 1
        i += 1
    except tf.errors.OutOfRangeError as e:
      coord.request_stop(e)
    finally:
      coord.request_stop()
      coord.join(threads)
      fp.close()
  copyfile(os.path.join(input_folder, "phone_set.json"), os.path.join(output_dir, "phone_set.json"))
  merge_npy2npz(output_dir)
  fw = open(os.path.join(output_dir, "melout.txt"), "w")
  fz = np.load(os.path.join(output_dir, "outputs.npz")) 

  for i in range(len(fz.keys())):
    mel = fz[str(i)]
    strmel = ""
    for m in mel:
      for mm in m:
        strmel += str(mm) + " "
    fw.write(strmel.strip() + "\n")
  fw.close()

if __name__ == "__main__":
  tf.logging.set_verbosity(tf.logging.INFO)
  tf.app.run()
