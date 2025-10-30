import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from collections import Counter

# Set Streamlit page configuration
st.set_page_config(
    page_title="Jeff Chang Music Trend Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 1. Load Data Function ---
@st.cache_data
def load_data(file_path):
    """Loads the CSV data and performs initial type conversion."""
    try:
        # Load the most enriched data file
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        st.error(f"Error: The data file '{file_path}' was not found in the repository. Please ensure it is uploaded.")
        return pd.DataFrame()

# --- 2. Data Cleaning and Preparation (FIXED) ---
@st.cache_data
def prepare_data(df):
    """Cleans up and prepares data for visualization."""
    if df.empty:
        return df

    # Replace empty strings/whitespace with NaN
    df = df.replace(r'^\s*$', np.nan, regex=True)
    
    # --- FIX IS HERE ---
    # Define all columns that need to be numeric for analysis/sorting
    numeric_cols = [
        'viewCount', 'likeCount', 'commentCount', 'popularity', 
        'danceability', 'timbre' # <-- ADDED danceability and timbre
    ]
    
    for col in numeric_cols:
        if col in df.columns:
            # Coerce all to numeric. errors='coerce' turns bad data into NaN
            df[col] = pd.to_numeric(df[col], errors='coerce')

            # Optional: We can still use Int64 for counts if we want
            if col in ['viewCount', 'likeCount', 'commentCount', 'popularity']:
                 df[col] = df[col].astype('Int64', errors='ignore')
            else:
                 # danceability and timbre will remain floats
                 pass
    # --- END FIX ---
            
    # Ensure release_year is Int64 (nullable integer) for filtering
    if 'release_year' in df.columns:
        df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce').astype('Int64', errors='ignore')
    
    # Check if 'consolidated_album_title' exists (it should, but we check)
    if 'consolidated_album_title' not in df.columns and 'album_title' in df.columns:
        # --- RE-INTEGRATE ALBUM CONSOLIDATION (as a safeguard) ---
        # This code is run only if the enriched column is missing, ensuring app stability.
        non_null_albums = df['album_title'].dropna().astype(str)
        all_sub_contents = []
        for title in non_null_albums.unique():
            all_sub_contents.extend([part.strip() for part in title.split('|') if part.strip()])
        sub_content_counts = Counter(all_sub_contents)
        title_mapping = {}
        for original_title in non_null_albums.unique():
            sub_contents = [part.strip() for part in original_title.split('|')]
            valid_sub_contents = [part for part in sub_contents if part]
            if valid_sub_contents:
                consolidated_title = max(valid_sub_contents, key=lambda x: sub_content_counts[x])
            else:
                consolidated_title = original_title 
            title_mapping[original_title] = consolidated_title
        df['consolidated_album_title'] = df['album_title'].map(title_mapping)
    # --- END SAFEGUARD ---
    
    return df

# --- 3. Visualization Helper Functions (Reusable) ---

def generate_pie_chart(data, column_name):
    # Filters out NaN/NA rows for the given column before counting
    data_filtered = data.dropna(subset=[column_name])
    
    if data_filtered.empty:
        st.warning(f"No non-empty data available for **{column_name}** to generate a pie chart.")
        return

    value_counts = data_filtered[column_name].value_counts().reset_index()
    value_counts.columns = [column_name, 'Count']
    total = value_counts['Count'].sum()

    fig = px.pie(
        value_counts, 
        values='Count', 
        names=column_name, 
        title=f'Distribution of **{column_name}** (N={total})',
        hole=0.3, 
        color_discrete_sequence=px.colors.qualitative.D3
    )
    
    st.plotly_chart(fig, use_container_width=True)

def generate_top_tracks_table(data, sort_column):
    data_filtered = data.dropna(subset=[sort_column])
    
    if data_filtered.empty:
        st.warning(f"No non-empty data available for **{sort_column}** to generate the table.")
        return

    display_cols = ['track_name', 'artist_credit_name', 'consolidated_album_title', 'release_year', sort_column]
    final_cols = [col for col in display_cols if col in data_filtered.columns]
    
    top_tracks = data_filtered[final_cols] \
        .sort_values(by=sort_column, ascending=False) \
        .head(50) \
        .reset_index(drop=True)

    st.subheader(f"🏆 Top 50 Tracks by **{sort_column}**")
    
    st.dataframe(
        top_tracks.style.format({
            sort_column: "{:,.0f}" 
        }), 
        use_container_width=True, 
        height=750
    )

# --- 4. Dashboard Page Functions (Updated for Release Year Filter) ---

def show_dashboard(df_filtered):
    """Displays the main visualization dashboard, now filtered by year."""
    
    st.header(f"General Dashboard (Analyzing {len(df_filtered)} rows)")
    st.markdown("---")
    
    st.header("Pie Chart Analysis: Categorical Features")
    
    # Define columns to chart
    pie_chart_cols = ['super_theme', 'genre_ros', 'timbre', 'danceability', 'combined_key']
    all_cols = df_filtered.columns.tolist()
    mood_cols = [col for col in all_cols if col.startswith('mood_')]
    ai_cols = [col for col in all_cols if col.startswith('ai_')]
    
    pie_chart_cols.extend(mood_cols)
    pie_chart_cols.extend(ai_cols)
    
    pie_chart_cols = sorted(list(set(pie_chart_cols)))
    if 'ai_notes' in pie_chart_cols: pie_chart_cols.remove('ai_notes')
    if 'lyrics_text' in pie_chart_cols: pie_chart_cols.remove('lyrics_text')

    # Display charts in 3 columns
    num_cols = 3
    cols = st.columns(num_cols)
    for i, col_name in enumerate(pie_chart_cols):
        try:
            with cols[i % num_cols]:
                generate_pie_chart(df_filtered, col_name)
        except KeyError:
            st.warning(f"Column '{col_name}' missing from the dataset.")

    st.markdown("---")

    # TOP TRACKS TABLES SECTION
    st.header("Top 50 Tracks: Quantitative Measures")
    
    top_track_cols = ['popularity', 'viewCount', 'likeCount', 'commentCount']
    
    num_cols_tables = 2
    table_cols = st.columns(num_cols_tables)
    
    for i, col_name in enumerate(top_track_cols):
        try:
            with table_cols[i % num_cols_tables]:
                generate_top_tracks_table(df_filtered, col_name)
        except KeyError:
             st.warning(f"Column '{col_name}' missing from the dataset.")


# --- 5. New Album Dashboard Function (Unchanged) ---
def show_new_album_dashboard(df):
    """Displays a detailed dashboard for the '屬於' album."""
    ALBUM_NAME = "屬於"
    
    if 'consolidated_album_title' not in df.columns:
        st.error("Album consolidation failed. Cannot filter by consolidated title.")
        return

    df_album = df[df['consolidated_album_title'] == ALBUM_NAME].copy()

    if df_album.empty:
        st.warning(f"Album '{ALBUM_NAME}' not found in the dataset after consolidation.")
        return

    st.title(f"🎵 New Album Analysis: **{ALBUM_NAME}**")
    st.subheader(f"Analyzing {len(df_album)} tracks from this album.")
    
    # 1. Album Track Listing
    st.markdown("### Album Track Listing & Features")
    track_list_cols = ['track_name', 'artist_credit_name', 'popularity', 'viewCount', 'ai_sentiment', 'combined_key']
    
    st.dataframe(
        df_album[track_list_cols].sort_values(by='popularity', ascending=False).reset_index(drop=True),
        use_container_width=True
    )
    
    st.markdown("---")
    
    # 2. Detailed Distribution Charts
    st.markdown("### Detailed Feature Distribution")
    
    detail_cols = ['normalized_key', 'mood_sad', 'ai_theme', 'genre_ros']
    
    cols = st.columns(2)
    for i, col_name in enumerate(detail_cols):
        with cols[i % 2]:
            generate_pie_chart(df_album, col_name)


# --- 6. Song Details Page Function (Unchanged) ---
def show_song_details(df):
    """Allows selection of a song and displays its full details."""
    st.title("🔍 Individual Song Details")
    
    # Create a unique name for the select box
    if 'artist_credit_name' in df.columns:
        df['display_name'] = df['track_name'] + ' - ' + df['artist_credit_name'].fillna('Unknown Artist')
    else:
        df['display_name'] = df['track_name']

    
    selected_track_name = st.selectbox(
        "Select a Song to View Full Details:", 
        options=sorted(df['display_name'].unique())
    )

    if selected_track_name:
        selected_row = df[df['display_name'] == selected_track_name].iloc[0]
        
        st.markdown("---")
        
        st.header(selected_row['track_name'])
        if 'artist_credit_name' in selected_row:
            st.subheader(f"Artist: {selected_row['artist_credit_name']}")
        
        st.markdown("### All Feature Details")
        
        details_df = selected_row.drop('display_name', errors='ignore').reset_index()
        details_df.columns = ['Feature', 'Value']
        
        details_df = details_df.dropna(subset=['Value'])
        
        st.dataframe(
            details_df, 
            use_container_width=True, 
            hide_index=True,
            height=600
        )

# --- 7. Time Series Dashboard Function (Now Safe to Run) ---
def show_time_series_dashboard(df):
    """Displays trends of music features over the release year."""
    st.title("📈 Time Series Analysis: Jeff's Music Evolution")
    
    # --- Data Prep: Filter and Group ---
    df_ts = df.dropna(subset=['release_year']).copy()
    
    if df_ts.empty:
        st.warning("No data available with a valid release year for time series analysis.")
        return

    # Ensure year is treated as discrete bins
    df_ts['release_year'] = df_ts['release_year'].astype(int)
    
    # Group by release year and calculate the mean for key quantitative and feature metrics
    metrics_cols = ['popularity', 'viewCount', 'likeCount', 'danceability', 'timbre']
    
    # Filter metrics_cols to only those that exist in the DataFrame
    available_metrics_cols = [col for col in metrics_cols if col in df_ts.columns]
    
    trend_data = df_ts.groupby('release_year')[available_metrics_cols].mean().reset_index()

    # Calculate missing data count for reporting
    missing_count = len(df) - len(df_ts)
    if missing_count > 0:
        st.info(f"⚠️ **Note:** {missing_count} tracks ({missing_count/len(df)*100:.2f}%) excluded due to missing release year.")

    st.markdown("---")
    
    # --- 1. Popularity/Metrics Trend ---
    st.markdown("### 1. 流行度與 YouTube 互動趨勢")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'viewCount' in trend_data.columns:
            fig_trend_v = px.line(
                trend_data,
                x='release_year',
                y=['viewCount', 'likeCount'],
                title='Avg. YouTube Metrics (Views/Likes) Over Time',
                labels={'value': 'Average Count'},
                markers=True
            )
            fig_trend_v.update_layout(xaxis_tickformat='d')
            st.plotly_chart(fig_trend_v, use_container_width=True)

    with col2:
        if 'popularity' in trend_data.columns:
            fig_trend_p = px.line(
                trend_data,
                x='release_year',
                y='popularity',
                title='Avg. Spotify Popularity Over Time',
                labels={'value': 'Average Popularity Score'},
                markers=True
            )
            fig_trend_p.update_layout(xaxis_tickformat='d')
            st.plotly_chart(fig_trend_p, use_container_width=True)
        
    st.markdown("---")

    # --- 2. Feature Trend ---
    st.markdown("### 2. 聲學特徵進化趨勢")
    
    feature_cols = ['danceability', 'timbre']
    available_feature_cols = [col for col in feature_cols if col in trend_data.columns]

    if available_feature_cols:
        fig_feature = px.line(
            trend_data,
            x='release_year',
            y=available_feature_cols,
            title='Average Audio Features Over Time',
            labels={'value': 'Average Feature Value'},
            markers=True
        )
        fig_feature.update_layout(xaxis_tickformat='d')
        st.plotly_chart(fig_feature, use_container_width=True)
    else:
        st.warning("Audio feature columns (danceability, timbre) not found.")

    st.markdown("---")

    # --- 3. Mood/Theme Distribution ---
    st.markdown("### 3. AI 情緒與主題分佈 (年度對比)")
    
    THEME_COL = 'ai_theme'
    if THEME_COL in df_ts.columns:
        theme_counts = df_ts.groupby(['release_year', THEME_COL]).size().reset_index(name='Count')
        
        fig_theme = px.bar(
            theme_counts,
            x='release_year',
            y='Count',
            color=THEME_COL,
            title=f'Distribution of AI Theme by Release Year',
            labels={'release_year': 'Release Year', 'Count': 'Number of Tracks'},
        )
        fig_theme.update_layout(xaxis_tickformat='d', legend_title="AI Theme")
        st.plotly_chart(fig_theme, use_container_width=True)
    else:
        st.warning("Column 'ai_theme' not found.")


# --- 8. Main App Logic ---

def main():
    st.title("🎶 Jeff Chang Music Evolution Dashboard")

    # Load and Prepare Data (Consolidation/Type conversion happens here)
    # *** 1. UPDATE FILE NAME ***
    FILE_NAME = 'final_enriched_tracks_v3.csv' 
    df = load_data(FILE_NAME)
    df = prepare_data(df) # <-- This calls the FIXED function

    if df.empty:
        return

    # --- Sidebar Filter (CHANGED TO RELEASE YEAR) ---
    st.sidebar.header("Data Filter")
    
    available_years = df['release_year'].dropna().unique()
    
    if available_years.size > 0:
        min_year = int(available_years.min())
        max_year = int(available_years.max())
        
        year_range = st.sidebar.slider(
            "Filter by Release Year Range:", 
            min_value=min_year, 
            max_value=max_year,
            value=(min_year, max_year) # Default to all years
        )
        
        df_filtered = df[(df['release_year'] >= year_range[0]) & (df['release_year'] <= year_range[1])].copy()
        st.sidebar.info(f"Filtered to **{len(df_filtered)}** tracks from {year_range[0]} to {year_range[1]}.")
    else:
        df_filtered = df
        st.sidebar.warning("Release year data is not sufficient for range filtering.")

    # --- Tabbed Interface ---
    # *** 2. REORDER TABS ***
    tab_dashboard, tab_timeseries, tab_album, tab_details = st.tabs([
        "📊 Main Dashboard (Filtered)", 
        "📈 Time Series Analysis",  # NEW/Promoted Tab
        "💿 New Album: 屬於", 
        "🎵 Song Details"
    ])

    with tab_dashboard:
        show_dashboard(df_filtered)

    with tab_timeseries: 
        show_time_series_dashboard(df) # Use the full DF for time analysis

    with tab_album:
        show_new_album_dashboard(df)

    with tab_details:
        show_song_details(df)


if __name__ == "__main__":
    main()
