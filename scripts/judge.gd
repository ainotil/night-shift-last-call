class_name Judge
extends RefCounted
## Grading rules from the GDD (三档评价). Mirrors tools/reference.py.
## grade: "read" (wakes up) | "pass" (returns next night) | "miss" (never comes back).

const FlavorCalcScript := preload("res://scripts/flavor_calc.gd")


## Returns {grade, infected, mine, true_hits, mouth_hits, misses:[{tag, dir}]}.
## misses drive the customer's reaction line (each tag has a "too high" and "too low" line).
static func grade(result: Dictionary, customer: Dictionary, yu_unlocked := false) -> Dictionary:
	var tags: Dictionary = result["tags"]
	var out := {"infected": FlavorCalcScript.is_infected(result), "mine": false}

	var mine = customer.get("mine")
	if mine != null and tags[mine[0]] > float(mine[1]):
		out.merge({"grade": "miss", "mine": true, "true_hits": 0, "mouth_hits": 0, "misses": []}, true)
		return out

	var t := _check(tags, customer["true"])
	var true_hits: int = t["hits"]
	var misses: Array = t["misses"]
	var impure: bool = customer.get("pure", false) and result["emotion_ml"] > 0.0
	if impure:
		misses.append({"tag": "pure", "dir": "high"})
	var true_ok := true_hits == 3 and not impure

	var mouth_hits := 0
	if customer.get("mouth") != null:
		mouth_hits = _check(tags, customer["mouth"])["hits"]

	var locked: bool = customer.get("locked_until_despair", false) and not yu_unlocked

	var g := "miss"
	if true_ok and not out["infected"] and not locked:
		g = "read"
	elif true_ok or true_hits >= 2 or mouth_hits == 3:
		g = "pass"
	out.merge({"grade": g, "true_hits": true_hits, "mouth_hits": mouth_hits, "misses": misses}, true)
	return out


static func _check(tags: Dictionary, goal: Dictionary) -> Dictionary:
	var hits := 0
	var misses := []
	for k in goal:
		var lo := float(goal[k][0])
		var hi := float(goal[k][1])
		var v: float = tags[k]
		if v < lo:
			misses.append({"tag": k, "dir": "low"})
		elif v > hi:
			misses.append({"tag": k, "dir": "high"})
		else:
			hits += 1
	return {"hits": hits, "misses": misses}
