# Copyright (c) 2020, Soohwan Kim. All rights reserved.
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

import os
import re


def bracket_filter(sentence, mode='phonetic'):
    new_sentence = str()

    if mode == 'phonetic':
        flag = False

        for ch in sentence:
            if ch == '(' and flag is False:
                flag = True
                continue
            if ch == '(' and flag is True:
                flag = False
                continue
            if ch != ')' and flag is False:
                new_sentence += ch

    elif mode == 'spelling':
        flag = True

        for ch in sentence:
            if ch == '(':
                continue
            if ch == ')':
                if flag is True:
                    flag = False
                    continue
                else:
                    flag = True
                    continue
            if ch != ')' and flag is True:
                new_sentence += ch

    else:
        raise ValueError("Unsupported mode : {0}".format(mode))

    return new_sentence

# Edited by DevTae
def special_filter(sentence, mode='phonetic', replace=None):
    new_sentence = str()
    for idx, ch in enumerate(sentence):
        if re.search(r"[ㄱ-ㅎ가-힣ㅏ-ㅣ]", ch) is None:
            if not (ch == '!' or ch == '?' or ch == '.' or ch == ',' or ch == ' '):
                return None
        new_sentence += ch

    pattern = re.compile(r'\s\s+') # 스페이스바 두 번 이상일 때
    new_sentence = re.sub(pattern, ' ', new_sentence.strip())
    return new_sentence

def sentence_filter(raw_sentence, mode, replace=None):
    return special_filter(bracket_filter(raw_sentence, mode), mode, replace)

# Edited by DevTae
def preprocess(dataset_path, mode='phonetic'):
    print('preprocess started..')

    audio_paths = list()
    transcripts = list()

    BASE_PATH = dataset_path
    META_PATH = "/1.Training/1.라벨링데이터/{THEME_FOLDER}/{THEME_LABEL}_{NUM}/{THEME_LABEL}_{NUM}_metadata.txt" # ipa 일때 .txt -> _ipa.txt 변경
    THEME_INFO = { "1.방송" : [ "broadcast", 5 ],
                   "2.취미" : [ "hobby", 1 ],
                   "3.일상안부" : [ "dialog", 4 ],
                   "4.생활" : [ "life", 10 ],
                                   "5.날씨" : [ "weather", 3 ],
                                   "6.경제" : [ "economy", 4 ],
                                   "7.놀이" : [ "play", 2 ],
                                   "8.쇼핑" : [ "shopping", 2] }

    paths = []

    for key, value in THEME_INFO.items():
            for i in range(1, value[1] + 1, 1):
                    metafile = BASE_PATH + META_PATH.replace("{THEME_FOLDER}", key).replace("{THEME_LABEL}", value[0]).replace("{NUM}", "{0:0>2d}".format(i))
                    paths.append(metafile)

    for i, path in enumerate(paths, start=1):
        if not os.path.isfile(path):
            continue

        with open(path, "r", encoding='utf8') as f:
            for j, line in enumerate(f.readlines(), start=1):
                datas = line.split('|')
                audio_path = BASE_PATH + datas[0].strip()
                sentence = str()
                with open(audio_path.replace(".wav", ".txt"), "r", encoding="utf8") as sentence_f: # ipa 일때 .txt -> _ipa.txt 변경
                    sentence = sentence_filter(sentence_f.read(), mode=mode) # ipa 일때 ipa 변환 함수 호출 추가
                audio_paths.append(audio_path)
                transcripts.append(sentence)
    return audio_paths, transcripts
