from urlextract import URLExtract
extract = URLExtract()
from wordcloud import WordCloud



def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # total messages
    num_messages = df.shape[0]

    # total words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # media messages (all omitted types)
    num_media = df[df['message'].str.contains('omitted', case=False)].shape[0]

    # stickers
    num_stickers = df[df['message'].str.contains('sticker omitted', case=False)].shape[0]

    # audio
    num_audio = df[df['message'].str.contains('audio omitted', case=False)].shape[0]

    #links
    links=[]
    for message in df['message']:
        links.extend(extract.find_urls(message))
    return num_messages, len(words), num_media, num_stickers, num_audio,len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df=round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'index': 'name', 'user': 'percent'})
    return x,df

    #word cloud


def create_wordcloud(selected_user, df):

    # filter for selected user
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # ❗ remove unwanted messages (media, stickers, audio, etc.)
    temp = df[~df['message'].str.contains('omitted', case=False)]

    # create wordcloud
    wc = WordCloud(
        width=500,
        height=500,
        min_font_size=10,
        background_color='white'
    )

    df_wc = wc.generate(temp['message'].str.cat(sep=" "))

    return df_wc