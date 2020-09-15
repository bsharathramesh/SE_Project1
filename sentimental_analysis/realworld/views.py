from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import sys
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from django.template.defaulttags import register
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from io import StringIO
from .utilityFunctions import *
import os
import json

def pdfparser(data):

    fp = open(data, 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
        data =  retstr.getvalue()

    text_file = open("Output.txt", "w", encoding="utf-8")
    text_file.write(data)

    text_file = open("Output.txt",'r', encoding="utf-8")
    final_comment = []
    a = ""
    for x in text_file:
            if len(x)>2:
                b = x.split()
                for i in b:
                    a+=" "+i
    final_comment = a.split('.')
    return final_comment

def analysis(request):
    return render(request,'realworld/analysis.html')

def get_clean_text(text):
    text = removeLinks(text)
    text = stripEmojis(text)
    text = removeSpecialChar(text)
    text = stripPunctuations(text)
    text = stripExtraWhiteSpaces(text)
    return text

def input(request):
    if request.method=='POST':
        name = request.POST.get("Name", "")
        file = request.FILES['document']
        fs = FileSystemStorage()
        fs.save(file.name,file)
        pathname = "media/"
        value = pdfparser(pathname+file.name)

        # Sentiment Analysis
        text = get_clean_text(value)
        result = sentiment_scores(text)
        print(result)
        return render(request, 'realworld/sentiment_graph.html', {'sentiment': result})
    else:
        note = "Please Enter the file you want it to be uploaded"
        return render(request, 'realworld/home.html', {'note': note})

def productanalysis(request):
    if request.method=='POST':
        blogname = request.POST.get("blogname", "")
        text_file = open("/Users/nischalkashyap/Downloads/Projects/SE_Project1/Amazon_Comments_Scrapper/amazon_reviews_scraping/amazon_reviews_scraping/spiders/ProductAnalysis.txt", "w")
        text_file.write(blogname)
        text_file.close()
        os.system('scrapy runspider /Users/nischalkashyap/Downloads/Projects/SE_Project1/Amazon_Comments_Scrapper/amazon_reviews_scraping/amazon_reviews_scraping/spiders/amazon_review.py -o reviews.json')
        final_comment = []
        with open('/Users/nischalkashyap/Downloads/Projects/SE_Project1/sentimental_analysis/reviews.json') as json_file:
            data = json.load(json_file)
            for p in range(1,len(data)-1):
                a = data[p]['comment']
                final_comment.append(a)

        #final_comment is a list of strings!
        text = get_clean_text(final_comment)
        result = sentiment_scores(text)
        print(result)
        return render(request, 'realworld/sentiment_graph.html', {'sentiment': result})

    else:
        note = "Please Enter the product blog name for analysis"
        return render(request, 'realworld/productanalysis.html', {'note': note})

# Custom template filter to retrieve a dictionary value by key.

def textanalysis(request):
    if request.method == 'POST':
        text_data = request.POST.get("Text", "")
        final_comment = text_data.split('.')

        # final_comment is a list of strings!
        text = get_clean_text(final_comment)
        result = sentiment_scores(text)
        print(result)
        return render(request, 'realworld/sentiment_graph.html', {'sentiment': result})
    else:
        note = "Text to be analysed!"
        return render(request, 'realworld/textanalysis.html', {'note': note})

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key, 0)