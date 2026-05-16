# app.py — Flask application updated for Azure SQL
# This version connects to Azure SQL Database instead of SQLite
# Deployed on Azure App Service (after Day 7 migration)
# Database: Azure SQL Database (migrated from SQLite on Day 6)

import pyodbc
import os
from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# ── Database connection ────────────────────────────────
# Credentials read from environment variables
# Never hardcoded — security best practice
def get_db():
    conn_string = (
        "Driver={ODBC Driver 18 for SQL Server};"
        f"Server={os.environ.get('SQL_SERVER')};"
        f"Database={os.environ.get('SQL_DATABASE')};"
        f"Uid={os.environ.get('SQL_USERNAME')};"
        f"Pwd={os.environ.get('SQL_PASSWORD')};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
    )
    return pyodbc.connect(conn_string)

# ── HTML Template ──────────────────────────────────────
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Migration App — Azure SQL</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 900px;
               margin: 40px auto; padding: 0 20px; background: #f5f5f5; }
        .header { background: #0078d4; color: white;
                  padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .badge { background: #50e6ff; color: #003a4c; padding: 4px 10px;
                 border-radius: 4px; font-size: 13px; font-weight: bold; }
        table { width: 100%; border-collapse: collapse; background: white;
                border-radius: 8px; overflow: hidden; }
        th { background: #0078d4; color: white; padding: 12px; text-align: left; }
        td { padding: 10px 12px; border-bottom: 1px solid #eee; }
        tr:hover { background: #f0f7ff; }
        .info { background: #e8f4fd; padding: 12px; border-radius: 6px;
                margin-bottom: 16px; border-left: 4px solid #0078d4; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Product Inventory System</h1>
        <span class="badge">AZURE CLOUD — POST-MIGRATION</span>
        <p style="margin:8px 0 0">
            Database: Azure SQL Database |
            Server: {{ server }}
        </p>
    </div>
    <div class="info">
        ✅ This application has been migrated to Azure cloud services.
        Database is now Azure SQL Database (was SQLite on-premises).
    </div>
    <h2>Products ({{ count }} total)</h2>
    <table>
        <tr>
            <th>ID</th><th>Name</th><th>Description</th>
            <th>Price (₹)</th><th>Stock</th>
        </tr>
        {% for p in products %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p.name }}</td>
            <td>{{ p.description }}</td>
            <td>{{ "%.2f"|format(p.price) }}</td>
            <td>{{ p.stock }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
'''

# ── Routes ─────────────────────────────────────────────
@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products ORDER BY id')
    rows = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    products = [
        dict(zip(columns, row)) for row in rows
    ]
    conn.close()
    return render_template_string(
        HTML_TEMPLATE,
        products=products,
        count=len(products),
        server=os.environ.get('SQL_SERVER', 'unknown')
    )

@app.route('/api/products', methods=['GET'])
def get_products():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    rows = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    products = [dict(zip(columns, row)) for row in rows]
    conn.close()
    return jsonify(products)

@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.get_json()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO products (name, description, price, stock) VALUES (?,?,?,?)',
        (data['name'], data.get('description',''),
         data['price'], data.get('stock', 0))
    )
    conn.commit()
    conn.close()
    return jsonify({'message': 'Product added'}), 201

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'environment': 'azure-app-service',
        'database': 'azure-sql',
        'server': os.environ.get('SQL_SERVER', 'unknown')
    })

@app.route('/api/migration-log')
def migration_log():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM migration_log ORDER BY logged_at DESC'
    )
    rows = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    logs = [dict(zip(columns, row)) for row in rows]
    conn.close()
    return jsonify(logs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)