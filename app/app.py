# app.py — Simulated on-premises Flask application
# This app runs on an Azure VM simulating an on-premises server
# It will be migrated to Azure App Service + Azure SQL in Phase 3

import sqlite3
import os
from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)
DB_PATH = '/home/azureuser/flaskapp/app.db'

# ── Database setup ─────────────────────────────────────
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            stock INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS migration_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event TEXT NOT NULL,
            details TEXT,
            logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Insert sample data if table is empty
    count = conn.execute('SELECT COUNT(*) FROM products').fetchone()[0]
    if count == 0:
        sample_products = [
            ('Laptop', 'High performance laptop', 75000.00, 15),
            ('Monitor', '27 inch 4K monitor', 32000.00, 8),
            ('Keyboard', 'Mechanical keyboard', 5500.00, 25),
            ('Mouse', 'Wireless ergonomic mouse', 3200.00, 30),
            ('Headset', 'Noise cancelling headset', 12000.00, 12),
        ]
        conn.executemany(
            'INSERT INTO products (name, description, price, stock) VALUES (?,?,?,?)',
            sample_products
        )
        conn.execute(
            "INSERT INTO migration_log (event, details) VALUES (?,?)",
            ('DB_INIT', 'Database initialised with sample product data on on-premises VM')
        )
    conn.commit()
    conn.close()

# ── HTML Template ──────────────────────────────────────
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>On-Premises App — Pre-Migration</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 900px;
               margin: 40px auto; padding: 0 20px; background: #f5f5f5; }
        .header { background: #d9534f; color: white;
                  padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .badge { background: #f0ad4e; color: #333; padding: 4px 10px;
                 border-radius: 4px; font-size: 13px; font-weight: bold; }
        table { width: 100%; border-collapse: collapse; background: white;
                border-radius: 8px; overflow: hidden; }
        th { background: #333; color: white; padding: 12px; text-align: left; }
        td { padding: 10px 12px; border-bottom: 1px solid #eee; }
        tr:hover { background: #f9f9f9; }
        .info { background: #fff3cd; padding: 12px; border-radius: 6px;
                margin-bottom: 16px; border-left: 4px solid #ffc107; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Product Inventory System</h1>
        <span class="badge">ON-PREMISES SERVER — PRE-MIGRATION</span>
        <p style="margin:8px 0 0">Running on: Azure VM (Ubuntu 22.04) |
           Database: SQLite | Web server: Nginx + Gunicorn</p>
    </div>
    <div class="info">
        ⚠️ This application is running on a simulated on-premises server.
        It will be migrated to Azure App Service + Azure SQL Database.
    </div>
    <h2>Products ({{ count }} total)</h2>
    <table>
        <tr>
            <th>ID</th><th>Name</th><th>Description</th>
            <th>Price (₹)</th><th>Stock</th>
        </tr>
        {% for p in products %}
        <tr>
            <td>{{ p['id'] }}</td>
            <td>{{ p['name'] }}</td>
            <td>{{ p['description'] }}</td>
            <td>{{ "%.2f"|format(p['price']) }}</td>
            <td>{{ p['stock'] }}</td>
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
    products = conn.execute('SELECT * FROM products ORDER BY id').fetchall()
    conn.close()
    return render_template_string(
        HTML_TEMPLATE,
        products=products,
        count=len(products)
    )

@app.route('/api/products', methods=['GET'])
def get_products():
    conn = get_db()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return jsonify([dict(p) for p in products])

@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.get_json()
    conn = get_db()
    conn.execute(
        'INSERT INTO products (name, description, price, stock) VALUES (?,?,?,?)',
        (data['name'], data.get('description',''), data['price'], data.get('stock', 0))
    )
    conn.commit()
    conn.close()
    return jsonify({'message': 'Product added'}), 201

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'environment': 'on-premises-vm',
        'database': 'sqlite',
        'server': 'nginx+gunicorn'
    })

@app.route('/api/migration-log')
def migration_log():
    conn = get_db()
    logs = conn.execute(
        'SELECT * FROM migration_log ORDER BY logged_at DESC'
    ).fetchall()
    conn.close()
    return jsonify([dict(l) for l in logs])

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=False)
