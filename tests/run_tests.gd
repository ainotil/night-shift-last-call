extends SceneTree
## Run: godot --headless --path . --script res://tests/run_tests.gd
## Compares FlavorCalc / Judge against tools/reference.py outputs in expected_cases.json.

const FlavorCalc := preload("res://scripts/flavor_calc.gd")
const Judge := preload("res://scripts/judge.gd")
const EPS := 1e-6


func _init() -> void:
	var ingredients := FlavorCalc.load_json("res://data/ingredients.json")
	var customers := FlavorCalc.load_json("res://data/customers.json")
	var f := FileAccess.open("res://tests/expected_cases.json", FileAccess.READ)
	var cases: Array = JSON.parse_string(f.get_as_text())
	var failed := 0
	for i in cases.size():
		var c: Dictionary = cases[i]
		var e: Dictionary = c["expect"]
		var r := FlavorCalc.mix(c["parts"], c["dilution"], ingredients)
		var j := Judge.grade(r, customers[c["customer"]], c["yu_unlocked"])
		var errs := []
		for k in FlavorCalc.TAGS:
			if absf(r["tags"][k] - e["tags"][k]) > EPS:
				errs.append("%s %f != %f" % [k, r["tags"][k], e["tags"][k]])
		for k in ["total_ml", "negative_share", "emotion_ml"]:
			if absf(r[k] - e[k]) > EPS:
				errs.append("%s %f != %f" % [k, r[k], e[k]])
		var ej: Dictionary = e["judge"]
		for k in ["grade", "infected", "mine"]:
			if j[k] != ej[k]:
				errs.append("%s %s != %s" % [k, j[k], ej[k]])
		for k in ["true_hits", "mouth_hits"]:
			if int(j[k]) != int(ej[k]):
				errs.append("%s %s != %s" % [k, j[k], ej[k]])
		if JSON.stringify(j["misses"]) != JSON.stringify(ej["misses"]):
			errs.append("misses %s != %s" % [j["misses"], ej["misses"]])
		if not errs.is_empty():
			failed += 1
			printerr("case %d (%s): %s" % [i, c["customer"], ", ".join(errs)])
	# technique helpers
	if not is_equal_approx(FlavorCalc.dilution_after("stir", 10.0), 0.2): failed += 1; printerr("stir 10s")
	if not is_equal_approx(FlavorCalc.dilution_after("shake", 30.0), 0.4): failed += 1; printerr("shake cap")
	if FlavorCalc.cue_ready("shake", 0.16): failed += 1; printerr("shake cue early")
	print("%d/%d cases passed" % [cases.size() - min(failed, cases.size()), cases.size()])
	quit(1 if failed > 0 else 0)
