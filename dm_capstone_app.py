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

# Utility function to sort the dictionary
def getKey(item):
    return item[1]

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

#    Debug
#    print(f"Number of places with atleast {doc_min} reviews: {len(places)}")
    
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
        
def food_csv(results):
    with open('dishes.csv', 'w', newline='') as csvfile:
        fieldnames = ['Dish', 'Pos']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for res in results:
            writer.writerow(res)

def places_csv(results):
    with open('restaurants.csv', 'w', newline='') as csvfile:
        fieldnames = ['Restaurant', 'Dish','Stars' , 'Price Range']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for res in results:
            writer.writerow(res)
        
def write_scores(food):
    results = []
    for f in food:
        pos_count = 0
        poor_info = 0
        for x in food[f]:
            score = sentiment_analyzer_scores(x[1])
#            print(f"{f} || {score}")
            if score['pos'] > (score['neg']+0.05):
                pos_count += 1
            elif score['neu'] > 0.9:
                poor_info += 1
        
        sentiment = pos_count / (len(food[f]) - poor_info)
        
        print(f"{pos_count} / {len(food[f])-poor_info} = {sentiment}")
        
        sentiment *= 100
        format_sentiment = "{:0.1f}".format(sentiment)
        results.append({'Dish': f, 'Pos': format_sentiment})

    food_csv(results)

def main():
    places, reviews = process_dataset()
    dishes = dish_list()
    
    # Compute the overall sentiment for each dish across all restaurants
    food = parse_food_reviews(reviews,dishes)
    
    write_scores(food)
    
    # Restaurant CSV Creation
    top_places = dict()
    places_set = set()
    results = []
    for f in food:
        top_places[f] = dict()
        print('===============================================================')
        print(f"===== {f} =====")
        for b in food[f]:
            places_set.add(b[0])
            if places[b[0]]['name'] in top_places[f]:
                top_places[f][places[b[0]]['name']] += 1
            else:
                top_places[f][places[b[0]]['name']] = 1
            
        for s in places_set:
            print(f"{places[s]['name']} || {places[s]['stars']} || {places[s]['attributes']['Price Range']}")
            p = {'Restaurant': places[s]['name'], 'Dish': f,'Stars': places[s]['stars'], 'Price Range': places[s]['attributes']['Price Range']}
            results.append(p)
        
        places_csv(results)
        
        print('===============================================================')


if __name__ == "__main__":
    main()


