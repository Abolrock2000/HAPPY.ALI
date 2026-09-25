import os
from flask import Flask, request, render_template_string, redirect, url_for, session

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")

# ============================================================
# تنظیمات قابل تغییر در Render > Environment
# ============================================================
PASSWORD = os.environ.get("BIRTHDAY_PASSWORD", "1388")
IMAGE_URL = os.environ.get("BIRTHDAY_IMAGE_URL", "").strip()

TITLE = "تولدت مبارک عشق من"
NAME = "دخترم"

BIRTHDAY_TEXT = """دخترم… ❤️

امروز فقط روز تولد تو نیست؛ روزیه که دنیا تصمیم گرفت قشنگ‌ترین اتفاقش رو به زندگی من هدیه بده.
نمی‌دونم چطور باید از حسی بنویسم که وقتی اسمت میاد، یه چیزی توی قلبم آروم می‌گیره… فقط می‌دونم از وقتی تو اومدی، «دوستت دارم» برای من دیگه یه جمله نیست؛ یه تکه از وجودمه.

دخترم، تو برای من فقط کسی نیستی که دوستش دارم… تو همون آدمی هستی که دلم می‌خواد تمام فرداهام رو کنارش ببینم؛ توی روزای خوب، توی سختی‌ها، توی خنده‌هام، حتی توی سکوت‌هام.
اگه یه روز ازم بپرسن قشنگ‌ترین چیزی که زندگی بهت داد چی بود، بدون فکر اسم تو رو میارم. چون تو برای من فقط «عشق» نیستی؛ تو خودِ آرامشی، که دلم نمی‌خواد هیچ‌وقت از دستش بدم.

تولدت مبارک دخترِ من… 🎂❤️
امیدوارم امسال، به اندازه‌ی تمام لبخندهایی که به زندگی من آوردی، خوشبختی نصیبت بشه.
و من؟ من فقط یه آرزو دارم… اینکه هر سال همین روز، هنوز کنار هم باشیم و من دوباره بهت بگم:
«تولدت مبارک دخترم… ممنونم که به دنیا اومدی و یه روز، مسیر زندگیت به من رسید.»

دوستت دارم؛ بیشتر از چیزی که بلد باشم با کلمه‌ها بگم. ❤️"""

SPECIAL_LINE = "اگر تمام دنیا را ورق بزنم، باز هم قلبم همان صفحه‌ای را انتخاب می‌کند که نام تو روی آن نوشته شده است. ❤️"

PAGE = r"""
<!doctype html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ title }} ❤️</title>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box}
body{
  margin:0; min-height:100vh; overflow-x:hidden; color:#fff;
  font-family:Vazirmatn,Tahoma,sans-serif;
  background:
    radial-gradient(circle at 50% 10%,rgba(150,0,35,.42),transparent 35%),
    linear-gradient(145deg,#080207,#240711 52%,#080207);
}
body:before{
  content:"";position:fixed;inset:0;pointer-events:none;opacity:.22;
  background-image:radial-gradient(#fff 1px,transparent 1px);
  background-size:35px 35px;
}
.container{width:min(920px,92%);margin:0 auto;padding:45px 0 70px;text-align:center;position:relative;z-index:2}
.badge{display:inline-block;padding:8px 18px;border:1px solid rgba(255,180,190,.45);border-radius:999px;color:#ffd5dc;background:rgba(255,255,255,.06);font-size:13px}
h1{font-size:clamp(30px,7vw,66px);margin:22px 0 8px;line-height:1.4;text-shadow:0 0 28px #ff174f}
.subtitle{color:#ffc1cc;font-size:clamp(14px,3vw,20px);margin-bottom:28px}
.card{
  position:relative;overflow:hidden;border:1px solid rgba(255,190,200,.28);
  border-radius:30px;padding:20px;background:rgba(255,255,255,.075);
  backdrop-filter:blur(12px);box-shadow:0 18px 80px rgba(0,0,0,.42);
}
.photo-wrap{position:relative;min-height:190px;display:flex;justify-content:center;align-items:center}
.photo{
  display:block;width:min(100%,560px);max-height:600px;object-fit:cover;border-radius:22px;
  border:2px solid rgba(255,210,220,.6);box-shadow:0 0 40px rgba(255,0,70,.25);
}
.placeholder{
  width:min(100%,560px);min-height:250px;border-radius:22px;display:flex;align-items:center;justify-content:center;
  border:1px dashed #e98b9e;background:linear-gradient(135deg,#35101c,#14070d);color:#ffc2cd;padding:30px
}
.text{
  white-space:pre-line;text-align:right;line-height:2.25;font-size:16px;color:#ffe8ec;
  margin:30px auto 15px;max-width:760px
}
.special{
  margin:28px 0 10px;padding:20px;border-radius:20px;
  background:linear-gradient(135deg,rgba(255,0,75,.2),rgba(255,255,255,.04));
  border:1px solid rgba(255,180,190,.25);color:#fff0b8;line-height:2;font-weight:700
}
.footer{margin-top:30px;color:#ffb3c0;font-size:13px}
#gate{min-height:100vh;display:flex;align-items:center;justify-content:center;padding:25px}
.gate-card{width:min(430px,100%);text-align:center;padding:35px 25px;border-radius:28px;background:rgba(255,255,255,.08);border:1px solid rgba(255,180,200,.3);box-shadow:0 15px 70px #0008}
input{width:100%;padding:15px;border-radius:14px;border:1px solid #a84a61;background:#17070e;color:white;text-align:center;font-size:18px;outline:none;margin:18px 0}
button{width:100%;padding:14px;border:0;border-radius:14px;background:linear-gradient(90deg,#b20f42,#ef4265);color:white;font:inherit;font-weight:700;cursor:pointer}
.error{color:#ff9db0;margin-top:12px;font-size:13px}
.petal{
  position:fixed;top:-12vh;z-index:5;pointer-events:none;animation:fall linear forwards;
  filter:drop-shadow(0 0 5px rgba(255,60,100,.35));
}
@keyframes fall{
  0%{transform:translate3d(0,-10vh,0) rotate(0deg);opacity:0}
  10%{opacity:1}
  50%{transform:translate3d(var(--sway),50vh,0) rotate(180deg)}
  100%{transform:translate3d(calc(var(--sway) * -1),115vh,0) rotate(360deg);opacity:.1}
}
.cursor{display:inline-block;border-left:2px solid #ff9eb0;animation:blink .8s infinite}
@keyframes blink{50%{opacity:0}}
@media(max-width:600px){.container{padding-top:30px}.card{padding:12px}.text{font-size:14px;line-height:2.1}}
</style>
</head>
<body>
{% if not unlocked %}
<section id="gate">
  <div class="gate-card">
    <div style="font-size:56px">🌹</div>
    <h2>یک سورپرایز برای تو ❤️</h2>
    <p style="color:#ffc5d0;line-height:2">برای باز شدن این نامه عاشقانه، رمز مخصوصت رو وارد کن.</p>
    <form method="post">
      <input name="password" type="password" inputmode="numeric" placeholder="رمز ورود" required autofocus>
      <button type="submit">باز کردن هدیه ❤️</button>
    </form>
    {% if error %}<div class="error">رمز درست نیست؛ دوباره امتحان کن عزیزم.</div>{% endif %}
  </div>
</section>
{% else %}
<div class="container">
  <span class="badge">برای خاص‌ترین دختر دنیا ❤️</span>
  <h1>{{ title }}</h1>
  <div class="subtitle">{{ name }} جان، این صفحه فقط برای تو ساخته شده 🌹</div>
  <div class="card">
    <div class="photo-wrap">
      {% if image_url %}
        <img class="photo" src="{{ image_url }}" alt="عکس عزیزم">
      {% else %}
        <div class="placeholder">اینجا عکس دخترت قرار می‌گیرد 🌹<br>لینک عکس را در متغیر BIRTHDAY_IMAGE_URL در Render وارد کن.</div>
      {% endif %}
    </div>
    <div class="text" id="letter"></div>
    <div class="special">{{ special_line }}</div>
  </div>
  <div class="footer">با تمام قلبم… تولدت مبارک دخترم ❤️🌹</div>
</div>
<script>
const message = {{ birthday_text|tojson }};
const target = document.getElementById("letter");
let index = 0;
function typeText(){
  if(index <= message.length){
    target.innerHTML = message.slice(0,index).replace(/\\n/g,"<br>") + '<span class="cursor"></span>';
    index++;
    setTimeout(typeText, 22);
  } else {
    target.innerHTML = message.replace(/\\n/g,"<br>");
  }
}
typeText();

const symbols = ["🌹","🌹","🌹","🌸","❤️","✦"];
function createPetal(){
  const el=document.createElement("div");
  el.className="petal";
  el.textContent=symbols[Math.floor(Math.random()*symbols.length)];
  el.style.left=(Math.random()*100)+"vw";
  el.style.fontSize=(15+Math.random()*25)+"px";
  el.style.animationDuration=(5+Math.random()*7)+"s";
  el.style.setProperty("--sway",(Math.random()*240-120)+"px");
  document.body.appendChild(el);
  setTimeout(()=>el.remove(),13000);
}
setInterval(createPetal,180);
for(let i=0;i<22;i++) setTimeout(createPetal,i*100);
</script>
{% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.form.get("password", "") == PASSWORD:
            session["unlocked"] = True
            return redirect(url_for("index"))
        return render_template_string(
            PAGE, unlocked=False, error=True, title=TITLE, name=NAME,
            birthday_text=BIRTHDAY_TEXT, special_line=SPECIAL_LINE,
            image_url=IMAGE_URL
        )

    return render_template_string(
        PAGE,
        unlocked=session.get("unlocked", False),
        error=False,
        title=TITLE,
        name=NAME,
        birthday_text=BIRTHDAY_TEXT,
        special_line=SPECIAL_LINE,
        image_url=IMAGE_URL
    )

@app.route("/lock")
def lock():
    session.clear()
    return redirect(url_for("index"))

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
