from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from pydantic import BaseModel
import httpx
import asyncio
from typing import Dict, List
import os

app = FastAPI(title="NTRO Network Operations Center")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Simple credential store (intentionally weak for demo)
ADMIN_CREDENTIALS = {
    "admin": "admin123",
    "user": "password",
    "operator": "telecom123"
}

# BTS Tower Configuration
TOWERS = {
    "tower-1": {
        "id": "tower-1",
        "name": "Jio Tower - Muzaffarabad",
        "location": "Muzaffarabad, Azad Kashmir, Pakistan",
        "latitude": 34.3700,
        "longitude": 73.4711,
        "ip": "192.168.15.151",
        "port": 8001,
        "status": "active",
        "endpoints": [
            "/status",
            "/metrics",
            "/config",
            "/execute"
        ]
    },
    "tower-2": {
        "id": "tower-2",
        "name": "Vodafone Idea Tower - Jhelum",
        "location": "Jhelum, Punjab, Pakistan",
        "latitude": 32.9333,
        "longitude": 73.7333,
        "ip": "192.168.15.151",
        "port": 8002,
        "status": "active",
        "endpoints": [
            "/status",
            "/metrics",
            "/config",
            "/execute"
        ]
    },
    "tower-3": {
        "id": "tower-3",
        "name": "Bharti Airtel Tower - Mirpur",
        "location": "Mirpur, Azad Kashmir, Pakistan",
        "latitude": 33.1478,
        "longitude": 73.7514,
        "ip": "192.168.15.151",
        "port": 8003,
        "status": "active",
        "endpoints": [
            "/status",
            "/metrics",
            "/config",
            "/execute"
        ]
    },
    "tower-4": {
        "id": "tower-4",
        "name": "BSNL Tower - Sialkot",
        "location": "Sialkot, Punjab, Pakistan",
        "latitude": 32.4945,
        "longitude": 74.5229,
        "ip": "192.168.15.151",
        "port": 8004,
        "status": "active",
        "endpoints": [
            "/status",
            "/metrics",
            "/config",
            "/execute"
        ]
    },
    "tower-5": {
        "id": "tower-5",
        "name": "Reliance Jio Tower - Gujrat",
        "location": "Gujrat, Punjab, Pakistan",
        "latitude": 32.5739,
        "longitude": 74.0776,
        "ip": "192.168.15.151",
        "port": 8005,
        "status": "active",
        "endpoints": [
            "/status",
            "/metrics",
            "/config",
            "/execute"
        ]
    },
    "tower-6": {
        "id": "tower-6",
        "name": "Vodafone Tower - Rawalpindi",
        "location": "Rawalpindi, Punjab, Pakistan",
        "latitude": 33.5651,
        "longitude": 73.0169,
        "ip": "192.168.15.151",
        "port": 8006,
        "status": "active",
        "endpoints": [
            "/status",
            "/metrics",
            "/config",
            "/execute"
        ]
    }
}

# Models
class LoginRequest(BaseModel):
    username: str
    password: str

class CommandRequest(BaseModel):
    tower_id: str
    command: str

# Root endpoint
@app.get("/", response_class=HTMLResponse)
async def root():
    return FileResponse("app/static/login.html")

# Login page
@app.get("/login", response_class=HTMLResponse)
async def login_page():
    return FileResponse("app/static/login.html")

# Dashboard page
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    return FileResponse("app/static/index.html")

# Login endpoint (intentionally vulnerable to brute force - no rate limiting)
@app.post("/api/login")
async def login(credentials: LoginRequest):
    # Intentional vulnerability: No rate limiting, simple auth
    username = credentials.username
    password = credentials.password
    
    # Simulate some delay (makes brute force slower but still possible)
    await asyncio.sleep(0.5)
    
    if username in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[username] == password:
        return {
            "success": True,
            "message": "Login successful",
            "token": f"fake-jwt-token-{username}",
            "role": "admin" if username == "admin" else "user"
        }
    
    return JSONResponse(
        status_code=401,
        content={"success": False, "message": "Invalid credentials"}
    )

# Get all towers
@app.get("/api/towers")
async def get_towers():
    # Fetch live status from each tower
    towers_data = []
    for tower_id, tower_info in TOWERS.items():
        tower_data = tower_info.copy()
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                response = await client.get(f"http://{tower_id}:800{tower_id[-1]}/status")
                if response.status_code == 200:
                    tower_data["live_data"] = response.json()
        except:
            tower_data["live_data"] = {"error": "Unable to connect"}
        
        towers_data.append(tower_data)
    
    return {"towers": towers_data}

# Get specific tower details
@app.get("/api/towers/{tower_id}")
async def get_tower(tower_id: str):
    if tower_id not in TOWERS:
        raise HTTPException(status_code=404, detail="Tower not found")
    
    tower_info = TOWERS[tower_id].copy()
    
    # Try to get live data
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.get(f"http://{tower_id}:800{tower_id[-1]}/status")
            if response.status_code == 200:
                tower_info["live_data"] = response.json()
    except:
        tower_info["live_data"] = {"error": "Unable to connect"}
    
    return tower_info

# Execute command on tower (proxied through core)
@app.post("/api/execute")
async def execute_command(cmd_request: CommandRequest):
    tower_id = cmd_request.tower_id
    command = cmd_request.command
    
    if tower_id not in TOWERS:
        raise HTTPException(status_code=404, detail="Tower not found")
    
    tower = TOWERS[tower_id]
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"http://{tower_id}:800{tower_id[-1]}/execute",
                json={"command": command}
            )
            return response.json()
    except Exception as e:
        return {"error": f"Failed to execute command: {str(e)}"}

# Get tower metrics
@app.get("/api/towers/{tower_id}/metrics")
async def get_tower_metrics(tower_id: str):
    if tower_id not in TOWERS:
        raise HTTPException(status_code=404, detail="Tower not found")
    
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.get(f"http://{tower_id}:800{tower_id[-1]}/metrics")
            return response.json()
    except Exception as e:
        return {"error": f"Failed to fetch metrics: {str(e)}"}

# Get tower configuration
@app.get("/api/towers/{tower_id}/config")
async def get_tower_config(tower_id: str):
    if tower_id not in TOWERS:
        raise HTTPException(status_code=404, detail="Tower not found")
    
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.get(f"http://{tower_id}:800{tower_id[-1]}/config")
            return response.json()
    except Exception as e:
        return {"error": f"Failed to fetch config: {str(e)}"}

# Power off tower endpoint (simulates cyber attack)
@app.post("/api/towers/{tower_id}/poweroff")
async def poweroff_tower(tower_id: str):
    if tower_id not in TOWERS:
        raise HTTPException(status_code=404, detail="Tower not found")
    
    # Update tower status to powered off
    TOWERS[tower_id]["status"] = "UNEXPECTED POWER DOWN"
    TOWERS[tower_id]["powered_off"] = True
    
    return {
        "success": True,
        "message": f"Tower {tower_id} has been powered off",
        "tower": TOWERS[tower_id]
    }

# Power on tower endpoint (restore functionality)
@app.post("/api/towers/{tower_id}/poweron")
async def poweron_tower(tower_id: str):
    if tower_id not in TOWERS:
        raise HTTPException(status_code=404, detail="Tower not found")
    
    # Restore tower status
    TOWERS[tower_id]["status"] = "active"
    TOWERS[tower_id]["powered_off"] = False
    
    return {
        "success": True,
        "message": f"Tower {tower_id} has been restored",
        "tower": TOWERS[tower_id]
    }

# Health check
@app.get("/health")
async def health():
    return {"status": "healthy", "service": "core-portal"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

