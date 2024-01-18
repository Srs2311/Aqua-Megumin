import random
import json

def refresh_quotes():
    with open("./json/quotes.json","r") as quotesList:
        quotes = json.load(quotesList)
    return quotes

def fetch_quote(quote_text):
    quotes = refresh_quotes()
    if quote_text.startswith(" "):
        quote_text = quote_text[1:]
    if(quote_text == ""):
        quote_response = quotes[random.randint(0,len(quotes))]
    else:
        search_results = []
        for quote in quotes:
            if quote_text.lower() in quote.lower():
                search_results.append(quote)                      
        if len(search_results) > 0:
            quote_response = search_results[random.randint(0,len(search_results)) -1]
        else:
            quote_response = "No Quote Found"
    return(quote_response)

def add_quote(quote_text):
    quotes = refresh_quotes()
    quotes.append(quote_text)
    with open("./json/quotes.json","w") as quoteList:
        quoteList.write(json.dumps(quotes))