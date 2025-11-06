#!/bin/bash

###############################################################################
# VM3 Installation Script - Customer Portal (Vulnerable)
# VM IP: 192.168.15.120
# Username: ubuntu / Password: ubuntu
###############################################################################

set -e

echo "==========================================="
echo "VM3: Customer Portal Installation"
echo "==========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root or with sudo
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}Please run with sudo: sudo bash install.sh${NC}"
    exit 1
fi

echo -e "${YELLOW}[1/6] Updating system packages...${NC}"
apt-get update -qq

echo -e "${YELLOW}[2/6] Installing prerequisites...${NC}"
apt-get install -y -qq curl apt-transport-https ca-certificates software-properties-common

echo -e "${YELLOW}[3/6] Installing Docker Compose...${NC}"
if ! command -v docker-compose &> /dev/null; then
    # Install docker-compose
    COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep 'tag_name' | cut -d\" -f4)
    curl -L "https://github.com/docker/compose/releases/download/${COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    echo -e "${GREEN}✓ Docker Compose installed: $(docker-compose --version)${NC}"
else
    echo -e "${GREEN}✓ Docker Compose already installed: $(docker-compose --version)${NC}"
fi

echo -e "${YELLOW}[4/6] Setting up firewall rules...${NC}"
# Allow customer portal port
ufw allow 9090/tcp comment "Customer Portal"
echo -e "${GREEN}✓ Firewall rules configured${NC}"

echo -e "${YELLOW}[5/6] Building Docker containers...${NC}"
cd "$(dirname "$0")"
docker-compose build --no-cache

echo -e "${YELLOW}[6/6] Starting services...${NC}"
docker-compose up -d

echo ""
echo -e "${GREEN}==========================================="
echo "✓ VM3 Installation Complete!"
echo "===========================================${NC}"
echo ""
echo "Services running on 192.168.15.120:"
echo ""
echo -e "${GREEN}Customer Portal (VULNERABLE):${NC}"
echo "  URL: http://192.168.15.120:9090"
echo "  Test Logins:"
echo "    • rajesh.kumar / password123"
echo "    • priya.sharma / priya@123"
echo "    • amit.patel / amit1234"
echo ""
echo -e "${RED}SQL Console (Vulnerable):${NC}"
echo "  URL: http://192.168.15.120:9090/api/query"
echo "  WARNING: Allows arbitrary SQL execution!"
echo ""
echo -e "${YELLOW}SQL Injection Test:${NC}"
echo "  Username: ' OR '1'='1'--"
echo "  Password: anything"
echo ""
echo -e "${YELLOW}Extracting NTRO Credentials:${NC}"
echo "  In SQL Console, execute:"
echo "  SELECT * FROM admin_credentials"
echo ""
echo -e "${YELLOW}Waiting for service to be ready...${NC}"
sleep 10

echo ""
echo "Checking service health..."
if curl -s -f http://localhost:9000/health > /dev/null 2>&1; then
    echo -e "  ${GREEN}✓${NC} Customer Portal is responding"
else
    echo -e "  ${RED}✗${NC} Customer Portal is not responding yet (may need more time)"
fi

echo ""
echo -e "${GREEN}To view logs:${NC} docker-compose logs -f"
echo -e "${GREEN}To stop:${NC} docker-compose down"
echo ""
echo -e "${YELLOW}Connect to NTRO Portal:${NC} http://192.168.15.151:8080"
echo ""

