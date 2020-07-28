# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25

Developed by: Zeed Jarrah
"""

# Produce the JSON output that will be used in the visualization
import json
# Perform sentiment analysis on the data
import vaderSentiment

def process_dataset():
    biz_dir = "../yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_business.json"
    reviews_dir = "../yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json"
    count = 0
    #Store business ids with category tag Restaurants in them
    with open(biz_dir, 'r') as fh:
        for line in fh:
            data = json.loads(line)
            
            if "Restaurants" in data['categories'] and "Mediterranean" in data['categories']:
                print(data['categories'])
                count += 1
    
    print(count)

            
            

def main():
    process_dataset()


if __name__ == "__main__":
    main()


