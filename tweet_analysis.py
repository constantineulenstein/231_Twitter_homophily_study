import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
import pandas as pd
import json

file_name = "twitter_data_corruption"


# Read list to memory
def read_list(name):
    with open(name, 'r') as f:
        tweets = list(map(json.loads, f))
    return tweets


def create_gender_dict():
    female_names = pd.read_csv('female_names.tsv', sep='\t')
    female_names = female_names.loc[female_names["year"] > 1940].loc[female_names["year"] < 2012]
    female_names = female_names.groupby(['name']).sum()["count"]

    male_names = pd.read_csv('male_names.tsv', sep='\t')
    male_names = male_names.loc[male_names["year"] > 1940].loc[male_names["year"] < 2012]
    male_names = male_names.groupby(['name']).sum()["count"]

    names = pd.merge(male_names, female_names, right_index=True, left_index=True, how="outer").fillna(0)
    names = names.rename(columns={"count_x": "M", "count_y": "F"})
    gender_dict = {}
    for index, row in names.iterrows():
        gender_dict[index] = "M" if row["M"] > row["F"] else "F"

    return gender_dict


def plot_tweet_dist(male, female, topic="Tweet numbers"):
    labels = list(male.keys())

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    plt.rcParams.update({'font.size': 8})
    fig, ax = plt.subplots(figsize=(16, 10))

    ax.bar(x - width / 2, list(male.values()), width, label='Men')
    ax.bar(x + width / 2, list(female.values()), width, label='Women')
    ax.set_ylabel(topic)
    ax.set_title(f'{topic} by time and gender')
    ax.set_xticks(x, labels)
    ax.legend()

    # fig.tight_layout()
    plt.xticks(rotation=90)
    plt.show()


def compute_weighted_average_homopholy(volume_male, volume_female, ratio_male, ratio_female):
    total_tweets_men = sum(volume_male.values())
    total_tweets_woman = sum(volume_female.values())
    wgt_avg_hom_men = 0
    wgt_avg_hom_women = 0
    for key in volume_male:
        wgt_avg_hom_men += volume_male[key] * ratio_male[key]
        wgt_avg_hom_women += volume_female[key] * ratio_female[key]
    return wgt_avg_hom_men/total_tweets_men, wgt_avg_hom_women/total_tweets_woman


tweets = read_list(file_name)

print(f"There are {len(tweets)} tweets with Corruption in total!")

name_allocation = create_gender_dict()

tweets_with_gender = []
for tweet in tweets:
    name = tweet["name"].split(" ")[0]
    if name in name_allocation:
        tweet["gender"] = name_allocation[name]
        tweets_with_gender.append(tweet)

male_tweets = [tweet["time"] for tweet in tweets_with_gender if tweet["gender"] == "M"]
female_tweets = [tweet["time"] for tweet in tweets_with_gender if tweet["gender"] == "F"]
print(f"There are {len(tweets_with_gender)} tweets that a gender could be assigned,{len(male_tweets)} of which are "
      f"men and {len(female_tweets)} of which are women.")

retweeted_tweets = [tweet for tweet in tweets_with_gender if tweet["retweet"] != "NA"]

tweets_with_gender_and_retweet = []
for tweet in retweeted_tweets:
    retweet_name = tweet["retweet"].split(" ")[0]
    if retweet_name in name_allocation:
        tweet["retweet_gender"] = name_allocation[retweet_name]
        tweets_with_gender_and_retweet.append(tweet)

male_tweets = [tweet["time"] for tweet in tweets_with_gender_and_retweet if tweet["gender"] == "M"]
female_tweets = [tweet["time"] for tweet in tweets_with_gender_and_retweet if tweet["gender"] == "F"]
print(f"There are {len(tweets_with_gender_and_retweet)} tweets that have a retweet and a gender could be assigned to "
      f"both the OG and tweet, {len(male_tweets)} of which are men and {len(female_tweets)} of which are women.")

male_counts = Counter(male_tweets)
female_counts = Counter(female_tweets)
male_counts = dict(sorted(male_counts.items()))
female_counts = dict(sorted(female_counts.items()))

plot_tweet_dist(male_counts, female_counts, "Tweet numbers")

male_tweets_with_retweets = [tweet["time"] for tweet in tweets_with_gender_and_retweet if
                             tweet["gender"] == "M" and tweet["retweet_gender"] == "M"]
female_tweets_with_retweets = [tweet["time"] for tweet in tweets_with_gender_and_retweet if
                               tweet["gender"] == "F" and tweet["retweet_gender"] == "F"]

male_retweet_counts = Counter(male_tweets_with_retweets)
female_retweet_counts = Counter(female_tweets_with_retweets)
male_retweet_counts = dict(sorted(male_retweet_counts.items()))
female_retweet_counts = dict(sorted(female_retweet_counts.items()))

male_retweet_ratio = {key: male_retweet_counts[key] / male_counts[key] for key in male_counts}
female_retweet_ratio = {key: female_retweet_counts[key] / female_counts[key] for key in female_counts}
plot_tweet_dist(male_retweet_ratio, female_retweet_ratio, "Homophily ratios")

wgt_avg_men, wgt_avg_women = compute_weighted_average_homopholy(male_counts, female_counts, male_retweet_ratio, female_retweet_ratio)

print(f"The weighted average homophily ratio for men is {wgt_avg_men} and for women is {wgt_avg_women}")

#female_tweets_nine_thirty = [tweet["text"] for tweet in tweets_with_gender_and_retweet if
#                             tweet["gender"] == "F" and tweet["retweet_gender"] == "F" and tweet["time"] == "21:30"]
#print(np.unique(female_tweets_nine_thirty, return_counts=True))
