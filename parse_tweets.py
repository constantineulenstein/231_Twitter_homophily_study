import json
import sys
import pickle


def round_to_nearest_15_interval(time_string):
    minutes = 15 * ((int(time_string[-2:]) + 7) // 15)
    hours = time_string[:2]
    if minutes == 0:
        return hours + ":" + "00"
    elif minutes == 60:
        if hours == "23":
            return "00:00"
        elif int(hours) <= 8:
            return "0" + str(int(hours) + 1) + ":" + "00"
        else:
            return str(int(hours) + 1) + ":" + "00"
    else:
        return time_string[:3] + str(minutes)


for line in sys.stdin:
    tweet = json.loads(line)
    tweet_dict = {"date": tweet["data"]["created_at"][:10],
                  "time": round_to_nearest_15_interval(tweet["data"]["created_at"][11:16]),
                  "name": tweet["includes"]["users"][0]["name"],
                  "text": tweet["data"]["text"]}

    try:
        tweet_dict["retweet"] = tweet["includes"]["users"][1]["name"] if tweet['data']['referenced_tweets'][0][
                                                                             "type"] == "retweeted" else "NA"
    except:
        tweet_dict["retweet"] = "NA"

    print(json.dumps(tweet_dict)) # This puts the result in sys.stdout straight
