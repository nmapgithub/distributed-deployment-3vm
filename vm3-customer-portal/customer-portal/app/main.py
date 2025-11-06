from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from pydantic import BaseModel
import sqlite3
import hashlib
from typing import List, Optional
import os
import shutil
import subprocess

app = FastAPI(title="Telecom Customer Portal")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Create uploads directory (VULNERABLE - no restrictions!)
UPLOAD_DIR = "app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Initialize database
DB_FILE = "app/customers.db"

def init_database():
    """Initialize customer database with fake Indian data"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            email TEXT,
            address TEXT,
            plan_type TEXT,
            data_limit TEXT,
            created_date TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            plan_name TEXT NOT NULL,
            plan_type TEXT NOT NULL,
            price INTEGER NOT NULL,
            data_limit TEXT,
            validity_days INTEGER,
            status TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
    ''')
    
    # Create admin_credentials table for NTRO portal (SECURITY RISK!)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin_credentials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            system_name TEXT NOT NULL,
            portal_url TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            access_level TEXT,
            department TEXT,
            notes TEXT
        )
    ''')
    
    # Insert NTRO admin credentials (CRITICAL SECURITY FLAW!)
    cursor.execute("SELECT COUNT(*) FROM admin_credentials")
    if cursor.fetchone()[0] == 0:
        admin_creds = [
            ('NTRO Portal', 'http://192.168.15.151:8080', 'admin', 'admin123', 'SUPER_ADMIN', 'Intelligence', 'Main admin account for NTRO NOC'),
            ('NTRO Portal', 'http://192.168.15.151:8080', 'operator', 'telecom123', 'OPERATOR', 'Operations', 'Tower operations access'),
            ('Tower Management', 'http://192.168.15.151:8001', 'root', 'toor123', 'ROOT', 'Infrastructure', 'Root access to tower systems'),
            ('Database Admin', 'postgresql://172.20.0.10:5432', 'dbadmin', 'dbpass@2024', 'DBA', 'IT', 'Database administrator account'),
        ]
        
        for cred in admin_creds:
            cursor.execute('''
                INSERT INTO admin_credentials (system_name, portal_url, username, password, access_level, department, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', cred)
    
    # Check if customer data already exists
    cursor.execute("SELECT COUNT(*) FROM customers")
    if cursor.fetchone()[0] == 0:
        # Insert fake Indian customer data (intentionally weak passwords)
        fake_customers = [
            ('rajesh.kumar', 'password123', 'Rajesh Kumar', '+91-9876543210', 'rajesh.k@gmail.com', 'Delhi', '4G', '2GB/day', '2023-01-15'),
            ('priya.sharma', 'priya@123', 'Priya Sharma', '+91-9876543211', 'priya.s@yahoo.com', 'Mumbai', '5G', 'Unlimited', '2023-02-20'),
            ('amit.patel', 'amit1234', 'Amit Patel', '+91-9876543212', 'amit.p@gmail.com', 'Gujarat', '3G', '1.5GB/day', '2023-03-10'),
            ('neha.singh', 'neha@pass', 'Neha Singh', '+91-9876543213', 'neha.singh@outlook.com', 'Lucknow', '4G', '2GB/day', '2023-04-05'),
            ('vikram.reddy', 'vikram123', 'Vikram Reddy', '+91-9876543214', 'vikram.r@gmail.com', 'Hyderabad', '5G', '3GB/day', '2023-05-12'),
            ('ananya.iyer', 'ananya@2023', 'Ananya Iyer', '+91-9876543215', 'ananya.i@gmail.com', 'Chennai', '4G', '2GB/day', '2023-06-18'),
            ('rohit.gupta', '123456', 'Rohit Gupta', '+91-9876543216', 'rohit.g@hotmail.com', 'Bangalore', '5G', 'Unlimited', '2023-07-22'),
            ('kavita.das', 'password', 'Kavita Das', '+91-9876543217', 'kavita.d@gmail.com', 'Kolkata', '4G', '1.5GB/day', '2023-08-30'),
            ('arjun.mehta', 'arjun@123', 'Arjun Mehta', '+91-9876543218', 'arjun.m@gmail.com', 'Pune', '4G', '2GB/day', '2023-09-14'),
            ('deepika.nair', 'deepika1234', 'Deepika Nair', '+91-9876543219', 'deepika.n@gmail.com', 'Kerala', '5G', '3GB/day', '2023-10-05'),
        ]
        
        for customer in fake_customers:
            cursor.execute('''
                INSERT INTO customers (username, password, full_name, phone_number, email, address, plan_type, data_limit, created_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', customer)
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_database()

# Models
class LoginRequest(BaseModel):
    username: str
    password: str

class SubscriptionRequest(BaseModel):
    plan_type: str
    plan_name: str

@app.get("/", response_class=HTMLResponse)
async def root():
    return FileResponse("app/static/customer_login.html")

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    return FileResponse("app/static/customer_dashboard.html")

@app.post("/api/login")
async def login(credentials: LoginRequest):
    """
    VULNERABLE LOGIN - SQL Injection possible!
    Intentionally insecure for educational purposes
    """
    username = credentials.username
    password = credentials.password
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # VULNERABLE: SQL Injection - not using parameterized queries
    query = f"SELECT * FROM customers WHERE username='{username}' AND password='{password}'"
    
    try:
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                "success": True,
                "message": "Login successful",
                "user": {
                    "id": user[0],
                    "username": user[1],
                    "full_name": user[3],
                    "phone": user[4],
                    "email": user[5],
                    "plan_type": user[7],
                    "data_limit": user[8]
                }
            }
        else:
            return JSONResponse(
                status_code=401,
                content={"success": False, "message": "Invalid credentials"}
            )
    except Exception as e:
        conn.close()
        # VULNERABLE: Exposing error details
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"Database error: {str(e)}"}
        )

@app.get("/api/customers")
async def get_all_customers():
    """
    VULNERABLE: No authentication required!
    Returns all customer data
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, username, full_name, phone_number, email, address, plan_type FROM customers")
    customers = cursor.fetchall()
    conn.close()
    
    return {
        "total": len(customers),
        "customers": [
            {
                "id": c[0],
                "username": c[1],
                "full_name": c[2],
                "phone": c[3],
                "email": c[4],
                "address": c[5],
                "plan": c[6]
            } for c in customers
        ]
    }

@app.get("/api/plans")
async def get_plans():
    """Get available subscription plans"""
    plans = [
        {"id": 1, "name": "Basic GSM", "type": "GSM", "price": 199, "data": "1GB/day", "validity": 28},
        {"id": 2, "name": "Smart 4G", "type": "4G", "price": 299, "data": "2GB/day", "validity": 28},
        {"id": 3, "name": "Premium 4G", "type": "4G", "price": 499, "data": "3GB/day", "validity": 56},
        {"id": 4, "name": "Ultra 5G", "type": "5G", "price": 699, "data": "Unlimited", "validity": 28},
        {"id": 5, "name": "Elite 5G", "type": "5G", "price": 999, "data": "Unlimited", "validity": 84},
    ]
    return {"plans": plans}

@app.get("/api/customer/{username}")
async def get_customer(username: str):
    """
    VULNERABLE: No authentication, exposes customer data
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM customers WHERE username=?", (username,))
    customer = cursor.fetchone()
    conn.close()
    
    if customer:
        return {
            "id": customer[0],
            "username": customer[1],
            "password": customer[2],  # VULNERABLE: Exposing password!
            "full_name": customer[3],
            "phone": customer[4],
            "email": customer[5],
            "address": customer[6],
            "plan_type": customer[7],
            "data_limit": customer[8]
        }
    else:
        raise HTTPException(status_code=404, detail="Customer not found")

@app.get("/api/query", response_class=HTMLResponse)
async def query_interface():
    """
    SQL Query Interface - EXTREMELY VULNERABLE!
    Allows executing arbitrary SQL queries
    """
    return FileResponse("app/static/sql_console.html")

@app.post("/api/execute_query")
async def execute_query(request: Request):
    """
    CRITICAL VULNERABILITY: Execute arbitrary SQL queries!
    No authentication, no input validation
    """
    data = await request.json()
    query = data.get("query", "")
    
    if not query:
        return {"error": "No query provided"}
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        cursor.execute(query)
        
        # If it's a SELECT query, return results
        if query.strip().upper().startswith("SELECT"):
            results = cursor.fetchall()
            columns = [description[0] for description in cursor.description] if cursor.description else []
            
            return {
                "success": True,
                "columns": columns,
                "rows": results,
                "row_count": len(results)
            }
        else:
            # For INSERT, UPDATE, DELETE
            conn.commit()
            return {
                "success": True,
                "message": f"Query executed successfully. Rows affected: {cursor.rowcount}",
                "rows_affected": cursor.rowcount
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "query": query
        }
    finally:
        conn.close()

@app.get("/api/database/tables")
async def list_tables():
    """
    VULNERABLE: List all database tables
    No authentication required!
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    conn.close()
    
    return {
        "tables": [table[0] for table in tables]
    }

@app.get("/api/database/dump")
async def dump_database():
    """
    CRITICAL VULNERABILITY: Dump entire database!
    Returns ALL data including admin credentials
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    data = {}
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [table[0] for table in cursor.fetchall()]
    
    for table in tables:
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({table})")
        columns = [col[1] for col in cursor.fetchall()]
        
        data[table] = {
            "columns": columns,
            "rows": rows,
            "count": len(rows)
        }
    
    conn.close()
    
    return {
        "database": "customers.db",
        "total_tables": len(tables),
        "data": data
    }

@app.get("/admin/profile")
async def admin_profile_page():
    """
    Admin Profile Update Page - VULNERABLE FILE UPLOAD!
    No authentication required, accepts any file type
    """
    return FileResponse("app/static/admin_profile.html")

@app.post("/admin/upload_profile")
async def upload_profile_image(file: UploadFile = File(...)):
    """
    CRITICAL VULNERABILITY: Unrestricted File Upload!
    - No file type validation
    - No authentication
    - Files are executable
    - Can upload web shells (PHP, Python, etc.)
    """
    try:
        # VULNERABILITY: Accept ANY file without validation
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        
        # Save the uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Make it executable (CRITICAL SECURITY FLAW!)
        os.chmod(file_path, 0o755)
        
        return {
            "success": True,
            "message": "Profile image uploaded successfully",
            "filename": file.filename,
            "url": f"/uploads/{file.filename}",
            "access_url": f"http://192.168.15.120:9090/uploads/{file.filename}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/uploads/{filename}")
async def access_upload(filename: str, request: Request):
    """
    Access uploaded files - VULNERABLE!
    If file is a Python script, it gets executed
    """
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    # VULNERABILITY: Execute Python files when accessed
    if filename.endswith('.py'):
        try:
            # Get query parameters for CGI-style scripts
            query_string = str(request.query_params)
            
            # Set up environment for CGI-style execution
            env = os.environ.copy()
            env['QUERY_STRING'] = query_string
            env['REQUEST_METHOD'] = 'GET'
            
            # Execute the Python file (WEB SHELL!)
            result = subprocess.run(
                ['python3', file_path],
                capture_output=True,
                text=True,
                timeout=10,
                env=env
            )
            
            # Return as HTML response
            return HTMLResponse(content=result.stdout)
        except Exception as e:
            return HTMLResponse(content=f"<html><body><h1>Error</h1><pre>{str(e)}</pre></body></html>")
    
    # Return the file normally
    return FileResponse(file_path)

@app.post("/shell/execute")
async def execute_shell_command(request: Request):
    """
    CRITICAL VULNERABILITY: Remote Command Execution!
    Allows executing arbitrary system commands
    Used for pivoting to NTRO network
    """
    data = await request.json()
    command = data.get("command", "")
    
    if not command:
        return {"error": "No command provided"}
    
    try:
        # VULNERABILITY: Execute arbitrary commands
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        return {
            "success": True,
            "command": command,
            "output": result.stdout,
            "error": result.stderr,
            "return_code": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Command timed out"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/pivot/ntro")
async def pivot_to_ntro():
    """
    Test connectivity to NTRO portal from customer portal
    Shows that customer portal can reach NTRO (pivot point)
    """
    import httpx
    
    try:
        async with httpx.AsyncClient() as client:
            # Try to reach NTRO portal
            response = await client.get("http://192.168.15.151:8080/health", timeout=5.0)
            
            return {
                "success": True,
                "message": "Can reach NTRO portal!",
                "ntro_status": response.json(),
                "pivot_possible": True
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Cannot reach NTRO portal"
        }

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "customer-portal"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)

