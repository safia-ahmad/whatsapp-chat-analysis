import streamlit as st
import preprocesser
import helper
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(page_title="Chatlytics", layout="wide")

st.sidebar.title("💬 Chatlytics")
uploaded_file = st.sidebar.file_uploader("Upload WhatsApp Chat (.txt)")

if uploaded_file:
    data = uploaded_file.getvalue().decode("utf-8")
    df = preprocesser.preprocess(data)

    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')

    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Analyze for", user_list)

    if st.sidebar.button("Analyze 🚀"):

        with st.spinner("Analyzing chat..."):

            # ---------- TOP STATS ----------
            st.title("📊 Overview")

            num_messages, words, media, stickers, audio, links = helper.fetch_stats(selected_user, df)

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Messages", num_messages)
            c2.metric("Words", words)
            c3.metric("Media", media)
            c4.metric("Links", links)

            c5, c6 = st.columns(2)
            c5.metric("Stickers", stickers)
            c6.metric("Audio", audio)

            # ---------- TIMELINE ----------
            st.title("📈 Monthly Timeline")
            timeline = helper.monthly_timeline(selected_user, df)

            fig, ax = plt.subplots(figsize=(10,4))
            ax.plot(timeline['time'], timeline['message'], color='green')
            plt.xticks(rotation=45)
            st.pyplot(fig)

            # ---------- DAILY ----------
            st.title("📅 Daily Timeline")
            daily = helper.daily_timeline(selected_user, df)

            fig, ax = plt.subplots(figsize=(10,4))
            ax.plot(daily['only_date'], daily['message'], color='black')
            plt.xticks(rotation=45)
            st.pyplot(fig)

            # ---------- ACTIVITY ----------
            st.title("📊 Activity Map")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Busy Days")
                busy_day = helper.week_activity_map(selected_user, df)

                fig, ax = plt.subplots()
                ax.bar(busy_day.index, busy_day.values)
                st.pyplot(fig)

            with col2:
                st.subheader("Busy Months")
                busy_month = helper.month_activity_map(selected_user, df)

                fig, ax = plt.subplots()
                ax.bar(busy_month.index, busy_month.values, color='orange')
                st.pyplot(fig)

            # ---------- HEATMAP ----------
            st.title("🔥 Weekly Activity Heatmap")
            heatmap = helper.activity_heatmap(selected_user, df)

            fig, ax = plt.subplots(figsize=(18,6))
            sns.heatmap(heatmap, cmap='coolwarm', ax=ax)
            st.pyplot(fig)

            # ---------- USERS ----------
            if selected_user == 'Overall':
                st.title("👥 Most Active Users")

                x, new_df = helper.most_busy_users(df)

                col1, col2 = st.columns(2)

                with col1:
                    fig, ax = plt.subplots()
                    ax.bar(x.index, x.values, color='red')
                    plt.xticks(rotation=45)
                    st.pyplot(fig)

                with col2:
                    st.dataframe(new_df)

            # ---------- WORDCLOUD ----------
            st.title("☁️ WordCloud")

            wc = helper.create_wordcloud(selected_user, df)

            fig, ax = plt.subplots(figsize=(8,8))  # 👈 bigger = not blurry
            ax.imshow(wc, interpolation='bilinear')  # 👈 smooth rendering
            ax.axis('off')
            st.pyplot(fig)

            # ---------- WORDS ----------
            st.title("📝 Most Common Words")
            common = helper.most_common_words(selected_user, df)

            fig, ax = plt.subplots(figsize=(8,6))
            ax.barh(common[0], common[1])
            st.pyplot(fig)

            # ---------- EMOJI ----------
            st.title("😂 Emoji Analysis")
            emoji_df = helper.emoji_helper(selected_user, df).head(5)

            col1, col2 = st.columns(2)
            col1.dataframe(emoji_df)

            with col2:
                fig, ax = plt.subplots()
                ax.pie(emoji_df[1], labels=emoji_df[0], autopct="%0.1f%%")
                st.pyplot(fig)

            # ---------- SENTIMENT ----------
            st.title("😊 Sentiment Analysis")
            sentiment = helper.sentiment_analysis(selected_user, df)

            fig, ax = plt.subplots()
            ax.bar(sentiment.index, sentiment.values, color=['green','red','gray'])
            st.pyplot(fig)