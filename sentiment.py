pip install textblob
from textblob import TextBlob

import pandas as pd
from textblob import TextBlob

# Reading the CSV file
df = pd.read_csv('/content/sample_data/sidhu moosewala_result.csv')

# Function to perform sentiment analysis
def get_sentiment(title):
    analysis = TextBlob(title)
    polarity = analysis.sentiment.polarity
    
    if polarity > 0:
        return 'Positive'
    elif polarity < 0:
        return 'Negative'
    else:
        return 'Neutral'

# Apply sentiment analysis function to the 'text' column
df['sentiment'] = df['title'].apply(get_sentiment)

# Displaying the DataFrame with sentiment analysis results
print(df)
