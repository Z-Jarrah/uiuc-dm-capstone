# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25

Developed by: Zeed Jarrah
"""

# Produce the JSON output that will be used in the visualization
import json
import csv
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
                    reviews_dir = "../yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json", doc_min=20):
    
    biz_ids = []
    places = dict()
    #Store business ids with category tag Restaurants in them
    with open(biz_dir, 'r') as fh:
        for line in fh:
            data = json.loads(line)
            
            if "Restaurants" in data['categories'] and "Middle Eastern" in data['categories']:
                places[data['business_id']] = data
                biz_ids.append(data['business_id'])
    
    reviews = dict()
    for biz in biz_ids:
        reviews[str(biz)] = []
    
    # Append reviews that go with each restaurant
    with open(reviews_dir) as fh:
        for line in fh:
            data = json.loads(line)
            for b in reviews:
                if b == data['business_id']:
                    reviews[b].append(data)
                    break
            
    for key in list(reviews):
        if doc_min > len(reviews[key]):
            reviews.pop(key, None)
            places.pop(key, None)
            
    print(f"Number of places with atleast {doc_min} reviews: {len(places)}")
    
    return places, reviews

# Parse all reviews for a business
def parse_food_reviews(reviews, dishes):
    for key in reviews:
        print(f"{key} {len(reviews[key])}")
        for rev in reviews[key]:
            for dish in dishes:
                if dish in str(rev['text']):
                    dish_review = str(rev['text'])
                    format_review = [sentence + '.' for sentence in dish_review.split('.') if dish in sentence]
                    dishes[dish].append((rev['business_id'], format_review[0]))
                    
    for key in dishes:
        print(f"\n\n{key} || Found {len(dishes[key])} relating to this dish\n\n")

    return dishes

# Produce the dict that will go into the 
def write_food_results(food):
    pass

def test_csv():
    test = {'first_name': 'David', 'last_name' : 'Keen', 'ID': 1 }
    
    
    with open('dishes.csv', 'w', newline='') as csvfile:
        fieldnames = ['first_name', 'last_name', 'ID']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow(test)
        
        
def write_scores(food):
    results = []
    poor_info = 0
    for f in food:
        pos_count = 0
        for x in food[f]:
            score = sentiment_analyzer_scores(x[1])
#            print(f"{f} || {score}")
            if score['pos'] > (score['neg']+0.05):
                pos_count += 1
            elif score['neu'] > 1.0:
                poor_info += 1
        
        print(f"{pos_count} / {len(food[f])-(poor_info + 1)} = {pos_count/ (len(food[f]) - poor_info + 1)}")

def main():
    places, reviews = process_dataset()
    dishes = dish_list()
    
    # Compute the overall sentiment for each dish across all restaurants
    food = parse_food_reviews(reviews,dishes)
    
    write_scores(food)


if __name__ == "__main__":
    test_csv()
    main()


