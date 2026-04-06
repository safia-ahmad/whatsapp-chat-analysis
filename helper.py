from urlextract import URLExtract
extract = URLExtract()

from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji


with open('stop_hinglish.txt', 'r') as f:
    stop_words = f.read().split()



def remove_stop_words(message):
    y = []
    for word in message.lower().split():
        if word not in stop_words:
            y.append(word)
    return " ".join(y)


def fetch_stats(selected_user, df):

    df['message'] = df['message'].astype(str)

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]

    words = []
    for message in df['message']:
        words.extend(message.split())

    num_media = df[df['message'].str.contains('omitted', case=False, na=False)].shape[0]
    num_stickers = df[df['message'].str.contains('sticker omitted', case=False, na=False)].shape[0]
    num_audio = df[df['message'].str.contains('audio omitted', case=False, na=False)].shape[0]

    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media, num_stickers, num_audio, len(links)


def most_busy_users(df):
    x = df['user'].value_counts().head()

    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2) \
        .reset_index().rename(columns={'index': 'name', 'user': 'percent'})

    return x, df



def create_wordcloud(selected_user, df):

    df['message'] = df['message'].astype(str)

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[~temp['message'].str.contains('omitted', case=False, na=False)]


    temp['message'] = temp['message'].apply(remove_stop_words)

    wc = WordCloud(
        width=500,
        height=500,
        min_font_size=10,
        background_color='white'
    )

    df_wc = wc.generate(temp['message'].str.cat(sep=" "))

    return df_wc


def most_common_words(selected_user, df):

    df['message'] = df['message'].astype(str)

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[~temp['message'].str.contains('omitted', case=False, na=False)]


    temp['message'] = temp['message'].apply(remove_stop_words)

    words = []

    for message in temp['message']:
        words.extend(message.split())

    most_common_df = pd.DataFrame(Counter(words).most_common(20))

    return most_common_df

def emoji_helper(selected_user, df):

        if selected_user != 'Overall':
            df = df[df['user'] == selected_user]

        emojis = []
        for message in df['message']:
            emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

        emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
        return emoji_df

def monthly_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline
def daily_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df['only_date'] = df['date'].dt.date

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline