# WhatsApp Chat Analyzer 💬

A comprehensive **NLP + Streamlit** web application for analyzing WhatsApp chat patterns, extracting meaningful insights, and visualizing communication behaviors.

## 🌟 Features

### 📊 Core Capabilities
- **Chat Preprocessing**: Parse raw WhatsApp exports and clean data automatically
- **Feature Engineering**: Extract 25+ temporal, textual, and behavioral features
- **Real-time Visualization**: Interactive dashboards using Plotly and Seaborn  
- **NLP Analysis**: Keyword extraction, emoji tracking, sentiment indicators
- **User Profiling**: Detailed behavior analytics for each participant

### 📈 Analysis Modules

#### Temporal Features
- Hour of day patterns
- Day of week trends
- Weekly conversation flows
- Message timing analysis

#### Textual Features
- Message length distribution
- Word count analytics
- Emoji usage tracking
- URL and mention detection
- Question/exclamation ratios
- Capitalization patterns

#### Behavioral Features
- Response time patterns
- Message frequency rates
- Participation consistency
- Communication balance
- Conversation health metrics

### 🎯 Dashboard Sections

1. **Overview** - Chat statistics, hourly/daily activity, time series trends
2. **User Analysis** - Individual user metrics, message distributions, comparison charts
3. **Trends** - Weekly trends, message length evolution, engagement patterns
4. **Text Analysis** - Top emojis, keywords, message properties
5. **Advanced** - Sentiment indicators, response patterns, raw data export

## 📋 Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/whatsappchat.git
cd whatsappchat
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash 
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📱 How to Export WhatsApp Chat

### Android:
1. Open WhatsApp and navigate to the chat
2. Tap on the three dots (menu)
3. Select "More" → "Export chat"
4. Choose "Without media"
5. Save to your device

### iOS:
1. Open WhatsApp and navigate to the chat
2. Swipe left on the chat
3. Tap "More" → "Export"
4. Choose "Email" or save to Files
5. Transfer to your computer

### WhatsApp Web:
1. Open `web.whatsapp.com`
2. Export using right-click options (if available)
3. Save as `.txt` file

## 📁 Project Structure

```
whatsappchat/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── .gitignore                  # Git ignore rules
│
├── src/
│   ├── __init__.py            # Package initialization
│   ├── preprocessing.py       # Chat parsing and cleaning
│   ├── feature_engineering.py # Feature extraction
│   └── analysis.py            # Analytical functions
│
├── data/
│   └── sample_chat.txt        # Example chat file for testing
│
└── assets/
    └── README.md              # Additional documentation
```

## 🔧 Usage

### Basic Usage

```python
from src.preprocessing import ChatPreprocessor
from src.feature_engineering import FeatureEngineer
from src.analysis import ChatAnalyzer

# Load and preprocess chat
preprocessor = ChatPreprocessor()
df = preprocessor.parse_chat_file('your_chat.txt')

# Engineer features
engineer = FeatureEngineer(df)
df_features = engineer.get_all_features()

# Analyze
analyzer = ChatAnalyzer(df_features)
stats = analyzer.get_conversation_health()
```

### Advanced Usage

```python
# Extract keywords for specific user
keywords = engineer.extract_keywords(user='Alice', top_n=20)

# Get user profiles
profiles = engineer.get_user_profiles()

# Analyze sentiment indicators
sentiment = analyzer.get_sentiment_indicators()

# Response patterns
patterns = analyzer.get_response_patterns()
```

## 📊 Example Outputs

### Chat Overview
- Total messages, unique users, chat balance metrics
- Hourly activity heatmap
- Daily message distribution
- Time series activity trends

### User Analytics
- Individual message statistics
- Average message length per user
- Emoji usage breakdown
- Questions asked vs exclamations used
- Most active hours/days

### Communication Patterns
- Response time distributions
- Conversation health indicator
- User participation balance
- Peak activity hours
- Emoji preferences

### Text Insights
- Most frequently used keywords
- Top emojis by frequency
- Question patterns
- Message length statistics
- Capitalization analysis

## 🤖 Technology Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python 3.8+ |
| Web Framework | Streamlit |
| Data Processing | Pandas, NumPy |
| Visualization | Plotly, Seaborn, Matplotlib |
| NLP | NLTK |
| ML | Scikit-learn |

## 🔍 Feature Extraction Details

### Temporal Features (Time-based)
- `hour`: Hour of day (0-23)
- `day_of_week`: Day name (Monday-Sunday)
- `date`: Message date
- `time_period`: Morning/Afternoon/Evening/Night
- `week_of_year`: Week number

### Textual Features (Content-based)
- `message_length`: Character count
- `word_count`: Total words
- `emoji_count`: Emoji count
- `punctuation_count`: Punctuation marks
- `url_count`: Links in message
- `mention_count`: @mentions
- `is_question`: Boolean (message ends with ?)
- `is_exclamation`: Boolean (message has !)
- `caps_ratio`: Ratio of capital letters

### Behavioral Features (User patterns)
- `message_rate`: Messages per hour
- `time_diff_seconds`: Gap since last message
- `hour_consistency`: Deviation in active hours
- User participation metrics
- Response patterns

## 📈 Insights Generated

1. **Discussion Balance**: Who dominates the conversation?
2. **Activity Patterns**: When is the group most active?
3. **Communication Style**: Question vs statement preference
4. **Emotional Indicators**: Emoji and exclamation usage
5. **Response Dynamics**: Who responds to whom?
6. **Engagement Trends**: Is conversation growing or declining?

## ⚙️ Configuration

### Customize Analysis
Edit `src/analysis.py` to:
- Add new analysis metrics
- Modify feature calculations
- Create custom insights

### Modify Streamlit UI
Edit `app.py` to:
- Add/remove dashboard sections
- Change visualization types
- Customize colors and themes

### Adjust Preprocessing
Edit `src/preprocessing.py` to:
- Support different chat formats
- Add system message handling
- Customize text cleaning

## 🐛 Troubleshooting

### Issue: "No messages found in chat file"
**Solution**: Ensure your chat export follows WhatsApp format:
```
[DD/MM/YYYY, HH:MM:SS] User:  Message
```

### Issue: NLTK data errors
**Solution**: The app auto-downloads required data on first run. If issues persist:
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

### Issue: Encoding errors
**Solution**: WhatsApp exports encoding. The app tries UTF-8 then Latin-1. If still failing:
1. Re-export chat from WhatsApp
2. Ensure .txt file is saved with UTF-8 encoding

## 🎨 Customization

### Add Custom Visualizations
```python
# In app.py, add new plotly chart:
fig = px.scatter(df, x='hour', y='message_length')
st.plotly_chart(fig)
```

### Create New Analysis
```python
# In src/analysis.py:
def custom_analysis(self):
    return {"custom_metric": self.df['metric'].sum()}
```

### Extend Feature Engineering
```python
# In src/feature_engineering.py:
df['custom_feature'] = df.apply(
    lambda row: your_custom_function(row),
    axis=1
)
```

## 📄 Sample Data

A sample chat file is included in `data/sample_chat.txt` for testing the application without exporting your actual chats.

```
[1/1/2024, 10:30:45] Alice: Hey! 👋
[1/1/2024, 10:31:12] Bob: Hi Alice! How are you? 😊
...
```

## 🚀 Deployment

### Local Deployment
```bash
streamlit run app.py
```

### Cloud Deployment (Streamlit Cloud)
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Select your repository and branch
4. Deploy!

### Docker Deployment
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 👨‍💻 Author

**WhatsApp Chat Analyzer** - NLP + Streamlit Project
- November 2025
- Focus on bridging NLP research with accessible insights

## 🌐 Connect

- GitHub: [Your Profile](https://github.com/yourusername)
- LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com

## 📚 Resources & Documentation

- [Streamlit Documentation](https://docs.streamlit.io)
- [Pandas Documentation](https://pandas.pydata.org/docs)
- [NLTK Documentation](https://www.nltk.org)
- [Plotly Documentation](https://plotly.com/python)

## 🙏 Acknowledgments

- WhatsApp for the data format
- Streamlit community for the amazing framework
- Open source community for Python libraries

---

**⭐ If you find this project helpful, please give it a star! ⭐**

**Made with ❤️ for data science enthusiasts**
