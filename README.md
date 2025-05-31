# Azerbaijani Excel Summarization Chatbot

A Streamlit-based web application that helps users analyze and summarize Excel files in Azerbaijani language.

## Features

- Upload and process Excel files
- Natural language processing in Azerbaijani
- Interactive data visualization
- Chatbot interface for data queries
- Summary generation and insights extraction

## Project Structure

```
├── app.py                 # Main Streamlit application
├── requirements.txt       # Project dependencies
├── config/
│   ├── __init__.py
│   └── settings.py       # Configuration settings
├── utils/
│   ├── __init__.py
│   ├── excel_processor.py # Excel file processing utilities
│   ├── nlp_utils.py      # Natural language processing utilities
│   └── visualization.py  # Data visualization utilities
├── resources/
│   ├── __init__.py
│   └── az_language.py    # Azerbaijani language resources
└── tests/
    ├── __init__.py
    └── test_utils.py     # Unit tests
```

## Setup and Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage

1. Launch the application using the command above
2. Upload your Excel file through the web interface
3. Use the chatbot to ask questions about your data
4. View generated summaries and visualizations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 