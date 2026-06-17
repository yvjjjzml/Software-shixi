# -*- coding: utf-8 -*-
"""AI功能路由"""
from flask import Blueprint, request, g
from app import get_db
from utils import make_response, call_deepseek, login_required

ai_bp = Blueprint('ai', __name__)


@ai_bp.route('/api/ai/summarize', methods=['POST'])
@login_required
def ai_summarize():
    data = request.get_json()
    content = data.get('content', '').strip()
    if not content:
        return make_response(400, msg='内容不能为空')
    messages = [
        {"role": "system", "content": "你是一个专业的文本摘要助手。请用简洁的中文生成摘要，不超过200字。"},
        {"role": "user", "content": f"请为以下内容生成摘要：\n\n{content[:3000]}"}
    ]
    result = call_deepseek(messages)
    note_id = data.get('note_id')
    if note_id:
        db = get_db()
        db.execute("UPDATE notes SET summary=? WHERE id=?", (result, note_id))
        db.commit()
    return make_response(200, {'summary': result})


@ai_bp.route('/api/ai/auto-tag', methods=['POST'])
@login_required
def ai_auto_tag():
    data = request.get_json()
    content = data.get('content', '').strip()
    if not content:
        return make_response(400, msg='内容不能为空')
    messages = [
        {"role": "system", "content": "你是一个标签提取助手。请从内容中提取3-5个关键词标签，用逗号分隔，不要其他文字。"},
        {"role": "user", "content": f"提取标签：\n\n{content[:2000]}"}
    ]
    result = call_deepseek(messages)
    note_id = data.get('note_id')
    if note_id:
        db = get_db()
        db.execute("UPDATE notes SET tags=? WHERE id=?", (result, note_id))
        db.commit()
    return make_response(200, {'tags': result})


@ai_bp.route('/api/ai/ask', methods=['POST'])
@login_required
def ai_ask():
    data = request.get_json()
    question = data.get('question', '').strip()
    if not question:
        return make_response(400, msg='问题不能为空')
    db = get_db()
    notes = db.execute("SELECT title, content, tags FROM notes WHERE user_id=? ORDER BY updated_at DESC LIMIT 10",
                       (g.user_id,)).fetchall()
    context = "\n\n".join([f"【{n['title']}】标签:{n['tags']}\n{n['content'][:500]}" for n in notes])
    messages = [
        {"role": "system", "content": f"你是一个智能知识助手。根据用户的知识库回答问题。\n\n知识库内容：\n{context[:4000]}"},
        {"role": "user", "content": question}
    ]
    result = call_deepseek(messages)
    return make_response(200, {'answer': result})


@ai_bp.route('/api/ai/recommend/<int:note_id>', methods=['GET'])
@login_required
def ai_recommend(note_id):
    db = get_db()
    note = db.execute("SELECT * FROM notes WHERE id=? AND user_id=?", (note_id, g.user_id)).fetchone()
    if not note:
        return make_response(404, msg='笔记不存在')
    others = db.execute("SELECT id, title, tags FROM notes WHERE user_id=? AND id!=? ORDER BY updated_at DESC LIMIT 20",
                        (g.user_id, note_id)).fetchall()
    others_text = "\n".join([f"ID:{o['id']} 标题:{o['title']} 标签:{o['tags']}" for o in others])
    messages = [
        {"role": "system", "content": "你是推荐助手。根据当前笔记，从列表中推荐3篇最相关的笔记。只返回ID，逗号分隔。"},
        {"role": "user", "content": f"当前笔记：{note['title']}，标签：{note['tags']}\n\n候选笔记：\n{others_text}"}
    ]
    result = call_deepseek(messages)
    try:
        ids = [int(x.strip()) for x in result.split(',') if x.strip().isdigit()]
        recommended = [dict(r) for r in db.execute(f"SELECT id, title, tags FROM notes WHERE id IN ({','.join(['?']*len(ids))})", ids).fetchall()] if ids else []
    except Exception:
        recommended = []
    return make_response(200, recommended)


@ai_bp.route('/api/ai/polish', methods=['POST'])
@login_required
def ai_polish():
    data = request.get_json()
    content = data.get('content', '').strip()
    style = data.get('style', 'professional')
    if not content:
        return make_response(400, msg='内容不能为空')
    style_map = {
        'professional': '专业正式、逻辑清晰、用词精准',
        'academic': '学术论文风格、严谨客观、引用规范',
        'simple': '简洁通俗、易于理解、适合大众阅读',
        'creative': '生动有趣、富有创意、引人入胜'
    }
    style_desc = style_map.get(style, style_map['professional'])
    messages = [
        {"role": "system", "content": f"你是文字润色助手。用{style_desc}的风格改写内容，保持原意。直接输出改写内容。"},
        {"role": "user", "content": f"润色以下内容：\n\n{content[:3000]}"}
    ]
    result = call_deepseek(messages, max_tokens=2000)
    return make_response(200, {'polished': result})
