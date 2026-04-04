from urlextract import URLExtract
extract = URLExtract()

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