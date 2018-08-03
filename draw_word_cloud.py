#! /usr/bin/env python
# --coding: utf-8 -*-

from wordcloud import WordCloud
import random
import sys


def top_10_color(word):
    #color_hash = {
    #    "TP53": "crimson",
    #    "NRAS": "coral",
    #    "FLT3": "blue",
    #    "TET2": "cornflowerblue",
    #    "U2AF1": "darkgreen",
    #    "RUNX1": "mediumturquoise",
    #    "CDKN2A": "brown",
    #    "ASXL1": "blueviolet",
    #    "WT1": "lightsalmon",
    #    "IDH1": "royalblue",
    #    "BCOR": "seagreen",
    #    "DNMT3A": "mediumorchid",
    #    "ETV6": "violet"
    #}
    #if color_hash.has_key(word):
    #    return color_hash[word]
    #else:
    #    return "black"

    return "black"


def grey_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    #print word,font_size
    word_color = top_10_color(word)

    return word_color

    #if font_size >= 30:
    #    return "red"
    #else:
    #    return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)



#y_text = ""
y_dict = {}
m_dict = {}
w_dict = {}
y_all = 0
m_all = 0
w_all = 0
with open("./venn_result/gene_summary.tsv", "r") as f:
    lines = f.read().rstrip("\n").split("\n")
    for line in lines:
        data = line.split("\t")
        gene = data[0]

        if gene == "gene":
            continue

        y_count = int(data[1])
        m_count = int(data[2])
        w_count = int(data[3])

        if y_count != 0:
            y_dict[gene] = y_count - m_count
        if m_count != 0:
            m_dict[gene] = m_count
        if w_count != 0:
            w_dict[gene] = w_count - m_count
        
        y_all += y_count - m_count
        m_all += m_count
        w_all += w_count - m_count

        #for i in range(y_count):
        #    y_text += gene+","


#fpath = "/Library/Fonts/ヒラギノ角ゴ Pro W3.otf"
fpath = "/Library/Fonts/Arial.ttf"

#wordcloud_y = WordCloud(background_color="white",font_path=fpath,
#    width=800,height=600).generate(y_text)

all_count = y_all + m_all + w_all


magni_y = round(float(y_all)/all_count,2)
magni_m = round(float(m_all)/all_count,2)
magni_w = round(float(w_all)/all_count,2)

magni_y = 0.2

max_index = 40
font_index = 400
scale_index = 0.5
width = 400
height = 600

max_y = int(round(max_index*magni_y,0))
max_m = int(round(max_index*magni_m,0))
max_w = int(round(max_index*magni_w,0))

font_y = int(round(font_index*magni_y,0))
font_m = int(round(font_index*magni_m,0))
font_w = int(round(font_index*magni_w,0))

width_y = int(round(width*magni_y,0))
width_m = int(round(width*magni_m,0))
width_w = int(round(width*magni_w,0))

height_y = int(round(height*magni_y,0))
height_m = int(round(height*magni_m,0))
height_w = int(round(height*magni_w,0))


max_y = 5
max_m = 10
max_w = 5

minfontsize = 10
margin_size = 8

print magni_y, magni_m, magni_w

#y_dict["FLT3"] = 5


wordcloud_y = WordCloud(background_color=None,
    mode="RGBA",
    font_path=fpath,
    margin=margin_size,
    width=width_y,
    height=height_y,
    relative_scaling=scale_index,
    prefer_horizontal=1,
    max_words=max_y,
    min_font_size=minfontsize,
    #max_font_size=round(300*magni_y,0),
    color_func=grey_color_func).generate_from_frequencies(y_dict, font_y)

wordcloud_m = WordCloud(background_color=None,
    mode="RGBA",
    font_path=fpath,
    margin=margin_size,
    width=width_m,
    height=height_m,
    relative_scaling=scale_index,
    prefer_horizontal=1,
    max_words=max_m,
    min_font_size=minfontsize,
    #max_font_size=round(300*magni_m,0),
    color_func=grey_color_func).generate_from_frequencies(m_dict, font_m)

wordcloud_w = WordCloud(background_color=None,
    mode="RGBA",
    font_path=fpath,
    margin=margin_size,
    width=width_w,
    height=height_w,
    relative_scaling=scale_index,
    prefer_horizontal=1,
    max_words=max_w,
    min_font_size=minfontsize,
    #max_font_size=round(300*magni_w,0),
    color_func=grey_color_func).generate_from_frequencies(w_dict, font_w)


wordcloud_y.to_file("./yokomon.png")
wordcloud_m.to_file("./match.png")
wordcloud_w.to_file("./watson.png")



