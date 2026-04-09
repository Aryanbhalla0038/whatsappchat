"""
WhatsApp Chat Analyzer - Streamlit Web Application
Real-time visualization and exploration of WhatsApp chat patterns using NLP
"""
import emoji
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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

# Custom styling - Modern Neutral Design
st.markdown("""
    <style>
        /* Main layout */
        .main {
            padding: 2rem 2rem;
            background: #ffffff;
            min-height: 100vh;
        }
        
        /* Headers and Typography */
        h1 {
            color: #1f2937;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            letter-spacing: -0.5px;
        }
        
        h2 {
            color: #374151;
            font-size: 1.75rem;
            font-weight: 600;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
            border-bottom: 2px solid #e5e7eb;
            padding-bottom: 0.5rem;
        }
        
        h3 {
            color: #4b5563;
            font-size: 1.25rem;
            font-weight: 600;
            margin-top: 1rem;
            margin-bottom: 0.75rem;
        }
        
        /* Metric cards */
        .metric-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            border-left: 4px solid #6366f1;
            margin: 0.5rem 0;
            transition: all 0.3s ease;
        }
        
        .metric-card:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.12);
            transform: translateY(-2px);
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: white;
            border-right: 1px solid #e5e7eb;
        }
        
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
            color: #1f2937;
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #6366f1 0%, #5b61e8 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .stButton > button:hover {
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
            transform: translateY(-2px);
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 1rem;
            border-bottom: 2px solid #e5e7eb;
            background: #f9fafb;
            padding: 0 1rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: transparent;
            border-radius: 8px 8px 0 0;
            color: #6b7280;
            font-weight: 600;
            padding: 1rem 1.5rem;
            border: none;
        }
        
        .stTabs [aria-selected="true"] {
            background: white;
            color: #6366f1;
            border-bottom: 3px solid #6366f1;
        }
        
        /* Alert and Info boxes - REMOVE BACKGROUND COLOR */
        [data-testid="stAlert"] {
            background: white;
            border-left: 4px solid #6366f1;
            border-radius: 8px;
            padding: 1rem;
            border-top: none;
            border-right: none;
            border-bottom: none;
        }
        
        /* File uploader styling */
        .stFileUploadDropzone {
            border: 2px dashed #d1d5db;
            border-radius: 8px;
            background: white;
        }
        
        /* Input fields */
        .stTextInput > div > div > input,
        .stSelectbox > div > div > select {
            border: 1px solid #d1d5db;
            border-radius: 6px;
            padding: 0.75rem;
            font-size: 0.95rem;
            background: white;
        }
        
        /* Markdown */
        p {
            color: #4b5563;
            line-height: 1.6;
        }
        
        /* Divider */
        hr {
            background: #e5e7eb;
            border: none;
            height: 1px;
            margin: 1.5rem 0;
        }
        
        /* Charts background */
        .plotly-graph-div {
            background: white !important;
            border-radius: 8px;
            padding: 1rem;
        }
        
        /* Content containers */
        .element-container {
            background: white;
        }
        
        [data-testid="stMetricContainer"] {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 1rem;
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
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Process Chat", use_container_width=True):
                    try:
                        with st.spinner("Processing chat..."):
                            # Save temporary file
                            temp_path = "temp_chat.txt"
                            with open(temp_path, 'w', encoding='utf-8') as f:
                                f.write(st.session_state.df_raw)
                            
                            # Preprocess
                            preprocessor = ChatPreprocessor()
                            raw_df = preprocessor.parse_chat_file(temp_path)
                            
                            # --- MASTER COLUMN FIXES ---
                            # Ensure standard column naming conventions for the app to use safely
                            col_map = {c.lower(): c for c in raw_df.columns}
                            
                            # Ensure 'message' exists
                            msg_col = col_map.get('message', col_map.get('user_message', list(raw_df.columns)[-1]))
                            
                            # Calculate core metrics ONCE here, so the tabs don't crash later
                            raw_df['message_length'] = raw_df[msg_col].astype(str).str.len()
                            raw_df['emoji_count'] = raw_df[msg_col].astype(str).apply(lambda x: emoji.emoji_count(x))
                            
                            st.session_state.df = raw_df
                            
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
            
            with col2:
                if st.button("🔍 Inspect Format", use_container_width=True):
                    st.info("First 5 lines of your file:")
                    lines = st.session_state.df_raw.split('\n')[:5]
                    for i, line in enumerate(lines, 1):
                        st.code(line, language=None)
    
    # Main content
    st.markdown("""
        <div style="margin-bottom: 2rem;">
            <h1 style="margin: 0; padding-bottom: 0.5rem;">💬 WhatsApp Chat Analyzer</h1>
            <p style="margin: 0; color: #6b7280; font-size: 1.1rem;">Uncover Hidden Communication Patterns with Advanced NLP</p>
            <hr style="margin-top: 1rem; margin-bottom: 0;">
        </div>
    """, unsafe_allow_html=True)
    
    if "df" not in st.session_state or st.session_state.df is None:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.info("💡 **Get Started:** Upload your WhatsApp chat file (.txt) from Android or iOS to begin analyzing your communication patterns.")
        return
    
    # Identify the correct date column dynamically to prevent KeyErrors
    date_col = next((col for col in ['timestamp', 'only_date', 'date', 'Date', 'Date_Time'] if col in st.session_state.df.columns), None)
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Overview",
        "👥 User Analysis",
        "📈 Trends",
        "💭 Text Analysis",
        "🤖 Advanced",
        "🚀 Intelligence"
    ])
    
    # ============= TAB 1: OVERVIEW =============
    with tab1:
        st.markdown("### 📊 Chat Overview & Statistics")
        
        health = st.session_state.analyzer.get_conversation_health()
        
        # Key metrics in a clean layout
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📨 Total Messages", health.get('total_messages', 0))
        with col2:
            st.metric("👥 Unique Users", health.get('unique_users', 0))
        with col3:
            ratio = health.get('balance_ratio', 0)
            st.metric("⚖️ Chat Balance", f"{ratio:.0%}" if isinstance(ratio, (int, float)) else "N/A")
        with col4:
            st.metric("🕐 Peak Hour", f"{health.get('most_active_hour', 'N/A')}:00")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### ⏰ Hourly Activity Pattern")
            try:
                hourly = st.session_state.analyzer.get_activity_by_hour()
                fig = px.bar(
                    x=hourly.index,
                    y=hourly.values,
                    labels={'x': 'Hour of Day', 'y': 'Messages'},
                    title="When do people chat most?",
                    color_discrete_sequence=['#6366f1']
                )
                fig.update_layout(
                    hovermode='x unified',
                    template='plotly_white',
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.warning("Could not load hourly chart.")
        
        with col2:
            st.markdown("#### 📅 Daily Activity Distribution")
            try:
                daily = st.session_state.analyzer.get_activity_by_day()
                fig = px.bar(
                    x=daily.index,
                    y=daily.values,
                    labels={'x': 'Day of Week', 'y': 'Messages'},
                    title="Which days are most active?",
                    color_discrete_sequence=['#06b6d4']
                )
                fig.update_layout(
                    hovermode='x unified',
                    template='plotly_white',
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.warning("Could not load daily chart.")
        
        # Time series
        st.write("**Activity Over Time**")
        try:
            daily_data = st.session_state.analyzer.get_activity_by_date()
            fig = px.line(
                x=daily_data.index,
                y=daily_data.values,
                labels={'x': 'Date', 'y': 'Messages'},
                title="Daily Message Count"
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.warning("Could not load timeline chart.")
    
    # ============= TAB 2: USER ANALYSIS =============
    with tab2:
        st.subheader("User Statistics & Behavior")
        
        user_stats = st.session_state.analyzer.get_user_statistics()
        
        # User selection
        selected_user = st.selectbox(
            "Select User",
            options=list(user_stats.keys()) if user_stats else []
        )
        
        if selected_user and user_stats:
            user_info = user_stats[selected_user]
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Messages", user_info.get('total_messages', 0))
            with col2:
                st.metric("Avg Length", f"{user_info.get('avg_message_length', 0):.0f} chars")
            with col3:
                st.metric("Avg Words", f"{user_info.get('avg_word_count', 0):.1f}")
            with col4:
                st.metric("Emojis Used", int(user_info.get('emoji_usage', 0)))
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Questions", int(user_info.get('questions_asked', 0)))
            with col2:
                st.metric("Most Active", user_info.get('most_active_day', "N/A"))
        
        # User comparison
        st.write("**Message Count by User**")
        user_messages = st.session_state.df['user'].value_counts() if 'user' in st.session_state.df.columns else pd.Series()
        if not user_messages.empty:
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
            if 'user' in st.session_state.df.columns and 'message_length' in st.session_state.df.columns:
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
            if 'user' in st.session_state.df.columns and 'emoji_count' in st.session_state.df.columns:
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
        try:
            weekly_trends = st.session_state.analyzer.get_conversation_trends()
            fig = px.line(
                weekly_trends,
                x='week_label',
                y='message_count',
                markers=True,
                title="Weekly Message Trends"
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.warning("Weekly trends not available.")
        
        # Message length trends
        st.write("**Message Length Over Time**")
        if date_col and 'message_length' in st.session_state.df.columns:
            try:
                df_trends = st.session_state.df.copy()
                # Convert timestamp to date for grouping
                if df_trends[date_col].dtype == 'object':
                    df_trends['date_only'] = pd.to_datetime(df_trends[date_col]).dt.date
                else:
                    df_trends['date_only'] = pd.to_datetime(df_trends[date_col]).dt.date
                
                daily_avg_length = df_trends.groupby('date_only')['message_length'].mean()
                fig = px.line(
                    x=daily_avg_length.index,
                    y=daily_avg_length.values,
                    labels={'x': 'Date', 'y': 'Avg Message Length'},
                    title="Average Message Length Trend"
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.info("Could not generate message length trend.")
        else:
            st.info("Date information missing for trend chart.")
    
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
            # Using .get() safely defaults to 0 if the preprocessor didn't create these columns
            properties = {
                'Questions': st.session_state.df.get('is_question', pd.Series([0])).sum(),
                'Exclamations': st.session_state.df.get('is_exclamation', pd.Series([0])).sum(),
                'URLs': st.session_state.df.get('url_count', pd.Series([0])).sum(),
                'Mentions': st.session_state.df.get('mention_count', pd.Series([0])).sum()
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
            # Fixed the chained assignment bug here
            engineer = FeatureEngineer(st.session_state.df_features)
            top_keywords = engineer.extract_keywords(top_n=15)
            
            if top_keywords:
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
            else:
                st.info("Not enough data to extract keywords.")
        except Exception as e:
            st.warning(f"Could not analyze keywords: {e}")
    
    # ============= TAB 5: ADVANCED =============
    with tab5:
        st.subheader("Advanced Analytics")
        
        # Multilingual sentiment indicators
        st.write("**Multilingual Sentiment (English + Hindi + Punjabi + Hinglish)**")
        try:
            sentiment = st.session_state.analyzer.get_multilingual_sentiment()
            if sentiment and sentiment.get('user_sentiment'):
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Overall Mood", sentiment.get('overall_label', 'Neutral'))
                with col2:
                    st.metric("Overall Score", sentiment.get('overall_score', 0.0))

                sentiment_df = pd.DataFrame(sentiment['user_sentiment'])
                st.dataframe(sentiment_df, use_container_width=True)

                fig = px.bar(
                    sentiment_df,
                    x='user',
                    y='avg_sentiment',
                    color='sentiment_label',
                    color_discrete_map={
                        'Positive': '#16a34a',
                        'Neutral': '#64748b',
                        'Negative': '#dc2626'
                    },
                    title='Per-User Multilingual Sentiment Score'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Sentiment data not available.")
        except Exception as e:
            st.warning("Could not analyze sentiment.")
        
        # Message length statistics
        st.write("**Message Length Statistics**")
        try:
            msg_stats = st.session_state.analyzer.get_message_length_stats()
            if msg_stats:
                msg_stats_df = pd.DataFrame(msg_stats).T
                st.dataframe(msg_stats_df, use_container_width=True)
        except Exception as e:
            st.warning("Could not calculate message stats.")
        
        # Response patterns
        st.write("**Response Patterns**")
        try:
            patterns = st.session_state.analyzer.get_response_patterns()
            if patterns:
                for user, responses in patterns.items():
                    if responses:
                        st.write(f"**{user}** is typically followed by:")
                        resp_df = pd.DataFrame(
                            list(responses.items()),
                            columns=['Respondent', 'Times']
                        )
                        st.bar_chart(resp_df.set_index('Respondent'))
            else:
                st.info("Not enough data for response patterns.")
        except Exception as e:
            st.warning("Could not analyze response patterns.")
        
        # Raw data
        st.write("**Raw Data Export**")
        if st.button("Show Raw Data"):
            st.dataframe(st.session_state.df_features, use_container_width=True)
            
            # Download button
            csv = st.session_state.df_features.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="chat_analysis.csv",
                mime="text/csv"
            )

    # ============= TAB 6: INTELLIGENCE =============
    with tab6:
        st.subheader("Intelligence Layer")

        # 1) AI Weekly Narrative Recaps
        st.write("**1) Weekly Narrative Recaps**")
        try:
            recaps = st.session_state.analyzer.get_weekly_narrative_recaps()
            if recaps:
                for row in recaps[-8:]:
                    st.markdown(f"- {row['summary']}")
            else:
                st.info("Not enough weekly data for narrative recaps.")
        except Exception:
            st.warning("Could not generate weekly recaps.")

        st.markdown("---")

        # 2) Reply Dynamics Engine
        st.write("**2) Reply Dynamics Engine**")
        try:
            dynamics = st.session_state.analyzer.get_reply_dynamics()
            user_reply = pd.DataFrame(dynamics.get('user_reply_stats', []))
            pair_reply = pd.DataFrame(dynamics.get('pair_reply_stats', []))

            if not user_reply.empty:
                user_reply = user_reply.sort_values('median')
                fig = px.bar(
                    user_reply,
                    x='user',
                    y='median',
                    title='Median Reply Time by User (seconds)',
                    color_discrete_sequence=['#0ea5e9']
                )
                st.plotly_chart(fig, use_container_width=True)
                st.dataframe(user_reply, use_container_width=True)

            if not pair_reply.empty:
                st.write("Pairwise Reply Latency")
                st.dataframe(pair_reply.sort_values('median'), use_container_width=True)
        except Exception:
            st.warning("Could not generate reply dynamics.")

        st.markdown("---")

        # 3) Topic Journey Timeline
        st.write("**3) Topic Journey Timeline**")
        try:
            topic_data = st.session_state.analyzer.get_topic_journey(n_topics=4, top_words=6)
            topic_timeline = pd.DataFrame(topic_data.get('timeline', []))
            topic_table = pd.DataFrame(topic_data.get('topics', []))

            if not topic_timeline.empty:
                fig = px.area(
                    topic_timeline,
                    x='week',
                    y='message_count',
                    color='topic_label',
                    groupnorm='fraction',
                    title='Topic Share Over Time'
                )
                st.plotly_chart(fig, use_container_width=True)

            if not topic_table.empty:
                st.dataframe(topic_table[['topic_label', 'keywords']], use_container_width=True)

            if topic_timeline.empty and topic_table.empty:
                st.info("Not enough data for topic modeling yet (need a larger chat history).")
        except Exception:
            st.warning("Could not generate topic journey.")

        st.markdown("---")

        # 4) Relationship Graph and Influence Map
        st.write("**4) Relationship Graph and Influence Map**")
        try:
            influence_data = st.session_state.analyzer.get_relationship_influence_map()
            edges = pd.DataFrame(influence_data.get('edges', []))
            influence = pd.DataFrame(influence_data.get('influence', []))

            if not edges.empty:
                users = sorted(set(edges['source'].tolist() + edges['target'].tolist()))
                user_to_idx = {u: i for i, u in enumerate(users)}

                sankey = go.Figure(
                    data=[
                        go.Sankey(
                            node=dict(
                                pad=15,
                                thickness=18,
                                line=dict(color='gray', width=0.4),
                                label=users
                            ),
                            link=dict(
                                source=[user_to_idx[s] for s in edges['source']],
                                target=[user_to_idx[t] for t in edges['target']],
                                value=edges['interaction_count'].tolist()
                            )
                        )
                    ]
                )
                sankey.update_layout(title_text='Who Responds to Whom', font_size=11)
                st.plotly_chart(sankey, use_container_width=True)

            if not influence.empty:
                st.dataframe(influence, use_container_width=True)

            if edges.empty and influence.empty:
                st.info("Not enough transitions to build a relationship map.")
        except Exception:
            st.warning("Could not build relationship influence map.")

        st.markdown("---")

        # 5) Semantic Search + QA
        st.write("**5) Semantic Chat Search + QA**")
        query = st.text_input(
            "Ask a question about your chat",
            placeholder="e.g., when did we talk about internships or travel plans?",
            key="semantic_query"
        )

        if st.button("Run Semantic Search", key="run_semantic_search"):
            if query.strip():
                try:
                    search_result = st.session_state.analyzer.semantic_chat_search(query=query, top_k=6)
                    st.success(search_result.get('answer', 'No answer generated.'))

                    result_df = pd.DataFrame(search_result.get('results', []))
                    if not result_df.empty:
                        result_df['score'] = result_df['score'].round(4)
                        st.dataframe(result_df[['score', 'user', 'timestamp', 'message']], use_container_width=True)
                    else:
                        st.info("No relevant messages found for this query.")
                except Exception:
                    st.warning("Semantic search could not be completed.")
            else:
                st.info("Enter a question first.")


if __name__ == "__main__":
    main()
