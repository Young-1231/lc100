#!/usr/bin/env python3
"""构建并自测「算法基础 / 经典算法」板块。

- 扫描 data/algos/*.json(每个算法一个文件)
- 对每个算法的每一种『写法』:在独立命名空间里 exec(code),再 exec(test_code),
  以此验证代码可运行且正确(test_code 内用 assert 自检)
- 校验与 data/algo_families.json 的一致性(每个 algo_id 都有文件,反之亦然)
- 生成 data/algos.json 索引(给列表页用)

用法:
    python3 scripts/build_algos.py            # 构建 + 自测,失败则退出码 1
    python3 scripts/build_algos.py --no-test  # 只重建索引,跳过自测(不推荐)
"""
from __future__ import annotations

import argparse
import json
import signal
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ALGOS_DIR = ROOT / "data" / "algos"
FAMILIES_FILE = ROOT / "data" / "algo_families.json"
INDEX_FILE = ROOT / "data" / "algos.json"

REQUIRED_FIELDS = ["id", "title", "category", "family", "tags", "summary",
                   "idea", "complexity", "variants"]
TIMEOUT_SEC = 8


class TimeoutError_(Exception):
    pass


def _alarm(signum, frame):
    raise TimeoutError_("execution exceeded time limit")


def run_variant(algo: dict, variant: dict) -> tuple[bool, str]:
    """在隔离命名空间里跑一种写法的 code + test_code。返回 (ok, message)。"""
    code = variant.get("code", "")
    test = variant.get("test_code") or algo.get("test_code") or ""
    if not code.strip():
        return False, "空 code"
    if not test.strip():
        return False, "缺少 test_code(算法级与写法级都没有)"
    ns: dict = {}
    has_alarm = hasattr(signal, "SIGALRM")
    if has_alarm:
        signal.signal(signal.SIGALRM, _alarm)
        signal.alarm(TIMEOUT_SEC)
    try:
        exec(compile(code, f"<{algo['id']}:{variant.get('title','?')}:code>", "exec"), ns)
        exec(compile(test, f"<{algo['id']}:{variant.get('title','?')}:test>", "exec"), ns)
        return True, "ok"
    except Exception:
        return False, traceback.format_exc(limit=4)
    finally:
        if has_alarm:
            signal.alarm(0)


def validate_algo(algo: dict) -> list[str]:
    errs = []
    for f in REQUIRED_FIELDS:
        if f not in algo or algo[f] in (None, "", []):
            errs.append(f"缺少字段 {f}")
    cx = algo.get("complexity", {})
    if isinstance(cx, dict):
        for k in ("avg", "space"):
            if not cx.get(k):
                errs.append(f"complexity.{k} 为空")
    if not isinstance(algo.get("variants"), list) or not algo["variants"]:
        errs.append("variants 必须是非空数组")
    return errs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-test", action="store_true", help="跳过代码自测")
    args = ap.parse_args()

    families = json.loads(FAMILIES_FILE.read_text(encoding="utf-8"))
    fam_order = []  # [(family_key, algo_id), ...] 保序
    for fkey, fam in families.items():
        for aid in fam.get("algo_ids", []):
            fam_order.append((fkey, aid))

    files = sorted(ALGOS_DIR.glob("*.json"))
    algos_by_id: dict[str, dict] = {}
    hard_errors = 0

    for fp in files:
        try:
            algo = json.loads(fp.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"❌ {fp.name}: JSON 解析失败 — {e}")
            hard_errors += 1
            continue
        aid = algo.get("id") or fp.stem
        if aid != fp.stem:
            print(f"⚠️  {fp.name}: id='{aid}' 与文件名不一致")
        errs = validate_algo(algo)
        if errs:
            print(f"❌ {fp.name}: " + "; ".join(errs))
            hard_errors += 1
            continue
        algos_by_id[aid] = algo

    # 一致性:families 引用的 id 都要有文件
    declared = {aid for _, aid in fam_order}
    for _, aid in fam_order:
        if aid not in algos_by_id:
            print(f"❌ algo_families.json 引用了 '{aid}' 但缺少 data/algos/{aid}.json")
            hard_errors += 1
    for aid in algos_by_id:
        if aid not in declared:
            print(f"⚠️  data/algos/{aid}.json 未被任何家族引用(不会出现在列表里)")

    # 自测:跑每种写法的 code + test
    test_total = test_fail = 0
    if not args.no_test:
        print("\n—— 代码自测 ——")
        for fkey, aid in fam_order:
            algo = algos_by_id.get(aid)
            if not algo:
                continue
            for v in algo.get("variants", []):
                test_total += 1
                ok, msg = run_variant(algo, v)
                if not ok:
                    test_fail += 1
                    print(f"❌ [{aid}] 写法「{v.get('title','?')}」自测失败:\n{msg}")
        passed = test_total - test_fail
        print(f"\n自测结果:{passed}/{test_total} 写法通过"
              + ("" if test_fail == 0 else f" ,{test_fail} 个失败"))

    # 生成索引(按家族顺序;未被引用的文件追加在末尾)
    index = []
    seen = set()
    for _, aid in fam_order:
        algo = algos_by_id.get(aid)
        if not algo:
            continue
        seen.add(aid)
        cx = algo.get("complexity", {})
        index.append({
            "id": algo["id"],
            "title": algo["title"],
            "category": algo.get("category", ""),
            "family": algo.get("family", ""),
            "tags": algo.get("tags", []),
            "summary": algo.get("summary", ""),
            "complexity_brief": cx.get("avg") or cx.get("worst") or "",
            "n_variants": len(algo.get("variants", [])),
        })
    for aid, algo in algos_by_id.items():
        if aid in seen:
            continue
        cx = algo.get("complexity", {})
        index.append({
            "id": algo["id"], "title": algo["title"],
            "category": algo.get("category", ""), "family": algo.get("family", ""),
            "tags": algo.get("tags", []), "summary": algo.get("summary", ""),
            "complexity_brief": cx.get("avg") or cx.get("worst") or "",
            "n_variants": len(algo.get("variants", [])),
        })

    INDEX_FILE.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n✅ 写入索引 data/algos.json — {len(index)} 个算法")

    if hard_errors or test_fail:
        print(f"\n构建未通过:{hard_errors} 个结构错误,{test_fail} 个自测失败。")
        return 1
    print("\n🎉 全部通过。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
