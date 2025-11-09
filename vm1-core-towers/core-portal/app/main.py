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
        "name": "Jio Tower - Jammu",
        "location": "Jammu, Jammu and Kashmir, India",
        "latitude": 32.7266,
        "longitude": 74.8570,
        "ip": "192.168.15.151",
        "port": 35111,
        "status": "active"
    },
    {
        "id": "tower-2",
        "name": "Vodafone Idea Tower - Kathua",
        "location": "Kathua, Jammu and Kashmir, India",
        "latitude": 32.3703,
        "longitude": 75.5180,
        "ip": "192.168.15.152",
        "port": 35221,
        "status": "active"
    },
    {
        "id": "tower-3",
        "name": "Bharti Airtel Tower - Pathankot",
        "location": "Pathankot, Punjab, India",
        "latitude": 32.2730,
        "longitude": 75.6520,
        "ip": "192.168.15.153",
        "port": 35331,
        "status": "active"
    },
    {
        "id": "tower-4",
        "name": "BSNL Tower - Amritsar",
        "location": "Amritsar, Punjab, India",
        "latitude": 31.6340,
        "longitude": 74.8723,
        "ip": "192.168.15.154",
        "port": 35441,
        "status": "active"
    },
    {
        "id": "tower-5",
        "name": "Reliance Jio Tower - Gurdaspur",
        "location": "Gurdaspur, Punjab, India",
        "latitude": 32.0416,
        "longitude": 75.4051,
        "ip": "192.168.15.155",
        "port": 35551,
        "status": "active"
    },
    {
        "id": "tower-6",
        "name": "Vodafone Tower - Firozpur",
        "location": "Firozpur, Punjab, India",
        "latitude": 30.9335,
        "longitude": 74.6225,
        "ip": "192.168.15.156",
        "port": 35661,
        "status": "active"
    },
    {
        "id": "tower-7",
        "name": "Airtel Tower - Fazilka",
        "location": "Fazilka, Punjab, India",
        "latitude": 30.4020,
        "longitude": 74.0280,
        "ip": "192.168.15.157",
        "port": 35771,
        "status": "active"
    },
    {
        "id": "tower-8",
        "name": "Jio Tower - Sri Ganganagar",
        "location": "Sri Ganganagar, Rajasthan, India",
        "latitude": 29.9030,
        "longitude": 73.8772,
        "ip": "192.168.15.158",
        "port": 35881,
        "status": "active"
    },
    {
        "id": "tower-9",
        "name": "Telenor Tower - Hanumangarh",
        "location": "Hanumangarh, Rajasthan, India",
        "latitude": 29.5812,
        "longitude": 74.3294,
        "ip": "192.168.15.159",
        "port": 35991,
        "status": "active"
    },
    {
        "id": "tower-10",
        "name": "Vi Tower - Abohar",
        "location": "Abohar, Punjab, India",
        "latitude": 30.1445,
        "longitude": 74.1999,
        "ip": "192.168.15.160",
        "port": 36101,
        "status": "active"
    },
    {
        "id": "tower-11",
        "name": "Airtel Tower - Bikaner",
        "location": "Bikaner, Rajasthan, India",
        "latitude": 28.0229,
        "longitude": 73.3119,
        "ip": "192.168.15.161",
        "port": 36211,
        "status": "active"
    },
    {
        "id": "tower-12",
        "name": "Jio Tower - Jaisalmer",
        "location": "Jaisalmer, Rajasthan, India",
        "latitude": 26.9157,
        "longitude": 70.9083,
        "ip": "192.168.15.162",
        "port": 36321,
        "status": "active"
    },
    {
        "id": "tower-13",
        "name": "BSNL Tower - Barmer",
        "location": "Barmer, Rajasthan, India",
        "latitude": 25.7560,
        "longitude": 71.3922,
        "ip": "192.168.15.163",
        "port": 36431,
        "status": "active"
    },
    {
        "id": "tower-14",
        "name": "Vi Tower - Bhuj",
        "location": "Bhuj, Gujarat, India",
        "latitude": 23.2410,
        "longitude": 69.6669,
        "ip": "192.168.15.164",
        "port": 36541,
        "status": "active"
    },
    {
        "id": "tower-15",
        "name": "Jio Tower - Gandhidham",
        "location": "Gandhidham, Gujarat, India",
        "latitude": 23.0753,
        "longitude": 70.1337,
        "ip": "192.168.15.165",
        "port": 36651,
        "status": "active"
    },
    {
        "id": "tower-16",
        "name": "Airtel Tower - Naliya",
        "location": "Naliya, Kutch, Gujarat, India",
        "latitude": 23.2600,
        "longitude": 68.8260,
        "ip": "192.168.15.166",
        "port": 36761,
        "status": "maintenance"
    },
    {
        "id": "tower-17",
        "name": "BSNL Tower - Poonch",
        "location": "Poonch, Jammu and Kashmir, India",
        "latitude": 33.7700,
        "longitude": 74.0920,
        "ip": "192.168.15.167",
        "port": 36871,
        "status": "active"
    },
    {
        "id": "tower-18",
        "name": "Airtel Tower - Kupwara",
        "location": "Kupwara, Jammu and Kashmir, India",
        "latitude": 34.5311,
        "longitude": 74.2686,
        "ip": "192.168.15.168",
        "port": 36981,
        "status": "active"
    },
    {
        "id": "tower-19",
        "name": "BSNL Tower - Kargil",
        "location": "Kargil, Ladakh, India",
        "latitude": 34.5590,
        "longitude": 76.1250,
        "ip": "192.168.15.169",
        "port": 37091,
        "status": "active"
    },
    {
        "id": "tower-20",
        "name": "Jio Tower - Turtuk",
        "location": "Turtuk, Ladakh, India",
        "latitude": 34.8470,
        "longitude": 76.8324,
        "ip": "192.168.15.170",
        "port": 37101,
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
    uvicorn.run(app, host="0.0.0.0", port=44880)

