import streamlit as st
import preprocesser
import helper
import matplotlib.pyplot as plt

st.sidebar.title("WhatsApp Chat Analyzer 💬")
uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocesser.preprocess(data)

    st.dataframe(df)

    # fetch users
    user_list = df['user'].unique().tolist()

    if 'group_notification' in user_list:
        user_list.remove('group_notification')

    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("show analysis"):

        num_messages, words, num_media, num_stickers, num_audio, num_links = helper.fetch_stats(selected_user, df)

        # top stats
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Messages", num_messages)

        with col2:
            st.metric("Words", words)

        with col3:
            st.metric("Media", num_media)

        col4, col5, col6 = st.columns(3)

        with col4:
            st.metric("Stickers", num_stickers)

        with col5:
            st.metric("Audio", num_audio)

        with col6:
            st.metric("Links", num_links)

        # busiest users
        if selected_user == 'Overall':
            st.title('Most Busy Users')

            x, new_df = helper.most_busy_users(df)

            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)


        st.title(f"WordCloud for {selected_user}")

        df_wc = helper.create_wordcloud(selected_user, df)

        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        ax.axis('off')
        st.pyplot(fig)

        # most common words
        most_common_df = helper.most_common_words(selected_user, df)

        fig, ax = plt.subplots(figsize=(10, 8))

        ax.barh(most_common_df[0], most_common_df[1])

        plt.tight_layout()
        st.title('Most Common Words')

        st.pyplot(fig)


        # emoji analysis
        # emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)

        # 🔥 limit data
        emoji_df = emoji_df.head(5).reset_index(drop=True)

        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig, ax = plt.subplots()

            ax.pie(
                emoji_df[1],
                labels=emoji_df[0],
                autopct="%0.1f%%",
                startangle=90
            )

            plt.tight_layout()
            st.pyplot(fig)