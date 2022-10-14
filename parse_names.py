import pickle
import os
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np


# Read list to memory
def read_list():
    # for reading also binary mode is important
    with open("twitter_data", 'rb') as fp:
        n_list = pickle.load(fp)
        return n_list


tweets = read_list()

# assign directory
directory = 'names'
name_dictionary = {}
# iterate over files in
# that directory
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f) and f.split(".")[0][-4:].isnumeric() and int(f.split(".")[0][-4:]) > 1940:
        with open(f, encoding='utf8') as file:
            for line in file:
                name, gender, count = line.split(",")[0], line.split(",")[1], int(line.split(",")[2])
                if name in name_dictionary:
                    if gender in name_dictionary[name]:
                        name_dictionary[name][gender] += count
                    else:
                        name_dictionary[name][gender] = count
                else:
                    name_dictionary[name] = {gender: count}

name_allocation = {}
for name in name_dictionary:
    if len(name_dictionary[name].keys()) > 1:
        majority_gender = max(name_dictionary[name], key=name_dictionary[name].get)
        name_allocation[name] = majority_gender
    else:
        name_allocation[name] = list(name_dictionary[name].keys())[0]

tweets = read_list()

tweets_with_gender = []
for tweet in tweets:
    name = tweet["name"].split(" ")[0]
    if name in name_allocation:
        tweet["gender"] = name_allocation[name]
        tweets_with_gender.append(tweet)


retweeted_tweets = [tweet for tweet in tweets_with_gender if tweet["retweet"] != "NA"]

tweets_with_gender_and_retweet = []
for tweet in retweeted_tweets:
    retweet_name = tweet["retweet"].split(" ")[0]
    if retweet_name in name_allocation:
        tweet["retweet_gender"] = name_allocation[retweet_name]
        tweets_with_gender_and_retweet.append(tweet)

male_tweets = [tweet["time"] for tweet in tweets_with_gender_and_retweet if tweet["gender"] == "M"]
female_tweets = [tweet["time"] for tweet in tweets_with_gender_and_retweet if tweet["gender"] == "F"]

# bins = []
# for h in range(0,24):
#    for min in ["00", "15", "30", "45"]:
#        time = str(h) + ":" + min if h >= 10 else "0" + str(h) + ":" + min
#        bins.append(time)

male_counts = Counter(male_tweets)
female_counts = Counter(female_tweets)
male_counts = dict(sorted(male_counts.items()))
female_counts = dict(sorted(female_counts.items()))

# plt.rcParams.update({'font.size': 5})
# plt.bar(list(male_counts.keys()), [list(male_counts.values()), list(female_counts.values())])
# plt.xticks(rotation=90)
# plt.show()
labels = list(male_counts.keys())
x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width / 2, list(male_counts.values()), width, label='Men')
rects2 = ax.bar(x + width / 2, list(female_counts.values()), width, label='Women')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Scores')
ax.set_title('Tweet numbers by time and gender')
ax.set_xticks(x, labels)
ax.legend()

# ax.bar_label(rects1, padding=3)
# ax.bar_label(rects2, padding=3)

fig.tight_layout()
plt.rcParams.update({'font.size': 5})
# plt.bar(list(male_counts.keys()), [list(male_counts.values()), list(female_counts.values())])
plt.xticks(rotation=90)
plt.show()




male_tweets = [tweet["time"] for tweet in tweets_with_gender_and_retweet if
               tweet["gender"] == "M" and tweet["retweet_gender"] == "M"]
female_tweets = [tweet["time"] for tweet in tweets_with_gender_and_retweet if
                 tweet["gender"] == "F" and tweet["retweet_gender"] == "F"]

male_retweet_counts = Counter(male_tweets)
female_retweet_counts = Counter(female_tweets)
male_retweet_counts = dict(sorted(male_retweet_counts.items()))
female_retweet_counts = dict(sorted(female_retweet_counts.items()))
print(male_counts)
print(male_retweet_counts)
male_retweet_ratio = { key : male_retweet_counts[key]/male_counts[key] for key in male_counts}
female_retweet_ratio = { key : female_retweet_counts[key]/female_counts[key] for key in female_counts}

labels = list(male_retweet_ratio.keys())
x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width / 2, list(male_retweet_ratio.values()), width, label='Men')
rects2 = ax.bar(x + width / 2, list(female_retweet_ratio.values()), width, label='Women')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Scores')
ax.set_title('Homophiligy ratio by time and gender')
ax.set_xticks(x, labels)
ax.legend()

fig.tight_layout()
plt.rcParams.update({'font.size': 5})
# plt.bar(list(male_counts.keys()), [list(male_counts.values()), list(female_counts.values())])
plt.xticks(rotation=90)
plt.show()
