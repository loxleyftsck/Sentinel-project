"""
Simplified FastAPI test - No heavy dependencies
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from datetime import datetime

app = FastAPI(title="SENTINEL API Test")

@app.get("/")
async def root():
    return {
        "service": "SENTINEL API",
        "version": "1.0.0",
        "status": "operational",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/test")
async def test_endpoint(request: Request):
    """Simple test endpoint"""
    body = await request.json()
    return {
        "received": body,
        "status": "success",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print("🚀 SENTINEL API - Simple Test Server")
    print("=" * 60)
    print("Starting server at http://localhost:8000")
    print("Docs at http://localhost:8000/docs")
    print("=" * 60)

    uvicorn.run(app, host="0.0.0.0", port=8000)
