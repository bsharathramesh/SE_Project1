from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from django.template.defaulttags import register
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from io import StringIO
from utilityFunctions import *
import os
import json
import speech_recognition as sr


def pdfparser(data):
    fp = open(data, 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
        data = retstr.getvalue()

    text_file = open("Output.txt", "w", encoding="utf-8")
    text_file.write(data)

    text_file = open("Output.txt", 'r', encoding="utf-8")
    a = ""
    for x in text_file:
        if len(x) > 2:
            b = x.split()
            for i in b:
                a += " " + i
    final_comment = a.split('.')
    return final_comment

def get_clean_text(text):
    text = removeLinks(text)
    text = stripEmojis(text)
    text = removeSpecialChar(text)
    text = stripPunctuations(text)
    text = stripExtraWhiteSpaces(text)

    # Tokenize using nltk
    tokens = nltk.word_tokenize(text)

    # Import stopwords
    stop_words = set(stopwords.words('english'))
    stop_words.add('rt')
    stop_words.add('')

    # Remove tokens which are in stop_words
    newtokens = [item for item in tokens if item not in stop_words]

    textclean = ' '.join(newtokens)
    return textclean


def detailed_analysis(result):
    result_dict = {}
    neg_count = 0
    pos_count = 0
    neu_count = 0
    total_count = len(result)

    for item in result:
        cleantext = get_clean_text(str(item))
        sentiment = sentiment_scores(cleantext)
        compound_score = sentiment['compound']

        pos_count += sentiment['pos']
        neu_count += sentiment['neu']
        neg_count += sentiment['neg']

    total = pos_count + neu_count + neg_count
    result_dict['pos'] = (pos_count / total)
    result_dict['neu'] = (neu_count / total)
    result_dict['neg'] = (neg_count / total)

    return result_dict

def input(pathname):
    extension_name = pathname[len(pathname) - 3:]
    result = {}
    if extension_name == 'pdf':
        value = pdfparser(pathname)
        result = detailed_analysis(value)
    elif extension_name == 'txt':
        text_file = open(pathname, 'r', encoding="utf-8")
        a = ""
        for x in text_file:
            if len(x) > 2:
                b = x.split()
                for i in b:
                    a += " " + i
        final_comment = a.split('.')
        result = detailed_analysis(final_comment)
    elif extension_name == 'wav':
        r = sr.Recognizer()
        with sr.AudioFile(pathname) as source:
            # listen for the data (load audio to memory)
            audio_data = r.record(source)
            # recognize (convert from speech to text)
            text = r.recognize_google(audio_data)
            value = text.split('.')
            result = detailed_analysis(value)
    # Sentiment Analysis
    return result


def productanalysis():
        os.system('scrapy runspider ./amazon_test.py -o ./reviews.json')
        final_comment = []
        with open('./reviews.json') as json_file:
            data = json.load(json_file)
            for p in range(1, len(data) - 1):
                a = data[p]['comment']
                final_comment.append(a)

        # final_comment is a list of strings!
        result = detailed_analysis(final_comment)
        return result

def textanalysis(final_comment):
        final_comment = final_comment.split('.')
        result = detailed_analysis(final_comment)
        return result

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key, 0)

if __name__ == "__main__":
    count = 0
    string_name = "Its been a pleasure working with you! The lunch was great and the ambience was amazing"
    test1_output = textanalysis(string_name)
    expected_output1 = {'pos': 0.699, 'neu': 0.301, 'neg': 0.0}
    if test1_output==expected_output1:
        count+=1

    test2_output = productanalysis()
    expected2_output = {'pos': 0.079474061957537, 'neu': 0.8279877153157976, 'neg': 0.09253822272666543}

    if test2_output==expected2_output:
        count+=1
    test3_output = input("../media/Nischal_Badarinath_Kashyap.pdf")
    expected_output3 = {'pos': 0.06351351351351352, 'neu': 0.9209189189189189, 'neg': 0.015567567567567572}

    if expected_output3==test3_output:
        count+=1

    if count==3:
        print("All test Cases Passed")
    else:
        print("One or more test cases failed!!")
