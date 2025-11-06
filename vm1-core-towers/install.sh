#!/bin/bash

###############################################################################
# VM1 Installation Script - NTRO Core Portal + All 6 BTS Towers
# VM IP: 192.168.15.151
# Username: ubuntu / Password: ubuntu
###############################################################################

set -e

echo "==========================================="
echo "VM1: NTRO Core Portal + Towers Installation"
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
# Allow ports for Core Portal and Towers
ufw allow 8080/tcp comment "NTRO Core Portal"
ufw allow 8001/tcp comment "Tower 1"
ufw allow 8002/tcp comment "Tower 2"
ufw allow 8003/tcp comment "Tower 3"
ufw allow 8004/tcp comment "Tower 4"
ufw allow 8005/tcp comment "Tower 5"
ufw allow 8006/tcp comment "Tower 6"
echo -e "${GREEN}✓ Firewall rules configured${NC}"

echo -e "${YELLOW}[5/6] Building Docker containers...${NC}"
cd "$(dirname "$0")"
docker-compose build --no-cache

echo -e "${YELLOW}[6/6] Starting services...${NC}"
docker-compose up -d

echo ""
echo -e "${GREEN}==========================================="
echo "✓ VM1 Installation Complete!"
echo "===========================================${NC}"
echo ""
echo "Services running on 192.168.15.151:"
echo ""
echo -e "${GREEN}NTRO Core Portal:${NC}"
echo "  URL: http://192.168.15.151:8080"
echo "  Login: admin / admin123"
echo ""
echo -e "${GREEN}BTS Towers:${NC}"
echo "  Tower 1 (Jio - Jammu):           http://192.168.15.151:8001"
echo "  Tower 2 (Vodafone - Pathankot):  http://192.168.15.151:8002"
echo "  Tower 3 (Airtel - Srinagar):     http://192.168.15.151:8003"
echo "  Tower 4 (BSNL - Amritsar):       http://192.168.15.151:8004"
echo "  Tower 5 (Jio - Ludhiana):        http://192.168.15.151:8005"
echo "  Tower 6 (Vodafone - Chandigarh): http://192.168.15.151:8006"
echo ""
echo -e "${YELLOW}Waiting for services to be ready...${NC}"
sleep 10

echo ""
echo "Checking service health..."
for port in 8080 8001 8002 8003 8004 8005 8006; do
    if curl -s -f http://localhost:$port/health > /dev/null 2>&1; then
        echo -e "  ${GREEN}✓${NC} Port $port is responding"
    else
        echo -e "  ${RED}✗${NC} Port $port is not responding yet (may need more time)"
    fi
done

echo ""
echo -e "${GREEN}To view logs:${NC} docker-compose logs -f"
echo -e "${GREEN}To stop:${NC} docker-compose down"
echo -e "${GREEN}To restart:${NC} docker-compose restart"
echo ""

