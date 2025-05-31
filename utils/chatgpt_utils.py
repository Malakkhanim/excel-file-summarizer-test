import os
from typing import Dict, Any, List
import openai
from dotenv import load_dotenv
import pandas as pd
from config.settings import get_settings

# Load environment variables
load_dotenv()

# Get API key from environment
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("""
        OpenAI API key not found! Please follow these steps:
        1. Create a file named '.env' in the project root directory
        2. Add your OpenAI API key like this: OPENAI_API_KEY=your-api-key-here
        3. Make sure to replace 'your-api-key-here' with your actual OpenAI API key
        4. Restart the application
    """)

# Initialize OpenAI client
client = openai.OpenAI(api_key=api_key)

def get_chatgpt_response(query: str, df: pd.DataFrame) -> str:
    """
    Get response from ChatGPT based on the query and DataFrame.
    
    Args:
        query: User's query in Azerbaijani
        df: DataFrame containing the data
        
    Returns:
        str: ChatGPT's response
    """
    try:
        # Prepare the system message with context about the data
        system_message = prepare_system_message(df)
        
        # Prepare the user message with the query
        user_message = prepare_user_message(query, df)
        
        # Get response from ChatGPT
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Xəta baş verdi: {str(e)}"

def prepare_system_message(df: pd.DataFrame) -> str:
    """
    Prepare the system message with context about the data.
    
    Args:
        df: DataFrame containing the data
        
    Returns:
        str: System message
    """
    # Get basic information about the DataFrame
    num_rows = len(df)
    num_cols = len(df.columns)
    column_info = []
    
    for col in df.columns:
        col_type = str(df[col].dtype)
        unique_vals = df[col].nunique()
        if pd.api.types.is_numeric_dtype(df[col]):
            col_info = f"{col} (rəqəmsal): {unique_vals} unikal dəyər"
        else:
            col_info = f"{col} (mətn): {unique_vals} unikal dəyər"
        column_info.append(col_info)
    
    system_message = f"""Sən Excel məlumatlarını analiz edən Azərbaycan dilində chatbot-san. 
Məlumatlar haqqında məlumat:
- Ümumi sətir sayı: {num_rows}
- Sütun sayı: {num_cols}
- Sütunlar:
{chr(10).join(column_info)}

Sənin vəzifən:
1. İstifadəçinin sualını başa düşmək
2. Məlumatları analiz etmək
3. Azərbaycan dilində cavab vermək
4. Lazım olduqda vizualizasiya təklif etmək

Cavablarını aşağıdakı formatlarda verə bilərsən:
- Sadə mətn cavabı
- Statistik məlumatlar
- Vizualizasiya təklifi (vizualizasiya açar sözü ilə)
- Xülasə

Əgər sualı başa düşməsən, istifadəçidən daha aydın soruşmağını xahiş et."""
    
    return system_message

def prepare_user_message(query: str, df: pd.DataFrame) -> str:
    """
    Prepare the user message with the query and relevant data.
    
    Args:
        query: User's query
        df: DataFrame containing the data
        
    Returns:
        str: User message
    """
    # Get a sample of the data (first 5 rows) to provide context
    sample_data = df.head().to_string()
    
    user_message = f"""İstifadəçi sualı: {query}

Məlumatların nümunəsi (ilk 5 sətir):
{sample_data}

Zəhmət olmasa, bu suala Azərbaycan dilində cavab ver və lazım olduqda vizualizasiya təklif et."""
    
    return user_message

def process_visualization_request(response: str, df: pd.DataFrame) -> tuple[str, bool]:
    """
    Process the ChatGPT response to determine if visualization is needed.
    
    Args:
        response: ChatGPT's response
        df: DataFrame containing the data
        
    Returns:
        tuple: (processed_response, needs_visualization)
    """
    # Check if the response suggests visualization
    viz_keywords = ["vizualizasiya", "qrafik", "diaqram", "histoqram", "pasta", "xətti", "sütun"]
    needs_viz = any(keyword in response.lower() for keyword in viz_keywords)
    
    if needs_viz:
        # Add visualization marker to the response
        response = response + " visualization"
    
    return response, needs_viz 