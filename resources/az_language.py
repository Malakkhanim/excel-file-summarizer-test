from typing import Dict, List

def get_az_translations() -> Dict[str, str]:
    """
    Get dictionary of common terms and their Azerbaijani translations.
    
    Returns:
        Dict mapping English terms to Azerbaijani translations
    """
    return {
        # Data types
        "numeric": "rəqəmsal",
        "categorical": "kateqoriyal",
        "text": "mətn",
        "date": "tarix",
        
        # Statistics
        "mean": "orta",
        "median": "median",
        "mode": "moda",
        "standard deviation": "standart kənarlaşma",
        "minimum": "minimum",
        "maximum": "maksimum",
        "count": "say",
        "sum": "cəm",
        "average": "orta",
        
        # Visualization
        "histogram": "histoqram",
        "bar chart": "sütun diaqramı",
        "line plot": "xətti qrafik",
        "scatter plot": "nöqtəli qrafik",
        "pie chart": "pasta diaqramı",
        
        # Common phrases
        "please upload": "zəhmət olmasa yükləyin",
        "file uploaded": "fayl yükləndi",
        "error occurred": "xəta baş verdi",
        "processing": "emal edilir",
        "analysis": "təhlil",
        "summary": "xülasə",
        "statistics": "statistika",
        "visualization": "vizualizasiya",
        "data": "məlumat",
        "column": "sütun",
        "row": "sətir",
        "value": "dəyər",
        "chart": "diaqram",
        "graph": "qrafik",
        "plot": "qrafik",
        "distribution": "paylanma",
        "trend": "trend",
        "correlation": "korrelyasiya",
        "relationship": "əlaqə"
    }

def get_common_queries() -> List[str]:
    """
    Get list of common queries in Azerbaijani.
    
    Returns:
        List of example queries
    """
    return [
        "Məlumatların xülasəsini göstər",
        "Statistik məlumatları göstər",
        "Rəqəmsal sütunların paylanmasını göstər",
        "Kateqoriyal sütunların pasta diaqramını göstər",
        "İki sütun arasındakı əlaqəni göstər",
        "Trend xəttini göstər",
        "Orta dəyərləri hesabla",
        "Minimum və maksimum dəyərləri göstər",
        "Sütunların statistikasını göstər",
        "Məlumatların ümumi görünüşünü göstər"
    ]

def get_error_messages() -> Dict[str, str]:
    """
    Get dictionary of error messages in Azerbaijani.
    
    Returns:
        Dict mapping error types to Azerbaijani messages
    """
    return {
        "file_not_found": "Fayl tapılmadı",
        "invalid_file": "Yanlış fayl formatı",
        "processing_error": "Məlumatlar emal edilərkən xəta baş verdi",
        "no_data": "Məlumat tapılmadı",
        "invalid_query": "Sual başa düşülmədi",
        "missing_columns": "Tələb olunan sütunlar tapılmadı",
        "invalid_visualization": "Bu tip vizualizasiya üçün məlumatlar uyğun deyil",
        "empty_data": "Məlumatlar boşdur",
        "invalid_data_type": "Yanlış məlumat tipi",
        "computation_error": "Hesablama zamanı xəta baş verdi"
    }

def get_success_messages() -> Dict[str, str]:
    """
    Get dictionary of success messages in Azerbaijani.
    
    Returns:
        Dict mapping success types to Azerbaijani messages
    """
    return {
        "file_uploaded": "Fayl uğurla yükləndi",
        "analysis_complete": "Təhlil tamamlandı",
        "visualization_ready": "Vizualizasiya hazırdır",
        "query_processed": "Sual uğurla emal edildi",
        "data_processed": "Məlumatlar uğurla emal edildi",
        "summary_generated": "Xülasə yaradıldı",
        "statistics_calculated": "Statistika hesablandı"
    } 