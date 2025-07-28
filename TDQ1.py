from ollama import chat
from ollama import ChatResponse
from pydantic import BaseModel
import pandas as pd
from sklearn.model_selection import train_test_split
import json
import re

class Sentiment (BaseModel):
    publish_date: str
    context: str
    assetclass: str
    country: str
    sentiment: str


df = pd.read_csv('TDS Global FX Assessment - Headlines.csv')


# Get llama3.2 response from prompt 
def llama(headline, date):
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
        The country label for headlines about a foreign currency should have the associated country for that currency.
        For example, if the headline is about CAD, the country should be Canada

        For example:
        Headline: IBM PLANS TO INVEST $150B IN AMERICA OVER NEXT FIVE YEARS
        Date: 2025-04-28 08:31:39
        Output: 
        {{
            "publish_date": "2025-04-28 08:31:39",
            "context": "IBM PLANS TO INVEST $150B IN AMERICA OVER NEXT FIVE YEARS",
            "assetclass": "Equities",
            "country": "US",
            "sentiment": "Positive"
        }}

        Your output must be only be valid JSON and nothing else. Include both opening and closing brackets and commas.
        """
    
    try:
        response = chat(
            model='llama3.2',
            messages=[{'role': 'user', 'content': prompt}],
            format='json', 
            options={'temperature': 0}  
        )
        
        # Clean LLM Output
        content = response['message']['content'].strip()
        data = json.loads(content)
        return data
        
    except Exception as e:
        return None




# Split data 
train_df, val_df = train_test_split(df, test_size=0.2, random_state=30)
results = []
for i in range(10):
    date = df.iloc[i]['date']
    headline = df.iloc[i]['headline']
    result = llama(headline=headline,date=date)
    results.append(result)
    print(i)
    
results_df=pd.DataFrame.from_dict(results)
results_df.to_json('sentiment_results.csv', orient='records',lines=True)
