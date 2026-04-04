import streamlit as st
import preprocesser
import helper

st.sidebar.title("WhatsApp Chat Analyzer 💬")
uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df=preprocesser.preprocess(data)
    st.dataframe(df)

    #fetch unique user
    user_list=df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)
    if st.sidebar.button("show analysis"):
        num_messages, words, num_media, num_stickers, num_audio,num_links = helper.fetch_stats(selected_user, df)
        col1, col2, col3, col4, col5,col6 = st.columns(6)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media")
            st.title(num_media)

        with col4:
            st.header("Stickers")
            st.title(num_stickers)

        with col5:
            st.header("Audio")
            st.title(num_audio)

        with col6:
            st.header("Links")
            st.title(num_links)



