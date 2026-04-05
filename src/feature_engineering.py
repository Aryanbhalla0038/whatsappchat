"""
Feature Engineering Module for WhatsApp Chat Analysis
Extracts temporal, textual, and behavioral features
"""

import pandas as pd
import numpy as np
import re
from datetime import datetime
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import nltk

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)


class FeatureEngineer:
    """Extract features from preprocessed chat data"""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize with preprocessed dataframe
        
        Args:
            df: DataFrame with columns: timestamp, user, message
        """
        self.df = df.copy()
        self.features = {}
    
    def engineer_temporal_features(self) -> pd.DataFrame:
        """
        Extract temporal features
        - Hour of day
        - Day of week
        - Date
        - Message streak patterns
        """
        df = self.df.copy()
        
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.day_name()
        df['date'] = df['timestamp'].dt.date
        df['week_of_year'] = df['timestamp'].dt.isocalendar().week
        df['month'] = df['timestamp'].dt.month
        df['year'] = df['timestamp'].dt.year
        
        # Time period categorization
        def categorize_time(hour):
            if 6 <= hour < 12:
                return 'Morning'
            elif 12 <= hour < 17:
                return 'Afternoon'
            elif 17 <= hour < 21:
                return 'Evening'
            else:
                return 'Night'
        
        df['time_period'] = df['hour'].apply(categorize_time)
        
        self.df = df
        return df
    
    def engineer_textual_features(self) -> pd.DataFrame:
        """
        Extract textual features
        - Message length
        - Word count
        - Emoji count
        - URL count
        - Mention count
        - Keyword extraction
        """
        df = self.df.copy()
        
        # Basic text features
        df['message_length'] = df['message'].str.len()
        df['word_count'] = df['message'].str.split().str.len()
        df['avg_word_length'] = df['message_length'] / df['word_count']
        
        # Special character features
        df['emoji_count'] = df['message'].apply(self._count_emojis)
        df['punctuation_count'] = df['message'].apply(self._count_punctuation)
        df['url_count'] = df['message'].apply(self._count_urls)
        df['mention_count'] = df['message'].apply(self._count_mentions)
        
        # Text properties
        df['is_question'] = df['message'].str.contains(r'\?', regex=True).astype(int)
        df['is_exclamation'] = df['message'].str.contains(r'!', regex=True).astype(int)
        df['has_caps'] = df['message'].apply(lambda x: int(any(c.isupper() for c in x)))
        df['caps_ratio'] = df['message'].apply(self._calc_caps_ratio)
        
        self.df = df
        return df
    
    def engineer_behavioral_features(self) -> pd.DataFrame:
        """
        Extract behavioral features
        - Response time patterns
        - Message frequency
        - Interaction patterns
        """
        df = self.df.copy()
        
        # Calculate response time (gap between messages from same user)
        df['time_diff_seconds'] = df['timestamp'].diff().dt.total_seconds()
        df['time_diff_seconds'] = df['time_diff_seconds'].fillna(0)
        
        # User participation metrics
        user_stats = df.groupby('user').agg({
            'message': 'count',
            'message_length': ['mean', 'sum'],
            'word_count': 'mean',
            'emoji_count': 'mean'
        }).round(2)
        
        # Message rate (messages per hour in conversation)
        time_span = (df['timestamp'].max() - df['timestamp'].min()).total_seconds() / 3600
        df['message_rate'] = df.groupby('user')['message'].transform('count') / max(time_span, 1)
        
        # Consistency (coefficient of variation of message times)
        df['hour_consistency'] = df.groupby('user')['hour'].transform(lambda x: x.std() if len(x) > 1 else 0)
        
        self.df = df
        return df
    
    def get_user_profiles(self) -> pd.DataFrame:
        """Get comprehensive user behavior profiles"""
        df = self.df
        
        profiles = df.groupby('user').agg({
            'message': 'count',
            'message_length': ['mean', 'min', 'max', 'std'],
            'word_count': 'mean',
            'emoji_count': 'mean',
            'punctuation_count': 'mean',
            'url_count': 'mean',
            'is_question': 'mean',
            'is_exclamation': 'mean',
            'has_caps': 'mean',
            'caps_ratio': 'mean',
            'hour': 'mean',
            'time_diff_seconds': 'mean'
        }).round(2)
        
        profiles.columns = ['_'.join(col).strip() for col in profiles.columns.values]
        profiles = profiles.rename(columns={'message_count': 'total_messages'})
        
        return profiles
    
    def extract_keywords(self, user: Optional[str] = None, top_n: int = 10) -> dict:
        """Extract top keywords for a user or entire chat"""
        if user:
            messages = self.df[self.df['user'] == user]['message']
        else:
            messages = self.df['message']
        
        # Combine all messages
        text = ' '.join(messages).lower()
        
        # Remove URLs and mentions
        text = re.sub(r'http\S+|@\S+', '', text)
        
        # Tokenize
        try:
            tokens = word_tokenize(text)
        except:
            tokens = text.split()
        
        # Remove stopwords
        try:
            stop_words = set(stopwords.words('english'))
        except:
            stop_words = set()
        
        tokens = [t for t in tokens if t.isalnum() and t not in stop_words and len(t) > 2]
        
        # Get top keywords
        keywords = Counter(tokens).most_common(top_n)
        
        return {word: count for word, count in keywords}
    
    @staticmethod
    def _count_emojis(text: str) -> int:
        """Count emojis in text"""
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "]+",
            flags=re.UNICODE
        )
        return len(emoji_pattern.findall(text))
    
    @staticmethod
    def _count_punctuation(text: str) -> int:
        """Count punctuation marks"""
        return len(re.findall(r'[.,!?;:\'"()[]{}]', text))
    
    @staticmethod
    def _count_urls(text: str) -> int:
        """Count URLs in text"""
        return len(re.findall(r'http\S+|www\S+', text))
    
    @staticmethod
    def _count_mentions(text: str) -> int:
        """Count mentions (@username) in text"""
        return len(re.findall(r'@\S+', text))
    
    @staticmethod
    def _calc_caps_ratio(text: str) -> float:
        """Calculate ratio of capital letters"""
        if len(text) == 0:
            return 0
        caps = sum(1 for c in text if c.isupper())
        return caps / len(text)
    
    def get_all_features(self) -> pd.DataFrame:
        """Engineer all features"""
        self.engineer_temporal_features()
        self.engineer_textual_features()
        self.engineer_behavioral_features()
        return self.df
