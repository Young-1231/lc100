#!/usr/bin/env python3
"""把 data/statements.json 里的完整题面合并进 data/problems/p####.json。

data/statements.json 是题面的「源」(authored source),结构为:
    { "1": { "description": "...", "examples": [...], "constraints": [...],
             "follow_up": "..." }, ... }   # key 为题号字符串

每题的 statement 对象会被写入对应 p####.json 的 "statement" 字段。
幂等:重复运行只覆盖 statement 字段,不动其它内容。
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROBLEMS_DIR = ROOT / "data" / "problems"
STATEMENTS = ROOT / "data" / "statements.json"


def main() -> int:
    if not STATEMENTS.exists():
        print(f"✗ 找不到 {STATEMENTS}")
        return 1
    statements = json.loads(STATEMENTS.read_text(encoding="utf-8"))

    applied, missing = 0, []
    for pid, stmt in statements.items():
        pid = int(pid)
        path = PROBLEMS_DIR / f"p{pid:04d}.json"
        if not path.exists():
            missing.append(pid)
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        data["statement"] = stmt
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        applied += 1

    # 报告覆盖情况
    have = {int(p) for p in statements}
    all_ids = {int(p.stem[1:]) for p in PROBLEMS_DIR.glob("p*.json")}
    no_stmt = sorted(all_ids - have)

    print(f"✓ 已写入 {applied} 题的题面")
    if missing:
        print(f"⚠ statements.json 里有 {len(missing)} 题找不到对应文件: {missing}")
    if no_stmt:
        print(f"⚠ 还有 {len(no_stmt)} 题没有题面: {no_stmt}")
    else:
        print("✓ 全部 100 题都有题面")
    return 0


if __name__ == "__main__":
    sys.exit(main())
