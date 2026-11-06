class_name FlavorCalc
extends RefCounted
## Flavor model from the GDD (调酒与评价). Pure logic, no scene dependencies.
## Must stay in sync with tools/reference.py — run tests/run_tests.gd after any change.

const TAGS: Array[String] = ["sweet", "sour", "bitter", "strong", "aroma", "body"]
const INFECT_THRESHOLD := 0.25

# Technique tuning (GDD first pass; tune after the colour-block prototype).
const DILUTION_RATE := {"stir": 0.02, "shake": 0.04}   # per second
const DILUTION_CAP := 0.40
const CUE_AT := {"stir": 0.15, "shake": 0.20}          # 起雾 / 结霜 cue thresholds


static func load_json(path: String) -> Dictionary:
	var f := FileAccess.open(path, FileAccess.READ)
	assert(f != null, "Cannot open %s" % path)
	var data = JSON.parse_string(f.get_as_text())
	assert(data is Dictionary, "%s is not a JSON object" % path)
	return data


## parts: [{"id": "courage", "ml": 45}, ...]; dilution: 0.0–0.4 (melt water / raw volume).
## Returns {tags, raw_ml, total_ml, negative_share, emotion_ml}.
static func mix(parts: Array, dilution: float, ingredients: Dictionary) -> Dictionary:
	var raw := 0.0
	var neg := 0.0
	var emo := 0.0
	var sums := {}
	for k in TAGS:
		sums[k] = 0.0
	for p in parts:
		var ing: Dictionary = ingredients[p["id"]]
		var ml := float(p["ml"])
		raw += ml
		if ing["polarity"] < 0:
			neg += ml
		if ing["is_emotion"]:
			emo += ml
		for k in TAGS:
			sums[k] += float(ing["tags"][k]) * ml
	var total := raw * (1.0 + dilution)
	var tags := {}
	for k in TAGS:
		tags[k] = sums[k] / total if total > 0.0 else 0.0
	return {
		"tags": tags,
		"raw_ml": raw,
		"total_ml": total,
		"negative_share": neg / total if total > 0.0 else 0.0,
		"emotion_ml": emo,
	}


## Dilution reached after holding a technique for `seconds`.
static func dilution_after(technique: String, seconds: float) -> float:
	return minf(DILUTION_RATE[technique] * seconds, DILUTION_CAP)


## True once the 起雾 / 结霜 cue should show.
static func cue_ready(technique: String, dilution: float) -> bool:
	return dilution >= CUE_AT[technique]


static func is_infected(result: Dictionary) -> bool:
	return result["negative_share"] > INFECT_THRESHOLD
