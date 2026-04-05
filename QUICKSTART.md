# WhatsApp Chat Analyzer - Quick Start Guide

## 🚀 Get Started in 2 Minutes

### Step 1: Install
```bash
pip install -r requirements.txt
```

### Step 2: Run
```bash
streamlit run app.py
```

### Step 3: Upload a Chat
- Export WhatsApp chat as `.txt` file
- Upload in the sidebar
- Click "Process Chat"
- Explore the dashboard!

## 📊 What You'll See

- **Overview**: Message counts, activity patterns, time trends
- **User Analysis**: Per-user statistics, comparison charts
- **Trends**: Weekly patterns, engagement evolution
- **Text Analysis**: Emoji usage, keywords, message properties
- **Advanced**: Sentiment indicators, response patterns, raw data

## 🔍 Key Metrics Extracted

### Temporal
- Hourly patterns, daily trends, weekly cycles
- Active time periods (Morning/Afternoon/Evening/Night)

### Textual
- Message length, word count, emoji usage
- Questions, exclamations, capitalization patterns

### Behavioral
- Response timing, participation balance
- User consistency and engagement rates

## 💡 Example Insights

- "Alice dominates with 65% of messages"
- "Group is most active at 9 PM"
- "Tuesday has 3x more messages than Monday"
- "Bob uses 5x more emojis than Alice"
- "Most common word: 'awesome' (124 times)"

## 📝 Sample Data

Try with the included `data/sample_chat.txt` to see it in action before uploading your own!

## 🆘 Troubleshooting

**Issue**: "No messages found"
- **Solution**: Check WhatsApp export format `[DD/MM/YYYY, HH:MM:SS] User: Message`

**Issue**: Module not found
- **Solution**: Verify Python virtual environment is activated

**Issue**: Slow processing
- **Solution**: Large chats (10k+ messages) take 1-2 minutes on first run

## 📖 Full Documentation

See `README.md` for comprehensive documentation
See `assets/INSTALLATION_GUIDE.md` for detailed setup

## 🐛 Report Issues

Found a bug? Open an issue on GitHub!

## 💬 Questions?

Check the documentation or open a discussion on GitHub

---

**Made with ❤️ for data enthusiasts** | [GitHub](https://github.com/yourusername/whatsappchat)
