# -*- coding: utf-8 -*-
"""标签路由"""
from flask import Blueprint, g
from app import get_db
from utils import make_response, login_required

tags_bp = Blueprint('tags', __name__)


@tags_bp.route('/api/tags', methods=['GET'])
def get_tags():
    db = get_db()
    rows = db.execute("SELECT name, count FROM tags WHERE count>0 ORDER BY count DESC").fetchall()
    return make_response(200, [dict(r) for r in rows])


@tags_bp.route('/api/tags/<name>', methods=['DELETE'])
@login_required
def delete_tag(name):
    db = get_db()
    notes = db.execute("SELECT id, tags FROM notes WHERE user_id=? AND tags LIKE ?", (g.user_id, f'%{name}%')).fetchall()
    for note in notes:
        tags = [t.strip() for t in (note['tags'] or '').split(',') if t.strip() and t.strip() != name]
        db.execute("UPDATE notes SET tags=? WHERE id=?", (','.join(tags), note['id']))
    db.execute("DELETE FROM tags WHERE name=?", (name,))
    db.commit()
    return make_response(200, msg='标签已删除')
