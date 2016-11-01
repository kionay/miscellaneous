# Credit goes to the maker(s) of http://hashtagify.me/
# as well as it's owner/maker company CyBranding Ltd.

import re, requests, json, codecs, math
from collections import OrderedDict

def my_sort(pop):
    split_unweighted = {}
    split_weighted = {}
    for item in pop:
        if pop[item]["unweighted"] in split_unweighted:
            split_unweighted[pop[item]["unweighted"]].add(item)
        else:
            split_unweighted[pop[item]["unweighted"]] = set({item})
        if pop[item]["weighted"] in split_weighted:
            split_weighted[pop[item]["weighted"]].add(item)
        else:
            split_weighted[pop[item]["weighted"]] = set({item})
    return split_unweighted,split_weighted

def getUniqueWords(words):
    subWords = re.sub('[^A-Za-z0-9\s]+','',words).split()
    longWords = set()
    for word in subWords:
        if len(word) >= 5:
            longWords.add(word)
    return longWords

def rating(t,e):
    a = math.log(1/e)
    i = t/e
    return round(1000*(a-math.log(i))/a)/10

popularity = {}

def main():
    post = '''

'''
    global popularity
    for word in getUniqueWords(post):
        print("Requesting \"" + word + "\"")
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36',
                   'Accept-Encoding':'gzipm deflate, sdch',
                   'Accept-Language':'en-US,en;q=0.8',
                   'Accept':'application/json, text/javascript, */*; q=0.01',
                   'Connection':'keep-alive',
                   'X-Requested-With':'XMLHttpRequest',
                   'Referer':'http://hashtagify.me/hashtag/'+word.lower()}
        res = requests.get("http://hashtagify.me/data/tags/" + word.lower() + "/10/6",headers=headers)
        if res.status_code == 404:
            continue
        res_json = res.json()
        word_tweet_count = int(res_json[word.lower()]["tweets_count"])
        word_nht_count = int(res_json["#stats"]["most_tweeted_nht"][1])
        word_popularity = rating(word_tweet_count,word_nht_count)
        if word_popularity == 0:
            continue
        popularity[word] = {}
        popularity[word]["weighted"] = int((post.count(word)/word_popularity)*100) #add weight based on word frequency
        # without word frequency weight:
        popularity[word]["unweighted"] = word_popularity
    sorted_unweighted, sorted_weighted = my_sort(popularity)
    ordered_unweighted = OrderedDict(sorted(sorted_unweighted.items()))
    ordered_weighted = OrderedDict(sorted(sorted_weighted.items()))
    for pop in ordered_unweighted:
        print("Popularity score: {}.\tWords: {}\n".format(pop,ordered_unweighted[pop]))

main()
input()
