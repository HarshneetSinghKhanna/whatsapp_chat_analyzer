from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji


extract = URLExtract()


def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

  
    num_messages = df.shape[0]

    
    words = df['message'].apply(lambda x: len(x.split())).sum()

    
    num_media_messages = df[df['message'] == '<media omitted>\n'].shape[0]

    # no of linkss
    links = []

    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, words, num_media_messages , len(links)


def most_busy_users(df):
    x = df['user'].value_counts().head()
    df =round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns ={'index' : 'name', 'user':'percent'})
    return x,df

def create_wordcloud(selected_user,df):

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()


    if selected_user != 'Overall':
     df = df[df['user'] == selected_user]
   

    temp = df[df['user'] != 'groupnotification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    
    wc = WordCloud(width = 500, height=500,min_font_size= 10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc



def most_common_words(selected_user,df):
   
   f = open('stop_hinglish.txt','r')
   stop_words = f.read()

   temp = df.copy()

   if selected_user != 'Overall':
    df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'groupnotification']
    temp = temp[temp['message'] != '<Media omitted>\n']


   words = []

   for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

   most_common_df = pd.DataFrame(Counter(words).most_common(20))
   return most_common_df
    
def emoji_helper(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)]) 

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Ensure 'date' column is in datetime format
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

   
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.strftime('%b')  

    
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    
    timeline['time'] = timeline.apply(lambda row: f"{row['month']}-{row['year']}", axis=1)

    return timeline
