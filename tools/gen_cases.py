import json, random, pathlib
from reference import mix, grade, ING, CUS, ROOT
random.seed(7)
cases = [  # GDD example solutions
 ("zhou",   [("courage",45)], .10), ("lin", [("longing",45)], .20),
 ("zhe",    [("calm",45)], .20),    ("oldk", [("base",60)], .20),
 ("xu",     [("regret",15),("longing",45),("calm",30)], .10),
 ("xiaoman",[("joy",30),("courage",15),("base",15)], .10),
 ("yu",     [("longing",30),("calm",15)], .10),
 # edge cases: infection, mine, mouth-only, pure violation
 ("xu",     [("regret",30),("calm",60)], .20),
 ("zhou",   [("fear",60)], .10),
 ("lin",    [("calm",45),("soda",15)], .10),
 ("oldk",   [("base",60),("longing",15)], .20),
]
ids = list(ING)
for _ in range(40):
    n = random.randint(1, 3)
    parts = [(i, random.choice([15, 30, 45, 60])) for i in random.sample(ids, n)]
    cases.append((random.choice(list(CUS)), parts, random.choice([.1, .2, .3, .4])))
out = []
for cid, parts, d in cases:
    p = [{"id": i, "ml": ml} for i, ml in parts]
    r = mix(p, d)
    for unlocked in ([False, True] if cid == "yu" else [False]):
        out.append({"customer": cid, "parts": p, "dilution": d, "yu_unlocked": unlocked,
                    "expect": {**r, "judge": grade(r, cid, unlocked)}})
(ROOT/"tests/expected_cases.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
from collections import Counter
print(len(out), "cases", Counter(c["expect"]["judge"]["grade"] for c in out))
for c in out[:12]: print(c["customer"], [(x["id"],x["ml"]) for x in c["parts"]], c["dilution"], c["yu_unlocked"], c["expect"]["judge"]["grade"], "infected" if c["expect"]["judge"]["infected"] else "")
