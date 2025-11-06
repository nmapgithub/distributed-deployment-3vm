#!/bin/bash

###############################################################################
# VM2 Installation Script - Telecom Database Server
# VM IP: 192.168.15.89
# Username: ubuntu / Password: ubuntu
###############################################################################

set -e

echo "==========================================="
echo "VM2: Telecom Database Server Installation"
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
apt-get install -y -qq curl apt-transport-https ca-certificates software-properties-common postgresql-client

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
# Allow database ports
ufw allow 5432/tcp comment "PostgreSQL Database"
ufw allow 5050/tcp comment "pgAdmin Web UI"
echo -e "${GREEN}✓ Firewall rules configured${NC}"

echo -e "${YELLOW}[5/6] Starting database services...${NC}"
cd "$(dirname "$0")"
docker-compose up -d

echo -e "${YELLOW}[6/6] Waiting for database initialization...${NC}"
sleep 15

echo ""
echo -e "${GREEN}==========================================="
echo "✓ VM2 Installation Complete!"
echo "===========================================${NC}"
echo ""
echo "Services running on 192.168.15.89:"
echo ""
echo -e "${GREEN}PostgreSQL Database:${NC}"
echo "  Host: 192.168.15.89"
echo "  Port: 5432"
echo "  Database: telecom_operations"
echo "  Username: telecom_admin"
echo "  Password: telecom_db_2024"
echo ""
echo -e "${GREEN}pgAdmin Web Interface:${NC}"
echo "  URL: http://192.168.15.89:5050"
echo "  Email: admin@telecom.local"
echo "  Password: admin123"
echo ""
echo -e "${YELLOW}Database Connection String:${NC}"
echo "  postgresql://telecom_admin:telecom_db_2024@192.168.15.89:5432/telecom_operations"
echo ""
echo -e "${YELLOW}To query database:${NC}"
echo "  docker exec -it telecom-database psql -U telecom_admin -d telecom_operations"
echo ""
echo -e "${GREEN}To view logs:${NC} docker-compose logs -f"
echo -e "${GREEN}To stop:${NC} docker-compose down"
echo ""

