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
ufw allow 44880/tcp comment "NTRO Core Portal"
ufw allow 35111/tcp comment "Tower 1 - Jammu"
ufw allow 35221/tcp comment "Tower 2 - Kathua"
ufw allow 35331/tcp comment "Tower 3 - Pathankot"
ufw allow 35441/tcp comment "Tower 4 - Amritsar"
ufw allow 35551/tcp comment "Tower 5 - Gurdaspur"
ufw allow 35661/tcp comment "Tower 6 - Firozpur"
ufw allow 35771/tcp comment "Tower 7 - Fazilka"
ufw allow 35881/tcp comment "Tower 8 - Sri Ganganagar"
ufw allow 35991/tcp comment "Tower 9 - Hanumangarh"
ufw allow 36101/tcp comment "Tower 10 - Abohar"
ufw allow 36211/tcp comment "Tower 11 - Bikaner"
ufw allow 36321/tcp comment "Tower 12 - Jaisalmer"
ufw allow 36431/tcp comment "Tower 13 - Barmer"
ufw allow 36541/tcp comment "Tower 14 - Bhuj"
ufw allow 36651/tcp comment "Tower 15 - Gandhidham"
ufw allow 36761/tcp comment "Tower 16 - Naliya"
ufw allow 36871/tcp comment "Tower 17 - Poonch"
ufw allow 36981/tcp comment "Tower 18 - Kupwara"
ufw allow 37091/tcp comment "Tower 19 - Kargil"
ufw allow 37101/tcp comment "Tower 20 - Turtuk"
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
echo "  URL: http://192.168.15.151:44880"
echo "  Login: admin / admin123"
echo ""
echo -e "${GREEN}BTS Towers:${NC}"
echo "  Tower 1  (Jio - Jammu):            http://192.168.15.151:35111"
echo "  Tower 2  (Vi - Kathua):            http://192.168.15.151:35221"
echo "  Tower 3  (Airtel - Pathankot):     http://192.168.15.151:35331"
echo "  Tower 4  (BSNL - Amritsar):        http://192.168.15.151:35441"
echo "  Tower 5  (Jio - Gurdaspur):        http://192.168.15.151:35551"
echo "  Tower 6  (Vodafone - Firozpur):    http://192.168.15.151:35661"
echo "  Tower 7  (Airtel - Fazilka):       http://192.168.15.151:35771"
echo "  Tower 8  (Jio - Sri Ganganagar):   http://192.168.15.151:35881"
echo "  Tower 9  (Telenor - Hanumangarh):  http://192.168.15.151:35991"
echo "  Tower 10 (Vi - Abohar):            http://192.168.15.151:36101"
echo "  Tower 11 (Airtel - Bikaner):       http://192.168.15.151:36211"
echo "  Tower 12 (Jio - Jaisalmer):        http://192.168.15.151:36321"
echo "  Tower 13 (BSNL - Barmer):          http://192.168.15.151:36431"
echo "  Tower 14 (Vi - Bhuj):              http://192.168.15.151:36541"
echo "  Tower 15 (Jio - Gandhidham):       http://192.168.15.151:36651"
echo "  Tower 16 (Airtel - Naliya):        http://192.168.15.151:36761"
echo "  Tower 17 (BSNL - Poonch):          http://192.168.15.151:36871"
echo "  Tower 18 (Airtel - Kupwara):       http://192.168.15.151:36981"
echo "  Tower 19 (BSNL - Kargil):          http://192.168.15.151:37091"
echo "  Tower 20 (Jio - Turtuk):           http://192.168.15.151:37101"
echo ""
echo -e "${YELLOW}Waiting for services to be ready...${NC}"
sleep 10

echo ""
echo "Checking service health..."
for port in 44880 35111 35221 35331 35441 35551 35661 35771 35881 35991 36101 36211 36321 36431 36541 36651 36761 36871 36981 37091 37101; do
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

