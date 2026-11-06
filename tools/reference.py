"""Reference implementation of the flavor model and grading rules (GDD: 调酒与评价).
FlavorCalc.gd / Judge.gd must produce identical results; gen_cases.py writes the expected outputs."""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
ING = json.loads((ROOT/"data/ingredients.json").read_text())
CUS = json.loads((ROOT/"data/customers.json").read_text())
TAGS = ["sweet", "sour", "bitter", "strong", "aroma", "body"]
INFECT = 0.25

def mix(parts, dilution):
    raw = sum(p["ml"] for p in parts)
    total = raw * (1 + dilution)
    tags = {k: sum(ING[p["id"]]["tags"][k] * p["ml"] for p in parts) / total for k in TAGS}
    neg = sum(p["ml"] for p in parts if ING[p["id"]]["polarity"] < 0)
    emo = sum(p["ml"] for p in parts if ING[p["id"]]["is_emotion"])
    return {"tags": tags, "raw_ml": raw, "total_ml": total,
            "negative_share": neg / total, "emotion_ml": emo}

def check(tags, goal):
    hits, misses = 0, []
    for k, (lo, hi) in goal.items():
        v = tags[k]
        if v < lo: misses.append({"tag": k, "dir": "low"})
        elif v > hi: misses.append({"tag": k, "dir": "high"})
        else: hits += 1
    return hits, misses

def grade(res, cid, yu_unlocked=False):
    c = CUS[cid]
    out = {"infected": res["negative_share"] > INFECT, "mine": False}
    if c["mine"] and res["tags"][c["mine"][0]] > c["mine"][1]:
        out.update(grade="miss", mine=True, true_hits=0, mouth_hits=0, misses=[])
        return out
    th, misses = check(res["tags"], c["true"])
    if c.get("pure") and res["emotion_ml"] > 0:
        misses.append({"tag": "pure", "dir": "high"})
    true_ok = th == 3 and not (c.get("pure") and res["emotion_ml"] > 0)
    mh = check(res["tags"], c["mouth"])[0] if c["mouth"] else 0
    locked = c.get("locked_until_despair") and not yu_unlocked
    if true_ok and not out["infected"] and not locked: g = "read"
    elif true_ok or th >= 2 or mh == 3: g = "pass"
    else: g = "miss"
    out.update(grade=g, true_hits=th, mouth_hits=mh, misses=misses)
    return out
