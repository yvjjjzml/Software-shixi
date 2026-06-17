# -*- coding: utf-8 -*-
"""认证路由"""
import json
import base64
from flask import Blueprint, request, g
from app import get_db
from utils import make_response, hash_password, login_required

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    nickname = data.get('nickname', username)
    if not username or not password:
        return make_response(400, msg='用户名和密码不能为空')
    if len(password) < 6:
        return make_response(400, msg='密码至少6位')
    db = get_db()
    if db.execute("SELECT id FROM users WHERE username=?", (username,)).fetchone():
        return make_response(400, msg='用户名已存在')
    db.execute("INSERT INTO users (username, password, nickname, role) VALUES (?, ?, ?, ?)",
               (username, hash_password(password), nickname, 'user'))
    db.commit()
    return make_response(200, msg='注册成功')


@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE username=? AND password=?",
                      (username, hash_password(password))).fetchone()
    if not user:
        return make_response(401, msg='用户名或密码错误')
    token = base64.b64encode(json.dumps({'uid': user['id'], 'username': user['username']}).encode()).decode()
    return make_response(200, {
        'token': token,
        'user': {'id': user['id'], 'username': user['username'], 'nickname': user['nickname'], 'role': user['role']}
    })


@auth_bp.route('/api/auth/profile', methods=['GET'])
@login_required
def get_profile():
    db = get_db()
    user = db.execute("SELECT id, username, nickname, role, created_at FROM users WHERE id=?", (g.user_id,)).fetchone()
    return make_response(200, dict(user))


@auth_bp.route('/api/auth/profile', methods=['PUT'])
@login_required
def update_profile():
    data = request.get_json()
    nickname = data.get('nickname', '').strip()
    old_pwd = data.get('old_password', '')
    new_pwd = data.get('new_password', '')
    db = get_db()
    if nickname:
        db.execute("UPDATE users SET nickname=? WHERE id=?", (nickname, g.user_id))
    if new_pwd:
        if not old_pwd:
            return make_response(400, msg='请输入旧密码')
        user = db.execute("SELECT password FROM users WHERE id=?", (g.user_id,)).fetchone()
        if hash_password(old_pwd) != user['password']:
            return make_response(400, msg='旧密码错误')
        if len(new_pwd) < 6:
            return make_response(400, msg='新密码至少6位')
        db.execute("UPDATE users SET password=? WHERE id=?", (hash_password(new_pwd), g.user_id))
    db.commit()
    user = db.execute("SELECT id, username, nickname, role, created_at FROM users WHERE id=?", (g.user_id,)).fetchone()
    return make_response(200, dict(user), '更新成功')
