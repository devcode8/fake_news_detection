# 📰 Fake News Verification System

A comprehensive AI-powered fake news detection system built using Fetch.ai agents, Tavily search API, and ASI:One language model. This system analyzes news headlines and articles to determine their authenticity through web search verification and AI analysis.

## 🚀 Features

- **Real-time News Analysis**: Submit news headlines for instant verification
- **AI-Powered Verification**: Uses ASI:One mini model for intelligent fact-checking
- **Web Search Integration**: Leverages Tavily API for comprehensive web searches
- **Interactive Frontend**: Clean Streamlit interface for easy interaction
- **Agent-Based Architecture**: Built on Fetch.ai's uAgents framework
- **REST API**: HTTP endpoints for programmatic access

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │───▶│   News Agent    │───▶│   Tavily API    │───▶│   ASI:One API   │
│   Frontend      │    │  (Fetch.ai)     │    │  (Web Search)   │    │  (AI Analysis)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Workflow

1. **User Input**: Submit news headline through Streamlit interface
2. **Agent Processing**: Fetch.ai agent receives the request via REST API
3. **Web Search**: Tavily API searches for relevant information about the headline
4. **AI Analysis**: ASI:One model analyzes search results against the headline
5. **Result Display**: Verification result (Valid/Fake) with detailed reasoning

## 📋 Prerequisites

- Python 3.8+
- Tavily API key
- ASI:One API key
- Internet connection for API calls

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fakenews
   ```

2. **Install dependencies**
   ```bash
   pip install uagents streamlit httpx python-dotenv requests
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   TAVILY_API_KEY=your_tavily_api_key_here
   ASI_ONE_API_KEY=your_asi_one_api_key_here
   ```

## 🚀 Usage

### Starting the System

1. **Start the News Agent**
   ```bash
   python3 agent.py
   ```
   The agent will start on `http://localhost:8080`

2. **Launch the Streamlit Frontend**
   ```bash
   streamlit run streamlit_app.py
   ```
   The interface will be available at `http://localhost:8501`

### Using the Interface

1. **Submit News**: Enter a news headline in the text area
2. **Analyze**: Click "Analyze News" to start verification
3. **View Results**: See the analysis result with validity status and detailed reasoning

### API Endpoints

- `GET /`: Health check endpoint
- `POST /news`: Submit news for analysis
  ```json
  {
    "query": "Your news headline here"
  }
  ```

## 🔧 Configuration

### Agent Configuration

The news agent is configured in `agent.py`:
- **Port**: 8080 (default)
- **Endpoint**: `/submit`
- **Timeout**: 30 seconds for API calls

### API Settings

- **Tavily Search**: Advanced search with 5 max results
- **ASI:One Model**: asi1-mini with temperature 0 for consistent results

## 📊 Analysis Criteria

The system evaluates news based on:

1. **Authenticity**: Verification against trusted sources
2. **Date Detection**: When the reported event occurred
3. **Location Verification**: Geographic accuracy of claims
4. **Misinformation Check**: Detection of fabricated events

### Output Format

```
1. The headline "[headline]" is Valid/Fake
2. Brief report explaining validation reasoning
3. Summary of incident (if valid) with actual date
```

## 🔍 Example Analysis

**Input**: "Major earthquake hits Tokyo today"

**Process**:
1. Tavily searches for recent Tokyo earthquake reports
2. ASI:One analyzes search results against the headline
3. Returns validity status with supporting evidence

**Output**:
```
The headline "Major earthquake hits Tokyo today" is Fake.

No credible sources report a major earthquake in Tokyo today. 
Recent seismic activity data shows only minor tremors with 
no significant earthquake events matching the headline's claims.
```

## 🔐 Security

- API keys are stored in `.env` file (not tracked in git)
- Input validation for news queries
- Timeout protection for API calls
- Error handling for failed requests

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

1. **Port 8080 already in use**
   ```bash
   lsof -ti:8080 | xargs kill
   ```

2. **API Connection Errors**
   - Verify API keys in `.env` file
   - Check internet connectivity
   - Ensure agent is running on port 8080

3. **Module Import Errors**
   ```bash
   pip install --upgrade uagents streamlit httpx python-dotenv
   ```

### Error Messages

- `"No response received from Tavily API"`: Check Tavily API key and connectivity
- `"No response received from ASI:One API"`: Verify ASI:One API key
- `"Address already in use"`: Kill existing process on port 8080

## 📞 Support

For issues and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Verify all dependencies are installed correctly

## 🔗 External APIs

- **Fetch.ai**: Agent framework and infrastructure
- **Tavily**: Web search and content retrieval
- **ASI:One**: AI language model for analysis

---

**Built with ❤️ using Fetch.ai agents and modern AI technologies**