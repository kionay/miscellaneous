import re, requests, json, codecs, math

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
        res = requests.get("http://hashtagify.me/data/tags/" + word.lower() + "/10/6")
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

    for pop in popularity:
        print(pop)
        print("\t\t\t weighted:" + str(popularity[pop]["weighted"]))
        print("\t\t\t unweighted:" + str(popularity[pop]["unweighted"]))
    #print(json.dumps(popularity,sort_keys=True,indent=4))

main()

