from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
import subprocess
import shlex
from datetime import datetime

app = FastAPI(title="BTS Tower 1 - Muzaffarabad")

# Tower Configuration
TOWER_CONFIG = {
    "tower_id": "tower-1",
    "name": "Jio Tower - Muzaffarabad",
    "location": "Muzaffarabad, Azad Kashmir, Pakistan",
    "frequency": "2100 MHz",
    "coverage": "15 km radius",
    "technology": "4G LTE",
    "installed_date": "2020-05-15",
    "serial_number": "ABC-JMU-001"
}

class CommandRequest(BaseModel):
    command: str

@app.get("/")
async def root():
    return {
        "tower": TOWER_CONFIG["name"],
        "status": "operational",
        "message": "BTS Tower API - Authorized access only"
    }

@app.get("/status")
async def get_status():
    """Get current tower status"""
    return {
        "tower_id": TOWER_CONFIG["tower_id"],
        "name": TOWER_CONFIG["name"],
        "status": "active",
        "timestamp": datetime.now().isoformat(),
        "operational": True
    }

@app.get("/metrics")
async def get_metrics():
    """Get tower performance metrics"""
    return {
        "tower_id": TOWER_CONFIG["tower_id"],
        "connections": random.randint(150, 300),
        "signal_strength": random.randint(85, 98),
        "data_transfer": round(random.uniform(500, 1500), 2),
        "uptime": random.randint(720, 8760),
        "temperature": random.randint(25, 45),
        "power_consumption": round(random.uniform(2.5, 4.2), 2),
        "error_rate": round(random.uniform(0.01, 0.5), 2),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/config")
async def get_config():
    """Get tower configuration - SECURITY RISK: Exposes internal config"""
    return {
        **TOWER_CONFIG,
        "admin_interface": "http://172.20.0.3:8001/admin",
        "ssh_port": 22,
        "telnet_enabled": True,
        "telnet_port": 23,
        "default_gateway": "172.20.0.1",
        "dns_server": "8.8.8.8",
        "ntp_server": "pool.ntp.org"
    }

@app.post("/execute")
async def execute_command(cmd_request: CommandRequest):
    """
    Execute system command - MAJOR SECURITY VULNERABILITY
    This allows arbitrary command execution for educational demonstration
    """
    command = cmd_request.command
    
    # Whitelist of "safe" commands for demo
    safe_commands = {
        "help": "Available commands: ls, pwd, whoami, id, uname, hostname, ifconfig, ps, cat /etc/passwd, cat /etc/shadow",
        "ls": "total 24\ndrwxr-xr-x 2 root root 4096 Jan 1 12:00 bin\ndrwxr-xr-x 2 root root 4096 Jan 1 12:00 config\ndrwxr-xr-x 2 root root 4096 Jan 1 12:00 logs\n-rw-r--r-- 1 root root 1024 Jan 1 12:00 tower.conf\n-rw-r--r-- 1 root root 2048 Jan 1 12:00 secrets.txt",
        "pwd": "/home/bts-tower",
        "whoami": "root",
        "id": "uid=0(root) gid=0(root) groups=0(root)",
        "uname": "Linux",
        "uname -a": "Linux bts-tower-1 5.15.0-generic #1 SMP x86_64 GNU/Linux",
        "hostname": "bts-tower-1-jammu",
        "ifconfig": "eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500\n        inet 172.20.0.3  netmask 255.255.255.0  broadcast 172.20.0.255\n        ether 02:42:ac:14:00:03  txqueuelen 0  (Ethernet)",
        "ps": "PID   USER     COMMAND\n    1 root     /usr/bin/python3 /app/main.py\n   45 root     /usr/sbin/sshd\n   67 root     /opt/tower/monitor",
        "cat /etc/passwd": "root:x:0:0:root:/root:/bin/bash\ntower:x:1000:1000:Tower User:/home/tower:/bin/bash\nadmin:x:1001:1001:Admin:/home/admin:/bin/bash",
        "cat /etc/shadow": "root:$6$xyz123$HashedPasswordHere:19000:0:99999:7:::\ntower:$6$abc456$AnotherHashedPassword:19000:0:99999:7:::\nadmin:!:19000:0:99999:7:::",
        "cat tower.conf": "[tower]\nid=tower-1\nname=Jammu BTS\napi_key=ABC-SECRET-KEY-12345\ncore_portal=http://172.20.0.2:8000\n\n[security]\nssl_enabled=false\nauth_required=true\ndefault_password=admin123",
        "cat secrets.txt": "# Tower Secrets\nAPI_KEY=ABC-SECRET-KEY-12345\nADMIN_PASSWORD=admin123\nROOT_PASSWORD=toor123\nDATABASE_URL=postgresql://tower:tower123@db:5432/bts\nENCRYPTION_KEY=super-secret-key-xyz",
        "netstat": "Active Internet connections\nProto Recv-Q Send-Q Local Address           Foreign Address         State\ntcp        0      0 0.0.0.0:8001            0.0.0.0:*               LISTEN\ntcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN\ntcp        0      0 172.20.0.3:8001         172.20.0.2:45678        ESTABLISHED",
        "env": "PATH=/usr/local/bin:/usr/bin:/bin\nHOSTNAME=bts-tower-1\nTOWER_ID=tower-1\nAPI_SECRET=ABC-SECRET-KEY-12345\nDATABASE_URL=postgresql://tower:tower123@db:5432/bts",
    }
    
    # Check for exact matches first
    if command in safe_commands:
        return {
            "success": True,
            "command": command,
            "output": safe_commands[command]
        }
    
    # Try to handle real system commands in a safe way
    try:
        # Only allow specific safe commands
        allowed_cmds = ["ls", "pwd", "whoami", "id", "hostname", "date", "uname"]
        cmd_parts = shlex.split(command)
        
        if cmd_parts[0] in allowed_cmds:
            result = subprocess.run(
                cmd_parts,
                capture_output=True,
                text=True,
                timeout=5,
                shell=False
            )
            
            output = result.stdout if result.stdout else result.stderr
            if not output:
                output = safe_commands.get(command, "Command executed successfully (no output)")
            
            return {
                "success": True,
                "command": command,
                "output": output.strip()
            }
    except Exception as e:
        pass
    
    # Fallback for unknown commands
    return {
        "success": False,
        "command": command,
        "error": f"Command not found or not allowed: {command}\nType 'help' for available commands"
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "tower": TOWER_CONFIG["name"]}

@app.get("/admin")
async def admin_panel():
    """Admin panel - SECURITY ISSUE: No authentication"""
    return {
        "message": "Admin panel access - Authentication bypassed!",
        "tower_id": TOWER_CONFIG["tower_id"],
        "admin_users": ["admin", "root", "tower"],
        "ssh_enabled": True,
        "root_access": True,
        "warning": "This endpoint should be protected!"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

