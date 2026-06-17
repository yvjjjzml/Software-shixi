# -*- coding: utf-8 -*-
"""演示数据路由"""
import random
from datetime import datetime, timedelta
from flask import Blueprint, g
from app import get_db
from utils import make_response, login_required

demo_bp = Blueprint('demo', __name__)


@demo_bp.route('/api/demo/init', methods=['POST'])
@login_required
def init_demo_data():
    db = get_db()
    user_id = g.user_id
    count = db.execute("SELECT COUNT(*) FROM notes WHERE user_id=?", (user_id,)).fetchone()[0]
    if count > 0:
        return make_response(200, msg='已有数据，无需重复初始化')

    demo_notes = [
        {'title': 'Python Flask框架入门指南', 'content': 'Flask是一个轻量级的Python Web框架。\n\n## 核心概念\n\n1. 路由装饰器\n2. 请求处理\n3. 响应格式化\n4. 蓝图组织', 'category': '技术笔记', 'status': 'published', 'tags': 'Python,Flask,Web开发'},
        {'title': 'Vue3组合式API学习总结', 'content': 'Vue3的组合式API是全新的组件逻辑组织方式。\n\n## ref和reactive\n\nref用于基本类型，reactive用于对象。\n\n## computed\n\n计算属性，自动追踪依赖。', 'category': '技术笔记', 'status': 'published', 'tags': 'Vue3,前端,JavaScript'},
        {'title': '数据库设计原则与实践', 'content': '良好的数据库设计是系统稳定运行的基础。\n\n## 范式化\n\n- 第一范式：字段不可再分\n- 第二范式：完全依赖主键\n- 第三范式：不传递依赖', 'category': '技术笔记', 'status': 'published', 'tags': '数据库,SQL,设计'},
        {'title': '人工智能发展史回顾', 'content': 'AI发展经历了多次起伏。\n\n## 发展阶段\n\n- 1956年达特茅斯会议\n- 2012年AlexNet\n- 2016年AlphaGo\n- 2020s大模型时代', 'category': '学习资料', 'status': 'published', 'tags': 'AI,人工智能,深度学习'},
        {'title': '项目管理方法论总结', 'content': '有效的项目管理是开发成功的关键。\n\n## Scrum框架\n\n- Sprint迭代\n- 每日站会\n- Sprint评审\n- 回顾会议', 'category': '学习资料', 'status': 'published', 'tags': '项目管理,敏捷,Scrum'},
        {'title': 'Git常用命令速查', 'content': 'Git是分布式版本控制系统。\n\n```bash\ngit init\ngit add .\ngit commit -m "msg"\ngit push\n```', 'category': '工具笔记', 'status': 'published', 'tags': 'Git,版本控制'},
        {'title': 'RESTful API设计规范', 'content': 'RESTful API是前后端分离的核心。\n\n- GET查询\n- POST创建\n- PUT更新\n- DELETE删除', 'category': '技术笔记', 'status': 'published', 'tags': 'API,REST,后端'},
        {'title': 'Markdown语法指南', 'content': 'Markdown是轻量级标记语言。\n\n# 标题\n**粗体** *斜体*\n\n```python\nprint("hello")\n```', 'category': '工具笔记', 'status': 'published', 'tags': 'Markdown,文档'},
        {'title': '软件测试方法与实践', 'content': '软件测试保证代码质量。\n\n## 测试分类\n\n1. 单元测试\n2. 集成测试\n3. 系统测试\n4. 验收测试', 'category': '技术笔记', 'status': 'published', 'tags': '测试,TDD,质量'},
        {'title': '个人学习计划', 'content': '本周计划：\n\n1. Vue3组合式API\n2. Flask API开发\n3. 数据库优化\n4. 代码整洁之道', 'category': '个人笔记', 'status': 'draft', 'tags': '学习,计划'},
    ]

    now = datetime.now()
    day_offsets = [0, 0, 0, 1, 1, 2, 2, 3, 4, 5]
    for i, note in enumerate(demo_notes):
        day_off = day_offsets[i]
        created = (now - timedelta(days=day_off, hours=random.randint(0, 23))).strftime('%Y-%m-%d %H:%M:%S')
        updated = (now - timedelta(days=day_off, hours=random.randint(0, 12))).strftime('%Y-%m-%d %H:%M:%S')
        db.execute("""INSERT INTO notes (user_id, title, content, summary, tags, category, status, is_public, view_count, created_at, updated_at)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                   (user_id, note['title'], note['content'], '', note['tags'], note['category'],
                    note['status'], 1, random.randint(20, 500), created, updated))

    for note in demo_notes:
        for tag in note['tags'].split(','):
            tag = tag.strip()
            if tag:
                existing = db.execute("SELECT id FROM tags WHERE name=?", (tag,)).fetchone()
                if existing:
                    db.execute("UPDATE tags SET count=count+1 WHERE name=?", (tag,))
                else:
                    db.execute("INSERT INTO tags (name, count) VALUES (?, 1)", (tag,))

    db.commit()
    return make_response(200, msg='演示数据初始化成功，共创建10条笔记')
