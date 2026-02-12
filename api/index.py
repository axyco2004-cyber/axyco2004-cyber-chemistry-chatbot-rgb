import sys
import os

# Add parent directory to path to import main
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

# Vercel serverless function handler
def handler(request, context):
    return app(request.environ, context)

# Also export app directly for WSGI
application = app
