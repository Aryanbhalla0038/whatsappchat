"""
Unit tests for WhatsApp Chat Analyzer
Run with: pytest tests/ -v
"""

import pandas as pd
import pytest
from datetime import datetime
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from preprocessing import ChatPreprocessor
from feature_engineering import FeatureEngineer
from analysis import ChatAnalyzer


class TestChatPreprocessor:
    """Test chat preprocessing functionality"""
    
    @pytest.fixture
    def sample_messages(self, tmp_path):
        """Create a sample chat file for testing"""
        chat_content = "[1/1/2024, 10:30:45] Alice: Hello world!\n"
        chat_content += "[1/1/2024, 10:31:12] Bob: Hi Alice! Hello\n"
        
        chat_file = tmp_path / "test_chat.txt"
        chat_file.write_text(chat_content, encoding='utf-8')
        return str(chat_file)
    
    def test_chat_parsing(self, sample_messages):
        """Test basic chat file parsing"""
        preprocessor = ChatPreprocessor()
        df = preprocessor.parse_chat_file(sample_messages)
        
        assert len(df) == 2
        assert 'timestamp' in df.columns
        assert 'user' in df.columns
        assert 'message' in df.columns
    
    def test_user_extraction(self, sample_messages):
        """Test correct user extraction"""
        preprocessor = ChatPreprocessor()
        df = preprocessor.parse_chat_file(sample_messages)
        
        users = df['user'].unique()
        assert 'Alice' in users
        assert 'Bob' in users


class TestFeatureEngineer:
    """Test feature engineering functionality"""
    
    @pytest.fixture
    def sample_df(self):
        """Create sample dataframe"""
        data = {
            'timestamp': [
                datetime(2024, 1, 1, 10, 30),
                datetime(2024, 1, 1, 14, 45),
                datetime(2024, 1, 2, 9, 15)
            ],
            'user': ['Alice', 'Bob', 'Alice'],
            'message': ['Hello!', 'Hi there! How are you?', 'Doing great!']
        }
        return pd.DataFrame(data)
    
    def test_temporal_features(self, sample_df):
        """Test temporal feature extraction"""
        engineer = FeatureEngineer(sample_df)
        df = engineer.engineer_temporal_features()
        
        assert 'hour' in df.columns
        assert 'day_of_week' in df.columns
        assert 'time_period' in df.columns
        assert df['hour'].max() <= 23


class TestChatAnalyzer:
    """Test analysis functionality"""
    
    @pytest.fixture
    def sample_df_with_features(self):
        """Create feature-engineered sample"""
        data = {
            'timestamp': pd.date_range('2024-01-01', periods=10, freq='h'),
            'user': ['Alice', 'Bob'] * 5,
            'message': ['Hello'] * 10,
            'message_length': [10, 15, 12, 18, 20, 11, 14, 19, 13, 16],
            'word_count': [1, 2, 1, 2, 3, 1, 2, 3, 2, 2],
            'emoji_count': [1, 0, 2, 1, 0, 1, 1, 0, 2, 1],
            'is_question': [0, 1, 0, 1, 0, 0, 1, 0, 0, 1],
            'is_exclamation': [1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
            'hour': [i % 24 for i in range(10)],
            'day_of_week': ['Monday'] * 10
        }
        return pd.DataFrame(data)
    
    def test_activity_by_hour(self, sample_df_with_features):
        """Test hourly activity analysis"""
        analyzer = ChatAnalyzer(sample_df_with_features)
        activity = analyzer.get_activity_by_hour()
        
        assert len(activity) > 0
        assert activity.max() > 0
    
    def test_user_statistics(self, sample_df_with_features):
        """Test user statistics generation"""
        analyzer = ChatAnalyzer(sample_df_with_features)
        stats = analyzer.get_user_statistics()
        
        assert 'Alice' in stats
        assert 'Bob' in stats
        assert stats['Alice']['total_messages'] == 5
        assert stats['Bob']['total_messages'] == 5
    
    def test_conversation_health(self, sample_df_with_features):
        """Test conversation health analysis"""
        analyzer = ChatAnalyzer(sample_df_with_features)
        health = analyzer.get_conversation_health()
        
        assert 'total_messages' in health
        assert 'unique_users' in health
        assert 'balance_ratio' in health
        assert health['total_messages'] == 10
        assert health['unique_users'] == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
