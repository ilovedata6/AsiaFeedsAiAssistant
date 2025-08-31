from backend.main import app
from config import API_HOST, API_PORT

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT)
