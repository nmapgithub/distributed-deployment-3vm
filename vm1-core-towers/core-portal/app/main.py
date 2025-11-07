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
DEFAULT_ENDPOINTS = ["/status", "/metrics", "/config", "/execute"]

TOWER_DEFINITIONS = [
    {
        "id": "tower-1",
        "name": "Jio Tower - Muzaffarabad",
        "location": "Muzaffarabad, Azad Kashmir, Pakistan",
        "latitude": 34.3700,
        "longitude": 73.4711,
        "ip": "192.168.15.151",
        "port": 8001,
        "status": "active"
    },
    {
        "id": "tower-2",
        "name": "Vodafone Idea Tower - Jhelum",
        "location": "Jhelum, Punjab, Pakistan",
        "latitude": 32.9333,
        "longitude": 73.7333,
        "ip": "192.168.15.152",
        "port": 8002,
        "status": "active"
    },
    {
        "id": "tower-3",
        "name": "Bharti Airtel Tower - Mirpur",
        "location": "Mirpur, Azad Kashmir, Pakistan",
        "latitude": 33.1478,
        "longitude": 73.7514,
        "ip": "192.168.15.153",
        "port": 8003,
        "status": "active"
    },
    {
        "id": "tower-4",
        "name": "BSNL Tower - Sialkot",
        "location": "Sialkot, Punjab, Pakistan",
        "latitude": 32.4945,
        "longitude": 74.5229,
        "ip": "192.168.15.154",
        "port": 8004,
        "status": "active"
    },
    {
        "id": "tower-5",
        "name": "Reliance Jio Tower - Gujrat",
        "location": "Gujrat, Punjab, Pakistan",
        "latitude": 32.5739,
        "longitude": 74.0776,
        "ip": "192.168.15.155",
        "port": 8005,
        "status": "active"
    },
    {
        "id": "tower-6",
        "name": "Vodafone Tower - Rawalpindi",
        "location": "Rawalpindi, Punjab, Pakistan",
        "latitude": 33.5651,
        "longitude": 73.0169,
        "ip": "192.168.15.156",
        "port": 8006,
        "status": "active"
    },
    {
        "id": "tower-7",
        "name": "Zong Tower - Islamabad",
        "location": "Islamabad Capital Territory, Pakistan",
        "latitude": 33.6844,
        "longitude": 73.0479,
        "ip": "192.168.15.157",
        "port": 8007,
        "status": "active"
    },
    {
        "id": "tower-8",
        "name": "Jazz Tower - Lahore",
        "location": "Lahore, Punjab, Pakistan",
        "latitude": 31.5204,
        "longitude": 74.3587,
        "ip": "192.168.15.158",
        "port": 8008,
        "status": "active"
    },
    {
        "id": "tower-9",
        "name": "Telenor Tower - Peshawar",
        "location": "Peshawar, Khyber Pakhtunkhwa, Pakistan",
        "latitude": 34.0151,
        "longitude": 71.5249,
        "ip": "192.168.15.159",
        "port": 8009,
        "status": "active"
    },
    {
        "id": "tower-10",
        "name": "Warid Tower - Faisalabad",
        "location": "Faisalabad, Punjab, Pakistan",
        "latitude": 31.4180,
        "longitude": 73.0790,
        "ip": "192.168.15.160",
        "port": 8010,
        "status": "active"
    },
    {
        "id": "tower-11",
        "name": "Ufone Tower - Multan",
        "location": "Multan, Punjab, Pakistan",
        "latitude": 30.1575,
        "longitude": 71.5249,
        "ip": "192.168.15.161",
        "port": 8011,
        "status": "active"
    },
    {
        "id": "tower-12",
        "name": "SCO Tower - Quetta",
        "location": "Quetta, Balochistan, Pakistan",
        "latitude": 30.1798,
        "longitude": 66.9750,
        "ip": "192.168.15.162",
        "port": 8012,
        "status": "active"
    },
    {
        "id": "tower-13",
        "name": "PTCL Tower - Karachi",
        "location": "Karachi, Sindh, Pakistan",
        "latitude": 24.8607,
        "longitude": 67.0011,
        "ip": "192.168.15.163",
        "port": 8013,
        "status": "active"
    },
    {
        "id": "tower-14",
        "name": "Zong Tower - Hyderabad",
        "location": "Hyderabad, Sindh, Pakistan",
        "latitude": 25.3960,
        "longitude": 68.3578,
        "ip": "192.168.15.164",
        "port": 8014,
        "status": "active"
    },
    {
        "id": "tower-15",
        "name": "Jazz Tower - Sukkur",
        "location": "Sukkur, Sindh, Pakistan",
        "latitude": 27.7052,
        "longitude": 68.8574,
        "ip": "192.168.15.165",
        "port": 8015,
        "status": "active"
    },
    {
        "id": "tower-16",
        "name": "Ufone Tower - Bahawalpur",
        "location": "Bahawalpur, Punjab, Pakistan",
        "latitude": 29.3544,
        "longitude": 71.6911,
        "ip": "192.168.15.166",
        "port": 8016,
        "status": "maintenance"
    },
    {
        "id": "tower-17",
        "name": "Telenor Tower - Abbottabad",
        "location": "Abbottabad, Khyber Pakhtunkhwa, Pakistan",
        "latitude": 34.1463,
        "longitude": 73.2114,
        "ip": "192.168.15.167",
        "port": 8017,
        "status": "active"
    },
    {
        "id": "tower-18",
        "name": "SCO Tower - Gilgit",
        "location": "Gilgit, Gilgit-Baltistan, Pakistan",
        "latitude": 35.9208,
        "longitude": 74.3089,
        "ip": "192.168.15.168",
        "port": 8018,
        "status": "active"
    },
    {
        "id": "tower-19",
        "name": "SCO Tower - Skardu",
        "location": "Skardu, Gilgit-Baltistan, Pakistan",
        "latitude": 35.3359,
        "longitude": 75.6333,
        "ip": "192.168.15.169",
        "port": 8019,
        "status": "active"
    },
    {
        "id": "tower-20",
        "name": "PTCL Tower - Gwadar",
        "location": "Gwadar, Balochistan, Pakistan",
        "latitude": 25.1276,
        "longitude": 62.3220,
        "ip": "192.168.15.170",
        "port": 8020,
        "status": "active"
    }
]

TOWERS = {
    tower["id"]: {
        **tower,
        "service_host": tower.get("service_host", tower["id"]),
        "service_port": tower.get("service_port", tower["port"]),
        "endpoints": list(tower.get("endpoints", DEFAULT_ENDPOINTS))
    }
    for tower in TOWER_DEFINITIONS
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
                response = await client.get(
                    f"http://{tower_info['service_host']}:{tower_info['service_port']}/status"
                )
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
            response = await client.get(
                f"http://{tower_info['service_host']}:{tower_info['service_port']}/status"
            )
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
                f"http://{tower['service_host']}:{tower['service_port']}/execute",
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
            response = await client.get(
                f"http://{tower['service_host']}:{tower['service_port']}/metrics"
            )
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
            response = await client.get(
                f"http://{tower['service_host']}:{tower['service_port']}/config"
            )
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

