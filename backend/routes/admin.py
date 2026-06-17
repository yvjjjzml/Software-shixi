# -*- coding: utf-8 -*-
"""管理员路由"""
from flask import Blueprint, request, g
from app import get_db
from utils import make_response, login_required, admin_required

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/api/admin/users', methods=['GET'])
@login_required
@admin_required
def admin_users():
    db = get_db()
    rows = db.execute("SELECT id, username, nickname, role, created_at FROM users").fetchall()
    return make_response(200, [dict(r) for r in rows])


@admin_bp.route('/api/admin/notes', methods=['GET'])
@login_required
@admin_required
def admin_notes():
    db = get_db()
    rows = db.execute("SELECT n.*, u.username FROM notes n JOIN users u ON n.user_id=u.id ORDER BY n.updated_at DESC LIMIT 100").fetchall()
    return make_response(200, [dict(r) for r in rows])


@admin_bp.route('/api/admin/users/<int:user_id>', methods=['DELETE'])
@login_required
@admin_required
def admin_delete_user(user_id):
    db = get_db()
    db.execute("DELETE FROM notes WHERE user_id=?", (user_id,))
    db.execute("DELETE FROM users WHERE id=?", (user_id,))
    db.commit()
    return make_response(200, msg='用户已删除')
