import os
import sys
import re

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

    while True:
        cand_line = clean_line(get_line(cand_fp))
        if len(cand_line) == 0:
            break

        ref_lines = []
        


def main():
    cand_path = sys.argv[1]
    ref_path = sys.argv[2]
    read_data(cand_path, ref_path)

if __name__ == '__main__':
    main()
