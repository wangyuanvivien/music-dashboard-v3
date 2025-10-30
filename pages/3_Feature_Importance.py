import streamlit as st
import pandas as pd

# Set the page title and layout
st.set_page_config(layout="wide")
st.title("🤖 Model Feature Importance")

# --- Introduction & Explanation ---
st.info(
    """
    **What is this?** This page shows the results from a **Random Forest** model. 
    
    Unlike simple correlation, this model finds complex, non-linear patterns. The "Importance Score" 
    shows which features were the **most *predictive*** of a song's popularity.
    
    A higher score means the feature was more important to the model's predictions.
    """
)

# --- The Most Important Caveat ---
st.warning(
    """
    **Key Finding:** The model's low accuracy score (R-squared = -0.23) tells us that the 
    available features (lyrics, genre, key) are **not enough** to reliably predict a 
    popularity score. 
    
    This strongly implies that the **missing audio data** (like `bpm`, `danceability`, 
    and `mood_*`) are the most critical features for predicting popularity.
    """
)

st.markdown("---")

# --- Finding 1: Top 20 Most Important Features ---
st.header("Top 20 Most Predictive Features")
st.write(
    """
    Even with low accuracy, the model shows us which of the available features it
    relied on most. **Lyric Word Count** was, by far, the most important feature,
    followed by specific keys and AI-generated themes.
    """
)

# Create a DataFrame for the Feature Importance
# Data is hard-coded from our analysis
feature_data = {
    'Feature': [
        'Lyric Word Count',
        'Key: D',
        'AI Theme: Unconditional Devotion (無條件的奉獻與承諾...)',
        'Genre: Pop',
        'AI Sentiment: Melancholy w/ Firm Relief (憂鬱中帶有堅定的釋懷...)',
        'AI Theme: Early-love Hesitation (戀愛初期的猶豫...)',
        'Genre: Jazz',
        'AI Theme: No-Regret Love & Fated Parting (無悔的愛與和平的分手...)',
        'Genre: Classical',
        'AI Theme: Firm Love Commitment (堅定的愛情承諾...)',
        'AI Sentiment: Anxious & Hopeful (忐忑不安、矛盾...)',
        'AI Sentiment: Firm, Hopeful Love (堅定、深情、充滿希望的愛意...)',
        'AI Sentiment: Urban Alienation to Hope (初始帶有都會的疏離...)',
        'AI Theme: Pain of Heartbreak (失戀的痛苦、情感的自我防衛...)',
        'AI Sentiment: Melancholy & Apathy (憂鬱、孤寂、決絕...)',
        'AI Theme: Yearning for Stable Love (對穩定關係的渴望...)',
        'AI Sentiment: Melancholy & Helplessness (憂鬱、沉重、無奈...)',
        'AI Sentiment: Relief & Gratitude (釋然、感恩與對幸福的珍視...)',
        'AI Sentiment: Passionate, Protective Melancholy (堅定、熱切...)',
        'AI Theme: Hidden Pain & Self-Sacrifice (隱藏的痛苦與自我犧牲...)'
    ],
    'Importance Score': [
        0.1667,  # lyric_word_count
        0.0569,  # key_D
        0.0436,  # ai_theme_無條件的奉獻與承諾...
        0.0341,  # genre_ros_pop
        0.0303,  # ai_sentiment_憂鬱中帶有堅定的釋懷...
        0.0290,  # ai_theme_戀愛初期的猶豫...
        0.0280,  # genre_ros_jaz
        0.0276,  # ai_theme_無悔的愛與和平的分手...
        0.0266,  # genre_ros_cla
        0.0263,  # ai_theme_堅定的愛情承諾...
        0.0245,  # ai_sentiment_忐忑不安、矛盾...
        0.0233,  # ai_sentiment_堅定、深情、充滿希望的愛意...
        0.0178,  # ai_sentiment_初始帶有都會的疏離...
        0.0166,  # ai_theme_失戀的痛苦、情感的自我防衛...
        0.0155,  # ai_sentiment_憂鬱、孤寂、決絕...
        0.0133,  # ai_theme_對穩定關係的渴望...
        0.0115,  # ai_sentiment_憂鬱、沉重、無奈...
        0.0112,  # ai_sentiment_釋然、感恩與對幸福的珍視...
        0.0104,  # ai_sentiment_堅定、熱切...
        0.0103   # ai_theme_隱藏的痛苦與自我犧牲...
    ]
}
feature_df = pd.DataFrame(feature_data).set_index('Feature')

# Display the bar chart
st.bar_chart(feature_df['Importance Score'])
