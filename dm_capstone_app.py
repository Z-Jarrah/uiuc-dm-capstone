# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25

Developed by: Zeed Jarrah
"""

# Produce the JSON output that will be used in the visualization
import json
# Perform sentiment analysis on the data
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Utilize VADER to compute a sentiment score for each review
def sentiment_analyzer_scores(sentence):
    analyser = SentimentIntensityAnalyzer()
    score = analyser.polarity_scores(sentence)
    return score

def dish_list(dish_dir="dish_names.txt"):
    dishes = dict()
    with open(dish_dir, 'r') as fh:
        for line in fh:
            line = line.strip('\n')
            dishes[line] = list()
    
    return dishes

# Process the business and review json files and produce a csv containing the sentiments, price categoryyn
def process_dataset(biz_dir = "../yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_business.json", 
                    reviews_dir = "../yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json", doc_min=50):
    
    biz_ids = []
    count = 0
    id2name = dict()
    #Store business ids with category tag Restaurants in them
    with open(biz_dir, 'r') as fh:
        for line in fh:
            data = json.loads(line)
            
            if "Restaurants" in data['categories'] and "Mediterranean" in data['categories']:
                id2name[data['business_id']] = data
                count += 1
                biz_ids.append(data['business_id'])
    
    
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
        if doc_min > len(dataset[key]):
            dataset.pop(key, None)
            id2name.pop(key, None)
           
    print(len(dataset))
    print(len(id2name))
    
    return id2name, dataset

# Parse all reviews for a business
def parse_reviews(reviews, dishes):
    
    for key in reviews:
        print(f"{key} {len(reviews[key])}")
        for rev in reviews[key]:
            for dish in dishes:
                if str(dish) in str(rev['text']):
                    print(rev['text'])
            
#    dish_review = str(r['text'])
#    format_review = [sentence + '.' for sentence in dish_review.split('.') if key in sentence]
#    print(format_review)

def main():
    idlist, restaurants = process_dataset()
    dishes = dish_list()
    
    parse_reviews(restaurants, dishes)
    


if __name__ == "__main__":
    main()


