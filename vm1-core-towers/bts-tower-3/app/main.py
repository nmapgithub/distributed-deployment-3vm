from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
import subprocess
import shlex
from datetime import datetime

app = FastAPI(title="BTS Tower 3 - Mirpur")

# Tower Configuration
TOWER_CONFIG = {
    "tower_id": "tower-3",
    "name": "Bharti Airtel Tower - Mirpur",
    "location": "Mirpur, Azad Kashmir, Pakistan",
    "frequency": "2600 MHz",
    "coverage": "18 km radius",
    "technology": "5G NR",
    "installed_date": "2021-12-10",
    "serial_number": "ABC-SRG-003"
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
        "connections": random.randint(300, 500),
        "signal_strength": random.randint(88, 99),
        "data_transfer": round(random.uniform(1200, 3000), 2),
        "uptime": random.randint(600, 8000),
        "temperature": random.randint(22, 42),
        "power_consumption": round(random.uniform(3.5, 5.5), 2),
        "error_rate": round(random.uniform(0.01, 0.3), 2),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/config")
async def get_config():
    """Get tower configuration - SECURITY RISK: Exposes internal config"""
    return {
        **TOWER_CONFIG,
        "admin_interface": "http://172.20.0.5:8003/admin",
        "ssh_port": 22,
        "telnet_enabled": False,
        "ftp_enabled": True,
        "ftp_port": 21,
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
        "ls": "total 40\ndrwxr-xr-x 2 root root 4096 Jan 1 12:00 bin\ndrwxr-xr-x 3 root root 4096 Jan 1 12:00 config\ndrwxr-xr-x 2 root root 4096 Jan 1 12:00 logs\ndrwxr-xr-x 2 root root 4096 Jan 1 12:00 scripts\ndrwxr-xr-x 2 root root 4096 Jan 1 12:00 keys\n-rw-r--r-- 1 root root 2048 Jan 1 12:00 tower.conf\n-rw-r--r-- 1 root root 4096 Jan 1 12:00 master.key",
        "pwd": "/home/bts-tower",
        "whoami": "root",
        "id": "uid=0(root) gid=0(root) groups=0(root)",
        "uname": "Linux",
        "uname -a": "Linux bts-tower-3 5.15.0-generic #1 SMP x86_64 GNU/Linux",
        "hostname": "bts-tower-3-srinagar",
        "ifconfig": "eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500\n        inet 172.20.0.5  netmask 255.255.255.0  broadcast 172.20.0.255\n        ether 02:42:ac:14:00:05  txqueuelen 0  (Ethernet)",
        "ps": "PID   USER     COMMAND\n    1 root     /usr/bin/python3 /app/main.py\n   48 root     /usr/sbin/sshd\n   65 root     /usr/sbin/vsftpd\n   82 root     /opt/tower/monitor\n   93 root     /opt/tower/5g-core",
        "cat /etc/passwd": "root:x:0:0:root:/root:/bin/bash\ntower:x:1000:1000:Tower User:/home/tower:/bin/bash\nadmin:x:1001:1001:Admin:/home/admin:/bin/bash\noperator:x:1002:1002:Operator:/home/operator:/bin/bash\nftp:x:1003:1003:FTP User:/home/ftp:/bin/bash",
        "cat /etc/shadow": "root:$6$srinagar$MasterRootHash:19000:0:99999:7:::\ntower:$6$srg001$TowerUserHash:19000:0:99999:7:::\nadmin:$6$abc123$AdminStrongHash:19000:0:99999:7:::\nftp:$6$ftp456$FTPUserHash:19000:0:99999:7:::",
        "cat tower.conf": "[tower]\nid=tower-3\nname=Srinagar BTS\napi_key=ABC-MASTER-KEY-99999\ncore_portal=http://172.20.0.2:8000\n\n[security]\nssl_enabled=false\nauth_required=true\nencryption=AES-256\ndefault_password=Srinagar@2024\n\n[5g_config]\nband=n78\nbandwidth=100MHz\nbeamforming=enabled\n\n[database]\nhost=172.20.0.10\nport=5432\nuser=tower_admin\npassword=5g_tower_secure_2024",
        "cat master.key": "# Master Encryption Keys\nMASTER_KEY=0x4D415354455252AABBCCDDEE1122334455\nAES_KEY=AES-256-CBC:89ABCDEF0123456789ABCDEF01234567\nRSA_PRIVATE=/keys/rsa_private.pem\nRSA_PUBLIC=/keys/rsa_public.pem\n\n# API Credentials\nCORE_API_KEY=ABC-MASTER-KEY-99999\nSUPER_ADMIN_TOKEN=Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.super.admin\n\n# Database\nDB_ENCRYPTION_KEY=MySuperSecretDBKey2024!\nBACKUP_ENCRYPTION=BackupKey#5G2024",
        "netstat": "Active Internet connections\nProto Recv-Q Send-Q Local Address           Foreign Address         State\ntcp        0      0 0.0.0.0:8003            0.0.0.0:*               LISTEN\ntcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN\ntcp        0      0 0.0.0.0:21              0.0.0.0:*               LISTEN\ntcp        0      0 172.20.0.5:8003         172.20.0.2:45682        ESTABLISHED\ntcp        0      0 172.20.0.5:8003         172.20.0.2:45684        ESTABLISHED",
        "env": "PATH=/usr/local/bin:/usr/bin:/bin\nHOSTNAME=bts-tower-3\nTOWER_ID=tower-3\nAPI_SECRET=ABC-MASTER-KEY-99999\nDB_PASSWORD=5g_tower_secure_2024\nENCRYPTION_ENABLED=true\nMASTER_KEY_PATH=/home/bts-tower/master.key",
        "ls keys": "-rw------- 1 root root 3243 Jan 1 12:00 rsa_private.pem\n-rw-r--r-- 1 root root  451 Jan 1 12:00 rsa_public.pem\n-rw------- 1 root root 1024 Jan 1 12:00 aes.key\n-rw------- 1 root root 2048 Jan 1 12:00 master.key",
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
    """Admin panel - SECURITY ISSUE: Minimal authentication"""
    return {
        "message": "5G Tower Admin Panel - Advanced Access",
        "tower_id": TOWER_CONFIG["tower_id"],
        "admin_users": ["admin", "root", "tower", "operator"],
        "ssh_enabled": True,
        "ftp_enabled": True,
        "root_access": True,
        "5g_capabilities": ["beamforming", "network_slicing", "edge_computing"],
        "critical_files": ["/home/bts-tower/master.key", "/keys/rsa_private.pem"],
        "vulnerabilities": ["Weak auth", "FTP enabled", "Keys in filesystem"],
        "warning": "This is the most critical tower in the network!"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)

