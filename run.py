"""
Development server runner.
Run this file to start the FastAPI development server.
"""
import asyncio
import sys
import uvicorn

# Fix for Windows: psycopg requires SelectorEventLoop instead of ProactorEventLoop
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
        loop="asyncio"
    )
