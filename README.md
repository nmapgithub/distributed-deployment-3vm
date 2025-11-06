# NTRO Cyber Attack Simulation - Distributed Deployment

## 🎯 Overview

This distributed deployment simulates a realistic telecom infrastructure across 3 virtual machines, demonstrating SQL injection, lateral movement, and infrastructure compromise.

---

## 🖥️ **VM Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                    Network Topology                          │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────┐       │
│  │ VM1: 192.168.15.151 (Core Infrastructure)        │       │
│  │  • NTRO Core Portal (Port 8080)                  │       │
│  │  • 6 BTS Towers (Ports 8001-8006)                │       │
│  │    - Jio Jammu, Vodafone Pathankot, Airtel      │       │
│  │      Srinagar, BSNL Amritsar, Jio Ludhiana,     │       │
│  │      Vodafone Chandigarh                         │       │
│  └──────────────────────────────────────────────────┘       │
│                           │                                   │
│                           │ Network Communication            │
│                           │                                   │
│  ┌──────────────────────────────────────────────────┐       │
│  │ VM2: 192.168.15.89 (Database Server)             │       │
│  │  • PostgreSQL (Port 5432)                        │       │
│  │  • pgAdmin Web UI (Port 5050)                    │       │
│  │  • Stores: Tower data, logs, credentials         │       │
│  └──────────────────────────────────────────────────┘       │
│                           │                                   │
│                           │                                   │
│  ┌──────────────────────────────────────────────────┐       │
│  │ VM3: 192.168.15.120 (Customer Portal)            │       │
│  │  • Customer Portal (Port 9090)                   │       │
│  │  • SQL Console (Vulnerable!)                     │       │
│  │  • Contains NTRO credentials (Security flaw!)    │       │
│  └──────────────────────────────────────────────────┘       │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 **Prerequisites**

### Each VM Must Have:
- **OS**: Ubuntu 20.04+ or similar Linux
- **Docker**: Installed and running
- **SSH**: Enabled and accessible
- **Firewall**: Configured to allow required ports
- **Resources**: 2GB RAM minimum, 10GB disk space

### Local Machine (for deployment):
- SSH client
- `sshpass` (will be installed automatically)
- Bash shell

---

## 🚀 **Quick Start - Automated Deployment**

### Option 1: Deploy to All VMs (Automated)

```bash
cd distributed-deployment-3vm
chmod +x deploy-all.sh
./deploy-all.sh
```

This script will:
1. Connect to each VM via SSH
2. Copy all necessary files
3. Install Docker Compose
4. Build and start containers
5. Configure firewall rules

---

### Option 2: Manual Deployment (VM by VM)

#### **VM1: Core Portal + Towers (192.168.15.151)**

```bash
# On your local machine
cd vm1-core-towers
scp -r * ubuntu@192.168.15.151:~/attack-simulation/

# SSH into VM1
ssh ubuntu@192.168.15.151

# Run installation
cd ~/attack-simulation
sudo bash install.sh
```

#### **VM2: Database Server (192.168.15.89)**

```bash
# On your local machine
cd vm2-database
scp -r * ubuntu@192.168.15.89:~/attack-simulation/

# SSH into VM2
ssh ubuntu@192.168.15.89

# Run installation
cd ~/attack-simulation
sudo bash install.sh
```

#### **VM3: Customer Portal (192.168.15.120)**

```bash
# On your local machine
cd vm3-customer-portal
scp -r * ubuntu@192.168.15.120:~/attack-simulation/

# SSH into VM3
ssh ubuntu@192.168.15.120

# Run installation
cd ~/attack-simulation
sudo bash install.sh
```

---

## 🌐 **Access Points After Deployment**

### **NTRO Intelligence Portal** (VM1)
```
URL: http://192.168.15.151:8080
Username: admin
Password: admin123

Features:
• Interactive map with 6 BTS towers
• Real-time monitoring dashboard
• Terminal access to each tower
• Classified military-grade interface
```

### **Customer Portal - VULNERABLE!** (VM3)
```
URL: http://192.168.15.120:9090

Test Accounts:
• rajesh.kumar / password123
• priya.sharma / priya@123
• amit.patel / amit1234

SQL Console (Vulnerable):
• URL: http://192.168.15.120:9090/api/query
• Allows arbitrary SQL execution
• Contains NTRO admin credentials!
```

### **Database Server** (VM2)
```
PostgreSQL:
• Host: 192.168.15.89
• Port: 5432
• Database: telecom_operations
• Username: telecom_admin
• Password: telecom_db_2024

pgAdmin Web UI:
• URL: http://192.168.15.89:5050
• Email: admin@telecom.local
• Password: admin123
```

### **BTS Towers** (All on VM1)
```
Tower 1 (Jio - Jammu):           http://192.168.15.151:8001
Tower 2 (Vodafone - Pathankot):  http://192.168.15.151:8002
Tower 3 (Airtel - Srinagar):     http://192.168.15.151:8003
Tower 4 (BSNL - Amritsar):       http://192.168.15.151:8004
Tower 5 (Jio - Ludhiana):        http://192.168.15.151:8005
Tower 6 (Vodafone - Chandigarh): http://192.168.15.151:8006
```

---

## 🎯 **Attack Simulation Guide**

### **Phase 1: Initial Access (SQL Injection)**

1. **Open Customer Portal**:
   ```
   http://192.168.15.120:9090
   ```

2. **SQL Injection Attack**:
   - Username: `' OR '1'='1'--`
   - Password: `anything`
   - Click **LOGIN**

3. **Access SQL Console**:
   ```
   http://192.168.15.120:9090/api/query
   ```

---

### **Phase 2: Credential Extraction**

In the SQL Console, execute these queries:

```sql
-- List all tables
SELECT name FROM sqlite_master WHERE type='table';

-- Extract NTRO credentials (JACKPOT!)
SELECT * FROM admin_credentials;

-- You'll see:
-- system_name: NTRO Portal
-- portal_url: http://192.168.15.151:8080
-- username: admin
-- password: admin123
-- access_level: SUPER_ADMIN
```

---

### **Phase 3: Lateral Movement**

1. **Use extracted credentials**:
   - Go to: `http://192.168.15.151:8080`
   - Login: `admin` / `admin123`

2. **You now have access to**:
   - Classified intelligence portal
   - All 6 BTS tower systems
   - Terminal access to infrastructure

---

### **Phase 4: Infrastructure Compromise**

1. **Click on any tower** on the map
2. **Click "Open Terminal"**
3. **Execute commands**:
   ```bash
   whoami
   ls -la
   cat secrets.txt
   ifconfig
   ps aux
   ```

---

## 🔧 **Management Commands**

### View Logs
```bash
# VM1
ssh ubuntu@192.168.15.151
cd ~/attack-simulation
docker-compose logs -f

# VM2
ssh ubuntu@192.168.15.89
cd ~/attack-simulation
docker-compose logs -f

# VM3
ssh ubuntu@192.168.15.120
cd ~/attack-simulation
docker-compose logs -f
```

### Stop Services
```bash
cd ~/attack-simulation
docker-compose down
```

### Restart Services
```bash
cd ~/attack-simulation
docker-compose restart
```

### Update Configuration
```bash
# Edit docker-compose.yml or code files
# Then rebuild and restart:
docker-compose up -d --build
```

---

## 🐛 **Troubleshooting**

### Cannot Connect to VM
```bash
# Test SSH connection
ssh ubuntu@192.168.15.151

# If password authentication fails
ssh-copy-id ubuntu@192.168.15.151

# Check firewall
sudo ufw status
```

### Service Not Starting
```bash
# Check logs
docker-compose logs <service-name>

# Check if port is already in use
sudo netstat -tulpn | grep <port>

# Restart Docker
sudo systemctl restart docker
```

### Cannot Access Web Interfaces
```bash
# Check if service is running
docker ps

# Check firewall rules
sudo ufw status

# Test from VM itself
curl http://localhost:8080/health
```

---

## 🔒 **Security Notes**

⚠️ **THIS IS AN EDUCATIONAL SIMULATION - DO NOT USE IN PRODUCTION!**

### Intentional Vulnerabilities:
1. **SQL Injection** in customer portal login
2. **Unrestricted SQL Console** accessible without authentication
3. **Plain-text credentials** in database
4. **Command Injection** in tower terminals
5. **No input validation** in multiple endpoints
6. **Weak passwords** (admin123, etc.)
7. **Admin credentials stored in customer database**

### Network Security:
- Configure firewall rules appropriately
- Use VPN or private network for demo
- Do not expose to public internet
- Monitor for unauthorized access

---

## 📊 **System Requirements**

| VM | vCPU | RAM | Disk | Services |
|----|------|-----|------|----------|
| VM1 | 2+ | 4GB | 20GB | Core Portal + 6 Towers |
| VM2 | 1+ | 2GB | 10GB | PostgreSQL + pgAdmin |
| VM3 | 1+ | 2GB | 10GB | Customer Portal |

---

## 📝 **File Structure**

```
distributed-deployment-3vm/
├── deploy-all.sh                 # Master deployment script
├── README.md                     # This file
│
├── vm1-core-towers/             # VM1 deployment
│   ├── docker-compose.yml       # Core + Towers orchestration
│   ├── install.sh               # VM1 installation script
│   ├── core-portal/             # NTRO portal code
│   └── bts-tower-*/             # Tower applications
│
├── vm2-database/                # VM2 deployment
│   ├── docker-compose.yml       # Database orchestration
│   ├── install.sh               # VM2 installation script
│   └── init-db.sql              # Database initialization
│
└── vm3-customer-portal/         # VM3 deployment
    ├── docker-compose.yml       # Customer portal orchestration
    ├── install.sh               # VM3 installation script
    └── customer-portal/         # Vulnerable portal code
```

---

## 🎓 **Educational Objectives**

This simulation teaches:
1. **SQL Injection** - How unsanitized inputs compromise databases
2. **Lateral Movement** - Using one compromise to access other systems
3. **Credential Theft** - Extracting stored passwords
4. **Command Injection** - Remote code execution vulnerabilities
5. **Network Segmentation** - Importance of proper isolation
6. **Defense in Depth** - Multiple security layers needed
7. **Incident Response** - Detecting and responding to attacks

---

## 📞 **Support**

For issues or questions:
1. Check the troubleshooting section
2. Review logs: `docker-compose logs`
3. Verify network connectivity between VMs
4. Ensure all ports are accessible

---

## ⚖️ **Legal Disclaimer**

This software is for **EDUCATIONAL PURPOSES ONLY**. Use only in authorized training environments. Unauthorized access to computer systems is illegal.

---

**Happy Learning! Stay Ethical! 🛡️**

