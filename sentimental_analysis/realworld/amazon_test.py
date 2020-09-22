# -*- coding: utf-8 -*-
# Reference: https://blog.datahut.co/scraping-amazon-reviews-python-scrapy/
# Importing Scrapy Library
import os
import scrapy


# Creating a new class to implement Spide
class AmazonReviewsSpider(scrapy.Spider):
    # Spider name
    name = 'amazon_reviews'

    # Domain names to scrape
    allowed_domains = ['amazon.com']
    os.system("rm ~/build/bsharathramesh/SE_Project1/sentimental_analysis/realworld/reviews.json")
    my_file_handle = open('~/build/bsharathramesh/SE_Project1/sentimental_analysis/realworld/ProductAnalysis.txt')
    myBaseUrl = my_file_handle.read()
    # myBaseUrl = "https://www.amazon.in/Apple-MacBook-Air-13-3-inch-MQD32HN/product-reviews/B073Q5R6VR/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&amp;amp;reviewerType=all_reviews&amp;amp;pageNumber="
    start_urls = []

    # Creating list of urls to be scraped by appending page number a the end of base url
    for i in range(1, 121):
        start_urls.append(myBaseUrl + str(i))

    # Defining a Scrapy parser
    def parse(self, response):
        data = response.css('#cm_cr-review_list')

        # Collecting product star ratings
        star_rating = data.css('.review-rating')

        # Collecting user reviews
        comments = data.css('.review-text')
        count = 0

        # Combining the results
        for review in star_rating:
            yield {'stars': ''.join(review.xpath('.//text()').extract()),
                   'comment': ''.join(comments[count].xpath(".//text()").extract())
                   }
            count = count + 1
