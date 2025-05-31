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
    initial_sidebar_state="collapsed"  # Start with collapsed sidebar
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
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
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
        display: none;
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
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #e0e0e0;
    }
    
    .clear-history-btn {
        font-size: 0.8em;
        padding: 5px 10px;
        background-color: #ff4444;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .clear-history-btn:hover {
        background-color: #cc0000;
    }
    
    /* Style the sidebar toggle button */
    [data-testid="collapsedControl"] {
        background-color: #1E88E5 !important;
        color: white !important;
        border-radius: 0 4px 4px 0 !important;
        padding: 10px !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="collapsedControl"]:hover {
        background-color: #1565C0 !important;
        padding-right: 15px !important;
    }
    
    /* Adjust main content padding when sidebar is expanded */
    .main .block-container {
        padding-left: 1rem;
        transition: padding-left 0.3s ease;
    }
    
    /* Hide the default Streamlit sidebar header */
    .css-1d391kg {
        display: none;
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
    st.session_state.sidebar_expanded = False

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
        'chat_history': []
    }
    st.session_state.upload_history.append(history_item)
    st.session_state.selected_history = history_item

def load_history_item(history_item):
    """Load a history item and its associated data."""
    st.session_state.selected_history = history_item
    st.session_state.chat_history = history_item['chat_history']
    # Here you would also need to load the associated data
    # This would require storing the data or file path in the history item

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
    # Sidebar header
    st.markdown("""
        <div class="sidebar-header">
            <h3>📚 Tarixçə</h3>
            <button class="clear-history-btn" onclick="document.querySelector('[data-testid=stButton][key=clear_history]').click()">Təmizlə</button>
        </div>
    """, unsafe_allow_html=True)
    
    # Show history items
    if st.session_state.upload_history:
        for item in st.session_state.upload_history:
            is_active = st.session_state.selected_history == item
            active_class = "active" if is_active else ""
            
            st.markdown(f"""
                <div class="sidebar-history-item {active_class}" onclick="document.querySelector('[data-testid=stButton][key=select_{item['file_name']}']').click()">
                    <div><strong>{item['file_name']}</strong></div>
                    <div class="sidebar-history-timestamp">{item['timestamp'].strftime('%Y-%m-%d %H:%M')}</div>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("Seç", key=f"select_{item['file_name']}", use_container_width=True):
                load_history_item(item)
    else:
        st.info("Hələ heç bir fayl yüklənməyib")
    
    # Hidden clear history button
    if st.button("Tarixçəni Təmizlə", key="clear_history", use_container_width=True):
        st.session_state.upload_history = []
        st.session_state.selected_history = None
        st.session_state.chat_history = []
        st.session_state.current_data = None
        st.session_state.show_chat = False
        st.rerun()

def main():
    # Create sidebar content
    with st.sidebar:
        create_sidebar_content()
    
    # Main content
    st.title(settings["app"]["name"])
    
    # Main content area
    if not st.session_state.show_chat:
        # Show upload area when no file is uploaded
        uploaded_file = create_upload_area()
        
        if uploaded_file is not None:
            if validate_excel_file(uploaded_file):
                with st.spinner("Fayl emal edilir..."):
                    try:
                        df = process_excel_file(uploaded_file)
                        if df is not None:
                            st.session_state.current_data = df
                            st.session_state.show_chat = True
                            # Add to history
                            add_to_history(uploaded_file.name, datetime.now())
                            st.success("Fayl uğurla yükləndi!")
                            st.rerun()
                    except Exception as e:
                        st.error(f"Xəta baş verdi: {str(e)}")
            else:
                st.error("Zəhmət olmasa yalnız Excel fayllarını (.xlsx və ya .xls) yükləyin.")
    else:
        # Show chat interface when a file is uploaded
        st.markdown("### 💬 Söhbət")
        
        # Add a button to upload a new file
        if st.button("Yeni Fayl Yüklə"):
            st.session_state.show_chat = False
            st.session_state.chat_history = []
            st.session_state.current_data = None
            st.rerun()
        
        # Display chat history
        chat_container = st.container()
        with chat_container:
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            for message in st.session_state.chat_history:
                if message["role"] == "user":
                    st.markdown(f"**Siz:** {message['content']}")
                else:
                    st.markdown(f"**Bot:** {message['content']}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Chat input
        if prompt := st.chat_input("Sualınızı yazın..."):
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.write(prompt)
            
            # Process query and get response
            with st.spinner("Sualınız emal edilir..."):
                response = process_query(prompt, st.session_state.current_data)
            
            # Add assistant response to chat history
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            
            # Display assistant response
            with st.chat_message("assistant"):
                st.write(response)
                
                # If response includes visualization, display it
                if "visualization" in response:
                    try:
                        fig = create_visualization(st.session_state.current_data, prompt)
                        st.plotly_chart(fig, use_container_width=True)
                    except Exception as e:
                        st.error(f"Vizualizasiya yaradılarkən xəta baş verdi: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main() 