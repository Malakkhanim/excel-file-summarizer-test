# Azerbaijani Excel Summarization Chatbot

A Streamlit-based web application that helps users analyze and summarize Excel files in Azerbaijani language.

## Features
- Upload and process Excel files
- Natural language processing in Azerbaijani
- Interactive data visualization
- Chatbot interface for data queries
- Summary generation and insights extraction
- Data cleaning and formatting
- Interactive dashboard with multiple chart types
- Statistical analysis and insights
- Data distribution analysis
- Relationship analysis between metrics

## Project Structure
```
├── app.py                 # Main Streamlit application
├── requirements.txt       # Project dependencies
├── .env                  # Environment variables (create this file)
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

1. Clone the repository:
```bash
git clone https://github.com/yourusername/excel-data-analysis-bot.git
cd excel-data-analysis-bot
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your API key:
```bash
# Create .env file
touch .env  # On Windows: type nul > .env

# Add the following line to .env file (replace with your actual API key)
OPENAI_API_KEY=your_api_key_here
```

5. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Launch the application using the command above
2. Upload your Excel file through the web interface
3. Use the chatbot to ask questions about your data
4. View generated summaries and visualizations
5. Access different views:
   - General Overview: View basic statistics and data characteristics
   - Visualizations: Explore interactive charts and graphs
   - Clean Data: Clean and download processed data

## Requirements

- Python 3.8+
- Streamlit
- Pandas
- Plotly
- NumPy
- OpenAI API key
- Other required packages are listed in `requirements.txt`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For questions and suggestions about the project:
- Email: your.email@example.com
- GitHub Issues: [Create an issue](https://github.com/yourusername/excel-data-analysis-bot/issues) 