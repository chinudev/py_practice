import requests  # Import the requests library to handle HTTP requests
import json

def sentiment_analyzer(text_to_analyse):  # Define a function named sentiment_analyzer that takes a string input (text_to_analyse)
    url = 'https://sn-watson-sentiment-bert.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/SentimentPredict'  # URL of the sentiment analysis service
    myobj = { "raw_document": { "text": text_to_analyse } }  # Create a dictionary with the text to be analyzed
    header = {"grpc-metadata-mm-model-id": "sentiment_aggregated-bert-workflow_lang_multi_stock"}  # Set the headers required for the API request
    response = requests.post(url, json = myobj, headers=header)  # Send a POST request to the API with the text and headers
    if response.status_code == 200: 
        response_dict = json.loads(response.text)
        label = response_dict['documentSentiment']['label']
        score = response_dict['documentSentiment']['score']
    else:
        label = None
        score = None
    
    return {'label' : label, 'score' : score}
