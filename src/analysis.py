"""
Analysis Module for WhatsApp Chat
Provides analytical functions and insights
"""

import pandas as pd
import numpy as np


class ChatAnalyzer:
    """Analyze WhatsApp chat patterns and generate insights"""
    
    def __init__(self, df: pd.DataFrame):
        """Initialize with feature-engineered dataframe"""
        self.df = df
    
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
        """Get indicators of message sentiment (basic analysis)"""
        indicators = {}
        
        for user in self.df['user'].unique():
            user_data = self.df[self.df['user'] == user]
            
            question_ratio = (user_data['is_question'].sum() / len(user_data)) * 100 if len(user_data) > 0 else 0
            exclamation_ratio = (user_data['is_exclamation'].sum() / len(user_data)) * 100 if len(user_data) > 0 else 0
            emoji_messages = (user_data['emoji_count'] > 0).sum() / len(user_data) * 100 if len(user_data) > 0 else 0
            
            indicators[user] = {
                'question_ratio': round(question_ratio, 2),
                'exclamation_ratio': round(exclamation_ratio, 2),
                'emoji_usage_ratio': round(emoji_messages, 2),
                'avg_emoji_per_message': round(user_data['emoji_count'].mean(), 2)
            }
        
        return indicators
