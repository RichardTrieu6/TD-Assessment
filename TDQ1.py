from ollama import chat
from ollama import ChatResponse
from pydantic import BaseModel
import pandas as pd
from sklearn.model_selection import train_test_split
import json

class Sentiment (BaseModel):
    publish_date: str
    context: str
    assetclass: str
    country: str
    sentiment: str


df = pd.read_csv('TDS Global FX Assessment - Headlines.csv')

# Sample headline and date for testing
date = "2025-05-27 09:44:46"
headline = "Nvidia Valued More Than Germany Points to Mispricing"

prompt = f"""
        You are an expert financial analyst and trader. 
        Given the headline: {headline}, with date: {date}, 
        your task is to provide only a JSON output of the following structure:
        publish_date: str (Exactly as given)
        context: str (Headline)
        assetclass: str (Equities, Fixed Income, Cash/Cash Equivalents, Real estate, Infrastructure as an asset class, Private Equity, Commodities, Cryptocurrency, Other)
        country: str (ISO 3166-1 alpha 2 country code convention)
        sentiment: str (Positive, Neutral, or Negative)
        
        Headlines unrelated to finance should have neutral sentiment, Other for asset class, and N/A for country.

        For example:
        Headline: IBM PLANS TO INVEST $150B IN AMERICA OVER NEXT FIVE YEARS
        Date: 2025-04-28 08:31:39
        Output: 
        {{
            publish_date: "2025-04-28 08:31:39",
            context: "IBM PLANS TO INVEST $150B IN AMERICA OVER NEXT FIVE YEARS",
            assetclass: "Equities",
            country: "US",
            sentiment: "Positive"
        }}
        """

# Get llama3.2 response from prompt 
response: ChatResponse = chat(model='llama3.2', messages=[
    {
        'role': 'user',
        'content': prompt
    }
])

print(response['message']['content'])

data = json.loads(response['message']['content'])

sentiment = Sentiment(**data)
print(sentiment)

# Split data 
train_df, val_df = train_test_split(df, test_size=0.2, random_state=30)
