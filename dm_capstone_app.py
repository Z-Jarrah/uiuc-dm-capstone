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

def cost_descriptor(desc):
    if 1 == int(desc):
        return "low cost"
    elif 2 == int(desc):
        return "moderate cost"
    elif 3 == int(desc):
        return "high cost" 

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

def places_csv(fname, results):
    with open( fname+'.csv', 'w', newline='') as csvfile:
        fieldnames = ['Restaurant', 'Stars' , 'Price Range']
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

# Return business ids that are in both of the provided dicts
def combo_plate(dish1, dish2):
    dish1_biz = set()
    dish2_biz = set()
    
    for d in dish1:
        dish1_biz.add(d[0])
        
    for d in dish2:
        dish2_biz.add(d[0])
    
#    print(list(dish1_biz & dish2_biz))
    
    return list(dish1_biz & dish2_biz)
    
    
def feature_score(feature_item):
    place_sentiment = dict()
    options = dict()
    for f in feature_item:
        options[f[0]] = []
        
    for f in feature_item:
        options[f[0]].append(f[1])
        
    for o in options:
        place_sentiment[o] = 0.0
        pos_count = 0
        for sent in options[o]:
            scores = sentiment_analyzer_scores(sent)
            if scores['pos'] > scores['neg']+0.05:
                pos_count += 1
        place_sentiment[o] = pos_count/len(options[o])
    
    return place_sentiment
    

def main():
    places, reviews = process_dataset()
    dishes = dish_list()
    
    # Compute the overall sentiment for each dish across all restaurants
    food = parse_food_reviews(reviews,dishes)
    
#    write_scores(food)
    
    # Restaurant CSV Creation
    # Curated combo of Hummus and Falafel
    print("=== Hummus & Falafel ===")
    combo_places = combo_plate(food['hummus'], food['falafel'])
    combo_result = []
    for c in combo_places:
        if 4.5 <= float(places[c]['stars']):
            combo_result.append({'Restaurant': places[c]['name'], 'Stars': places[c]['stars'] , 'Price Range': cost_descriptor(places[c]['attributes']['Price Range'])})
    
    places_csv('combo', combo_result)
    
    # Top feature for Kabobs
    print("=== Best Kabobs ===")
    candidate_places = feature_score(food['kabob'])
    
    feature_result = [] 
    for c in candidate_places:
        if 0.666 <= candidate_places[c]:
            float_sentiment =candidate_places[c] * 100
            format_sentiment = "{:0.1f}".format(float_sentiment)
            feature_result.append({'Restaurant': places[c]['name'], "Sentiment(%)": format_sentiment, 'Stars': places[c]['stars'] , 'Price Range': cost_descriptor(places[c]['attributes']['Price Range'])})
    
    with open('topkabob.csv', 'w', newline='') as csvfile:
        fieldnames = ['Restaurant', 'Sentiment(%)', 'Stars' , 'Price Range']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for res in feature_result:
            writer.writerow(res)
    
    # Shawarma Night: Restaurants that are good for dinner    
    print("=== Shawarma night ===")
    good_spots = []
    good_for_attribute = set()
    for s in food['shawarma']:
        good_for_attribute.add(s[0])
    
    for g in good_for_attribute:
        if True == bool(places[g]['attributes']['Good For']['dinner']) and 4.0 <= float(places[g]['stars']):
            good_spots.append({'Restaurant': places[g]['name'] , 'Stars': places[g]['stars'] , 'Price Range': cost_descriptor(places[g]['attributes']['Price Range'])})
    
    places_csv('shawarma_night', good_spots)


if __name__ == "__main__":
    main()


