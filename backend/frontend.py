from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os

# Create a router for frontend routes
frontend_router = APIRouter()

def get_html_content(filename):
    """Helper function to read HTML file content"""
    # Look for HTML files in the frontend directory
    # Get the absolute path to the frontend directory
    frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
    filepath = os.path.join(frontend_dir, filename)
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            return HTMLResponse(content=file.read(), status_code=200)
    return HTMLResponse(content="<h1>Page not found</h1>", status_code=404)

# Serve the main client page
@frontend_router.get("/", response_class=HTMLResponse)
async def read_root():
    return get_html_content("client.html")

# Serve the login page
@frontend_router.get("/login", response_class=HTMLResponse)
async def read_login():
    return get_html_content("login.html")

# Serve the register page
@frontend_router.get("/register", response_class=HTMLResponse)
async def read_register():
    return get_html_content("register.html")

# Serve the client page at /client route as well
@frontend_router.get("/client", response_class=HTMLResponse)
async def read_client():
    return get_html_content("client.html")

# Handle direct file access for backward compatibility
@frontend_router.get("/login.html", response_class=HTMLResponse)
async def read_login_html():
    return get_html_content("login.html")

@frontend_router.get("/register.html", response_class=HTMLResponse)
async def read_register_html():
    return get_html_content("register.html")

@frontend_router.get("/client.html", response_class=HTMLResponse)
async def read_client_html():
    return get_html_content("client.html")

# Handle client-side routing for SPA navigation
# Removed /todos route to avoid conflict with API endpoint
@frontend_router.get("/dashboard", response_class=HTMLResponse)
async def read_client_routes():
    """Serve the main client app for client-side routes"""
    return get_html_content("client.html")