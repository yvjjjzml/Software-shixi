# -*- coding: utf-8 -*-
"""模板路由"""
from flask import Blueprint
from utils import make_response, login_required

templates_bp = Blueprint('templates', __name__)


@templates_bp.route('/api/templates', methods=['GET'])
@login_required
def get_templates():
    templates = [
        {'id': 'meeting', 'name': '会议记录', 'icon': '📋', 'content': '# 会议记录\n\n**日期**: \n**参会人**: \n\n## 议题\n\n\n## 决议\n\n1. \n2. \n'},
        {'id': 'daily', 'name': '每日总结', 'icon': '📝', 'content': '# 每日总结\n\n**日期**: \n\n## 完成\n\n1. \n\n## 明日计划\n\n1. \n'},
        {'id': 'study', 'name': '学习笔记', 'icon': '📚', 'content': '# 学习笔记\n\n**主题**: \n**来源**: \n\n## 核心概念\n\n\n## 总结\n\n'},
        {'id': 'project', 'name': '项目方案', 'icon': '🏗️', 'content': '# 项目方案\n\n## 背景\n\n\n## 目标\n\n\n## 技术方案\n\n\n## 计划\n\n'},
        {'id': 'bug', 'name': 'Bug报告', 'icon': '🐛', 'content': '# Bug报告\n\n**严重程度**: \n\n## 描述\n\n\n## 复现步骤\n\n1. \n\n## 解决方案\n\n'},
        {'id': 'review', 'name': '读书笔记', 'icon': '📖', 'content': '# 读书笔记\n\n**书名**: \n**作者**: \n**评分**: ⭐⭐⭐⭐⭐\n\n## 核心观点\n\n\n## 摘录\n\n> \n'},
    ]
    return make_response(200, templates)
