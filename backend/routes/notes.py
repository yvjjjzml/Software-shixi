# -*- coding: utf-8 -*-
"""笔记路由"""
from datetime import datetime
from flask import Blueprint, request, Response, g
from app import get_db
from utils import make_response, login_required

notes_bp = Blueprint('notes', __name__)


@notes_bp.route('/api/notes', methods=['GET'])
@login_required
def get_notes():
    db = get_db()
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    offset = (page - 1) * per_page
    total = db.execute("SELECT COUNT(*) FROM notes WHERE user_id=?", (g.user_id,)).fetchone()[0]
    rows = db.execute("SELECT * FROM notes WHERE user_id=? ORDER BY updated_at DESC LIMIT ? OFFSET ?",
                      (g.user_id, per_page, offset)).fetchall()
    return make_response(200, {'notes': [dict(r) for r in rows], 'total': total, 'page': page, 'per_page': per_page})


@notes_bp.route('/api/notes', methods=['POST'])
@login_required
def create_note():
    data = request.get_json()
    title = data.get('title', '').strip()
    if not title:
        return make_response(400, msg='标题不能为空')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db = get_db()
    db.execute("""INSERT INTO notes (user_id, title, content, summary, tags, category, status, is_public, created_at, updated_at)
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
               (g.user_id, title, data.get('content', ''), data.get('summary', ''),
                data.get('tags', ''), data.get('category', ''), data.get('status', 'draft'),
                data.get('is_public', 0), now, now))
    db.commit()
    note_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
    note = db.execute("SELECT * FROM notes WHERE id=?", (note_id,)).fetchone()
    return make_response(200, dict(note), '创建成功')


@notes_bp.route('/api/notes/<int:note_id>', methods=['GET'])
@login_required
def get_note(note_id):
    db = get_db()
    note = db.execute("SELECT * FROM notes WHERE id=? AND user_id=?", (note_id, g.user_id)).fetchone()
    if not note:
        return make_response(404, msg='笔记不存在')
    db.execute("UPDATE notes SET view_count=view_count+1 WHERE id=?", (note_id,))
    db.commit()
    note = db.execute("SELECT * FROM notes WHERE id=?", (note_id,)).fetchone()
    return make_response(200, dict(note))


@notes_bp.route('/api/notes/<int:note_id>', methods=['PUT'])
@login_required
def update_note(note_id):
    db = get_db()
    note = db.execute("SELECT * FROM notes WHERE id=? AND user_id=?", (note_id, g.user_id)).fetchone()
    if not note:
        return make_response(404, msg='笔记不存在')
    data = request.get_json()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db.execute("""UPDATE notes SET title=?, content=?, summary=?, tags=?, category=?, is_public=?, updated_at=?
                  WHERE id=?""",
               (data.get('title', note['title']), data.get('content', note['content']),
                data.get('summary', note['summary']), data.get('tags', note['tags']),
                data.get('category', note['category']), data.get('is_public', note['is_public']),
                now, note_id))
    db.commit()
    updated = db.execute("SELECT * FROM notes WHERE id=?", (note_id,)).fetchone()
    return make_response(200, dict(updated), '更新成功')


@notes_bp.route('/api/notes/<int:note_id>', methods=['DELETE'])
@login_required
def delete_note(note_id):
    db = get_db()
    note = db.execute("SELECT * FROM notes WHERE id=? AND user_id=?", (note_id, g.user_id)).fetchone()
    if not note:
        return make_response(404, msg='笔记不存在')
    db.execute("DELETE FROM notes WHERE id=?", (note_id,))
    db.commit()
    return make_response(200, msg='删除成功')


@notes_bp.route('/api/notes/<int:note_id>/status', methods=['PUT'])
@login_required
def update_note_status(note_id):
    db = get_db()
    note = db.execute("SELECT * FROM notes WHERE id=? AND user_id=?", (note_id, g.user_id)).fetchone()
    if not note:
        return make_response(404, msg='笔记不存在')
    data = request.get_json()
    new_status = data.get('status', '')
    if new_status not in ('draft', 'published', 'archived'):
        return make_response(400, msg='无效状态')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db.execute("UPDATE notes SET status=?, updated_at=? WHERE id=?", (new_status, now, note_id))
    db.commit()
    return make_response(200, msg='状态已更新')


@notes_bp.route('/api/notes/import', methods=['POST'])
@login_required
def import_note():
    if 'file' not in request.files:
        return make_response(400, msg='请上传文件')
    file = request.files['file']
    if not file.filename:
        return make_response(400, msg='文件名为空')
    ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
    if ext not in ('txt', 'md', 'markdown'):
        return make_response(400, msg='只支持 .txt 和 .md 文件')
    content = file.read().decode('utf-8', errors='ignore')
    title = file.filename.rsplit('.', 1)[0]
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db = get_db()
    db.execute("""INSERT INTO notes (user_id, title, content, tags, category, status, is_public, created_at, updated_at)
                  VALUES (?, ?, ?, ?, ?, 'draft', 0, ?, ?)""",
               (g.user_id, title, content, '', '导入', now, now))
    db.commit()
    note_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
    note = db.execute("SELECT * FROM notes WHERE id=?", (note_id,)).fetchone()
    return make_response(200, dict(note), '导入成功')


@notes_bp.route('/api/notes/<int:note_id>/export', methods=['GET'])
@login_required
def export_note(note_id):
    db = get_db()
    note = db.execute("SELECT * FROM notes WHERE id=? AND user_id=?", (note_id, g.user_id)).fetchone()
    if not note:
        return make_response(404, msg='笔记不存在')
    md = f"# {note['title']}\n\n"
    md += f"**分类**: {note['category'] or '无'} | **标签**: {note['tags'] or '无'} | **状态**: {note['status']}\n\n"
    md += f"---\n\n{note['content']}"
    if note['summary']:
        md += f"\n\n---\n\n**AI摘要**: {note['summary']}"
    return Response(md, mimetype='text/markdown',
                    headers={'Content-Disposition': f'attachment; filename="{note["title"]}.md"'})
