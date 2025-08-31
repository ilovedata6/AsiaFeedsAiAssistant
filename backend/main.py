from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
from .models import GenerateRequest, GenerateResponse
from .services import ModelSelector
from .ollama_client import OllamaService
from config import FRONTEND_HOST, FRONTEND_PORT, API_HOST, API_PORT

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Assistant API",
    description="A minimal AI assistant backend using Ollama",
    version="1.0.0"
)

# Add CORS middleware to allow Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        f"http://{FRONTEND_HOST}:{FRONTEND_PORT}",
        f"http://127.0.0.1:{FRONTEND_PORT}",
        f"http://localhost:{FRONTEND_PORT}",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
ollama_service = OllamaService()
model_selector = ModelSelector()


@app.get("/")
async def root():
    """Root endpoint with basic info."""
    return {
        "message": "AI Assistant API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest):
    """
    Generate AI response based on user prompt.
    
    Args:
        request: Generate request containing model, prompt, and thinking flag
        
    Returns:
        Generated response from AI model
        
    Raises:
        HTTPException: If generation fails
    """
    try:
        # Select appropriate model
        selected_model = model_selector.select_model(
            thinking=request.thinking,
            requested_model=request.model
        )
        
        logger.info(f"Generating response with model: {selected_model}")
        logger.info(f"Prompt: {request.prompt[:100]}...")
        
        # Generate response
        response_text = await ollama_service.generate_response(
            prompt=request.prompt,
            model=selected_model
        )
        
        logger.info(f"Generated response length: {len(response_text)}")
        
        return GenerateResponse(response=response_text)
        
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate response: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT)
