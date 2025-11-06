#!/bin/bash

###############################################################################
# Master Deployment Script - Deploy to All 3 VMs
# Copies files and executes installation on each VM
###############################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# VM Configuration
VM1_IP="192.168.15.151"
VM1_USER="ubuntu"
VM1_PASS="ubuntu"

VM2_IP="192.168.15.89"
VM2_USER="ubuntu"
VM2_PASS="ubuntu"

VM3_IP="192.168.15.120"
VM3_USER="ubuntu"
VM3_PASS="ubuntu"

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  NTRO Cyber Attack Simulation - Distributed Deployment  ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if sshpass is installed
if ! command -v sshpass &> /dev/null; then
    echo -e "${YELLOW}Installing sshpass for automated deployment...${NC}"
    sudo apt-get update -qq
    sudo apt-get install -y sshpass
fi

echo -e "${GREEN}Deployment Plan:${NC}"
echo "  VM1 (192.168.15.151): NTRO Core Portal + 6 BTS Towers"
echo "  VM2 (192.168.15.89):  PostgreSQL Database Server"
echo "  VM3 (192.168.15.120): Customer Portal (Vulnerable)"
echo ""

read -p "Continue with deployment? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Deployment cancelled."
    exit 1
fi

# Function to deploy to a VM
deploy_to_vm() {
    local VM_IP=$1
    local VM_USER=$2
    local VM_PASS=$3
    local VM_DIR=$4
    local VM_NAME=$5
    
    echo ""
    echo -e "${YELLOW}═══════════════════════════════════════${NC}"
    echo -e "${YELLOW}Deploying to $VM_NAME ($VM_IP)...${NC}"
    echo -e "${YELLOW}═══════════════════════════════════════${NC}"
    
    # Test SSH connection
    echo -e "${BLUE}[1/4] Testing SSH connection...${NC}"
    if sshpass -p "$VM_PASS" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=10 "$VM_USER@$VM_IP" "echo 'Connection successful'" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ SSH connection successful${NC}"
    else
        echo -e "${RED}✗ Cannot connect to $VM_IP${NC}"
        echo -e "${RED}Please check:${NC}"
        echo "  1. VM is running"
        echo "  2. SSH is enabled"
        echo "  3. IP address is correct"
        echo "  4. Username/password is correct"
        return 1
    fi
    
    # Copy files to VM
    echo -e "${BLUE}[2/4] Copying files to VM...${NC}"
    sshpass -p "$VM_PASS" ssh "$VM_USER@$VM_IP" "mkdir -p ~/attack-simulation"
    sshpass -p "$VM_PASS" scp -r -o StrictHostKeyChecking=no "$VM_DIR"/* "$VM_USER@$VM_IP:~/attack-simulation/"
    echo -e "${GREEN}✓ Files copied${NC}"
    
    # Execute installation
    echo -e "${BLUE}[3/4] Running installation script...${NC}"
    sshpass -p "$VM_PASS" ssh -t "$VM_USER@$VM_IP" "cd ~/attack-simulation && echo '$VM_PASS' | sudo -S bash install.sh"
    
    echo -e "${GREEN}✓ $VM_NAME deployment complete!${NC}"
}

# Deploy to each VM
deploy_to_vm "$VM1_IP" "$VM1_USER" "$VM1_PASS" "vm1-core-towers" "VM1 - Core Portal"
deploy_to_vm "$VM2_IP" "$VM2_USER" "$VM2_PASS" "vm2-database" "VM2 - Database"
deploy_to_vm "$VM3_IP" "$VM3_USER" "$VM3_PASS" "vm3-customer-portal" "VM3 - Customer Portal"

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║        Deployment Complete - All VMs Ready!              ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}═══ Access Points ═══${NC}"
echo ""
echo -e "${GREEN}NTRO Intelligence Portal:${NC}"
echo "  URL: http://192.168.15.151:8080"
echo "  Login: admin / admin123"
echo ""
echo -e "${GREEN}Customer Portal (Vulnerable):${NC}"
echo "  URL: http://192.168.15.120:9090"
echo "  SQL Console: http://192.168.15.120:9090/api/query"
echo ""
echo -e "${GREEN}Database Server:${NC}"
echo "  PostgreSQL: 192.168.15.89:5432"
echo "  pgAdmin: http://192.168.15.89:5050"
echo ""
echo -e "${GREEN}BTS Towers (All on VM1):${NC}"
echo "  Tower 1-6: http://192.168.15.151:8001-8006"
echo ""
echo -e "${YELLOW}═══ Attack Simulation Flow ═══${NC}"
echo "1. Access Customer Portal: http://192.168.15.120:9090"
echo "2. SQL Injection: Use ' OR '1'='1'-- in login"
echo "3. SQL Console: http://192.168.15.120:9090/api/query"
echo "4. Extract credentials: SELECT * FROM admin_credentials"
echo "5. Lateral Movement: Use credentials at http://192.168.15.151:8080"
echo "6. Access classified towers and execute commands"
echo ""

