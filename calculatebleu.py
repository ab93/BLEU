import os
import sys
import re
import math
import pprint

pp = pprint.PrettyPrinter(indent=1)
c = 0.0
r = 0.0
#punct = re.compile(r'[^0-9a-zA-Z ]')

def calculate_ngram_precision(cand_ngram,count_clip_sum):
    return float(count_clip_sum)/len(cand_ngram)

def get_ngrams(n, text):
    ngrams = []
    text_length = len(text)
    max_index_ngram_start = text_length - n
    if n == 1:
        for i in range (max_index_ngram_start + 1):
            ngrams.append(text[i])
    else:
        for i in range (max_index_ngram_start + 1):
            ngrams.append(tuple(text[i:i+n]))
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

    #print clip
    return clip


def get_line(fp):
    line = fp.readline()
    return line

def clean_line(line):
    #global punct
    line = line.lower()
    #line = punct.sub('',line)
    return line.split()

def get_best_match_length(cand_line,ref_lines):
    c = len(cand_line)
    r = len(ref_lines[0])
    min_diff = sys.maxint
    for ref in ref_lines:
        diff = abs(len(ref) - c)
        #print "r_other,diff:",len(ref),diff
        if diff < min_diff:
            min_diff = diff
            r = len(ref)

    #print "c,r:",c,r
    return c,r

def calculate_brevity_penalty():
    global c,r
    BP = 1
    if c <= r:
        BP = math.exp(1 - (r/c))

    return BP

def calculate_BLEU(BP,p_n):
    N = 4
    w = 1.0/N
    geo_sum = 0.0
    for n in range(N):
        geo_sum += w * math.log(p_n[n])
    BLEU = BP * math.exp(geo_sum)
    return BLEU

def find_bleu_score(cand_path,ref_path):
    global c,r
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
        #print "count_clip_sum:",count_clip_sum
        p_n.append(calculate_ngram_precision(total_cand_ngrams,count_clip_sum))

    print "c,r:",c,r
    print "p_n:",p_n

    BP = calculate_brevity_penalty()
    print "BP:",BP
    BLEU = calculate_BLEU(BP,p_n)
    print "BLEU:",BLEU


def calculate_count_clip_by_sentence(n,cand_fp,ref_fp,total_cand_ngrams):
    global c,r
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

        if n == 1:
            c0, r0 = get_best_match_length(cand_ngrams,ref_ngrams)
            c += c0
            r += r0

        count_clip_sum += calculate_count_clip(cand_ngrams,ref_ngrams)
    return count_clip_sum,total_cand_ngrams


def main():
    cand_path = sys.argv[1]
    ref_path = sys.argv[2]
    find_bleu_score(cand_path, ref_path)

if __name__ == '__main__':
    main()
