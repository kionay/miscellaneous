# Credit goes to the maker(s) of http://hashtagify.me/
# as well as it's owner/maker company CyBranding Ltd.

import re, requests, json, codecs, math
from collections import OrderedDict

# This sort doesn't *really* sort anything.
# I'm flipping the structure from the words being the keys and popularity the values
#   to the popularity being the keys and the words with that popularity being the values.
# With this flip we can use OrderedDict to sort by popularity, and I don't have to write a sort.
def my_sort(pop):
    split_unweighted = {}
    split_weighted = {}
    for item in pop:
        if pop[item]["unweighted"] in split_unweighted: # Once for weighted items
            split_unweighted[pop[item]["unweighted"]].add(item)
        else:
            split_unweighted[pop[item]["unweighted"]] = set({item})
        if pop[item]["weighted"] in split_weighted:     # Once for unweighted items
            split_weighted[pop[item]["weighted"]].add(item)
        else:
            split_weighted[pop[item]["weighted"]] = set({item})
    return split_unweighted,split_weighted  # Return two dictionaries

# I'm removing words shorter than 5 characters as a quick and dirty way to filter out stop-words.
# I'm removing forward and back slashes before the regex,because they're characters that seperate words without spaces.
# Most punctuation will turn "in, for" regex into "in for" and split to [in,for]
# Slashes will turn "in/for" regex into "infor" and split to [infor]
def getUniqueWords(words):
    subWords = re.sub('[^A-Za-z0-9\s]+','',words.replace("\\"," ").replace("/"," ")).split()
    longWords = set()
    for word in subWords:
        if len(word) >= 5:
            longWords.add(word)
    return longWords

# Ripped from hashtagify's javascript.
# I have no idea how this works, really, just replicating what they've done.
# Which is why they get credit for basically all of this.
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
        res = requests.get("http://hashtagify.me/data/tags/" + word.lower() + "/10/6")
        if res.status_code == 404: # The word isn't popular enough to have a page.
            continue
        res_json = res.json()
        word_tweet_count = int(res_json[word.lower()]["tweets_count"])
        word_nht_count = int(res_json["#stats"]["most_tweeted_nht"][1])
        word_popularity = rating(word_tweet_count,word_nht_count)
        if word_popularity == 0:
            continue
        popularity[word] = {}
        popularity[word]["weighted"] = int((post.count(word)/word_popularity)*100) # add weight based on word frequency
        # without word frequency weight:
        popularity[word]["unweighted"] = word_popularity

   sorted_unweighted, sorted_weighted = my_sort(popularity)
   
   ordered_unweighted = OrderedDict(sorted(sorted_unweighted.items()))
   ordered_weighted = OrderedDict(sorted(sorted_weighted.items()))

   for pop in ordered_unweighted:
       print("Popularity score: {}.\tWords: {}\n".format(pop,ordered__unweighted[pop]))

main()

