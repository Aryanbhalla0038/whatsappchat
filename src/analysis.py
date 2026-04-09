"""
Analysis Module for WhatsApp Chat
Provides analytical functions and insights
"""

import re
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.metrics.pairwise import cosine_similarity


class ChatAnalyzer:
    """Analyze WhatsApp chat patterns and generate insights"""
    
    def __init__(self, df: pd.DataFrame):
        """Initialize with feature-engineered dataframe"""
        self.df = df
        if 'message' in self.df.columns:
            self.df['message'] = self.df['message'].fillna('').astype(str)

        # Lexicons for multilingual (English + Hindi + Punjabi + Hinglish) sentiment.
        self.positive_words = {
            'good', 'great', 'awesome', 'happy', 'love', 'best', 'nice', 'cool', 'amazing',
            'accha', 'acha', 'badhiya', 'mast', 'badiya', 'khush', 'sahi', 'shukriya', 'dhanyavaad',
            'vadhiya', 'vadiya', 'sohna', 'sohni', 'changa', 'changi', 'wadhia', 'thanku', 'thanks',
            'hanji', 'haanji', 'hmm ok', 'theek', 'thik', 'bhot badiya', 'bohot accha', '👍', '🔥',
            '😂', '🤣', '😊', '❤️', '❤', '🙏', '💯', '😄', '😁', '🎉', '🥳', 'ਚੰਗਾ', 'ਵਧੀਆ', 'ਖੁਸ਼', 'ਪਿਆਰ'
        }
        self.negative_words = {
            'bad', 'sad', 'angry', 'hate', 'worse', 'worst', 'upset', 'annoying', 'problem',
            'bura', 'gussa', 'dukhi', 'pareshan', 'tension', 'bekar', 'beakar', 'faltu', 'jhagda',
            'kharab', 'chup', 'ignore', 'galat', 'nahi', 'naah', 'naa', 'bekaar', '😭', '😡', '😠',
            '😢', '💔', '😤', 'mood off', 'frustrated', 'disappointed', 'ਬੁਰਾ', 'ਗੁੱਸਾ', 'ਉਦਾਸ', 'ਨਾਰਾਜ਼'
        }
    
    def get_activity_by_hour(self) -> pd.Series:
        """Get message count by hour of day"""
        return self.df['hour'].value_counts().sort_index()
    
    def get_activity_by_day(self) -> pd.Series:
        """Get message count by day of week"""
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        activity = self.df['day_of_week'].value_counts()
        return activity.reindex(day_order)
    
    def get_activity_by_date(self) -> pd.Series:
        """Get message count by date"""
        return self.df.groupby('date').size().sort_index()
    
    def get_user_statistics(self) -> dict:
        """Get statistics for each user"""
        stats = {}
        for user in self.df['user'].unique():
            user_data = self.df[self.df['user'] == user]
            stats[user] = {
                'total_messages': len(user_data),
                'avg_message_length': user_data['message_length'].mean(),
                'avg_word_count': user_data['word_count'].mean(),
                'emoji_usage': user_data['emoji_count'].sum(),
                'questions_asked': user_data['is_question'].sum(),
                'active_hours': user_data['hour'].mode().values.tolist(),
                'most_active_day': user_data['day_of_week'].mode().values[0] if len(user_data['day_of_week'].mode()) > 0 else 'N/A'
            }
        return stats
    
    def get_conversation_trends(self) -> pd.DataFrame:
        """Get weekly message trends"""
        weekly = self.df.groupby(['year', 'week_of_year']).size().reset_index(name='message_count')
        weekly['week_label'] = weekly['year'].astype(str) + '-W' + weekly['week_of_year'].astype(str)
        return weekly[['week_label', 'message_count']]
    
    def get_top_emojis(self, n: int = 10) -> dict:
        """Get top emojis used"""
        import re
        
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"
            "\U0001F300-\U0001F5FF"
            "\U0001F680-\U0001F6FF"
            "\U0001F1E0-\U0001F1FF"
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "]+",
            flags=re.UNICODE
        )
        
        all_emojis = []
        for msg in self.df['message']:
            all_emojis.extend(emoji_pattern.findall(msg))
        
        emoji_counts = {}
        for emoji in all_emojis:
            emoji_counts[emoji] = emoji_counts.get(emoji, 0) + 1
        
        top_emojis = sorted(emoji_counts.items(), key=lambda x: x[1], reverse=True)[:n]
        return {emoji: count for emoji, count in top_emojis}
    
    def get_response_patterns(self) -> dict:
        """Analyze response patterns between users"""
        if len(self.df['user'].unique()) < 2:
            return {'message': 'Need at least 2 users for response pattern analysis'}
        
        users = self.df['user'].unique()
        patterns = {}
        
        for user in users:
            user_messages = self.df[self.df['user'] == user].copy()
            user_messages['next_user'] = user_messages['user'].shift(-1)
            
            # Get who typically responds to this user
            responses = user_messages[user_messages['next_user'] != user]['next_user'].value_counts()
            patterns[user] = responses.to_dict() if len(responses) > 0 else {}
        
        return patterns
    
    def get_message_length_stats(self) -> dict:
        """Get message length statistics by user"""
        stats = {}
        for user in self.df['user'].unique():
            user_data = self.df[self.df['user'] == user]
            stats[user] = {
                'min': int(user_data['message_length'].min()),
                'max': int(user_data['message_length'].max()),
                'mean': round(user_data['message_length'].mean(), 2),
                'median': int(user_data['message_length'].median()),
                'std': round(user_data['message_length'].std(), 2)
            }
        return stats
    
    def get_conversation_health(self) -> dict:
        """Analyze conversation balance and health"""
        total_messages = len(self.df)
        user_distribution = self.df['user'].value_counts()
        
        # Balance metric (0 = one user dominates, 1 = perfectly balanced)
        balance_ratio = (1 - user_distribution.max() / total_messages) if total_messages > 0 else 0
        
        return {
            'total_messages': total_messages,
            'unique_users': self.df['user'].nunique(),
            'balance_ratio': round(balance_ratio, 2),
            'dominant_user': user_distribution.index[0],
            'dominant_user_percentage': round((user_distribution.iloc[0] / total_messages) * 100, 2),
            'most_active_day': self.df['day_of_week'].mode()[0] if len(self.df) > 0 else 'N/A',
            'most_active_hour': int(self.df['hour'].mode()[0]) if len(self.df) > 0 else 'N/A'
        }
    
    def get_sentiment_indicators(self) -> dict:
        """Get indicators of message sentiment (multilingual friendly)."""
        indicators = {}
        sentiment_summary = self.get_multilingual_sentiment()
        sentiment_by_user = {
            row['user']: row for row in sentiment_summary.get('user_sentiment', [])
        }
        
        for user in self.df['user'].unique():
            user_data = self.df[self.df['user'] == user]
            
            question_ratio = (user_data['is_question'].sum() / len(user_data)) * 100 if len(user_data) > 0 else 0
            exclamation_ratio = (user_data['is_exclamation'].sum() / len(user_data)) * 100 if len(user_data) > 0 else 0
            emoji_messages = (user_data['emoji_count'] > 0).sum() / len(user_data) * 100 if len(user_data) > 0 else 0
            sentiment_data = sentiment_by_user.get(user, {})
            
            indicators[user] = {
                'question_ratio': round(question_ratio, 2),
                'exclamation_ratio': round(exclamation_ratio, 2),
                'emoji_usage_ratio': round(emoji_messages, 2),
                'avg_emoji_per_message': round(user_data['emoji_count'].mean(), 2),
                'sentiment_score': sentiment_data.get('avg_sentiment', 0.0),
                'sentiment_label': sentiment_data.get('sentiment_label', 'Neutral')
            }
        
        return indicators

    def _score_message_sentiment(self, text: str) -> float:
        """Score one message using multilingual lexicons."""
        text = str(text).lower()
        tokens = re.findall(r"[a-zA-Z']+|[\u0900-\u097F]+|[\u0A00-\u0A7F]+|[\U0001F300-\U0001FAFF]", text)
        if not tokens:
            return 0.0

        pos = 0
        neg = 0
        for token in tokens:
            if token in self.positive_words:
                pos += 1
            if token in self.negative_words:
                neg += 1

        raw_score = pos - neg
        return raw_score / max(len(tokens), 1)

    def get_multilingual_sentiment(self) -> dict:
        """Sentiment analysis for English/Hindi/Punjabi/Hinglish messages."""
        if 'message' not in self.df.columns:
            return {'overall_score': 0.0, 'user_sentiment': []}

        data = self.df.copy()
        data['sentiment_score'] = data['message'].apply(self._score_message_sentiment)

        def sentiment_label(score: float) -> str:
            if score > 0.03:
                return 'Positive'
            if score < -0.03:
                return 'Negative'
            return 'Neutral'

        user_rows = []
        for user, group in data.groupby('user'):
            avg_score = float(group['sentiment_score'].mean()) if len(group) else 0.0
            user_rows.append({
                'user': user,
                'avg_sentiment': round(avg_score, 4),
                'sentiment_label': sentiment_label(avg_score),
                'positive_messages': int((group['sentiment_score'] > 0.03).sum()),
                'neutral_messages': int(((group['sentiment_score'] >= -0.03) & (group['sentiment_score'] <= 0.03)).sum()),
                'negative_messages': int((group['sentiment_score'] < -0.03).sum())
            })

        overall = float(data['sentiment_score'].mean()) if len(data) else 0.0
        return {
            'overall_score': round(overall, 4),
            'overall_label': sentiment_label(overall),
            'user_sentiment': user_rows
        }

    def get_reply_dynamics(self) -> dict:
        """Reply latency engine: who replies fastest and conversation momentum."""
        if 'timestamp' not in self.df.columns or 'user' not in self.df.columns:
            return {'message': 'Timestamp/user columns not available.'}

        data = self.df.sort_values('timestamp').copy()
        data['prev_user'] = data['user'].shift(1)
        data['prev_timestamp'] = data['timestamp'].shift(1)
        data['reply_seconds'] = (data['timestamp'] - data['prev_timestamp']).dt.total_seconds()

        replies = data[(data['prev_user'].notna()) & (data['user'] != data['prev_user'])].copy()
        if replies.empty:
            return {'message': 'Not enough multi-user transitions for reply dynamics.'}

        user_stats = replies.groupby('user')['reply_seconds'].agg(['mean', 'median', 'count']).reset_index()
        user_stats['quick_reply_rate_pct'] = replies.groupby('user')['reply_seconds'].apply(
            lambda s: (s <= 300).mean() * 100
        ).values
        user_stats['momentum_score'] = 1 / (1 + user_stats['median'])

        pair_stats = replies.groupby(['prev_user', 'user'])['reply_seconds'].agg(['mean', 'median', 'count']).reset_index()
        pair_stats = pair_stats.rename(columns={'prev_user': 'from_user', 'user': 'to_user'})

        return {
            'user_reply_stats': user_stats.to_dict('records'),
            'pair_reply_stats': pair_stats.to_dict('records')
        }

    def get_relationship_influence_map(self) -> dict:
        """Interaction map and influence score by user."""
        if 'timestamp' not in self.df.columns or 'user' not in self.df.columns:
            return {'edges': [], 'influence': []}

        data = self.df.sort_values('timestamp').copy()
        data['prev_user'] = data['user'].shift(1)
        data['prev_timestamp'] = data['timestamp'].shift(1)
        data['gap_seconds'] = (data['timestamp'] - data['prev_timestamp']).dt.total_seconds()

        # Directed edges: previous speaker -> current speaker when user changes.
        transitions = data[(data['prev_user'].notna()) & (data['user'] != data['prev_user'])]
        if transitions.empty:
            return {'edges': [], 'influence': []}

        edges = transitions.groupby(['prev_user', 'user']).agg(
            interaction_count=('user', 'count'),
            avg_reply_seconds=('gap_seconds', 'mean')
        ).reset_index().rename(columns={'prev_user': 'source', 'user': 'target'})

        # Thread starters: first message or gap > 30 minutes.
        thread_start = data[(data['prev_timestamp'].isna()) | (data['gap_seconds'] > 1800)]
        starters = thread_start['user'].value_counts()

        incoming = edges.groupby('target')['interaction_count'].sum()
        outgoing = edges.groupby('source')['interaction_count'].sum()

        influence_rows = []
        for user in data['user'].unique():
            starts = int(starters.get(user, 0))
            in_count = int(incoming.get(user, 0))
            out_count = int(outgoing.get(user, 0))
            influence_score = (starts * 1.2) + (in_count * 0.8) + (out_count * 0.6)
            influence_rows.append({
                'user': user,
                'thread_starts': starts,
                'incoming_replies': in_count,
                'outgoing_replies': out_count,
                'influence_score': round(influence_score, 2)
            })

        influence_rows = sorted(influence_rows, key=lambda x: x['influence_score'], reverse=True)
        return {
            'edges': edges.to_dict('records'),
            'influence': influence_rows
        }

    def get_topic_journey(self, n_topics: int = 4, top_words: int = 6) -> dict:
        """Topic timeline using lightweight LDA + weekly trend aggregation."""
        if 'message' not in self.df.columns or 'timestamp' not in self.df.columns:
            return {'topics': [], 'timeline': []}

        data = self.df.copy()
        docs = data['message'].fillna('').astype(str)
        docs = docs[docs.str.len() >= 3]
        if len(docs) < 10:
            return {'topics': [], 'timeline': []}

        # Language-agnostic tokenization by unicode words.
        vectorizer = CountVectorizer(
            lowercase=True,
            token_pattern=r'(?u)\b\w\w+\b',
            min_df=2,
            max_df=0.9
        )

        try:
            dtm = vectorizer.fit_transform(docs)
        except ValueError:
            return {'topics': [], 'timeline': []}

        if dtm.shape[1] < 5:
            return {'topics': [], 'timeline': []}

        k = max(2, min(n_topics, dtm.shape[0] // 3, 6))
        lda = LatentDirichletAllocation(n_components=k, random_state=42)
        topic_matrix = lda.fit_transform(dtm)

        vocab = np.array(vectorizer.get_feature_names_out())
        topic_labels = {}
        topic_rows = []
        for i, comp in enumerate(lda.components_):
            top_idx = comp.argsort()[-top_words:][::-1]
            keywords = [vocab[idx] for idx in top_idx]
            label = ', '.join(keywords[:3]) if keywords else f'Topic {i + 1}'
            topic_labels[i] = label
            topic_rows.append({
                'topic_id': i,
                'topic_label': label,
                'keywords': keywords
            })

        docs_df = data.loc[docs.index, ['timestamp']].copy()
        docs_df['topic_id'] = topic_matrix.argmax(axis=1)
        docs_df['topic_label'] = docs_df['topic_id'].map(topic_labels)
        docs_df['week'] = docs_df['timestamp'].dt.to_period('W').astype(str)

        timeline = docs_df.groupby(['week', 'topic_label']).size().reset_index(name='message_count')
        return {
            'topics': topic_rows,
            'timeline': timeline.to_dict('records')
        }

    def get_weekly_narrative_recaps(self) -> list:
        """Generate weekly narrative summaries from metrics."""
        if 'timestamp' not in self.df.columns:
            return []

        data = self.df.copy().sort_values('timestamp')
        data['week'] = data['timestamp'].dt.to_period('W').astype(str)

        recaps = []
        for week, group in data.groupby('week'):
            total = len(group)
            top_user = group['user'].value_counts().index[0] if 'user' in group.columns and total > 0 else 'N/A'
            top_user_share = (group['user'].value_counts().iloc[0] / total * 100) if total else 0
            avg_words = group['word_count'].mean() if 'word_count' in group.columns else np.nan
            emoji_rate = (group['emoji_count'] > 0).mean() * 100 if 'emoji_count' in group.columns else 0

            week_sent = group['message'].apply(self._score_message_sentiment)
            mood = 'neutral'
            if week_sent.mean() > 0.03:
                mood = 'positive'
            elif week_sent.mean() < -0.03:
                mood = 'negative'

            recap = (
                f"{week}: {total} messages. {top_user} drove {top_user_share:.1f}% of activity. "
                f"Average words/message: {0 if np.isnan(avg_words) else avg_words:.1f}. "
                f"Emoji-active messages: {emoji_rate:.1f}%. Weekly tone: {mood}."
            )
            recaps.append({
                'week': week,
                'summary': recap,
                'total_messages': total,
                'top_user': top_user,
                'mood': mood
            })

        return recaps

    def semantic_chat_search(self, query: str, top_k: int = 5) -> dict:
        """Semantic search + lightweight QA retrieval over messages."""
        if not query or 'message' not in self.df.columns:
            return {'answer': 'Please enter a question.', 'results': []}

        data = self.df.copy()
        corpus = data['message'].fillna('').astype(str).tolist()
        if not corpus:
            return {'answer': 'No messages available for search.', 'results': []}

        # Character n-gram TF-IDF works better for mixed scripts and Hinglish/Punjabi.
        vectorizer = TfidfVectorizer(analyzer='char_wb', ngram_range=(3, 5), min_df=1)
        matrix = vectorizer.fit_transform(corpus)
        query_vec = vectorizer.transform([query])

        scores = cosine_similarity(query_vec, matrix).flatten()
        if len(scores) == 0:
            return {'answer': 'No relevant messages found.', 'results': []}

        top_idx = scores.argsort()[::-1][:top_k]
        results = []
        for idx in top_idx:
            if scores[idx] <= 0:
                continue
            row = data.iloc[idx]
            results.append({
                'score': float(scores[idx]),
                'user': row.get('user', 'Unknown'),
                'timestamp': str(row.get('timestamp', 'N/A')),
                'message': row.get('message', '')
            })

        if not results:
            return {'answer': 'I could not find relevant lines for that question.', 'results': []}

        top_users = pd.Series([r['user'] for r in results]).value_counts().head(2).index.tolist()
        answer = (
            f"Found {len(results)} relevant messages. "
            f"Most relevant speakers: {', '.join(top_users)}. "
            f"Top match: \"{results[0]['message'][:140]}\""
        )
        return {'answer': answer, 'results': results}
