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
    a = ""
    for x in text_file:
            if len(x)>2:
                b = x.split()
                for i in b:
                    a += i + " "
    return a

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
        text_file = open("ProductAnalysis.txt", "w")
        text_file.write(blogname)
    else:
        note = "Please Enter the product blog name for analysis"
        return render(request, 'realworld/productanalysis.html', {'note': note})

# Custom template filter to retrieve a dictionary value by key.
@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key, 0)