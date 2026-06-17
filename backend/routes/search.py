# -*- coding: utf-8 -*-
"""搜索路由"""
from flask import Blueprint, request, g
from app import get_db
from utils import make_response, login_required

search_bp = Blueprint('search', __name__)


@search_bp.route('/api/search', methods=['GET'])
@login_required
def search_notes():
    keyword = request.args.get('keyword', '').strip()
    category = request.args.get('category', '')
    tag = request.args.get('tag', '')
    db = get_db()
    query = "SELECT * FROM notes WHERE user_id=?"
    params = [g.user_id]
    if keyword:
        query += " AND (title LIKE ? OR content LIKE ? OR tags LIKE ?)"
        kw = f'%{keyword}%'
        params.extend([kw, kw, kw])
    if category:
        query += " AND category=?"
        params.append(category)
    if tag:
        query += " AND tags LIKE ?"
        params.append(f'%{tag}%')
    query += " ORDER BY updated_at DESC LIMIT 50"
    rows = db.execute(query, params).fetchall()
    return make_response(200, [dict(r) for r in rows])
