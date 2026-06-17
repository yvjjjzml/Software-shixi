# -*- coding: utf-8 -*-
"""工具函数"""
import hashlib
import json
import base64
import requests
from functools import wraps
from flask import request, jsonify, g
from config.config import DEEPSEEK_API_KEY, DEEPSEEK_API_URL


def make_response(code=200, data=None, msg=''):
    return jsonify({'code': code, 'data': data, 'msg': msg})


def hash_password(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()


def call_deepseek(messages, max_tokens=1500):
    try:
        resp = requests.post(
            DEEPSEEK_API_URL,
            headers={'Authorization': f'Bearer {DEEPSEEK_API_KEY}', 'Content-Type': 'application/json'},
            json={'model': 'deepseek-chat', 'messages': messages, 'max_tokens': max_tokens},
            timeout=30
        )
        result = resp.json()
        return result['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f'AI服务调用失败: {str(e)}'


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', '')
        if not auth.startswith('Bearer '):
            return make_response(401, msg='未登录')
        try:
            payload = json.loads(base64.b64decode(auth[7:]))
            g.user_id = payload.get('uid')
            g.username = payload.get('username')
            if not g.user_id:
                return make_response(401, msg='Token无效')
        except Exception:
            return make_response(401, msg='Token无效')
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        from app import get_db
        db = get_db()
        user = db.execute("SELECT role FROM users WHERE id=?", (g.user_id,)).fetchone()
        if not user or user['role'] != 'admin':
            return make_response(403, msg='无权限')
        return f(*args, **kwargs)
    return decorated
