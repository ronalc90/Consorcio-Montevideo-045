"""Inspeccionar data.json y comparativa.json para el análisis 03."""
import json
from pathlib import Path

ROOT = Path(r"C:\Users\johan albeiro\Documents\Johan\Consorcio-Montevideo-045")

data = json.load(open(ROOT / "data.json", "r", encoding="utf-8"))
comp = json.load(open(ROOT / "comparativa.json", "r", encoding="utf-8"))

print("=== data.json ===")
if isinstance(data, dict):
    print("keys:", list(data.keys()))
    if "civs" in data:
        civs = data["civs"]
        print("civs len:", len(civs))
        print("primer civ:", json.dumps(civs[0], ensure_ascii=False, indent=2)[:2000])
        print("segundo civ:", json.dumps(civs[1], ensure_ascii=False, indent=2)[:1000])

print()
print("=== comparativa.json ===")
if isinstance(comp, dict):
    print("keys:", list(comp.keys()))
    for k in comp.keys():
        v = comp[k]
        if isinstance(v, list):
            print(f"  {k}: list len={len(v)}")
            if v:
                print(f"    primer elem: {json.dumps(v[0], ensure_ascii=False, indent=2)[:800]}")
        elif isinstance(v, dict):
            print(f"  {k}: dict keys={list(v.keys())[:20]}")
        else:
            print(f"  {k}: {type(v).__name__} = {v}")
