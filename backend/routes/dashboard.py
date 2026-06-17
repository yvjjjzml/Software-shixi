# -*- coding: utf-8 -*-
"""仪表盘路由"""
from datetime import datetime, timedelta
from flask import Blueprint, g
from app import get_db
from utils import make_response, login_required

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/api/dashboard/stats', methods=['GET'])
@login_required
def dashboard_stats():
    db = get_db()
    user_id = g.user_id
    total = db.execute("SELECT COUNT(*) FROM notes WHERE user_id=?", (user_id,)).fetchone()[0]
    published = db.execute("SELECT COUNT(*) FROM notes WHERE user_id=? AND status='published'", (user_id,)).fetchone()[0]
    draft = db.execute("SELECT COUNT(*) FROM notes WHERE user_id=? AND status='draft'", (user_id,)).fetchone()[0]
    archived = db.execute("SELECT COUNT(*) FROM notes WHERE user_id=? AND status='archived'", (user_id,)).fetchone()[0]
    views = db.execute("SELECT COALESCE(SUM(view_count),0) FROM notes WHERE user_id=?", (user_id,)).fetchone()[0]

    trend = []
    for i in range(6, -1, -1):
        day = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        cnt = db.execute("SELECT COUNT(*) FROM notes WHERE user_id=? AND DATE(created_at)=?", (user_id, day)).fetchone()[0]
        trend.append({'date': day, 'count': cnt})

    tag_rows = db.execute("SELECT tags FROM notes WHERE user_id=? AND tags IS NOT NULL AND tags!=''", (user_id,)).fetchall()
    tag_counts = {}
    for row in tag_rows:
        for t in row['tags'].split(','):
            t = t.strip()
            if t:
                tag_counts[t] = tag_counts.get(t, 0) + 1
    tag_data = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]

    heatmap = []
    for d in range(7):
        day = (datetime.now() - timedelta(days=d)).strftime('%Y-%m-%d')
        for h in range(24):
            cnt = db.execute("SELECT COUNT(*) FROM notes WHERE user_id=? AND DATE(created_at)=? AND CAST(strftime('%H',created_at) AS INTEGER)=?",
                             (user_id, day, h)).fetchone()[0]
            if cnt > 0:
                heatmap.append([d, h, cnt])

    scatter_rows = db.execute("SELECT LENGTH(content) as wc, view_count FROM notes WHERE user_id=?", (user_id,)).fetchall()
    scatter = [[r['wc'], r['view_count']] for r in scatter_rows]

    return make_response(200, {
        'total_notes': total, 'published': published, 'draft': draft, 'archived': archived,
        'total_views': views, 'trend': trend, 'tags': [{'name': t[0], 'count': t[1]} for t in tag_data],
        'heatmap': heatmap, 'scatter': scatter
    })


@dashboard_bp.route('/api/dashboard/wordcloud', methods=['GET'])
@login_required
def dashboard_wordcloud():
    db = get_db()
    tag_rows = db.execute("SELECT tags FROM notes WHERE user_id=? AND tags IS NOT NULL AND tags!=''", (g.user_id,)).fetchall()
    tag_counts = {}
    for row in tag_rows:
        for t in row['tags'].split(','):
            t = t.strip()
            if t:
                tag_counts[t] = tag_counts.get(t, 0) + 1
    return make_response(200, [{'name': k, 'value': v} for k, v in tag_counts.items()])
