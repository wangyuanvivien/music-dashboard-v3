import streamlit as st
import pandas as pd

# Set the page title and layout
st.set_page_config(layout="wide")
st.title("Correlation: What Makes a Song Popular?")

# --- Introduction & Explanation ---
st.info(
    """
    **What is this?** This page shows the **linear correlation (r)** between a song's features
    and its popularity score.
    
    * A value near **+1.0** means as the feature increases, popularity tends to increase.
    * A value near **-1.0** means as the feature increases, popularity tends to decrease.
    * A value near **0.0** means there is little to no *linear* relationship.
    
    This is a first step. The **Random Forest** model (in progress) will find more 
    complex, non-linear patterns.
    """
)

st.markdown("---")

# --- Finding 1: Lyric Sentiment ---
st.header("Finding 1: Lyric Sentiment (The Strongest Link)")
st.write(
    """
    The **AI-analyzed sentiment** of the lyrics was the feature with the strongest
    connection to popularity. Complex, emotional sentiments showed the highest positive
    correlation.
    """
)

# Create a DataFrame for the sentiment correlations
# We'll show the Top 5 Positive and Top 5 Negative
sentiment_data = {
    'Sentiment': [
        'Sincere affection w/ hidden anxiety (懇切的深情與隱藏的焦慮和脆弱)',
        'Firm, affectionate, hopeful love (堅定、深情、充滿希望的愛意...)',
        'Nostalgic, gentle, helplessness (懷舊、溫柔、對時光飛逝的無奈與感傷)',
        'Melancholy w/ firm relief (憂鬱中帶有堅定的釋懷與自我安慰)',
        'Anxious, contradictory, hopeful (忐忑不安、矛盾、帶有希望的猶豫)',
        '...',
        'Passionate worship, dramatic tension (激昂的崇拜、迷戀與戲劇性的張力)',
        'Firm, rebellious, resolute (堅定、反抗、追求自主的決心)',
        'Active, optimistic, uplifting (積極、樂觀、振奮)',
        'Warm, sincere gratitude, joy (溫暖、真摯的感激、喜悅)',
        'Reflective and tranquil (反思與平靜)'
    ],
    'Correlation (r)': [
        0.46,  # 懇切的深情與隱藏的焦慮和脆弱
        0.27,  # 堅定、深情、充滿希望的愛意...
        0.22,  # 懷舊、溫柔、對時光飛逝的無奈與感傷
        0.20,  # 憂鬱中帶有堅定的釋懷與自我安慰
        0.20,  # 忐忑不安、矛盾、帶有希望的猶豫
        0.0,   # ... separator
        -0.11, # 激昂的崇拜、迷戀與戲劇性的張力
        -0.11, # 堅定、反抗、追求自主的決心
        -0.10, # 積極、樂觀、振奮
        -0.10, # 溫暖、真摯的感激、喜悅
        -0.10  # 反思與平靜
    ]
}

# --- THIS IS THE FIX ---
# The error was caused by a missing comma in the list above.
# This code block is now correct.

sentiment_df = pd.DataFrame(sentiment_data).set_index('Sentiment')

# Display the bar chart
st.bar_chart(sentiment_df['Correlation (r)'])


st.markdown("---")

# --- Finding 2: Audio Features ---
st.header("Finding 2: Audio Features (Genre & Key)")
st.write(
    """
    Basic audio features also showed a moderate correlation. 
    Songs identified as **"Classical"** or in the **"Key of E"** had a noticeable positive link to popularity.
    """
)

# Create a DataFrame for the audio feature correlations
audio_data = {
    'Feature': [
        'Genre: Classical (cla)',
        'Key: E',
        'Genre: Pop (pop)'
    ],
    'Correlation (r)': [
        0.24,  # genre_ros_cla
        0.22,  # key_E
        -0.10  # genre_ros_pop
    ]
}
audio_df = pd.DataFrame(audio_data).set_index('Feature')

# Display the bar chart
st.bar_chart(audio_df['Correlation (r)'])


st.markdown("---")

# --- Finding 3: The Missing Data Caveat ---
st.header("Important Data Limitations")
st.warning(
    """
    **Critical Finding:** For the 245 songs that had a `popularity` score, 
    there was **0% overlap** with the following audio features:
    
    * `bpm` (Beats Per Minute)
    * `danceability`
    * All `mood_*` columns (happy, sad, party, etc.)
    
    Because this data was missing, **their correlation could not be calculated.** The next step, a Machine Learning model, will use data imputation to help 
    analyze these features.
    """
)
