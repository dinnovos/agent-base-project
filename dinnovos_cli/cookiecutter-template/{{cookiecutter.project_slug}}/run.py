"""
Development server runner.
Run this file to start the FastAPI development server.
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port={{cookiecutter.port}},
        reload=True,
        log_level="info"
    )
