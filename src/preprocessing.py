"""
Data Preprocessing Module for WhatsApp Chat Analysis
Handles chat export parsing and data cleaning
"""

import re
import pandas as pd


class ChatPreprocessor:
    """Preprocess WhatsApp chat exports into structured data"""
    
    # Regex patterns for WhatsApp message formats
    # Pattern 1: [DD/MM/YYYY, HH:MM:SS] User: Message  (with brackets and seconds)
    PATTERN_BRACKET_SECONDS = r'\[(\d{1,2}[./\-]\d{1,2}[./\-]\d{2,4}),\s+(\d{1,2}:\d{2}:\d{2})\]\s+(.+?):\s+(.*)'
    # Pattern 2: [DD/MM/YYYY, HH:MM] User: Message  (with brackets, no seconds)
    PATTERN_BRACKET_NO_SECONDS = r'\[(\d{1,2}[./\-]\d{1,2}[./\-]\d{2,4}),\s+(\d{1,2}:\d{2})\]\s+(.+?):\s+(.*)'
    # Pattern 3: [DD/MM/YYYY, HH:MM AM/PM] User: Message  (with brackets and AM/PM)
    PATTERN_BRACKET_AMPM = r'\[(\d{1,2}[./\-]\d{1,2}[./\-]\d{2,4}),\s+(\d{1,2}:\d{2}\s*[AP]M)\]\s+(.+?):\s+(.*)'
    # Pattern 4: DD/MM/YYYY, HH:MM - User: Message  (no brackets, with dash)
    PATTERN_DASH = r'(\d{1,2}[./\-]\d{1,2}[./\-]\d{2,4}),\s+(\d{1,2}:\d{2}(?::\d{2})?(?:\s*[AP]M)?)\s*-\s+(.+?):\s+(.*)'
    # Pattern 5: M/D/YYYY, H:MM:SS AM/PM User: Message (US format no brackets)
    PATTERN_US = r'^(\d{1,2}/\d{1,2}/\d{4}),\s+(\d{1,2}:\d{2}(?::\d{2})?\s+[AP]M)\s+(.+?):\s+(.*)'
    # Pattern 6: [YYYY-MM-DD, HH:MM:SS] User: Message (ISO format with brackets)
    PATTERN_ISO_BRACKET = r'\[(\d{4}[./\-]\d{1,2}[./\-]\d{1,2}),\s+(\d{1,2}:\d{2}:\d{2})\]\s+(.+?):\s+(.*)'
    # Pattern 7: YYYY-MM-DD HH:MM:SS - User: Message (ISO format no brackets)
    PATTERN_ISO_DASH = r'(\d{4}[./\-]\d{1,2}[./\-]\d{1,2})\s+(\d{1,2}:\d{2}:\d{2})\s+-\s+(.+?):\s+(.*)'
    # Pattern 8: [DD/MM/YYYY, HH:MM:SS AM/PM] User: Message (with seconds and AM/PM)
    PATTERN_BRACKET_SEC_AMPM = r'\[(\d{1,2}[./\-]\d{1,2}[./\-]\d{2,4}),\s+(\d{1,2}:\d{2}:\d{2}\s*[AP]M)\]\s+(.+?):\s+(.*)'
    
    MESSAGE_PATTERNS = [PATTERN_BRACKET_SECONDS, PATTERN_BRACKET_NO_SECONDS, 
                       PATTERN_BRACKET_AMPM, PATTERN_BRACKET_SEC_AMPM, 
                       PATTERN_DASH, PATTERN_US, PATTERN_ISO_BRACKET, PATTERN_ISO_DASH]
    
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
            
            # Try each pattern
            match = None
            for pattern in self.MESSAGE_PATTERNS:
                match = re.match(pattern, line)
                if match:
                    break
            
            # Fallback: if no patterns match, try a very lenient pattern
            if not match:
                match = self._try_lenient_pattern(line)
                    
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
            # Provide detailed error info
            file_sample = '\n'.join([l.strip() for l in lines[:5] if l.strip()])
            raise ValueError(
                f"No messages found. Expected WhatsApp format like:\n"
                f"[DD/MM/YYYY, HH:MM:SS] User: Message\n\n"
                f"Your file starts with:\n{file_sample}\n\n"
                f"Supported formats:\n"
                f"- [DD/MM/YYYY, HH:MM:SS] User: Message\n"
                f"- [DD/MM/YYYY, HH:MM] User: Message\n"
                f"- [DD/MM/YYYY, HH:MM AM/PM] User: Message\n"
                f"- DD/MM/YYYY, HH:MM - User: Message"
            )
        
        # Parse datetime
        df = self._parse_datetime(df)
        
        # Clean data
        df = self._clean_data(df)
        
        self.df = df
        return df
    
    def _try_lenient_pattern(self, line: str):
        """Try a very lenient pattern for edge cases"""
        # Pattern: anything with date-like start and a colon separator
        lenient = r'^\[?(.+?)[,\s]\s+(.+?)\]?\s+(.+?):\s+(.*)'
        match = re.match(lenient, line)
        
        if match:
            date_str, time_str, user, text = match.groups()
            # Only accept if date and time look reasonable
            if any(c.isdigit() for c in date_str) and ':' in time_str:
                return match
        return None
    
    def _parse_datetime(self, df: pd.DataFrame) -> pd.DataFrame:
        """Parse and combine date and time columns into datetime"""
        df = df.copy()
        
        # List of common date and time formats to try
        date_formats = ['%d/%m/%Y', '%d/%m/%y', '%m/%d/%Y', '%m/%d/%y', 
                       '%d.%m.%Y', '%d.%m.%y', '%d-%m-%Y', '%d-%m-%y',
                       '%Y-%m-%d', '%Y/%m/%d', '%Y.%m.%d']
        time_formats = ['%I:%M:%S %p', '%I:%M %p', '%H:%M:%S', '%H:%M']
        
        timestamp = None
        
        # Try with space separator first
        for date_fmt in date_formats:
            if timestamp is not None:
                break
            for time_fmt in time_formats:
                try:
                    timestamp = pd.to_datetime(
                        df['date'] + ' ' + df['time'],
                        format=f'{date_fmt} {time_fmt}'
                    )
                    break
                except (ValueError, TypeError):
                    continue
        
        # Try without space separator
        if timestamp is None:
            for date_fmt in date_formats:
                if timestamp is not None:
                    break
                for time_fmt in time_formats:
                    try:
                        timestamp = pd.to_datetime(
                            df['date'] + df['time'],
                            format=f'{date_fmt}{time_fmt}'
                        )
                        break
                    except (ValueError, TypeError):
                        continue
        
        # Fallback: try pandas infer_datetime_format
        if timestamp is None:
            try:
                timestamp = pd.to_datetime(
                    df['date'] + ' ' + df['time'],
                    infer_datetime_format=True,
                    errors='coerce'
                )
                # Check if any values were successfully parsed
                if timestamp.isna().all():
                    timestamp = None
            except:
                pass
        
        # Last resort: try stripping and recombining
        if timestamp is None:
            try:
                date_clean = df['date'].astype(str).str.strip()
                time_clean = df['time'].astype(str).str.strip()
                timestamp = pd.to_datetime(
                    date_clean + ' ' + time_clean,
                    infer_datetime_format=True,
                    errors='coerce'
                )
                if timestamp.isna().all():
                    timestamp = None
            except:
                pass
        
        if timestamp is not None:
            df['timestamp'] = timestamp
        else:
            # Provide detailed error with sample data
            sample_dates = df['date'].head(3).tolist()
            sample_times = df['time'].head(3).tolist()
            raise ValueError(
                f"Could not parse datetime. Check date format in your export.\n\n"
                f"Sample dates: {sample_dates}\n"
                f"Sample times: {sample_times}\n\n"
                f"Expected formats like:\n"
                f"  Date: DD/MM/YYYY or MM/DD/YYYY or YYYY-MM-DD\n"
                f"  Time: HH:MM:SS or HH:MM or H:MM:SS AM/PM"
            )
        
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
