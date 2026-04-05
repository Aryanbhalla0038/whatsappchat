# Installation & Setup Guide

## System Requirements
- Python 3.8 or higher
- pip (Python package manager)
- 2GB minimum RAM
- Terminal/Command Prompt access

## Step-by-Step Installation

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/whatsappchat.git
cd whatsappchat
```

### 2. Create Virtual Environment (Recommended)

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Verify Installation
```bash
python -c "import streamlit; print('Streamlit installed successfully')"
```

## Running the Application

### Start the App
```bash
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

### First-Time Setup
- The app will auto-download required NLTK data on first run
- This may take 1-2 minutes on first execution
- Subsequent runs will be faster

## Troubleshooting

### Port Already in Use
If port 8501 is busy:
```bash
streamlit run app.py --server.port 8502
```

### Module Not Found Errors
Ensure virtual environment is activated and dependencies installed:
```bash
pip install -r requirements.txt --force-reinstall
```

### NLTK Data Issues
```python
python -m nltk.downloader punkt stopwords
```

## Project Structure Explained

```
whatsappchat/
├── app.py                      # Main Streamlit interface
├── requirements.txt            # Package dependencies
├── README.md                   # Project overview
├── .gitignore                  # Git configuration
│
├── src/                        # Source code package
│   ├── __init__.py            # Package initialization
│   ├── preprocessing.py       # Chat parsing (ChatPreprocessor class)
│   ├── feature_engineering.py # Feature extraction (FeatureEngineer class)
│   └── analysis.py            # Analysis tools (ChatAnalyzer class)
│
├── data/                       # Data folder
│   └── sample_chat.txt        # Example WhatsApp export
│
└── assets/                     # Supporting files
    └── docs/                   # Additional documentation
```

## Code Architecture

### Module: `preprocessing.py`
**Purpose**: Parse and clean raw WhatsApp chat exports

**Main Class**: `ChatPreprocessor`
- `parse_chat_file(file_path)`: Load and parse chat file
- `_parse_datetime()`: Convert date/time strings
- `_clean_data()`: Remove system messages and normalize data
- `get_stats()`: Get basic chat statistics

**Usage**:
```python
from src.preprocessing import ChatPreprocessor

preprocessor = ChatPreprocessor()
df = preprocessor.parse_chat_file('your_chat.txt')
print(preprocessor.get_stats())
```

### Module: `feature_engineering.py`
**Purpose**: Extract engineered features from processed chats

**Main Class**: `FeatureEngineer`
- `engineer_temporal_features()`: Time-based features
- `engineer_textual_features()`: Content-based features
- `engineer_behavioral_features()`: User behavior patterns
- `get_user_profiles()`: Comprehensive user analytics
- `extract_keywords()`: Top keywords per user
- `get_all_features()`: Engineer all features at once

**Usage**:
```python
from src.feature_engineering import FeatureEngineer

engineer = FeatureEngineer(df)
df_features = engineer.get_all_features()
profiles = engineer.get_user_profiles()
keywords = engineer.extract_keywords(user='Alice', top_n=10)
```

### Module: `analysis.py`
**Purpose**: Analyze patterns and generate insights

**Main Class**: `ChatAnalyzer`
- `get_activity_by_hour()`: Messages per hour
- `get_activity_by_day()`: Messages per day of week
- `get_user_statistics()`: Per-user metrics
- `get_conversation_trends()`: Weekly trends
- `get_response_patterns()`: User interaction patterns
- `get_conversation_health()`: Overall chat balance
- `get_sentiment_indicators()`: Emotional markers

**Usage**:
```python
from src.analysis import ChatAnalyzer

analyzer = ChatAnalyzer(df_features)
health = analyzer.get_conversation_health()
stats = analyzer.get_user_statistics()
sentiment = analyzer.get_sentiment_indicators()
```

## Feature List

### Temporal Features (Time-based)
- Hour of day (0-23)
- Day of week (Monday-Sunday)
- Date
- Week of year
- Month and year
- Time period (Morning/Afternoon/Evening/Night)

### Textual Features (Content-based)
- Message length (character count)
- Word count
- Average word length
- Emoji count
- Punctuation count
- URL count
- Mention count
- Question indicator
- Exclamation indicator
- Capitalization ratio

### Behavioral Features (User patterns)
- Response time (seconds since last message)
- Message rate (messages per hour)
- Activity consistency (hour deviation)
- User participation percentage
- Keyword frequency

## Dashboard Walkthrough

### 📊 Overview Tab
- Total message count
- Number of unique participants
- Chat balance metric (0-1 scale)
- Most active hour
- Hourly activity distribution
- Daily activity by day of week
- Timeline of message activity

### 👥 User Analysis Tab
- Individual user message counts
- Average message length per user
- Word count statistics
- Emoji usage by user
- Question count per user
- Most active day/hour per user
- User comparison charts

### 📈 Trends Tab
- Weekly message trends
- Message length evolution over time
- Long-term engagement patterns
- Peak activity windows

### 💭 Text Analysis Tab
- Top 10 emojis used
- Message property distribution (questions, exclamations, URLs, mentions)
- Top 15 keywords in conversation
- Keyword frequency analysis

### 🤖 Advanced Tab
- Sentiment indicators by user
- Message length detailed statistics
- Response patterns (who replies to whom)
- Raw data export to CSV
- Download analyzed data

## Common Tasks

### Export Your WhatsApp Chat

#### Android
1. Open WhatsApp → Chats
2. Long-press the chat you want
3. Tap ⋮ (More) → Export chat
4. Choose "Without Media"
5. Save to device

#### iPhone
1. Open WhatsApp → Chats
2. Swipe left on the chat
3. Tap ⋯ → More → Export Chat
4. Choose Email or Save to Files
5. Send to computer

### Analyze a New Chat
1. Export chat from WhatsApp
2. Open WhatsApp Chat Analyzer
3. Upload the .txt file in the sidebar
4. Click "Process Chat"
5. Explore the dashboard tabs

### Customize Analysis
Edit the modules in `src/`:
- `preprocessing.py`: Change chat parsing rules
- `feature_engineering.py`: Add new features
- `analysis.py`: Create custom analytics
- `app.py`: Modify dashboard layout

## Performance Tips

- **Large Chats (10,000+ messages)**:
  - Processing may take 30-60 seconds
  - Use a computer with 4GB+ RAM
  
- **Multiple Analyses**:
  - The app caches results in session state
  - Changing tabs won't require reprocessing
  
- **Keyword Extraction**:
  - Set `top_n` parameter to 10-20 for best performance
  - Lower values are faster for very large chats

## Extending the Project

### Add Custom Analysis
```python
# In src/analysis.py
def get_custom_metric(self):
    return self.df['column'].custom_operation()
```

### Add New Visualization
```python
# In app.py
import plotly.express as px
fig = px.your_chart_type(df, x='column1', y='column2')
st.plotly_chart(fig)
```

### Create New Feature
```python
# In src/feature_engineering.py
df['new_feature'] = df['message'].apply(your_function)
```

## Support & Help

- **Documentation**: See README.md
- **Issues**: Open an issue on GitHub
- **Contributing**: See contributing guidelines
- **Contact**: Email or GitHub discussions
