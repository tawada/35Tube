"""FastAPI app entry point."""
from app import app
from fastapi_pagination import add_pagination

add_pagination(app)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)
