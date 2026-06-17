#!/usr/bin/env python3
"""
全平台作品批量采集脚本
逐平台打开创作者中心 → snapshot提取 → POST到工厂API

用法:
  python3 scripts/batch_collect_works.py [--platform zhihu|bilibili|douyin|xiaohongshu|shipinhao|csdn|all]

依赖: Kimi WebBridge (localhost:10086), 工厂 API (192.168.31.32:8195)

PITFALLS (2026.6.16 已验证):
  - SPA 页面用 snapshot accessibility tree 提取，不是 innerText
  - 懒加载内容无法用 scrollTo 触发
  - 每次运行可能只采集到当前可见的内容
"""

import subprocess, json, time, sys, urllib.request, os

WEBRIDGE = 'http://127.0.0.1:10086/command'
FACTORY_BASE = 'http://192.168.31.32:8195/api/v1'

env_path = os.path.expanduser('~') + '/project/xinhe-marketing-factory/cli/.env'
with open(env_path) as f:
    for line in f:
        if line.startswith('API_TOKEN='):
            API_TOKEN = line.strip().split('=', 1)[1]
            break


def webbridge(action, args=None, session='collector'):
    body = {'action': action, 'session': session}
    if args:
        body['args'] = args
    req = urllib.request.Request(
        WEBRIDGE,
        data=json.dumps(body).encode(),
        headers={'Content-Type': 'application/json'}
    )
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read())


def api(method, path, data=None):
    url = FACTORY_BASE + path
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header('Authorization', 'Bearer ' + API_TOKEN)
    req.add_header('Content-Type', 'application/json')
    try:
        resp = urllib.request.urlopen(req)
        return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return {'error': e.code, 'items': []}


def get_snapshot_text(session):
    """获取页面 snapshot 的 accessibility tree 文本"""
    result = webbridge('snapshot', {}, session)
    if result.get('ok'):
        return str(result['data']['tree'])
    return ''


# 各平台采集配置
PLATFORMS = {
    'shipinhao': {
        'url': 'https://channels.weixin.qq.com/platform',
        'username': '绘梦心河',
        'content_type': 'video',
        'keywords': ['数模', 'Paper', 'Vibe', '中青杯', '亚太杯', '建模'],
    },
    'douyin': {
        'url': 'https://creator.douyin.com/creator-micro/content/manage',
        'username': '心河Paper',
        'content_type': 'short_video',
        'keywords': ['数模', 'VibeCoding', 'Paper', '心河', '亚太', '中青', '建模', '教程'],
    },
    'xiaohongshu': {
        'url': 'https://creator.xiaohongshu.com/new/home',
        'username': 'Ai个锤子🔨',
        'content_type': 'image_text',
        'keywords': ['数模', 'Paper', '心河', '教程', '亚太', '中青', 'Vibe', '论文'],
    },
    'bilibili': {
        'url': 'https://member.bilibili.com/platform/content-manager/video',
        'username': '是小小河呀',
        'content_type': 'video',
        'keywords': ['数模', '建模', 'Vibe', 'Paper', '心河', '教程', '亚太', '中青', '山东', '农林', 'Latex'],
    },
    'zhihu': {
        'url': 'https://www.zhihu.com/creator',
        'username': '论文不会鸭',
        'content_type': 'article',
        'keywords': ['中青杯', '数模', '心河', 'Paper', '教程', '论文', 'Vibe', 'LaTeX', '模板', '排版'],
    },
    'csdn': {
        'url': 'https://mp.csdn.net/mp_blog/manage/article',
        'username': '论文不会鸭',
        'content_type': 'article',
        'keywords': ['中青杯', '数模', '心河', 'Paper', '教程', 'Vibe'],
    },
}


def collect_platform(platform, config):
    """采集单个平台的作品"""
    print(f"\n=== {platform} ({config['username']}) ===")
    
    webbridge('navigate', {'url': config['url'], 'newTab': True})
    time.sleep(5)
    
    # 尝试滚动加载
    for i in range(3):
        webbridge('evaluate', {
            'code': 'window.scrollTo(0, document.body.scrollHeight)'
        })
        time.sleep(1.5)
    
    tree = get_snapshot_text('collector')
    if not tree:
        print("  ⚠ snapshot 为空")
        return 0
    
    # 提取标题
    import re
    all_text = re.findall(r"name': '([^']{15,250})'", tree)
    works = []
    seen = set()
    
    for t in all_text:
        clean = t.replace('\\n', ' ').strip()
        if len(clean) < 15:
            continue
        if any(k in clean for k in config['keywords']):
            key = clean[:50]
            if key not in seen:
                seen.add(key)
                works.append(clean)
    
    print(f"  提取到 {len(works)} 条")
    
    # 获取账号 ID
    accounts = api('GET', '/social-accounts?page_size=30')
    acct_id = None
    for a in accounts.get('items', []):
        if a['platform'] == platform and a['username'] == config['username']:
            acct_id = a['id']
            break
    
    if not acct_id:
        print(f"  ❌ 找不到账号")
        return 0
    
    # 获取已有作品去重
    existing = api('GET', '/works?page_size=100')
    existing_keys = set()
    for w in existing.get('items', []):
        if w['platform'] == platform:
            existing_keys.add((w.get('title', '')[:50]))
    
    # 创建作品
    created = 0
    for title in works:
        if title[:50] in existing_keys:
            continue
        
        result = api('POST', '/works', {
            'platform': platform,
            'account_id': acct_id,
            'content_type': config['content_type'],
            'title': title[:200],
            'published_at': '2026-06-01T12:00:00Z',
            'status': 'published',
        })
        if result.get('id'):
            created += 1
            print(f"  ✅ {title[:70]}")
    
    webbridge('close_session')
    return created


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else 'all'
    
    total = 0
    for platform, config in PLATFORMS.items():
        if target not in ('all', platform):
            continue
        try:
            n = collect_platform(platform, config)
            total += n
        except Exception as e:
            print(f"  ❌ {platform}: {e}")
    
    print(f"\n=== 总计新录入 {total} 条 ===")


if __name__ == '__main__':
    main()
