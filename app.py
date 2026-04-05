"""
WhatsApp Chat Analyzer - Streamlit Web Application
Real-time visualization and exploration of WhatsApp chat patterns using NLP
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from preprocessing import ChatPreprocessor
from feature_engineering import FeatureEngineer
from analysis import ChatAnalyzer

# Page configuration
st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
        .main {
            padding: 0rem 0rem;
        }
        .metric-card {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
        }
    </style>
""", unsafe_allow_html=True)


@st.cache_resource
def initialize_session_state():
    """Initialize session state variables"""
    if 'df' not in st.session_state:
        st.session_state.df = None
    if 'df_features' not in st.session_state:
        st.session_state.df_features = None
    if 'analyzer' not in st.session_state:
        st.session_state.analyzer = None


def load_sample_data():
    """Load sample chat data for demonstration"""
    sample_data = """[1/1/2024, 10:30:45] Alice: Hey! 👋
[1/1/2024, 10:31:12] Bob: Hi Alice! How are you? 😊
[1/1/2024, 10:32:00] Alice: I'm doing great! Just finished a project
[1/1/2024, 10:32:45] Bob: That's awesome! 🎉 Tell me more
[1/1/2024, 10:33:30] Alice: It's an NLP project with Streamlit
[1/1/2024, 10:34:15] Bob: Wow! That sounds interesting 🤓
[1/1/2024, 10:35:00] Alice: Yes! Want to collaborate?
[1/1/2024, 10:35:45] Bob: Definitely! 💯
[1/1/2024, 11:00:00] Alice: Let's start tomorrow morning
[1/1/2024, 11:00:45] Bob: Sounds good! See you then 👍
[2/1/2024, 9:15:00] Alice: Good morning Bob!
[2/1/2024, 9:15:45] Bob: Morning! Ready to code? 🚀
[2/1/2024, 9:16:30] Alice: Let's go! ⚡
[2/1/2024, 10:00:00] Bob: How's your code coming along?
[2/1/2024, 10:00:45] Alice: Making good progress! Almost done with preprocessing
[2/1/2024, 10:01:30] Bob: Great! I'm working on visualization
[2/1/2024, 11:30:00] Alice: Feature engineering is complete!
[2/1/2024, 11:30:45] Bob: Perfect! Let's test it together
[2/1/2024, 2:00:00] Alice: The app looks amazing! 🌟
[2/1/2024, 2:00:45] Bob: Thanks! Should we deploy it?
"""
    return sample_data


def main():
    """Main application"""
    initialize_session_state()
    
    # Sidebar
    with st.sidebar:
        st.title("🔧 Controls")
        
        # File upload or sample data
        st.subheader("Load Data")
        use_sample = st.checkbox("Use Sample Data", value=False)
        
        if use_sample:
            if st.button("Load Sample Chat"):
                sample = load_sample_data()
                st.session_state.df_raw = sample
                st.success("Sample data loaded!")
        else:
            uploaded_file = st.file_uploader(
                "Upload WhatsApp Chat (.txt)",
                type=['txt'],
                help="Export your WhatsApp chat as text file"
            )
            if uploaded_file:
                st.session_state.df_raw = uploaded_file.getvalue().decode('utf-8')
        
        # Process data
        if hasattr(st.session_state, 'df_raw'):
            if st.button("🔄 Process Chat", use_container_width=True):
                try:
                    with st.spinner("Processing chat..."):
                        # Save temporary file
                        temp_path = "temp_chat.txt"
                        with open(temp_path, 'w', encoding='utf-8') as f:
                            f.write(st.session_state.df_raw)
                        
                        # Preprocess
                        preprocessor = ChatPreprocessor()
                        st.session_state.df = preprocessor.parse_chat_file(temp_path)
                        
                        # Feature engineering
                        engineer = FeatureEngineer(st.session_state.df)
                        st.session_state.df_features = engineer.get_all_features()
                        
                        # Analysis
                        st.session_state.analyzer = ChatAnalyzer(st.session_state.df_features)
                        
                        st.success("✅ Chat processed successfully!")
                        
                        # Clean up
                        os.remove(temp_path)
                except Exception as e:
                    st.error(f"Error processing chat: {str(e)}")
    
    # Main content
    st.title("💬 WhatsApp Chat Analyzer")
    st.markdown("**Uncover Hidden Communication Patterns with NLP**")
    
    if st.session_state.df is None:
        st.info("📤 Please upload a WhatsApp chat file or load sample data to get started")
        return
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview",
        "👥 User Analysis",
        "📈 Trends",
        "💭 Text Analysis",
        "🤖 Advanced"
    ])
    
    # ============= TAB 1: OVERVIEW =============
    with tab1:
        st.subheader("Chat Overview")
        
        health = st.session_state.analyzer.get_conversation_health()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Messages", health['total_messages'])
        with col2:
            st.metric("Unique Users", health['unique_users'])
        with col3:
            st.metric("Chat Balance", f"{health['balance_ratio']:.0%}")
        with col4:
            st.metric("Active Hours", health['most_active_hour'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Hourly Activity**")
            hourly = st.session_state.analyzer.get_activity_by_hour()
            fig = px.bar(
                x=hourly.index,
                y=hourly.values,
                labels={'x': 'Hour of Day', 'y': 'Messages'},
                title="Messages by Hour"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Daily Activity**")
            daily = st.session_state.analyzer.get_activity_by_day()
            fig = px.bar(
                x=daily.index,
                y=daily.values,
                labels={'x': 'Day', 'y': 'Messages'},
                title="Messages by Day of Week"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Time series
        st.write("**Activity Over Time**")
        daily_data = st.session_state.analyzer.get_activity_by_date()
        fig = px.line(
            x=daily_data.index,
            y=daily_data.values,
            labels={'x': 'Date', 'y': 'Messages'},
            title="Daily Message Count"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # ============= TAB 2: USER ANALYSIS =============
    with tab2:
        st.subheader("User Statistics & Behavior")
        
        user_stats = st.session_state.analyzer.get_user_statistics()
        
        # User selection
        selected_user = st.selectbox(
            "Select User",
            options=list(user_stats.keys())
        )
        
        if selected_user:
            user_info = user_stats[selected_user]
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Messages", user_info['total_messages'])
            with col2:
                st.metric("Avg Length", f"{user_info['avg_message_length']:.0f} chars")
            with col3:
                st.metric("Avg Words", f"{user_info['avg_word_count']:.1f}")
            with col4:
                st.metric("Emojis Used", int(user_info['emoji_usage']))
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Questions", int(user_info['questions_asked']))
            with col2:
                st.metric("Most Active", user_info['most_active_day'])
        
        # User comparison
        st.write("**Message Count by User**")
        user_messages = st.session_state.df['user'].value_counts()
        fig = px.bar(
            x=user_messages.index,
            y=user_messages.values,
            labels={'x': 'User', 'y': 'Number of Messages'},
            title="Message Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Avg Message Length by User**")
            user_avg_length = st.session_state.df.groupby('user')['message_length'].mean()
            fig = px.bar(
                x=user_avg_length.index,
                y=user_avg_length.values,
                labels={'x': 'User', 'y': 'Avg Length (chars)'},
                title="Average Message Length"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Emoji Usage by User**")
            user_emojis = st.session_state.df.groupby('user')['emoji_count'].sum()
            fig = px.bar(
                x=user_emojis.index,
                y=user_emojis.values,
                labels={'x': 'User', 'y': 'Total Emojis'},
                title="Emoji Usage"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # ============= TAB 3: TRENDS =============
    with tab3:
        st.subheader("Communication Trends")
        
        # Weekly trends
        weekly_trends = st.session_state.analyzer.get_conversation_trends()
        
        fig = px.line(
            weekly_trends,
            x='week_label',
            y='message_count',
            markers=True,
            title="Weekly Message Trends"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Message length trends
        st.write("**Message Length Over Time**")
        daily_avg_length = st.session_state.df.groupby('date')['message_length'].mean()
        fig = px.line(
            x=daily_avg_length.index,
            y=daily_avg_length.values,
            labels={'x': 'Date', 'y': 'Avg Message Length'},
            title="Average Message Length Trend"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # ============= TAB 4: TEXT ANALYSIS =============
    with tab4:
        st.subheader("Text & Sentiment Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Top Emojis Used**")
            try:
                top_emojis = st.session_state.analyzer.get_top_emojis(10)
                if top_emojis:
                    emoji_df = pd.DataFrame(
                        list(top_emojis.items()),
                        columns=['Emoji', 'Count']
                    )
                    fig = px.bar(
                        emoji_df,
                        x='Emoji',
                        y='Count',
                        title="Top 10 Emojis"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No emojis found in chat")
            except Exception as e:
                st.warning(f"Could not analyze emojis: {e}")
        
        with col2:
            st.write("**Message Properties**")
            properties = {
                'Questions': st.session_state.df['is_question'].sum(),
                'Exclamations': st.session_state.df['is_exclamation'].sum(),
                'URLs': st.session_state.df['url_count'].sum(),
                'Mentions': st.session_state.df['mention_count'].sum()
            }
            prop_df = pd.DataFrame(list(properties.items()), columns=['Type', 'Count'])
            fig = px.bar(
                prop_df,
                x='Type',
                y='Count',
                title="Message Properties"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Top keywords
        st.write("**Top Keywords**")
        try:
            keywords = st.session_state.analyzer.df_features = st.session_state.df_features or st.session_state.df
            engineer = FeatureEngineer(st.session_state.df)
            top_keywords = engineer.extract_keywords(top_n=15)
            
            kw_df = pd.DataFrame(
                list(top_keywords.items()),
                columns=['Keyword', 'Frequency']
            ).sort_values('Frequency', ascending=False)
            
            fig = px.bar(
                kw_df,
                x='Keyword',
                y='Frequency',
                title="Top 15 Keywords"
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.warning(f"Could not analyze keywords: {e}")
    
    # ============= TAB 5: ADVANCED =============
    with tab5:
        st.subheader("Advanced Analytics")
        
        # Sentiment indicators
        st.write("**Sentiment Indicators by User**")
        try:
            sentiment = st.session_state.analyzer.get_sentiment_indicators()
            sentiment_df = pd.DataFrame(sentiment).T
            st.dataframe(sentiment_df, use_container_width=True)
        except Exception as e:
            st.warning(f"Could not analyze sentiment: {e}")
        
        # Message length statistics
        st.write("**Message Length Statistics**")
        msg_stats = st.session_state.analyzer.get_message_length_stats()
        msg_stats_df = pd.DataFrame(msg_stats).T
        st.dataframe(msg_stats_df, use_container_width=True)
        
        # Response patterns
        st.write("**Response Patterns**")
        try:
            patterns = st.session_state.analyzer.get_response_patterns()
            for user, responses in patterns.items():
                if responses:
                    st.write(f"**{user}** is typically followed by:")
                    resp_df = pd.DataFrame(
                        list(responses.items()),
                        columns=['Respondent', 'Times']
                    )
                    st.bar_chart(resp_df.set_index('Respondent'))
        except Exception as e:
            st.warning(f"Could not analyze response patterns: {e}")
        
        # Raw data
        st.write("**Raw Data Export**")
        if st.button("Show Raw Data"):
            st.dataframe(st.session_state.df_features, use_container_width=True)
            
            # Download button
            csv = st.session_state.df_features.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="chat_analysis.csv",
                mime="text/csv"
            )


if __name__ == "__main__":
    main()
