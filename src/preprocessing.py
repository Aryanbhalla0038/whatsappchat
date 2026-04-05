"""
Data Preprocessing Module for WhatsApp Chat Analysis
Handles chat export parsing and data cleaning
"""

import re
import pandas as pd


class ChatPreprocessor:
    """Preprocess WhatsApp chat exports into structured data"""
    
    # Regex pattern for WhatsApp message format (updated format)
    # Handles: [HH:MM, DD/MM/YYYY] or [DD/MM/YY, HH:MM] patterns
    MESSAGE_PATTERN = r'\[(\d{1,2}/\d{1,2}/\d{2,4}),?\s+(\d{1,2}:\d{2}(?::\d{2})?(?:\s*[AP]M)?)\]\s+([^:]+):\s+(.*)'
    
    def __init__(self):
        self.df = None
        
    def parse_chat_file(self, file_path: str) -> pd.DataFrame:
        """
        Parse WhatsApp chat export file
        
        Args:
            file_path: Path to WhatsApp chat export file (.txt)
            
        Returns:
            DataFrame with columns: timestamp, user, message
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='latin-1') as f:
                lines = f.readlines()
        
        messages = []
        current_message = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if line matches message pattern
            match = re.match(self.MESSAGE_PATTERN, line)
            if match:
                if current_message:
                    messages.append(current_message)
                
                date_str, time_str, user, text = match.groups()
                current_message = {
                    'date': date_str,
                    'time': time_str,
                    'user': user.strip(),
                    'message': text.strip()
                }
            else:
                # Continuation of previous message
                if current_message:
                    current_message['message'] += '\n' + line
        
        # Add last message
        if current_message:
            messages.append(current_message)
        
        # Create DataFrame
        df = pd.DataFrame(messages)
        
        if df.empty:
            raise ValueError("No messages found in chat file. Check file format.")
        
        # Parse datetime
        df = self._parse_datetime(df)
        
        # Clean data
        df = self._clean_data(df)
        
        self.df = df
        return df
    
    def _parse_datetime(self, df: pd.DataFrame) -> pd.DataFrame:
        """Parse and combine date and time columns into datetime"""
        df = df.copy()
        
        for date_format in ['%d/%m/%Y', '%d/%m/%y', '%m/%d/%Y']:
            try:
                df['timestamp'] = pd.to_datetime(
                    df['date'] + ' ' + df['time'],
                    format=f'{date_format} %I:%M %p'
                )
                break
            except:
                try:
                    df['timestamp'] = pd.to_datetime(
                        df['date'] + ' ' + df['time'],
                        format=f'{date_format} %H:%M:%S'
                    )
                    break
                except:
                    pass
        
        df = df.drop(['date', 'time'], axis=1)
        return df
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and normalize chat data"""
        df = df.copy()
        
        # Remove system messages (optional based on analysis preference)
        system_indicators = ['created group', 'added', 'removed', 'changed subject', 
                            'You created this group', 'Messages and calls are encrypted',
                            'left', 'joined using', 'security code changed', 'image omitted',
                            'video omitted', 'audio omitted', 'file omitted', '<Media omitted>']
        
        mask = ~df['message'].str.contains('|'.join(system_indicators), case=False, na=False)
        df = df[mask].reset_index(drop=True)
        
        # Remove empty messages
        df = df[df['message'].str.len() > 0]
        
        # Normalize user names
        df['user'] = df['user'].str.strip()
        
        return df
    
    def get_stats(self) -> dict:
        """Get basic statistics about the chat"""
        if self.df is None:
            return {}
        
        df = self.df
        return {
            'total_messages': len(df),
            'unique_users': df['user'].nunique(),
            'date_range': f"{df['timestamp'].min().date()} to {df['timestamp'].max().date()}",
            'users': df['user'].value_counts().to_dict()
        }


def load_and_preprocess_chat(file_path: str) -> pd.DataFrame:
    """Convenience function to load and preprocess a chat file"""
    preprocessor = ChatPreprocessor()
    return preprocessor.parse_chat_file(file_path)
