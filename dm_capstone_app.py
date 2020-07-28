# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25

Developed by: Zeed Jarrah
"""

# Produce the JSON output that will be used in the visualization
import json
# Perform sentiment analysis on the data
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def sentiment_analyzer_scores(sentence):
    analyser = SentimentIntensityAnalyzer()
    score = analyser.polarity_scores(sentence)
    return score

def process_dataset(biz_dir = "../yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_business.json", 
                    reviews_dir = "../yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json"):
    
    biz_ids = []
    count = 0
    
    #Store business ids with category tag Restaurants in them
    with open(biz_dir, 'r') as fh:
        for line in fh:
            data = json.loads(line)
            
            if "Restaurants" in data['categories'] and "Mediterranean" in data['categories']:
                print(data['categories'])
                count += 1
                biz_ids.append(data['business_id'])
    
    print(count)
    
    dataset = dict()
    for biz in biz_ids:
        dataset[str(biz)] = []
    
    # Append reviews that go with each restaurant
    with open(reviews_dir) as fh:
        for line in fh:
            data = json.loads(line)
            for b in dataset:
                if b == data['business_id']:
                    dataset[b].append(data)
                    break
            
    for key in list(dataset):
        if 50 <= len(dataset[key]):
            print(f"{key} {len(dataset[key])}")
        else:
            dataset.pop(key, None)
           
    print(len(dataset))
    
    return dataset
            

def main():
    restaurants = process_dataset()
    


if __name__ == "__main__":
    main()


