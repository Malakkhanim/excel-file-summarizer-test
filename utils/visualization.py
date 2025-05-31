import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Optional
import numpy as np

def create_visualization(df: pd.DataFrame, query: str) -> go.Figure:
    """
    Create appropriate visualization based on the query and data.
    
    Args:
        df: Input DataFrame
        query: User's query to determine visualization type
        
    Returns:
        plotly.graph_objects.Figure: Interactive plot
    """
    # Convert query to lowercase for easier processing
    query = query.lower()
    
    # Determine visualization type based on query
    if "histoqram" in query or "paylanma" in query:
        return create_histogram(df, query)
    elif "xətti" in query or "trend" in query:
        return create_line_plot(df, query)
    elif "sütun" in query or "bar" in query:
        return create_bar_plot(df, query)
    elif "pasta" in query or "dairə" in query:
        return create_pie_chart(df, query)
    else:
        # Default to scatter plot if no specific type is mentioned
        return create_scatter_plot(df, query)

def create_histogram(df: pd.DataFrame, query: str) -> go.Figure:
    """Create histogram plot."""
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_columns) == 0:
        raise ValueError("Histoqram üçün rəqəmsal sütunlar tələb olunur")
    
    column = numeric_columns[0]  # Use first numeric column by default
    
    fig = px.histogram(
        df,
        x=column,
        title=f"{column} sütununun paylanması",
        labels={column: column},
        template="plotly_white"
    )
    
    fig.update_layout(
        title_x=0.5,
        showlegend=True,
        xaxis_title=column,
        yaxis_title="Say"
    )
    
    return fig

def create_line_plot(df: pd.DataFrame, query: str) -> go.Figure:
    """Create line plot."""
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_columns) < 2:
        raise ValueError("Xətti qrafik üçün ən azı iki rəqəmsal sütun tələb olunur")
    
    x_column = numeric_columns[0]
    y_column = numeric_columns[1]
    
    fig = px.line(
        df,
        x=x_column,
        y=y_column,
        title=f"{y_column} - {x_column} asılılığı",
        labels={x_column: x_column, y_column: y_column},
        template="plotly_white"
    )
    
    fig.update_layout(
        title_x=0.5,
        showlegend=True,
        xaxis_title=x_column,
        yaxis_title=y_column
    )
    
    return fig

def create_bar_plot(df: pd.DataFrame, query: str) -> go.Figure:
    """Create bar plot."""
    # Try to find categorical and numeric columns
    categorical_columns = df.select_dtypes(include=['object']).columns
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    
    if len(categorical_columns) == 0 or len(numeric_columns) == 0:
        raise ValueError("Sütun qrafiki üçün həm kateqoriyal, həm də rəqəmsal sütunlar tələb olunur")
    
    category_column = categorical_columns[0]
    value_column = numeric_columns[0]
    
    # Group by category and calculate mean
    grouped_df = df.groupby(category_column)[value_column].mean().reset_index()
    
    fig = px.bar(
        grouped_df,
        x=category_column,
        y=value_column,
        title=f"{category_column} üzrə {value_column} orta dəyərləri",
        labels={category_column: category_column, value_column: value_column},
        template="plotly_white"
    )
    
    fig.update_layout(
        title_x=0.5,
        showlegend=True,
        xaxis_title=category_column,
        yaxis_title=f"Orta {value_column}"
    )
    
    return fig

def create_pie_chart(df: pd.DataFrame, query: str) -> go.Figure:
    """Create pie chart."""
    categorical_columns = df.select_dtypes(include=['object']).columns
    
    if len(categorical_columns) == 0:
        raise ValueError("Pasta diaqramı üçün kateqoriyal sütunlar tələb olunur")
    
    column = categorical_columns[0]
    
    # Count values
    value_counts = df[column].value_counts().reset_index()
    value_counts.columns = [column, 'count']
    
    fig = px.pie(
        value_counts,
        values='count',
        names=column,
        title=f"{column} sütununun paylanması",
        template="plotly_white"
    )
    
    fig.update_layout(
        title_x=0.5,
        showlegend=True
    )
    
    return fig

def create_scatter_plot(df: pd.DataFrame, query: str) -> go.Figure:
    """Create scatter plot."""
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_columns) < 2:
        raise ValueError("Nöqtəli qrafik üçün ən azı iki rəqəmsal sütun tələb olunur")
    
    x_column = numeric_columns[0]
    y_column = numeric_columns[1]
    
    fig = px.scatter(
        df,
        x=x_column,
        y=y_column,
        title=f"{y_column} - {x_column} əlaqəsi",
        labels={x_column: x_column, y_column: y_column},
        template="plotly_white"
    )
    
    fig.update_layout(
        title_x=0.5,
        showlegend=True,
        xaxis_title=x_column,
        yaxis_title=y_column
    )
    
    return fig 