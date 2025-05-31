import pandas as pd
from typing import Dict, Any, List, Tuple
import re
from resources.az_language import get_az_translations
from .chatgpt_utils import get_chatgpt_response, process_visualization_request

def process_query(query: str, df: pd.DataFrame) -> str:
    """
    Process user query in Azerbaijani using ChatGPT and generate appropriate response.
    
    Args:
        query: User's query in Azerbaijani
        df: DataFrame containing the data
        
    Returns:
        str: Response to the query
    """
    try:
        # Get response from ChatGPT
        response = get_chatgpt_response(query, df)
        
        # Process visualization request if needed
        response, needs_viz = process_visualization_request(response, df)
        
        return response
    
    except Exception as e:
        return f"Xəta baş verdi: {str(e)}"

def detect_query_type(query: str, columns: List[str], translations: Dict[str, str]) -> Tuple[str, List[str]]:
    """
    Detect the type of query and relevant columns.
    This function is kept for backward compatibility but is no longer used.
    
    Args:
        query: User's query
        columns: List of DataFrame columns
        translations: Dictionary of Azerbaijani translations
        
    Returns:
        Tuple of (query_type, relevant_columns)
    """
    # Summary keywords
    summary_keywords = ["xülasə", "ümumi", "qısa", "məlumat"]
    
    # Statistics keywords
    stats_keywords = ["statistika", "orta", "minimum", "maksimum", "say"]
    
    # Visualization keywords
    viz_keywords = ["qrafik", "diaqram", "vizual", "göstər"]
    
    # Detect query type
    if any(keyword in query for keyword in summary_keywords):
        return "summary", columns
    elif any(keyword in query for keyword in stats_keywords):
        return "statistics", extract_columns_from_query(query, columns)
    elif any(keyword in query for keyword in viz_keywords):
        return "visualization", extract_columns_from_query(query, columns)
    
    return "unknown", []

def extract_columns_from_query(query: str, columns: List[str]) -> List[str]:
    """
    Extract column names mentioned in the query.
    This function is kept for backward compatibility but is no longer used.
    
    Args:
        query: User's query
        columns: List of available columns
        
    Returns:
        List of mentioned columns
    """
    mentioned_columns = []
    for column in columns:
        if column.lower() in query.lower():
            mentioned_columns.append(column)
    
    return mentioned_columns if mentioned_columns else columns

def generate_summary(df: pd.DataFrame, columns: List[str]) -> str:
    """
    Generate a summary of the data.
    This function is kept for backward compatibility but is no longer used.
    
    Args:
        df: Input DataFrame
        columns: Columns to include in summary
        
    Returns:
        str: Summary text
    """
    summary = []
    summary.append(f"Ümumi sətir sayı: {len(df)}")
    summary.append(f"Sütun sayı: {len(columns)}")
    
    # Add column information
    for column in columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            summary.append(f"\n{column} sütunu üçün:")
            summary.append(f"Orta qiymət: {df[column].mean():.2f}")
            summary.append(f"Minimum: {df[column].min():.2f}")
            summary.append(f"Maksimum: {df[column].max():.2f}")
    
    return "\n".join(summary)

def generate_statistics(df: pd.DataFrame, columns: List[str]) -> str:
    """
    Generate statistical analysis of the data.
    This function is kept for backward compatibility but is no longer used.
    
    Args:
        df: Input DataFrame
        columns: Columns to analyze
        
    Returns:
        str: Statistical analysis text
    """
    stats = []
    
    for column in columns:
        stats.append(f"\n{column} sütunu üçün statistika:")
        
        if pd.api.types.is_numeric_dtype(df[column]):
            stats.append(f"Orta: {df[column].mean():.2f}")
            stats.append(f"Standart kənarlaşma: {df[column].std():.2f}")
            stats.append(f"Median: {df[column].median():.2f}")
        else:
            stats.append(f"Unikal dəyərlər: {df[column].nunique()}")
            stats.append(f"Ən çox təkrarlanan: {df[column].mode().iloc[0]}")
    
    return "\n".join(stats)

def generate_visualization_response(df: pd.DataFrame, columns: List[str]) -> str:
    """
    Generate response for visualization requests.
    This function is kept for backward compatibility but is no longer used.
    
    Args:
        df: Input DataFrame
        columns: Columns to visualize
        
    Returns:
        str: Response indicating visualization will be shown
    """
    return "Görsel təqdimat hazırlanır... visualization" 