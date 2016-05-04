import os
import sys
import re
import pprint

pp = pprint.PrettyPrinter(indent=1)
punct = re.compile(r'[^0-9a-zA-Z ]')

def calculate_ngram_precision(cand_ngram,count_clip_sum):
    return float(count_clip_sum)/len(cand_ngram)

def get_ngrams(n, text):
    ngrams = []
    text_length = len(text)
    max_index_ngram_start = text_length - n
    for i in range (max_index_ngram_start + 1):
        #ngram_set.add(tuple(text[i:i+n]))
        ngrams.append(tuple(text[i:i+n]))
        #ngram_set.add(text[i])
    return ngrams

def calculate_count_clip(cand_ngrams, ref_ngrams):
    clip = 0
    cand_count = {}
    for word in cand_ngrams:
        if word in cand_count:
            cand_count[word] += 1
        else:
            cand_count[word] = 1
    #print cand_count
    #pp.pprint(cand_count)

    ref_count = [None] * len(ref_ngrams)
    for index,line in enumerate(ref_ngrams):
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


def get_line(fp):
    line = fp.readline()
    return line

def clean_line(line):
    global punct
    line = line.lower()
    line = punct.sub('',line)
    return line.split()


def calculate_bleu(cand_path,ref_path):
    cand_fp = open(cand_path,'r')
    ref_fp = []
    p_n = []
    N = 4

    try:
        for filename in os.listdir(ref_path):
            fp = open(ref_path + filename, 'r')
            ref_fp.append(fp)
    except Exception as e:
        fp = open(ref_path, 'r')
        ref_fp.append(fp)

    for n in range(1,N+1):
        total_cand_ngrams = []
        count_clip_sum, total_cand_ngrams = calculate_count_clip_by_sentence(n,cand_fp,ref_fp,total_cand_ngrams)
        print "count_clip_sum:",count_clip_sum
        p_n.append(calculate_ngram_precision(total_cand_ngrams,count_clip_sum))

    print "p_n:",p_n


def calculate_count_clip_by_sentence(n,cand_fp,ref_fp,total_cand_ngrams):
    count_clip_sum = 0
    cand_fp.seek(0)
    [fp.seek(0) for fp in ref_fp]
    while True:
        cand_ngrams = get_ngrams(n,clean_line(get_line(cand_fp)))
        total_cand_ngrams.extend(cand_ngrams)

        if len(cand_ngrams) == 0:
            break

        ref_ngrams = []
        for fp in ref_fp:
            ref_ngrams.append(get_ngrams(n,clean_line(get_line(fp))))

        count_clip_sum += calculate_count_clip(cand_ngrams,ref_ngrams)
        #print "one sentence over!"
    return count_clip_sum,total_cand_ngrams


def main():
    cand_path = sys.argv[1]
    ref_path = sys.argv[2]
    calculate_bleu(cand_path, ref_path)

if __name__ == '__main__':
    main()
