import pandas as pd
import numpy as np
from typing import Union, Dict, Any

def process_excel_file(file: Any) -> pd.DataFrame:
    """
    Process uploaded Excel file and return a pandas DataFrame.
    
    Args:
        file: Uploaded file object from Streamlit
        
    Returns:
        pd.DataFrame: Processed DataFrame
        
    Raises:
        ValueError: If file cannot be processed
    """
    try:
        df = pd.read_excel(file)
        
        # Basic data cleaning
        df = df.replace([np.inf, -np.inf], np.nan)
        df = df.fillna("")
        
        # Convert column names to string
        df.columns = df.columns.astype(str)
        
        return df
    except Exception as e:
        raise ValueError(f"Excel faylı emal edilə bilmədi: {str(e)}")

def get_column_statistics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate basic statistics for each column in the DataFrame.
    
    Args:
        df: Input DataFrame
        
    Returns:
        Dict containing column statistics
    """
    stats = {}
    
    for column in df.columns:
        col_stats = {
            "data_type": str(df[column].dtype),
            "non_null_count": df[column].count(),
            "null_count": df[column].isnull().sum(),
            "unique_values": df[column].nunique()
        }
        
        # Add numerical statistics if applicable
        if pd.api.types.is_numeric_dtype(df[column]):
            col_stats.update({
                "mean": df[column].mean(),
                "std": df[column].std(),
                "min": df[column].min(),
                "max": df[column].max()
            })
        
        stats[column] = col_stats
    
    return stats

def detect_column_types(df: pd.DataFrame) -> Dict[str, str]:
    """
    Detect and categorize column types (numeric, categorical, date, text).
    
    Args:
        df: Input DataFrame
        
    Returns:
        Dict mapping column names to their types
    """
    column_types = {}
    
    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            column_types[column] = "numeric"
        elif pd.api.types.is_datetime64_dtype(df[column]):
            column_types[column] = "date"
        elif df[column].nunique() < len(df) * 0.5:  # Less than 50% unique values
            column_types[column] = "categorical"
        else:
            column_types[column] = "text"
    
    return column_types 