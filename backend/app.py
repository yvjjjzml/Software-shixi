# -*- coding: utf-8 -*-
"""
AI智能知识管理工作台 - Flask后端
模块化架构，蓝图路由
"""
import os
import sqlite3
from flask import Flask, g, send_from_directory
from flask_cors import CORS
from config.config import DB_PATH, DIST_DIR

# ============================================================
# Flask App
# ============================================================
app = Flask(__name__, static_folder=DIST_DIR, static_url_path='')
CORS(app)

# ============================================================
# 数据库
# ============================================================
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exc):
    db = g.pop('db', None)
    if db:
        db.close()

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            nickname TEXT,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT,
            summary TEXT,
            tags TEXT,
            category TEXT,
            status TEXT DEFAULT 'draft',
            is_public INTEGER DEFAULT 0,
            view_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            count INTEGER DEFAULT 0
        );
    ''')
    conn.close()

init_db()

# ============================================================
# 注册蓝图
# ============================================================
from routes.auth import auth_bp
from routes.notes import notes_bp
from routes.ai import ai_bp
from routes.dashboard import dashboard_bp
from routes.search import search_bp
from routes.admin import admin_bp
from routes.tags import tags_bp
from routes.templates import templates_bp
from routes.demo import demo_bp

app.register_blueprint(auth_bp)
app.register_blueprint(notes_bp)
app.register_blueprint(ai_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(search_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(tags_bp)
app.register_blueprint(templates_bp)
app.register_blueprint(demo_bp)

# ============================================================
# 前端路由
# ============================================================
@app.route('/')
def serve_index():
    return send_from_directory(DIST_DIR, 'index.html')

@app.errorhandler(404)
def catch_all(e):
    from flask import request
    if '/api/' in request.path:
        from utils import make_response
        return make_response(404, msg='接口不存在')
    return send_from_directory(DIST_DIR, 'index.html')

# ============================================================
# 启动
# ============================================================
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
