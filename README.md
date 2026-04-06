# 💬 Chatlytics – WhatsApp Chat Analyzer

A Streamlit-based data analysis application that extracts meaningful insights from exported WhatsApp chats. The system processes raw chat data and visualizes user behavior, communication patterns, and sentiment using Python-based data analysis and visualization techniques.

---

## 📌 Project Overview

With the growing use of messaging platforms, large volumes of conversational data are generated daily. However, this data often remains unstructured and underutilized.

This project aims to transform WhatsApp chat data into meaningful insights by applying data preprocessing, natural language processing (NLP), and visualization techniques.

Users can upload exported WhatsApp chat files and instantly get:

- Message statistics  
- Activity trends over time  
- User participation analysis  
- Word frequency insights  
- Emoji usage patterns  
- Sentiment analysis  

---

## 🎯 Objectives

- Build an end-to-end data analysis pipeline for WhatsApp chat data  
- Handle multiple chat formats (12-hour & 24-hour timestamps)  
- Provide interactive visual insights using Streamlit  
- Implement basic NLP techniques for text cleaning and sentiment analysis  
- Create a clean and user-friendly web interface  

---

## 🧠 Methodology

### Data Processing
- Regex-based parsing of WhatsApp chat exports  
- Extraction of:
  - Users  
  - Messages  
  - Timestamps  
- Handling both:
  - 24-hour format  
  - AM/PM format  

### Feature Engineering
Derived features include:
- Year, Month, Day  
- Day name (Monday–Sunday)  
- Hour-based time intervals  
- Message counts per time unit  

---

## 📊 Analysis Modules

### 📈 Timeline Analysis
- Monthly message trends  
- Daily activity tracking  

### 🔥 Activity Analysis
- Most active days of the week  
- Most active months  
- Hour-wise activity heatmap  

### 👥 User Analysis
- Most active users  
- Percentage contribution of each user  

### ☁️ Text Analysis
- WordCloud visualization  
- Most common words after stopword removal  
- Filtering of system messages (e.g., "media omitted")  

### 😂 Emoji Analysis
- Most frequently used emojis  
- Distribution visualization using charts  

### 😊 Sentiment Analysis
- Message polarity classification:
  - Positive  
  - Negative  
  - Neutral  
- Implemented using TextBlob  

---

## ⚙️ System Architecture

Raw WhatsApp Chat (.txt)  
        ↓  
Preprocessing (Regex + Parsing)  
        ↓  
Feature Engineering  
        ↓  
Analysis Functions (helper.py)  
        ↓  
Visualization (Matplotlib + Seaborn)  
        ↓  
Streamlit Web Interface  

---

## 🛠️ Technologies Used

- Python  
- Streamlit  
- Pandas  
- Matplotlib  
- Seaborn  
- WordCloud  
- TextBlob  
- Regex (re module)  

---

## 🌐 Web Application Features

- Upload WhatsApp chat file (.txt)  
- Select specific user or overall analysis  
- Interactive charts and visualizations  
- Real-time insights generation  
- Clean and responsive UI  

---

## 🚧 Limitations

- Sentiment analysis may not be accurate for Hinglish/slang  
- Does not support multimedia content analysis  
- Depends on WhatsApp export format consistency  
- No real-time chat integration  

---

## 🔮 Future Improvements

- Advanced NLP using transformer models (BERT)  
- Topic modeling for conversation themes  
- Chat relationship insights (who talks to whom more)  
- Emotion detection beyond polarity  
- Deployment as a full-stack SaaS product  

---

## ▶️ How to Run the Project

git clone https://github.com/safia-ahmad/whatsapp-chat-analysis.git  
cd whatsapp-chat-analysis  
pip install -r requirements.txt  
streamlit run app.py  

---

## 👤 Author

Safia Ahmad  
B.Tech – Computer Science  

---

## ✅ Conclusion

This project demonstrates how unstructured conversational data can be transformed into actionable insights using data analysis and visualization techniques. By combining efficient preprocessing, intuitive visualizations, and a simple web interface, the system provides a practical and scalable solution for chat analytics.

---

## 🚀 Live Demo

https://whatsapp-chat-analyz.streamlit.app/
