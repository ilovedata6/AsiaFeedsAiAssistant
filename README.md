# AI Assistant - Minimal Backend + UI

A minimal AI assistant built with FastAPI backend and Streamlit frontend, using Ollama for AI model inference.

## Features

- **FastAPI Backend**: RESTful API with automatic documentation
- **Streamlit Frontend**: Clean, interactive user interface
- **Ollama Integration**: Local AI model inference
- **Model Selection**: Choose between Llama3.2:3b (normal) and Qwen3:4b (thinking mode)
- **Real-time Generation**: Streaming responses from AI models

## Project Structure

```
AI Assistant/
├── backend/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── models.py        # Pydantic models
│   ├── services.py      # Business logic services
│   └── ollama_client.py # Ollama API client
├── frontend/
│   ├── __init__.py
│   ├── app.py           # Streamlit application
│   ├── api_client.py    # FastAPI client
│   └── ui_components.py # UI components
├── run_backend.py       # Backend runner
├── run_frontend.py      # Frontend runner
├── requirements.txt     # Dependencies
└── README.md           # This file
```

## Setup & Installation

### Prerequisites

1. **Python 3.8+** installed
2. **Ollama** installed and running locally
3. Required models downloaded in Ollama:
   ```bash
   ollama pull llama3.2:3b
   ollama pull qwen3:4b
   ```

### Installation

1. **Clone/Navigate to the project directory**
2. **Create and activate virtual environment** (if not already done):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Start Ollama (if not already running)
```bash
ollama serve
```

### Start the Backend (Terminal 1)
```bash
python run_backend.py
```
Or use the batch file:
```bash
start_backend.bat
```
- Backend will run on http://localhost:8000
- API documentation available at http://localhost:8000/docs

### Start the Frontend (Terminal 2)
```bash
streamlit run run_frontend.py
```
Or use the batch file:
```bash
start_frontend.bat
```
- Frontend will run on http://localhost:8501

## API Usage

### Generate Endpoint

**POST** `/generate`

```json
{
  "model": "llama3.2:3b",  // or "qwen3:4b"
  "prompt": "Your question here",
  "thinking": false  // true for qwen3:4b, false for llama3.2:3b
}
```

**Response:**
```json
{
  "response": "AI generated response"
}
```

### Model Selection Logic

- `thinking: true` → Always uses `qwen3:4b`
- `thinking: false` → Uses specified model or defaults to `llama3.2:3b`

## Architecture

### Backend (FastAPI)
- **SOLID Principles**: Separation of concerns with services, models, and clients
- **DRY Principle**: Reusable components and utilities
- **Error Handling**: Comprehensive error handling and logging
- **CORS Enabled**: Allows frontend connection

### Frontend (Streamlit)
- **Component-based UI**: Modular UI components
- **Session Management**: Chat history and state management
- **Real-time Status**: Backend connection monitoring
- **Responsive Design**: Clean, centered layout

## Development

### Code Organization
- **Models**: Pydantic models for request/response validation
- **Services**: Business logic and model selection
- **Clients**: External API integrations (Ollama)
- **UI Components**: Reusable Streamlit components

### Key Features
- **Health Checks**: Monitor backend availability
- **Error Handling**: Graceful error management
- **Logging**: Comprehensive application logging
- **Validation**: Input validation and sanitization

## Troubleshooting

### Common Issues

1. **Backend connection failed**
   - Ensure FastAPI server is running on port 8000
   - Check if port is available

2. **Ollama connection failed**
   - Verify Ollama is running: `ollama serve`
   - Check if models are downloaded: `ollama list`

3. **Model not found**
   - Download required models:
     ```bash
     ollama pull llama3.2:3b
     ollama pull qwen3:4b
     ```

4. **Port conflicts**
   - Backend: Change port in `run_backend.py`
   - Frontend: Use `--server.port` flag with streamlit

## License

This project is for educational and development purposes.
