import streamlit as st
import pandas as pd
from pathlib import Path
import sys
import base64
from datetime import datetime

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from utils.excel_processor import process_excel_file
from utils.nlp_utils import process_query
from utils.visualization import create_visualization
from resources.az_language import get_az_translations
from config.settings import get_settings

# Get settings
settings = get_settings()

# Set page configuration
st.set_page_config(
    page_title=settings["app"]["name"],
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"  # Changed to expanded
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    .upload-area {
        border: 2px dashed #ccc;
        border-radius: 5px;
        padding: 20px;
        text-align: center;
        background-color: #f8f9fa;
        margin: 20px 0;
    }
    .upload-area:hover {
        border-color: #666;
        background-color: #f0f0f0;
    }
    .upload-icon {
        font-size: 48px;
        color: #1E88E5;
        margin-bottom: 1rem;
    }
    .upload-text {
        font-size: 18px;
        color: #262730;
        margin-bottom: 0.5rem;
    }
    .upload-hint {
        font-size: 14px;
        color: #666666;
    }
    .chat-container {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stChatMessage {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .stChatMessage[data-testid="stChatMessage"] {
        background-color: #F0F2F6;
    }
    .history-slider {
        position: relative;
        overflow: hidden;
        padding: 10px 0;
    }
    
    .history-items-container {
        display: flex;
        transition: transform 0.3s ease;
        gap: 10px;
    }
    
    .history-item {
        min-width: 200px;
        padding: 15px;
        margin: 5px;
        border-radius: 8px;
        background-color: #f0f0f0;
        cursor: pointer;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        flex: 0 0 auto;
    }
    
    .history-item:hover {
        background-color: #e0e0e0;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    .history-item.active {
        background-color: #1E88E5;
        color: white;
    }
    
    .history-item.active .history-timestamp {
        color: #e0e0e0;
    }
    
    .history-timestamp {
        font-size: 0.8em;
        color: #666;
        margin-top: 5px;
    }
    
    .slider-nav {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin-top: 10px;
    }
    
    .slider-nav button {
        background-color: #1E88E5;
        color: white;
        border: none;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .slider-nav button:hover {
        background-color: #1565C0;
        transform: scale(1.1);
    }
    
    .slider-nav button:disabled {
        background-color: #ccc;
        cursor: not-allowed;
    }
    
    .history-title {
        font-size: 1rem;
        color: #666;
        margin: 1rem 0 0.5rem 0;
        padding: 0 1rem;
    }
    
    .clear-history-btn {
        font-size: 0.8em;
        padding: 5px 10px;
        background-color: #ff4444;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }
    
    .clear-history-btn:hover {
        background-color: #cc0000;
    }
    
    .sidebar-toggle {
        position: fixed;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        z-index: 999;
        background-color: #1E88E5;
        color: white;
        border: none;
        border-radius: 0 4px 4px 0;
        padding: 10px;
        cursor: pointer;
        box-shadow: 2px 0 4px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .sidebar-toggle:hover {
        background-color: #1565C0;
        padding-right: 15px;
    }
    
    .sidebar-toggle.collapsed {
        left: 0;
    }
    
    .sidebar-toggle.expanded {
        left: 250px;
    }
    
    .sidebar-content {
        transition: all 0.3s ease;
        padding: 1rem;
    }
    
    .sidebar-content.collapsed {
        display: none;
    }
    
    .sidebar-content.expanded {
        display: block;
    }
    
    /* Hide the default Streamlit sidebar toggle */
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    
    /* Style the history items in sidebar */
    .sidebar-history-item {
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
        background-color: #f0f0f0;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .sidebar-history-item:hover {
        background-color: #e0e0e0;
        transform: translateX(5px);
    }
    
    .sidebar-history-item.active {
        background-color: #1E88E5;
        color: white;
    }
    
    .sidebar-history-timestamp {
        font-size: 0.8em;
        color: #666;
        margin-top: 5px;
    }
    
    .sidebar-history-item.active .sidebar-history-timestamp {
        color: #e0e0e0;
    }
    
    .sidebar-header {
        display: flex;
        align-items: center;
        padding: 1.5rem;
        background-color: #1E88E5;
        color: white;
        margin: -1rem -1rem 1rem -1rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .sidebar-header img {
        height: 40px;
        margin-right: 10px;
    }
    
    .sidebar-header h3 {
        margin: 0;
        color: white;
        font-size: 1.2rem;
        font-weight: 600;
    }
    
    /* New chat button */
    .new-chat-button {
        background-color: #1E88E5;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        margin: 1rem 0;
        width: 100%;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
    }
    
    .new-chat-button:hover {
        background-color: #1565C0;
        transform: translateY(-1px);
    }
    
    /* Adjust main content padding */
    .main .block-container {
        padding-left: 320px;
        padding-top: 1rem;
    }
    
    /* Hide the default Streamlit header */
    header[data-testid="stHeader"] {
        display: none;
    }
    
    /* Header styling */
    .header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 1rem 0;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1rem;
    }
    
    .logo-container img {
        max-height: 80px;
        width: auto;
        margin-right: 1rem;
    }
    
    .app-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        margin: 0;
        text-align: center;
    }
    
    .app-subtitle {
        font-size: 1.2rem;
        color: #666;
        margin-top: 0.5rem;
        text-align: center;
    }
    
    /* File info container styles */
    .file-info-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 2rem 0;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .file-info {
        text-align: center;
        padding: 1rem 2rem;
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .file-name {
        color: #1E88E5;
        font-size: 1.5rem;
        margin: 0;
        padding: 0.5rem 0;
        font-weight: 600;
    }
    
    .file-stats {
        color: #666;
        font-size: 1rem;
        margin: 0.5rem 0 0 0;
    }
    
    /* Upload container styles */
    .upload-container {
        text-align: center;
        margin: 2rem 0;
        padding: 2rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
    
    .upload-title {
        color: #1E88E5;
        font-size: 1.8rem;
        margin-bottom: 0.5rem;
    }
    
    .upload-subtitle {
        color: #666;
        font-size: 1.1rem;
        margin: 0;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #f8f9fa;
        padding-top: 0;
        width: 300px !important;
    }
    
    /* Stats container styles */
    .stats-container {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .stats-title {
        color: #1E88E5;
        font-size: 1.2rem;
        margin: 0 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #eee;
    }
    
    .column-info {
        background: #f8f9fa;
        padding: 0.8rem;
        margin: 0.5rem 0;
        border-radius: 6px;
        border-left: 3px solid #1E88E5;
    }
    
    .column-info strong {
        color: #1E88E5;
    }
    
    .column-info small {
        color: #666;
    }
    
    /* Preview container styles */
    .preview-container {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .preview-title {
        color: #1E88E5;
        font-size: 1.2rem;
        margin: 0 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #eee;
    }
    
    /* Metric styling */
    [data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 1rem !important;
        color: #666 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_data' not in st.session_state:
    st.session_state.current_data = None
if 'show_chat' not in st.session_state:
    st.session_state.show_chat = False
if 'upload_history' not in st.session_state:
    st.session_state.upload_history = []
if 'selected_history' not in st.session_state:
    st.session_state.selected_history = None
if 'history_slider_position' not in st.session_state:
    st.session_state.history_slider_position = 0
if 'sidebar_expanded' not in st.session_state:
    st.session_state.sidebar_expanded = True

def create_upload_area():
    """Create a styled upload area with drag and drop functionality."""
    st.markdown("""
    <div class="upload-area">
        <h3>📊 Excel Faylını Buraya Sürüşdürün</h3>
        <p>və ya fayl seçmək üçün klikləyin</p>
    </div>
    """, unsafe_allow_html=True)
    return st.file_uploader("", type=['xlsx', 'xls'], key="file_uploader")

def validate_excel_file(file):
    """Validate if the uploaded file is an Excel file."""
    if file is not None:
        return file.name.endswith(('.xlsx', '.xls'))
    return False

def add_to_history(file_name, timestamp):
    """Add a new file to the upload history."""
    history_item = {
        'file_name': file_name,
        'timestamp': timestamp,
        'chat_history': [],
        'df': st.session_state.df  # Store the DataFrame in history
    }
    st.session_state.upload_history.append(history_item)
    st.session_state.selected_history = history_item

def load_history_item(history_item):
    """Load a history item and its associated data."""
    st.session_state.selected_history = history_item
    st.session_state.chat_history = history_item['chat_history']
    st.session_state.df = history_item['df']  # Load the DataFrame from history
    st.session_state.show_chat = True

def create_history_slider():
    """Create a swipeable history slider."""
    if not st.session_state.upload_history:
        st.info("Hələ heç bir fayl yüklənməyib")
        return
    
    # Calculate visible items and total pages
    items_per_page = 3
    total_items = len(st.session_state.upload_history)
    total_pages = (total_items + items_per_page - 1) // items_per_page
    
    # Ensure slider position is within bounds
    st.session_state.history_slider_position = max(0, min(st.session_state.history_slider_position, total_pages - 1))
    
    # Create slider container
    st.markdown('<div class="history-slider">', unsafe_allow_html=True)
    
    # Create items container with transform
    transform = f"translateX(-{st.session_state.history_slider_position * 100}%)"
    st.markdown(f'<div class="history-items-container" style="transform: {transform}">', unsafe_allow_html=True)
    
    # Display history items
    for idx, item in enumerate(st.session_state.upload_history):
        is_active = st.session_state.selected_history == item
        active_class = "active" if is_active else ""
        
        st.markdown(f"""
            <div class="history-item {active_class}" onclick="document.querySelector('[data-testid=stButton][key=select_{item['file_name']}']').click()">
                <div><strong>{item['file_name']}</strong></div>
                <div class="history-timestamp">{item['timestamp'].strftime('%Y-%m-%d %H:%M')}</div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Seç", key=f"select_{item['file_name']}", use_container_width=True):
            load_history_item(item)
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="slider-nav">', unsafe_allow_html=True)
        
        # Previous button
        if st.button("←", key="prev_slide", disabled=st.session_state.history_slider_position == 0):
            st.session_state.history_slider_position = max(0, st.session_state.history_slider_position - 1)
            st.rerun()
        
        # Page indicator
        st.markdown(f"<div style='text-align: center; line-height: 30px;'>{st.session_state.history_slider_position + 1}/{total_pages}</div>", unsafe_allow_html=True)
        
        # Next button
        if st.button("→", key="next_slide", disabled=st.session_state.history_slider_position >= total_pages - 1):
            st.session_state.history_slider_position = min(total_pages - 1, st.session_state.history_slider_position + 1)
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

def toggle_sidebar():
    """Toggle the sidebar state."""
    st.session_state.sidebar_expanded = not st.session_state.sidebar_expanded

def create_sidebar_content():
    """Create the sidebar content with history items."""
    # Sidebar header with logo
    st.markdown(f"""
        <div class="sidebar-header">
            <img src="data:image/png;base64,{get_base64_encoded_image("Copy of 4Sim_Logotype_Eng.png")}" alt="Logo">
            <h3>Excel Məlumat Analiz Botu</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # New Chat button
    if st.button("🆕 Yeni Söhbət", key="new_chat", use_container_width=True):
        st.session_state.show_chat = False
        st.session_state.df = None
        st.session_state.chat_history = []
        st.rerun()
    
    # History section
    st.markdown('<div class="history-title">📚 Söhbət Tarixçəsi</div>', unsafe_allow_html=True)
    
    # Show history items
    if st.session_state.upload_history:
        for item in st.session_state.upload_history:
            is_active = st.session_state.selected_history == item
            active_class = "active" if is_active else ""
            
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"""
                    <div class="sidebar-history-item {active_class}">
                        <div><strong>{item['file_name']}</strong></div>
                        <div class="sidebar-history-timestamp">{item['timestamp'].strftime('%Y-%m-%d %H:%M')}</div>
                    </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("→", key=f"select_{item['file_name']}", use_container_width=True):
                    load_history_item(item)
                    st.rerun()
    else:
        st.info("Hələ heç bir fayl yüklənməyib")
    
    # Clear history button at the bottom
    st.markdown('<div style="margin-top: auto; padding: 1rem;">', unsafe_allow_html=True)
    if st.button("🗑️ Tarixçəni Təmizlə", key="clear_history", use_container_width=True):
        st.session_state.upload_history = []
        st.session_state.selected_history = None
        st.session_state.chat_history = []
        st.session_state.df = None
        st.session_state.show_chat = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def create_header():
    """Create the header with logo and app name."""
    st.markdown("""
        <div class="header-container">
            <div class="logo-container">
                <img src="data:image/png;base64,{}" alt="Logo">
            </div>
            <h1 class="app-title">Excel Məlumat Analiz Botu</h1>
            <p class="app-subtitle">Azərbaycan dilində Excel məlumatlarını analiz edən chatbot</p>
        </div>
    """.format(get_base64_encoded_image("Copy of 4Sim_Logotype_Eng.png")), unsafe_allow_html=True)

def get_base64_encoded_image(image_path):
    """Get base64 encoded image."""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def display_data_preview(df):
    """Display data preview and statistics."""
    # Create two columns for stats and preview
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Display statistics in a styled container
        st.markdown("""
            <div class='stats-container'>
                <h3 class='stats-title'>📊 Məlumat Statistikası</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Basic statistics
        stats_data = {
            "Sətir sayı": len(df),
            "Sütun sayı": len(df.columns),
            "Boş dəyərlər": df.isnull().sum().sum(),
            "Unikal dəyərlər": df.nunique().sum()
        }
        
        for stat_name, stat_value in stats_data.items():
            st.metric(stat_name, stat_value)
        
        # Column information
        st.markdown("""
            <div class='stats-container' style='margin-top: 1rem;'>
                <h3 class='stats-title'>📋 Sütunlar</h3>
            </div>
        """, unsafe_allow_html=True)
        
        for col in df.columns:
            col_type = str(df[col].dtype)
            unique_vals = df[col].nunique()
            st.markdown(f"""
                <div class='column-info'>
                    <strong>{col}</strong><br>
                    <small>Tip: {col_type} | Unikal: {unique_vals}</small>
                </div>
            """, unsafe_allow_html=True)
    
    with col2:
        # Display data preview
        st.markdown("""
            <div class='preview-container'>
                <h3 class='preview-title'>👁️ Məlumat Önizləməsi</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Show first 5 rows of the data
        st.dataframe(df.head(), use_container_width=True)
        
        # Add download button for the full data
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Tam Məlumatı Yüklə",
            csv,
            "data.csv",
            "text/csv",
            key='download-csv'
        )

def main():
    # Create header
    create_header()
    
    # Initialize session state variables
    if 'df' not in st.session_state:
        st.session_state.df = None
    if 'show_chat' not in st.session_state:
        st.session_state.show_chat = False
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'upload_history' not in st.session_state:
        st.session_state.upload_history = []
    if 'selected_history' not in st.session_state:
        st.session_state.selected_history = None

    # Create sidebar content
    with st.sidebar:
        create_sidebar_content()

    # Main content area
    main_content = st.container()
    
    with main_content:
        if not st.session_state.show_chat:
            # File upload section with custom styling
            st.markdown("""
                <div class='upload-container'>
                    <h2 class='upload-title'>Excel Faylını Yükləyin</h2>
                    <p class='upload-subtitle'>Məlumatları analiz etmək üçün Excel faylını seçin</p>
                </div>
            """, unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader("", type=['xlsx', 'xls'], label_visibility="collapsed")
            
            if uploaded_file is not None:
                try:
                    # Process the uploaded file
                    df = process_excel_file(uploaded_file)
                    st.session_state.df = df
                    st.session_state.show_chat = True
                    
                    # Add to history
                    add_to_history(uploaded_file.name, datetime.now())
                    
                    # Display file name prominently
                    st.markdown(f"""
                        <div class='file-info-container'>
                            <div class='file-info'>
                                <h3 class='file-name'>📊 {uploaded_file.name}</h3>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Display data preview and statistics
                    display_data_preview(df)
                    
                    # Add success message
                    st.success("Fayl uğurla yükləndi! İndi suallarınızı soruşa bilərsiniz.")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Xəta baş verdi: {str(e)}")
                    st.session_state.show_chat = False

        # Chat interface
        if st.session_state.show_chat and st.session_state.df is not None:
            # Add a button to show/hide data preview
            if st.button("📊 Məlumatları Göstər/Gizlət"):
                if 'show_data_preview' not in st.session_state:
                    st.session_state.show_data_preview = True
                else:
                    st.session_state.show_data_preview = not st.session_state.show_data_preview
                st.rerun()
            
            # Show data preview if enabled
            if st.session_state.get('show_data_preview', False):
                display_data_preview(st.session_state.df)
            
            st.markdown("""
                <div class='chat-container'>
                    <h2 class='chat-title'>Sualınızı Yazın</h2>
                </div>
            """, unsafe_allow_html=True)
            
            # Display chat history
            chat_container = st.container()
            with chat_container:
                for message in st.session_state.chat_history:
                    if message["role"] == "user":
                        st.markdown(f"**Siz:** {message['content']}")
                    else:
                        st.markdown(f"**Bot:** {message['content']}")
            
            # Chat input
            if prompt := st.chat_input("Sualınızı yazın..."):
                # Add user message to chat history
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                
                # Display user message
                with st.chat_message("user"):
                    st.write(prompt)
                
                # Process query and get response
                with st.spinner("Sualınız emal edilir..."):
                    response = process_query(prompt, st.session_state.df)
                
                # Add assistant response to chat history
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                
                # Display assistant response
                with st.chat_message("assistant"):
                    st.write(response)
                    
                    # If response includes visualization, display it
                    if "visualization" in response:
                        try:
                            fig = create_visualization(st.session_state.df, prompt)
                            st.plotly_chart(fig, use_container_width=True)
                        except Exception as e:
                            st.error(f"Vizualizasiya yaradılarkən xəta baş verdi: {str(e)}")

if __name__ == "__main__":
    main() 