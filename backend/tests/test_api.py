import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Set dummy environment variables to avoid pydantic ValidationError
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["YOUTUBE_API_KEY"] = "dummy"
os.environ["PROJECT_ID"] = "dummy"
os.environ["LOCATION"] = "dummy"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "dummy.json"

import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)
