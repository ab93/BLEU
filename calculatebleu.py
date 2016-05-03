import os
import sys
import re
import pprint

pp = pprint.PrettyPrinter(indent=1)

def calculate_count_clip(cand_line, ref_lines):
    clip = 0
    cand_count = {}
    for word in cand_line:
        if word in cand_count:
            cand_count[word] += 1
        else:
            cand_count[word] = 1
    #print cand_count
    #pp.pprint(cand_count)

    ref_count = [None] * len(ref_lines)
    for index,line in enumerate(ref_lines):
        ref_count[index] = {}
        for word in line:
            if word in ref_count[index]:
                ref_count[index][word] += 1
            else:
                ref_count[index][word] = 1
        #print ref_count[index],'\n'

    #print cand_count
    for word in cand_count:
        #print "word:",word
        ref_word_count = []
        for index,line in enumerate(ref_count):
            try:
                ref_word_count.append(ref_count[index][word])
            except Exception as e:
                #print e
                ref_word_count.append(0)
            max_ref_word_count = max(ref_word_count)

        #print ref_word_count,cand_count[word]
        clip += min(cand_count[word],max_ref_word_count)

    print clip
    return clip



def read_data(cand_path,ref_path):
    punct = re.compile(r'[^0-9a-zA-Z ]')

    def get_line(fp):
        line = fp.readline()
        return line

    def clean_line(line):
        line = line.lower()
        line = punct.sub('',line)
        return line.split()

    cand_fp = open(cand_path,'r')

    ref_fp = []
    try:
        for filename in os.listdir(ref_path):
            fp = open(ref_path + filename, 'r')
            ref_fp.append(fp)

    except Exception as e:
        fp = open(ref_path, 'r')
        ref_fp.append(fp)

    count_clip = 0
    while True:  #for each sentence
        cand_line = clean_line(get_line(cand_fp))
        if len(cand_line) == 0:
            break

        ref_lines = []
        for fp in ref_fp:
            ref_lines.append(clean_line(get_line(fp)))

        count_clip += calculate_count_clip(cand_line,ref_lines)
        raw_input("one sentence over!\n")

    print count_clip


def main():
    cand_path = sys.argv[1]
    ref_path = sys.argv[2]
    read_data(cand_path, ref_path)

if __name__ == '__main__':
    main()
