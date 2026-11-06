"""Generates data/ingredients.json and data/customers.json from the GDD tables."""
import json, pathlib
TAGS = ["sweet", "sour", "bitter", "strong", "aroma", "body"]
def t(*v): return dict(zip(TAGS, v))
ING = [
 # id, zh, en, polarity(-1/0/1), is_emotion, tags, color
 ("base",     "基酒", "Base Spirit", 0, False, t(0,0,0,80,0,20),   "#d9d9d9"),
 ("soda",     "苏打", "Soda",        0, False, t(0,0,0,0,0,0),     "#eeeeee"),
 ("calm",     "安心", "Calm",        1, True,  t(50,0,0,10,30,50), "#f3e3c3"),
 ("joy",      "喜悦", "Joy",         1, True,  t(60,40,0,20,50,20),"#f2c94c"),
 ("courage",  "勇气", "Courage",     1, True,  t(10,30,0,60,30,30),"#f2994a"),
 ("longing",  "思念", "Longing",     0, True,  t(30,0,20,0,80,30), "#b7a6d9"),
 ("fear",     "恐惧", "Fear",       -1, True,  t(0,70,20,40,10,20),"#8fb39a"),
 ("anger",    "愤怒", "Anger",      -1, True,  t(0,20,30,90,10,40),"#8b2f2f"),
 ("loneliness","孤独","Loneliness", -1, True,  t(10,10,40,10,40,20),"#6f86a6"),
 ("regret",   "悔恨", "Regret",     -1, True,  t(0,20,70,30,20,60),"#8a5a2b"),
 ("despair",  "绝望", "Despair",    -1, True,  t(0,0,80,50,0,80),  "#2e1f3a"),
]
ingredients = {i[0]: {"zh": i[1], "en": i[2], "polarity": i[3], "is_emotion": i[4], "tags": i[5], "color": i[6]} for i in ING}
def g(**kw): return {k: list(v) for k, v in kw.items()}
customers = {
 "zhou":   {"zh":"小周","en":"Zhou","dump":"fear","gift":"courage","nights":[1],
            "mouth":None,"true":g(strong=(45,70),sour=(15,35),aroma=(15,35)),"mine":["sour",45]},
 "lin":    {"zh":"林阿姨","en":"Mrs. Lin","dump":"loneliness","gift":"longing","nights":[1],
            "mouth":g(sweet=(30,50),body=(30,50),strong=(0,20)),"true":g(aroma=(45,70),sweet=(15,30),bitter=(8,20)),"mine":["strong",40]},
 "zhe":    {"zh":"阿哲","en":"Zhe","dump":"anger","gift":"joy","nights":[2],
            "mouth":g(strong=(50,75),bitter=(15,35),sour=(0,20)),"true":g(strong=(0,20),body=(35,60),sweet=(25,45)),"mine":["sour",40]},
 "oldk":   {"zh":"老K","en":"Old K","dump":"regret","gift":"joy","nights":[2,4,5],
            "mouth":g(sweet=(30,50),aroma=(30,60),bitter=(0,10)),"true":g(strong=(50,75),body=(10,30),aroma=(0,10)),"mine":None,
            "pure":True},
 "xu":     {"zh":"许然","en":"Xu Ran","dump":"regret","gift":"calm","nights":[3],
            "mouth":g(sweet=(35,55),aroma=(30,50),bitter=(0,10)),"true":g(bitter=(18,35),body=(35,55),sweet=(15,30)),"mine":["sweet",60]},
 "xiaoman":{"zh":"小满","en":"Xiaoman","dump":"fear","gift":None,"nights":[4],
            "mouth":g(strong=(0,20),sweet=(30,50),sour=(10,30)),"true":g(sweet=(20,40),sour=(25,45),strong=(25,45)),"mine":["body",50]},
 "yu":     {"zh":"余","en":"Yu","dump":"despair","gift":None,"nights":[1,3,5],
            "mouth":None,"true":g(sweet=(25,40),bitter=(12,25),body=(30,50)),"mine":None,
            "locked_until_despair":True},
}
d = pathlib.Path(__file__).resolve().parent.parent / "data"
(d/"ingredients.json").write_text(json.dumps(ingredients, ensure_ascii=False, indent=2))
(d/"customers.json").write_text(json.dumps(customers, ensure_ascii=False, indent=2))
print("ok")
