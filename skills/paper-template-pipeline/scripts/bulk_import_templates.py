#!/usr/bin/env python3
"""
心河Paper 模板批量导入脚本
通过 Kimi WebBridge 自动化浏览器操作，从 GitHub 仓库批量创建模板到心河Paper平台。

依赖: Kimi WebBridge (localhost:10086), Python 3.9+

用法:
  python3 bulk_import_templates.py <templates.csv>
  python3 bulk_import_templates.py --single --repo <name> --name "显示名称" ...

CSV 格式 (无表头):
  repo_name,display_name,description,tags,category,branch,subdir

关键技巧:
  使用 Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set
  来触发 React controlled input 的状态更新。直接 .value = 赋值无效。
  详见: kimi-webbridge skill → references/react-controlled-inputs.md
"""

import json
import os
import sys
import time
import csv
import argparse
import urllib.request
from pathlib import Path

WEBBRIDGE_URL = "http://127.0.0.1:10086/command"
SESSION = "hermes"
BASE_URL = "https://paper.huimengxinhe.com/writing/new"


def wb_call(action, args=None, timeout=15):
    body = {"action": action, "session": SESSION}
    if args:
        body["args"] = args
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        WEBBRIDGE_URL, data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read())
    except Exception as e:
        return {"ok": False, "error": str(e)}


def wb_click(selector):
    r = wb_call("click", {"selector": selector})
    return r.get("ok", False)


def wb_fill(selector, value):
    r = wb_call("fill", {"selector": selector, "value": value})
    return r.get("ok", False)


def wb_eval(code):
    r = wb_call("evaluate", {"code": code})
    if r.get("ok") and "data" in r:
        return r["data"].get("value", "")
    return ""


def wb_navigate(url):
    r = wb_call("navigate", {"url": url, "newTab": False})
    return r.get("ok", False)


def wb_wait_for_inputs(expected_count=6, max_wait=10.0):
    start = time.time()
    while time.time() - start < max_wait:
        code = (
            "(function(){"
            "var inp=document.querySelectorAll('input,textarea');"
            "var result=[];"
            "for(var i=0;i<inp.length;i++){"
            "result.push({idx:i,ph:inp[i].placeholder||'',tag:inp[i].tagName});"
            "}"
            "return JSON.stringify(result)"
            "})()"
        )
        result = wb_eval(code)
        if result:
            try:
                items = json.loads(result)
                if len(items) >= expected_count:
                    return items
            except (json.JSONDecodeError, ValueError):
                pass
        time.sleep(0.5)
    return []


def fill_import_form(repo, name, desc, tags, branch="main", subdir="."):
    """使用原生 value setter 触发 React controlled input 状态更新"""
    url = "https://github.com/iftaken/" + repo
    values = [url, branch, subdir, name, desc, tags]
    code = (
        "(function(){"
        "var nis=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set;"
        "var nts=Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype,'value').set;"
        "var vals=" + json.dumps(values) + ";"
        "var inp=document.querySelectorAll('input,textarea');"
        "for(var i=0;i<vals.length&&i<inp.length;i++){"
        "var el=inp[i],v=vals[i];"
        "if(el.tagName==='TEXTAREA')nts.call(el,v);else nis.call(el,v);"
        "el.dispatchEvent(new Event('input',{bubbles:true}));"
        "el.dispatchEvent(new Event('change',{bubbles:true}));"
        "}"
        "return 'filled_'+vals.length+'fields'"
        "})()"
    )
    wb_eval(code)
    time.sleep(0.5)

    # Click 添加 button for tags
    wb_eval(
        "(function(){"
        "var btns=document.querySelectorAll('button');"
        "for(var i=0;i<btns.length;i++){"
        "if(btns[i].textContent.trim()==='添加'){btns[i].click();break;}"
        "}})"
    )
    time.sleep(0.3)
    return True


def click_confirm():
    refs = wb_snapshot_refs()
    for ref, name in refs:
        if name == "确认导入":
            wb_click(ref)
            time.sleep(3)
            return True
    wb_eval(
        "(function(){"
        "var b=[...document.querySelectorAll('button')]"
        ".find(function(x){return x.textContent.trim()==='确认导入'});"
        "if(b)b.click();"
        "})()"
    )
    time.sleep(3)
    return True


def wb_snapshot_refs():
    import re
    r = wb_call("snapshot", {})
    if not r.get("ok"):
        return []
    tree = str(r.get("data", {}).get("tree", ""))
    return re.findall(r"'ref': '(@e\d+)'.*?'name': '([^']+)'", tree)


def open_import_dialog():
    wb_eval(
        "(function(){"
        "var b=[...document.querySelectorAll('button')]"
        ".find(function(x){return x.textContent.trim()==='新增模板'});"
        "if(b)b.click();"
        "})()"
    )
    time.sleep(1.5)
    wb_eval(
        "(function(){"
        "var b=[...document.querySelectorAll('button')]"
        ".find(function(x){return x.textContent.includes('GitHub')||x.textContent.includes('Gitee')});"
        "if(b)b.click();"
        "})()"
    )
    time.sleep(2)
    inputs = wb_wait_for_inputs(6)
    if not inputs:
        print("    ERROR: Form inputs did not appear")
        return False
    print("    Found", len(inputs), "form inputs")
    return True


def ensure_my_templates_tab():
    wb_eval(
        "(function(){"
        "var tabs=document.querySelectorAll('[role=tab],button');"
        "for(var i=0;i<tabs.length;i++){"
        "if(tabs[i].textContent.trim()==='我的模板'){tabs[i].click();return;}"
        "}"
        "})()"
    )
    time.sleep(1)
    return True


def import_one_template(repo, name, desc, tags, category="期刊论文",
                        branch="main", subdir="."):
    print("\n  Importing:", repo, "->", name)
    wb_navigate(BASE_URL)
    time.sleep(3)
    ensure_my_templates_tab()
    if not open_import_dialog():
        return False
    fill_import_form(repo, name, desc, tags, branch, subdir)
    click_confirm()
    time.sleep(2)
    result = wb_eval(
        "(function(){"
        "return document.body.textContent.includes(" + json.dumps(name) + ")?'found':'not_found'"
        "})()"
    )
    success = "found" in str(result)
    status = "OK" if success else "VERIFY"
    print("    Result:", status)
    return success


def main():
    parser = argparse.ArgumentParser(description="心河Paper 模板批量导入")
    parser.add_argument("csv_file", nargs="?", help="CSV 文件路径")
    parser.add_argument("--single", action="store_true")
    parser.add_argument("--repo")
    parser.add_argument("--name")
    parser.add_argument("--desc", default="")
    parser.add_argument("--tags", default="")
    parser.add_argument("--category", default="期刊论文")
    parser.add_argument("--branch", default="main")
    parser.add_argument("--subdir", default=".")
    parser.add_argument("--start-from", type=int, default=0)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    # Check WebBridge
    print("Checking WebBridge...")
    try:
        import subprocess as sp
        result = sp.run(
            [os.path.expanduser("~/.kimi-webbridge/bin/kimi-webbridge"), "status"],
            capture_output=True, text=True, timeout=10
        )
        if '"running":true' in result.stdout and '"extension_connected":true' in result.stdout:
            print("WebBridge connected")
        else:
            print("WebBridge not ready")
            sys.exit(1)
    except Exception as e:
        print("WebBridge error:", e)
        sys.exit(1)

    if args.single:
        success = import_one_template(
            args.repo, args.name, args.desc, args.tags,
            args.category, args.branch, args.subdir
        )
        print("\nSuccess" if success else "\nCheck manually")
        return

    csv_path = Path(args.csv_file)
    templates = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or row[0].startswith("#"):
                continue
            if len(row) >= 4:
                templates.append({
                    "repo": row[0].strip(),
                    "name": row[1].strip(),
                    "desc": row[2].strip() if len(row) > 2 else "",
                    "tags": row[3].strip() if len(row) > 3 else "",
                    "category": row[4].strip() if len(row) > 4 else "期刊论文",
                    "branch": row[5].strip() if len(row) > 5 else "main",
                    "subdir": row[6].strip() if len(row) > 6 else ".",
                })

    print("\nLoaded", len(templates), "templates from", csv_path)
    if args.dry_run:
        for i, t in enumerate(templates):
            print(" ", i, t["repo"], "->", t["name"])
        return

    ok = 0
    fail = 0
    for i, t in enumerate(templates):
        if i < args.start_from:
            continue
        print("\n[" + str(i+1) + "/" + str(len(templates)) + "]", end="")
        try:
            if import_one_template(t["repo"], t["name"], t["desc"], t["tags"],
                                   t["category"], t["branch"], t["subdir"]):
                ok += 1
            else:
                fail += 1
        except Exception as e:
            print("    EXCEPTION:", e)
            fail += 1
        if (i + 1) % 5 == 0:
            print("\n  Progress:", ok, "OK,", fail, "FAIL. Pausing 3s...")
            time.sleep(3)

    print("\n" + "=" * 50)
    print("Final:", ok, "succeeded,", fail, "failed out of", len(templates))
    print("=" * 50)


if __name__ == "__main__":
    main()
