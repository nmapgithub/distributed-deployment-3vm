import os
import random
import shlex
import subprocess
from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel


def env(key: str, default: str) -> str:
    return os.getenv(key, default)


def env_int(key: str, default: int) -> int:
    try:
        return int(os.getenv(key, default))
    except (TypeError, ValueError):
        return default


TOWER_CONFIG = {
    "tower_id": env("TOWER_ID", "tower-unknown"),
    "name": env("TOWER_NAME", "Unknown Tower"),
    "location": env("TOWER_LOCATION", "Undisclosed Location"),
    "frequency": env("TOWER_FREQUENCY", "2100 MHz"),
    "coverage": env("TOWER_COVERAGE", "15 km radius"),
    "technology": env("TOWER_TECHNOLOGY", "4G LTE"),
    "installed_date": env("TOWER_INSTALLED_DATE", "2020-01-01"),
    "serial_number": env("TOWER_SERIAL", "UNKNOWN-SERIAL"),
    "status": env("TOWER_STATUS", "active"),
}

SERVICE_PORT = env_int("TOWER_PORT", 8001)

app = FastAPI(title=f"BTS Tower {TOWER_CONFIG['tower_id']} - {TOWER_CONFIG['name']}")


class CommandRequest(BaseModel):
    command: str


def _base_response() -> dict:
    return {
        "tower_id": TOWER_CONFIG["tower_id"],
        "name": TOWER_CONFIG["name"],
        "location": TOWER_CONFIG["location"],
    }


@app.get("/")
async def root():
    return {
        **_base_response(),
        "status": "operational",
        "message": "BTS Tower API - Authorized access only",
    }


@app.get("/status")
async def get_status():
    return {
        **_base_response(),
        "status": TOWER_CONFIG["status"],
        "operational": TOWER_CONFIG["status"] == "active",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/metrics")
async def get_metrics():
    return {
        "tower_id": TOWER_CONFIG["tower_id"],
        "connections": random.randint(150, 450),
        "signal_strength": random.randint(70, 99),
        "data_transfer": round(random.uniform(400, 2500), 2),
        "uptime": random.randint(240, 8760),
        "temperature": random.randint(20, 55),
        "power_consumption": round(random.uniform(2.0, 5.5), 2),
        "error_rate": round(random.uniform(0.01, 1.2), 2),
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/config")
async def get_config():
    gateway = env("TOWER_GATEWAY", "172.25.0.1")
    admin_host = env("TOWER_ADMIN_HOST", f"{TOWER_CONFIG['tower_id']}.internal")
    ntp = env("TOWER_NTP_SERVER", "pool.ntp.org")
    dns = env("TOWER_DNS_SERVER", "8.8.8.8")

    return {
        **TOWER_CONFIG,
        "admin_interface": f"http://{admin_host}:{SERVICE_PORT}/admin",
        "ssh_port": env_int("TOWER_SSH_PORT", 22),
        "telnet_enabled": env("TOWER_TELNET_ENABLED", "true").lower() == "true",
        "telnet_port": env_int("TOWER_TELNET_PORT", 23),
        "default_gateway": gateway,
        "dns_server": dns,
        "ntp_server": ntp,
    }


def _safe_commands() -> dict:
    serial = TOWER_CONFIG["serial_number"]
    return {
        "help": "Available commands: ls, pwd, whoami, id, uname, hostname, ifconfig, ps, env",
        "ls": "bin  config  logs  secrets  tower.conf",
        "pwd": "/home/bts-tower",
        "whoami": "root",
        "id": "uid=0(root) gid=0(root) groups=0(root)",
        "uname": "Linux",
        "uname -a": f"Linux {TOWER_CONFIG['tower_id']} 5.15.0-generic #1 SMP x86_64 GNU/Linux",
        "hostname": f"{TOWER_CONFIG['tower_id']}-{serial.lower()[:6]}",
        "ifconfig": (
            "eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500\n"
            "        inet 172.25.0.50  netmask 255.255.0.0  broadcast 172.25.255.255\n"
            "        ether 02:42:ac:19:00:32  txqueuelen 0  (Ethernet)"
        ),
        "ps": (
            "PID   USER     COMMAND\n"
            "    1 root     /usr/bin/python3 /app/main.py\n"
            "   42 root     /usr/sbin/sshd\n"
            "   73 root     /opt/tower/monitor"
        ),
        "env": (
            f"TOWER_ID={TOWER_CONFIG['tower_id']}\n"
            f"TOWER_NAME={TOWER_CONFIG['name']}\n"
            f"SERIAL={serial}\n"
            f"PORT={SERVICE_PORT}"
        ),
    }


@app.post("/execute")
async def execute_command(cmd_request: CommandRequest):
    command = cmd_request.command.strip()

    safe_commands = _safe_commands()
    if command in safe_commands:
        return {"success": True, "command": command, "output": safe_commands[command]}

    allowed_cmds = {"ls", "pwd", "whoami", "id", "hostname", "date", "uname"}

    try:
        cmd_parts = shlex.split(command)
        if cmd_parts and cmd_parts[0] in allowed_cmds:
            result = subprocess.run(
                cmd_parts,
                capture_output=True,
                text=True,
                timeout=5,
                shell=False,
            )
            output = result.stdout or result.stderr or "Command executed successfully (no output)"
            return {"success": True, "command": command, "output": output.strip()}
    except Exception as exc:  # pragma: no cover - demo only
        return {
            "success": False,
            "command": command,
            "error": f"Execution failed: {exc}",
        }

    return {
        "success": False,
        "command": command,
        "error": f"Command not found or not allowed: {command}\nType 'help' for available commands",
    }


@app.get("/health")
async def health():
    return {"status": "healthy", "tower": TOWER_CONFIG["name"]}


@app.get("/admin")
async def admin_panel():
    return {
        "message": "Admin panel access - Authentication bypassed!",
        "tower_id": TOWER_CONFIG["tower_id"],
        "admin_users": ["admin", "root", "tower"],
        "ssh_enabled": True,
        "telnet_enabled": True,
        "root_access": True,
        "warning": "This endpoint should be protected!",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=SERVICE_PORT)

