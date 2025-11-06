# Manual Deployment Guide

Since you're in a container, you need to copy files to your VMs manually.

## Step 1: Get Files to Your Local Machine

From your local machine (outside container):

```bash
# Find your container ID
docker ps

# Copy deployment folder out of container
docker cp <container-id>:/ATTACK-SIMULATION/distributed-deployment-3vm ~/ntro-deployment
```

## Step 2: Deploy to Each VM

### Deploy VM1 (192.168.15.151)

```bash
cd ~/ntro-deployment/vm1-core-towers
tar czf - . | ssh ubuntu@192.168.15.151 'mkdir -p ~/attack-simulation && cd ~/attack-simulation && tar xzf - && echo "ubuntu" | sudo -S bash install.sh'
```

### Deploy VM2 (192.168.15.89)

```bash
cd ~/ntro-deployment/vm2-database
tar czf - . | ssh ubuntu@192.168.15.89 'mkdir -p ~/attack-simulation && cd ~/attack-simulation && tar xzf - && echo "ubuntu" | sudo -S bash install.sh'
```

### Deploy VM3 (192.168.15.120)

```bash
cd ~/ntro-deployment/vm3-customer-portal
tar czf - . | ssh ubuntu@192.168.15.120 'mkdir -p ~/attack-simulation && cd ~/attack-simulation && tar xzf - && echo "ubuntu" | sudo -S bash install.sh'
```

## Step 3: Verify Deployment

Test each service:

```bash
# Test VM1
curl http://192.168.15.151:8080/health

# Test VM2
telnet 192.168.15.89 5432

# Test VM3
curl http://192.168.15.120:9090/health
```

## Alternative: SSH into each VM individually

### VM1
```bash
ssh ubuntu@192.168.15.151
mkdir -p ~/attack-simulation
# Then copy vm1-core-towers/* here and run install.sh
```

### VM2
```bash
ssh ubuntu@192.168.15.89
mkdir -p ~/attack-simulation
# Then copy vm2-database/* here and run install.sh
```

### VM3
```bash
ssh ubuntu@192.168.15.120
mkdir -p ~/attack-simulation
# Then copy vm3-customer-portal/* here and run install.sh
```

## After Deployment

Access your simulation:
- Customer Portal: http://192.168.15.120:9090
- NTRO Portal: http://192.168.15.151:8080
- Database: http://192.168.15.89:5050
