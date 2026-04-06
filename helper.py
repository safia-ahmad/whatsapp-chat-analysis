from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
from textblob import TextBlob

extract = URLExtract()

# ---------------- STOP WORDS ----------------
with open('stop_hinglish.txt', 'r') as f:
    stop_words = f.read().split()


def remove_stop_words(message):
    y = []
    for word in message.lower().split():
        if word not in stop_words:
            y.append(word)
    return " ".join(y)


# ---------------- FETCH STATS ----------------
def fetch_stats(selected_user, df):

    df['message'] = df['message'].astype(str)

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]

    words = []
    for message in df['message']:
        words.extend(message.split())

    num_media = df['message'].str.contains('omitted', case=False, na=False).sum()
    num_stickers = df['message'].str.contains('sticker', case=False, na=False).sum()
    num_audio = df['message'].str.contains('audio', case=False, na=False).sum()

    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media, num_stickers, num_audio, len(links)


# ---------------- MOST BUSY USERS ----------------
def most_busy_users(df):
    x = df['user'].value_counts().head()

    new_df = (df['user'].value_counts() / df.shape[0] * 100).round(2).reset_index()
    return x, new_df


# ---------------- WORDCLOUD ----------------
def create_wordcloud(selected_user, df):

    df['message'] = df['message'].astype(str)

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[~temp['message'].str.contains('omitted', case=False, na=False)]

    temp['message'] = temp['message'].apply(remove_stop_words)

    wc = WordCloud(
        width=800,
        height=800,
        min_font_size=10,
        background_color='white'
    )

    return wc.generate(temp['message'].str.cat(sep=" "))


# ---------------- MOST COMMON WORDS ----------------
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

    return pd.DataFrame(Counter(words).most_common(20))


# ---------------- EMOJI ----------------
def emoji_helper(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    return pd.DataFrame(Counter(emojis).most_common())


# ---------------- MONTHLY TIMELINE ----------------
def monthly_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    timeline['time'] = timeline['month'] + "-" + timeline['year'].astype(str)

    return timeline


# ---------------- DAILY TIMELINE ----------------
def daily_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df['only_date'] = df['date'].dt.date

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline


# ---------------- WEEK ACTIVITY ----------------
def week_activity_map(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()


# ---------------- MONTH ACTIVITY ----------------
def month_activity_map(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()


# ---------------- HEATMAP ----------------
def activity_heatmap(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    heatmap = df.pivot_table(
        index='day_name',
        columns='period',
        values='message',
        aggfunc='count'
    ).fillna(0)

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    heatmap = heatmap.reindex(days)

    heatmap = heatmap.reindex(sorted(heatmap.columns), axis=1)

    return heatmap


# ---------------- SENTIMENT ----------------
def sentiment_analysis(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    sentiments = {"Positive": 0, "Negative": 0, "Neutral": 0}

    for message in df['message']:
        polarity = TextBlob(message).sentiment.polarity

        if polarity > 0:
            sentiments["Positive"] += 1
        elif polarity < 0:
            sentiments["Negative"] += 1
        else:
            sentiments["Neutral"] += 1

    return pd.Series(sentiments)