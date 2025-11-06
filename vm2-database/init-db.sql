-- Telecom Operations Database Initialization
-- This database stores network operations data, tower logs, and system credentials

-- Create towers table
CREATE TABLE IF NOT EXISTS towers (
    id SERIAL PRIMARY KEY,
    tower_id VARCHAR(50) UNIQUE NOT NULL,
    tower_name VARCHAR(100) NOT NULL,
    location VARCHAR(100),
    ip_address VARCHAR(50),
    port INTEGER,
    status VARCHAR(20),
    last_heartbeat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create network_logs table
CREATE TABLE IF NOT EXISTS network_logs (
    id SERIAL PRIMARY KEY,
    tower_id VARCHAR(50),
    log_level VARCHAR(20),
    message TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tower_id) REFERENCES towers(tower_id)
);

-- Create system_users table (vulnerable - stores passwords in plain text!)
CREATE TABLE IF NOT EXISTS system_users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    role VARCHAR(50),
    department VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial tower data
INSERT INTO towers (tower_id, tower_name, location, ip_address, port, status) VALUES
('tower-1', 'Jio Tower - Muzaffarabad', 'Muzaffarabad, Azad Kashmir, Pakistan', '192.168.15.151', 8001, 'active'),
('tower-2', 'Vodafone Idea Tower - Jhelum', 'Jhelum, Punjab, Pakistan', '192.168.15.151', 8002, 'active'),
('tower-3', 'Bharti Airtel Tower - Mirpur', 'Mirpur, Azad Kashmir, Pakistan', '192.168.15.151', 8003, 'active'),
('tower-4', 'BSNL Tower - Sialkot', 'Sialkot, Punjab, Pakistan', '192.168.15.151', 8004, 'active'),
('tower-5', 'Reliance Jio Tower - Gujrat', 'Gujrat, Punjab, Pakistan', '192.168.15.151', 8005, 'active'),
('tower-6', 'Vodafone Tower - Rawalpindi', 'Rawalpindi, Punjab, Pakistan', '192.168.15.151', 8006, 'active')
ON CONFLICT (tower_id) DO NOTHING;

-- Insert vulnerable admin credentials (SECURITY FLAW!)
INSERT INTO system_users (username, password, role, department) VALUES
('ntro_admin', 'admin123', 'SUPER_ADMIN', 'Intelligence Operations'),
('tower_operator', 'telecom123', 'OPERATOR', 'Tower Management'),
('db_admin', 'dbpass@2024', 'DBA', 'IT Infrastructure'),
('security_analyst', 'security999', 'ANALYST', 'Security Operations')
ON CONFLICT (username) DO NOTHING;

-- Insert some sample network logs
INSERT INTO network_logs (tower_id, log_level, message) VALUES
('tower-1', 'INFO', 'Tower initialized successfully'),
('tower-2', 'INFO', 'Tower initialized successfully'),
('tower-3', 'WARNING', 'High network traffic detected'),
('tower-4', 'INFO', 'Tower initialized successfully'),
('tower-5', 'INFO', 'Tower initialized successfully'),
('tower-6', 'ERROR', 'Connection timeout - retry in progress');

-- Create indexes for performance
CREATE INDEX idx_tower_status ON towers(status);
CREATE INDEX idx_network_logs_timestamp ON network_logs(timestamp);
CREATE INDEX idx_network_logs_tower ON network_logs(tower_id);

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO telecom_admin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO telecom_admin;

