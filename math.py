# -*- coding: utf-8 -*-
"""
الفرق بين مربعين — تطبيق تفاعلي شامل
إعداد الطالبات: أية • رفيف • سارة • هزار
يعمل بـ Python 3 + Tkinter (مكتبة قياسية، لا حاجة لتثبيت شيء)
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import math
import time

# ==========================================================
# 1) توليد بنك الأسئلة (120 سؤالاً)
# ==========================================================

def gcd(a, b):
    return math.gcd(int(a), int(b))


def sq(n):
    """هل العدد مربع كامل؟ يُرجع الجذر أو None"""
    r = int(round(math.isqrt(int(n))))
    return r if r * r == int(n) else None


def term(coef, var, power):
    """تنسيق حد جبري مثل 9س^2"""
    c = "" if coef == 1 else str(coef)
    if not var:
        return str(coef)
    p = "" if power == 1 else f"^{power}"
    return f"{c}{var}{p}"


class Question:
    def __init__(self, expr, answer, category, level, steps, hint):
        self.expr = expr            # المقدار المطلوب تحليله
        self.answer = answer        # الحل الصحيح
        self.category = category    # التصنيف
        self.level = level          # المستوى 1..3
        self.steps = steps          # خطوات الحل
        self.hint = hint            # تلميح
        self.options = []           # خيارات الاختبار


VARS = ["س", "ص", "ع", "ل"]


def build_bank():
    """يبني 120 سؤالاً موزعة على أربعة تصنيفات"""
    bank = []
    rnd = random.Random(2026)   # بذرة ثابتة => نفس البنك في كل تشغيل

    # ---------- (أ) تحليل مباشر: a²س² - b² ----------
    for i in range(35):
        a = rnd.choice([1, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12])
        b = rnd.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13])
        v = VARS[i % len(VARS)]
        left = term(a * a, v, 2)
        right = b * b
        expr = f"{left} - {right}"
        ans = f"({term(a, v, 1)} - {b})({term(a, v, 1)} + {b})"
        steps = [
            f"نتحقق أن الحدّين مربعان كاملان: {left} = ({term(a, v, 1)})²  و  {right} = ({b})².",
            "نطبّق القاعدة: أ² − ب² = (أ − ب)(أ + ب).",
            f"أ = {term(a, v, 1)}  ،  ب = {b}.",
            f"الناتج: {ans}.",
        ]
        hint = f"ما جذر {left}؟ وما جذر {right}؟ ثم ضع الجذرين في (أ−ب)(أ+ب)."
        bank.append(Question(expr, ans, "تحليل مباشر", 1, steps, hint))

    # ---------- (ب) إخراج العامل المشترك أولاً ----------
    for i in range(35):
        k = rnd.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 12])
        a = rnd.choice([1, 2, 3, 4, 5, 6])
        b = rnd.choice([1, 2, 3, 4, 5, 7, 8, 9])
        v = VARS[(i + 1) % len(VARS)]
        expr = f"{term(k * a * a, v, 2)} - {k * b * b}"
        inner = f"({term(a, v, 1)} - {b})({term(a, v, 1)} + {b})"
        ans = f"{k}{inner}"
        steps = [
            f"العامل المشترك الأكبر بين {k*a*a} و {k*b*b} هو {k}.",
            f"نُخرجه: {expr} = {k}({term(a*a, v, 2)} - {b*b}).",
            f"داخل القوس فرق بين مربعين: {term(a*a, v, 2)} = ({term(a, v, 1)})²  و  {b*b} = ({b})².",
            f"الناتج النهائي: {ans}.",
        ]
        hint = f"لا تحلّل قبل إخراج العامل المشترك {k}."
        bank.append(Question(expr, ans, "عامل مشترك (G.C.F)", 2, steps, hint))

    # ---------- (ج) حساب ذهني للأعداد: n² - m² ----------
    pairs = [(101, 99), (52, 48), (75, 25), (63, 37), (120, 80), (45, 35),
             (210, 190), (99, 1), (86, 14), (55, 45), (31, 29), (150, 50),
             (77, 23), (64, 36), (98, 2), (250, 150), (41, 39), (88, 12),
             (72, 28), (135, 65), (96, 4), (58, 42), (111, 89), (140, 60),
             (33, 27)]
    for (n, m) in pairs:
        expr = f"{n}² - {m}²"
        d, s = n - m, n + m
        ans = f"{d} × {s} = {d * s}"
        steps = [
            "نستخدم القاعدة بدل الحساب الطويل: أ² − ب² = (أ − ب)(أ + ب).",
            f"أ − ب = {n} − {m} = {d}.",
            f"أ + ب = {n} + {m} = {s}.",
            f"الناتج: {d} × {s} = {d * s}.",
        ]
        hint = f"اطرح العددين ثم اجمعهما، واضرب الناتجين ({d} و {s})."
        bank.append(Question(expr, ans, "حساب ذهني للأعداد", 2, steps, hint))

    # ---------- (د) أسس أعلى وكسور ----------
    high = [
        ("س^4 - 16", "(س² - 4)(س² + 4) = (س - 2)(س + 2)(س² + 4)",
         ["س⁴ = (س²)²  و  16 = 4².",
          "أولاً: (س² − 4)(س² + 4).",
          "القوس الأول ما زال فرق بين مربعين: س² − 4 = (س − 2)(س + 2).",
          "الناتج التام: (س − 2)(س + 2)(س² + 4)."],
         "حلّل مرتين: الناتج الأول ليس تاماً بعد."),
        ("16س^4 - 81", "(4س² - 9)(4س² + 9) = (2س - 3)(2س + 3)(4س² + 9)",
         ["16س⁴ = (4س²)²  و  81 = 9².",
          "(4س² − 9)(4س² + 9).",
          "4س² − 9 = (2س − 3)(2س + 3).",
          "الناتج: (2س − 3)(2س + 3)(4س² + 9)."],
         "بعد التحليل الأول، افحص كل قوس مجدداً."),
        ("س^6 - 64", "(س³ - 8)(س³ + 8)",
         ["س⁶ = (س³)²  و  64 = 8².",
          "الناتج: (س³ − 8)(س³ + 8)."],
         "اقسم الأس 6 على 2 لتحصل على س³."),
        ("س^2/9 - 25", "(س/3 - 5)(س/3 + 5)",
         ["س²/9 = (س/3)²  و  25 = 5².",
          "الناتج: (س/3 − 5)(س/3 + 5)."],
         "جذر المقام 9 هو 3، فالجذر هو س/3."),
        ("4س^2/25 - 1", "(2س/5 - 1)(2س/5 + 1)",
         ["4س²/25 = (2س/5)²  و  1 = 1².",
          "الناتج: (2س/5 − 1)(2س/5 + 1)."],
         "جذر البسط 4س² هو 2س وجذر المقام 25 هو 5."),
        ("س^2 - ص^2", "(س - ص)(س + ص)",
         ["الحدّان مربعان: (س)² و (ص)².",
          "الناتج: (س − ص)(س + ص)."],
         "الصورة الأساسية للقاعدة."),
        ("49س^2 - 36ص^2", "(7س - 6ص)(7س + 6ص)",
         ["49س² = (7س)²  و  36ص² = (6ص)².",
          "الناتج: (7س − 6ص)(7س + 6ص)."],
         "خذ جذر كل حد مع متغيّره."),
        ("س^8 - 1", "(س^4 - 1)(س^4 + 1) = (س - 1)(س + 1)(س² + 1)(س^4 + 1)",
         ["س⁸ = (س⁴)²  و  1 = 1².",
          "(س⁴ − 1)(س⁴ + 1).",
          "س⁴ − 1 = (س² − 1)(س² + 1)، و س² − 1 = (س − 1)(س + 1).",
          "الناتج التام: (س − 1)(س + 1)(س² + 1)(س⁴ + 1)."],
         "كرّر التحليل ثلاث مرات حتى لا يبقى فرق بين مربعين."),
        ("100 - س^2", "(10 - س)(10 + س)",
         ["الترتيب مقلوب: العدد أولاً.",
          "100 = 10²  و  س² = (س)².",
          "الناتج: (10 − س)(10 + س)."],
         "لا يهم الترتيب، المهم أيّهما المطروح."),
        ("س^2 ص^2 - 121", "(سص - 11)(سص + 11)",
         ["س²ص² = (سص)²  و  121 = 11².",
          "الناتج: (سص − 11)(سص + 11)."],
         "اجمع المتغيّرين تحت جذر واحد: سص."),
        ("(س+1)^2 - 9", "(س - 2)(س + 4)",
         ["أ = (س + 1)  ،  ب = 3.",
          "(س + 1 − 3)(س + 1 + 3).",
          "نبسّط: (س − 2)(س + 4)."],
         "اعتبر القوس كلّه حدّاً واحداً (أ)."),
        ("س^4 - ص^4", "(س - ص)(س + ص)(س² + ص²)",
         ["س⁴ = (س²)²  و  ص⁴ = (ص²)².",
          "(س² − ص²)(س² + ص²).",
          "س² − ص² = (س − ص)(س + ص).",
          "الناتج: (س − ص)(س + ص)(س² + ص²)."],
         "القوس الأول يقبل تحليلاً إضافياً."),
        ("0.25س^2 - 0.09", "(0.5س - 0.3)(0.5س + 0.3)",
         ["0.25س² = (0.5س)²  و  0.09 = (0.3)².",
          "الناتج: (0.5س − 0.3)(0.5س + 0.3)."],
         "جذر 0.25 = 0.5 وجذر 0.09 = 0.3."),
        ("س^10 - 1", "(س^5 - 1)(س^5 + 1)",
         ["س¹⁰ = (س⁵)²  و  1 = 1².",
          "الناتج: (س⁵ − 1)(س⁵ + 1)."],
         "اقسم الأس على 2."),
        ("9/16 - س^2", "(3/4 - س)(3/4 + س)",
         ["9/16 = (3/4)²  و  س² = (س)².",
          "الناتج: (3/4 − س)(3/4 + س)."],
         "جذر الكسر = جذر البسط على جذر المقام."),
        ("81س^4 - 16ص^4", "(9س² - 4ص²)(9س² + 4ص²) = (3س - 2ص)(3س + 2ص)(9س² + 4ص²)",
         ["81س⁴ = (9س²)²  و  16ص⁴ = (4ص²)².",
          "(9س² − 4ص²)(9س² + 4ص²).",
          "9س² − 4ص² = (3س − 2ص)(3س + 2ص).",
          "الناتج: (3س − 2ص)(3س + 2ص)(9س² + 4ص²)."],
         "حلّل، ثم افحص القوس الأول."),
        ("س^2 - 1/4", "(س - 1/2)(س + 1/2)",
         ["1/4 = (1/2)².",
          "الناتج: (س − 1/2)(س + 1/2)."],
         "جذر 1/4 هو 1/2."),
        ("2س^4 - 32", "2(س² - 4)(س² + 4) = 2(س - 2)(س + 2)(س² + 4)",
         ["العامل المشترك 2: 2(س⁴ − 16).",
          "س⁴ − 16 = (س² − 4)(س² + 4).",
          "س² − 4 = (س − 2)(س + 2).",
          "الناتج: 2(س − 2)(س + 2)(س² + 4)."],
         "عامل مشترك أولاً، ثم تحليل مزدوج."),
        ("(2س)^2 - (3ص)^2", "(2س - 3ص)(2س + 3ص)",
         ["الحدّان مكتوبان أصلاً كمربعين.",
          "الناتج: (2س − 3ص)(2س + 3ص)."],
         "طبّق القاعدة مباشرة."),
        ("س^12 - ص^12", "(س^6 - ص^6)(س^6 + ص^6)",
         ["س¹² = (س⁶)²  و  ص¹² = (ص⁶)².",
          "الناتج: (س⁶ − ص⁶)(س⁶ + ص⁶)."],
         "نصّف الأسس."),
        ("144 - 25س^2", "(12 - 5س)(12 + 5س)",
         ["144 = 12²  و  25س² = (5س)².",
          "الناتج: (12 − 5س)(12 + 5س)."],
         "ابدأ بالعدد لأنه المطروح منه."),
        ("س^2/36 - ص^2/49", "(س/6 - ص/7)(س/6 + ص/7)",
         ["س²/36 = (س/6)²  و  ص²/49 = (ص/7)².",
          "الناتج: (س/6 − ص/7)(س/6 + ص/7)."],
         "خذ جذر البسط والمقام لكل كسر."),
        ("3س^2 - 75", "3(س - 5)(س + 5)",
         ["العامل المشترك 3: 3(س² − 25).",
          "س² − 25 = (س − 5)(س + 5).",
          "الناتج: 3(س − 5)(س + 5)."],
         "أخرج 3 أولاً."),
        ("س^2 - 0.01", "(س - 0.1)(س + 0.1)",
         ["0.01 = (0.1)².",
          "الناتج: (س − 0.1)(س + 0.1)."],
         "جذر 0.01 هو 0.1."),
        ("(س+ص)^2 - (س-ص)^2", "4سص",
         ["أ = (س+ص) ، ب = (س−ص).",
          "الفرق: [(س+ص) − (س−ص)][(س+ص) + (س−ص)].",
          "= (2ص)(2س).",
          "الناتج: 4سص."],
         "بسّط كل قوس بعد الطرح والجمع."),
    ]
    for expr, ans, steps, hint in high:
        bank.append(Question(expr, ans, "أسس أعلى وكسور", 3, steps, hint))

    return bank[:120]


# ==========================================================
# 2) توليد خيارات الاختبار (إجابة صحيحة + 3 مشتّتات)
# ==========================================================

def make_options(q, bank, rnd):
    wrongs = set()
    # مشتّت كلاسيكي: مجموع المربعين أو تكرار الإشارة
    if "(" in q.answer and ")" in q.answer:
        wrongs.add(q.answer.replace(" - ", " + ", 1))
        wrongs.add(q.answer.replace(" + ", " - ", 1))
    pool = [o.answer for o in bank if o.answer != q.answer]
    rnd.shuffle(pool)
    for cand in pool:
        if len(wrongs) >= 3:
            break
        if cand != q.answer:
            wrongs.add(cand)
    opts = [q.answer] + list(wrongs)[:3]
    rnd.shuffle(opts)
    return opts


# ==========================================================
# 3) الواجهة الرسومية
# ==========================================================

BG = "#0f172a"
CARD = "#1e293b"
ACCENT = "#38bdf8"
OK = "#22c55e"
BAD = "#ef4444"
TXT = "#e2e8f0"
GOLD = "#fbbf24"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("الفرق بين مربعين — إعداد: أية • رفيف • سارة • هزار")
        self.geometry("1000x720")
        self.configure(bg=BG)
        self.rnd = random.Random()
        self.bank = build_bank()
        for q in self.bank:
            q.options = make_options(q, self.bank, self.rnd)

        self.total_points = 0
        self.solved = 0
        self.correct_total = 0

        self._header()
        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True, padx=12, pady=8)
        self._style()

        self.tab_cards()
        self.tab_bank()
        self.tab_exam()
        self.tab_practice()
        self.tab_geometry()
        self._footer()

    # -------------------- تنسيق عام --------------------
    def _style(self):
        st = ttk.Style(self)
        try:
            st.theme_use("clam")
        except tk.TclError:
            pass
        st.configure("TNotebook", background=BG, borderwidth=0)
        st.configure("TNotebook.Tab", background=CARD, foreground=TXT,
                     padding=(18, 10), font=("Arial", 11, "bold"))
        st.map("TNotebook.Tab", background=[("selected", ACCENT)],
               foreground=[("selected", "#0f172a")])
        st.configure("TFrame", background=BG)
        st.configure("TLabel", background=BG, foreground=TXT, font=("Arial", 12))
        st.configure("TRadiobutton", background=CARD, foreground=TXT,
                     font=("Arial", 12))
        st.configure("Horizontal.TProgressbar", background=ACCENT,
                     troughcolor=CARD)

    def _header(self):
        h = tk.Frame(self, bg=CARD, pady=10)
        h.pack(fill="x")
        tk.Label(h, text="بطاقات التأسيس والتحليل — الفرق بين مربعين",
                 bg=CARD, fg=ACCENT, font=("Arial", 20, "bold")).pack()
        tk.Label(h, text="إعداد الطالبات:  أية • رفيف • سارة • هزار",
                 bg=CARD, fg=GOLD, font=("Arial", 12)).pack()

    def _footer(self):
        f = tk.Frame(self, bg=CARD, pady=8)
        f.pack(fill="x")
        self.lbl_points = tk.Label(f, text="إجمالي النقاط: 0", bg=CARD,
                                   fg=GOLD, font=("Arial", 12, "bold"))
        self.lbl_points.pack(side="right", padx=20)
        self.lbl_acc = tk.Label(f, text="نسبة الدقة: 100%", bg=CARD,
                                fg=OK, font=("Arial", 12, "bold"))
        self.lbl_acc.pack(side="right", padx=20)
        self.lbl_solved = tk.Label(f, text="الأسئلة المحلولة: 0", bg=CARD,
                                   fg=TXT, font=("Arial", 12, "bold"))
        self.lbl_solved.pack(side="right", padx=20)

    def add_score(self, points, correct):
        self.total_points += points
        self.solved += 1
        if correct:
            self.correct_total += 1
        acc = round(self.correct_total / self.solved * 100) if self.solved else 100
        self.lbl_points.config(text=f"إجمالي النقاط: {self.total_points}")
        self.lbl_solved.config(text=f"الأسئلة المحلولة: {self.solved}")
        self.lbl_acc.config(text=f"نسبة الدقة: {acc}%")

    # -------------------- (1) البطاقات القابلة للقلب --------------------
    def tab_cards(self):
        fr = ttk.Frame(self.nb)
        self.nb.add(fr, text="بطاقات الشرح")

        tk.Label(fr, text="اضغط على أي بطاقة لقلبها ورؤية خطوات الحل التفصيلية.",
                 bg=BG, fg=TXT, font=("Arial", 12)).pack(pady=6)

        bar = tk.Frame(fr, bg=BG)
        bar.pack(pady=4)
        self.card_cat = tk.StringVar(value="الكل")
        cats = ["الكل", "عامل مشترك (G.C.F)", "تحليل مباشر",
                "حساب ذهني للأعداد", "أسس أعلى وكسور"]
        for c in cats:
            tk.Radiobutton(bar, text=c, value=c, variable=self.card_cat,
                           command=self.render_cards, bg=BG, fg=TXT,
                           selectcolor=CARD, activebackground=BG,
                           activeforeground=ACCENT,
                           font=("Arial", 10)).pack(side="right", padx=4)

        canvas = tk.Canvas(fr, bg=BG, highlightthickness=0)
        sb = ttk.Scrollbar(fr, orient="vertical", command=canvas.yview)
        self.cards_holder = tk.Frame(canvas, bg=BG)
        self.cards_holder.bind("<Configure>",
                               lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.cards_holder, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True, padx=8, pady=8)
        sb.pack(side="right", fill="y")
        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(int(-e.delta / 120), "units"))

        self.render_cards()

    def render_cards(self):
        for w in self.cards_holder.winfo_children():
            w.destroy()
        cat = self.card_cat.get()
        pool = [q for q in self.bank if cat == "الكل" or q.category == cat][:12]
        for i, q in enumerate(pool):
            self._flip_card(self.cards_holder, q, i)

    def _flip_card(self, parent, q, idx):
        box = tk.Frame(parent, bg=CARD, bd=2, relief="ridge",
                       highlightbackground=ACCENT, highlightthickness=1)
        box.grid(row=idx // 3, column=idx % 3, padx=10, pady=10, sticky="nsew")
        parent.grid_columnconfigure(idx % 3, weight=1)

        state = {"flipped": False}
        title = tk.Label(box, text=q.category, bg=CARD, fg=GOLD,
                         font=("Arial", 9, "bold"))
        title.pack(anchor="e", padx=8, pady=(6, 0))
        body = tk.Label(box, text=q.expr, bg=CARD, fg=ACCENT,
                        font=("Arial", 15, "bold"), wraplength=260,
                        justify="center", height=6)
        body.pack(fill="both", expand=True, padx=10, pady=8)
        foot = tk.Label(box, text="اضغط للقلب ↻", bg=CARD, fg="#64748b",
                        font=("Arial", 9))
        foot.pack(pady=(0, 6))

        def flip(_=None):
            state["flipped"] = not state["flipped"]
            if state["flipped"]:
                text = "\n".join(f"{n+1}. {s}" for n, s in enumerate(q.steps))
                body.config(text=text, fg=OK, font=("Arial", 10))
                foot.config(text="اضغط للعودة ↺")
            else:
                body.config(text=q.expr, fg=ACCENT, font=("Arial", 15, "bold"))
                foot.config(text="اضغط للقلب ↻")

        for w in (box, title, body, foot):
            w.bind("<Button-1>", flip)

    # -------------------- (2) بنك الأسئلة --------------------
    def tab_bank(self):
        fr = ttk.Frame(self.nb)
        self.nb.add(fr, text="بنك الأسئلة (120)")

        top = tk.Frame(fr, bg=BG)
        top.pack(fill="x", pady=6)
        tk.Label(top, text="تصفح جميع أسئلة المنهاج مع الحلول:", bg=BG,
                 fg=TXT, font=("Arial", 12)).pack(side="right", padx=10)

        self.bank_filter = tk.StringVar(value="الكل")
        for c in ["الكل", "عامل مشترك (G.C.F)", "تحليل مباشر",
                  "حساب ذهني للأعداد", "أسس أعلى وكسور"]:
            tk.Radiobutton(top, text=c, value=c, variable=self.bank_filter,
                           command=self.fill_bank, bg=BG, fg=TXT,
                           selectcolor=CARD, activebackground=BG,
                           font=("Arial", 10)).pack(side="right", padx=3)

        cols = ("#", "المقدار", "التصنيف", "الحل")
        self.tree = ttk.Treeview(fr, columns=cols, show="headings", height=18)
        for c, w in zip(cols, (50, 220, 170, 420)):
            self.tree.heading(c, text=c)
            self.tree.column(c, width=w, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=6)
        self.tree.bind("<Double-1>", self.show_solution)

        tk.Label(fr, text="انقر نقراً مزدوجاً على أي سؤال لعرض خطوات حله والتلميح.",
                 bg=BG, fg="#94a3b8", font=("Arial", 10)).pack(pady=(0, 8))
        self.fill_bank()

    def fill_bank(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        f = self.bank_filter.get()
        for i, q in enumerate(self.bank, 1):
            if f == "الكل" or q.category == f:
                self.tree.insert("", "end", iid=str(i - 1),
                                 values=(i, q.expr, q.category, q.answer))

    def show_solution(self, _):
        sel = self.tree.selection()
        if not sel:
            return
        q = self.bank[int(sel[0])]
        body = f"المقدار:  {q.expr}\n\nالتلميح:  {q.hint}\n\nخطوات الحل:\n"
        body += "\n".join(f"  {n+1}. {s}" for n, s in enumerate(q.steps))
        body += f"\n\nالحل النهائي:  {q.answer}"
        messagebox.showinfo("الحل التفصيلي", body)

    # -------------------- (3) الاختبار --------------------
    def tab_exam(self):
        fr = ttk.Frame(self.nb)
        self.nb.add(fr, text="الاختبار الشامل")
        self.exam_frame = fr
        self.exam_home()

    def exam_home(self):
        for w in self.exam_frame.winfo_children():
            w.destroy()
        tk.Label(self.exam_frame, text="اختبار الانطلاقة والتمكن الشامل",
                 bg=BG, fg=ACCENT, font=("Arial", 18, "bold")).pack(pady=14)

        row = tk.Frame(self.exam_frame, bg=BG)
        row.pack(pady=12)
        modes = [("تحدي سريع", 10, "مراجعة سريعة"),
                 ("مستوى قياسي", 30, "شامل للمهارات"),
                 ("التحدي الشامل", 120, "بنك الأسئلة بالكامل")]
        for name, n, sub in modes:
            c = tk.Frame(row, bg=CARD, bd=2, relief="ridge", padx=26, pady=18)
            c.pack(side="right", padx=14)
            tk.Label(c, text=name, bg=CARD, fg=GOLD,
                     font=("Arial", 13, "bold")).pack()
            tk.Label(c, text=f"{n} أسئلة", bg=CARD, fg=ACCENT,
                     font=("Arial", 22, "bold")).pack(pady=6)
            tk.Label(c, text=sub, bg=CARD, fg="#94a3b8",
                     font=("Arial", 10)).pack()
            tk.Button(c, text="ابدأ الآن", bg=ACCENT, fg="#0f172a",
                      font=("Arial", 11, "bold"), relief="flat", padx=14,
                      command=lambda k=n: self.exam_start(k)).pack(pady=(10, 0))

    def exam_start(self, n):
        self.ex_qs = self.rnd.sample(self.bank, min(n, len(self.bank)))
        self.ex_i = 0
        self.ex_ans = [None] * len(self.ex_qs)
        self.ex_t0 = time.time()
        self.exam_screen()

    def exam_screen(self):
        for w in self.exam_frame.winfo_children():
            w.destroy()
        f = self.exam_frame

        top = tk.Frame(f, bg=BG)
        top.pack(fill="x", pady=6, padx=12)
        self.ex_lbl = tk.Label(top, text="", bg=BG, fg=TXT,
                               font=("Arial", 11, "bold"))
        self.ex_lbl.pack(side="right")
        self.ex_timer = tk.Label(top, text="00:00", bg=BG, fg=GOLD,
                                 font=("Arial", 13, "bold"))
        self.ex_timer.pack(side="left")
        tk.Button(top, text="إنهاء الاختبار", bg=BAD, fg="white", relief="flat",
                  command=self.exam_finish).pack(side="left", padx=12)

        self.ex_bar = ttk.Progressbar(f, maximum=len(self.ex_qs))
        self.ex_bar.pack(fill="x", padx=14, pady=4)

        self.ex_q = tk.Label(f, text="", bg=CARD, fg=ACCENT,
                             font=("Arial", 20, "bold"), pady=22)
        self.ex_q.pack(fill="x", padx=14, pady=10)

        self.ex_var = tk.StringVar(value="")
        self.ex_opts = tk.Frame(f, bg=BG)
        self.ex_opts.pack(fill="both", expand=True, padx=40)

        nav = tk.Frame(f, bg=BG)
        nav.pack(pady=14)
        tk.Button(nav, text="السابق", bg=CARD, fg=TXT, relief="flat", padx=20,
                  command=lambda: self.exam_move(-1)).pack(side="right", padx=8)
        tk.Button(nav, text="التالي", bg=ACCENT, fg="#0f172a", relief="flat",
                  padx=20, font=("Arial", 11, "bold"),
                  command=lambda: self.exam_move(1)).pack(side="left", padx=8)

        self.exam_render()
        self.exam_tick()

    def exam_tick(self):
        if not hasattr(self, "ex_timer") or not self.ex_timer.winfo_exists():
            return
        el = int(time.time() - self.ex_t0)
        self.ex_timer.config(text=f"{el//60:02d}:{el%60:02d}")
        self.after(1000, self.exam_tick)

    def exam_render(self):
        q = self.ex_qs[self.ex_i]
        self.ex_lbl.config(text=f"سؤال {self.ex_i+1} من {len(self.ex_qs)}  "
                                f"| المستوى {q.level} | {q.level*10} نقاط")
        self.ex_bar["value"] = self.ex_i + 1
        self.ex_q.config(text=f"حلّل تحليلاً تاماً:    {q.expr}")
        for w in self.ex_opts.winfo_children():
            w.destroy()
        self.ex_var.set(self.ex_ans[self.ex_i] or "")
        for op in q.options:
            tk.Radiobutton(self.ex_opts, text=op, value=op, variable=self.ex_var,
                           bg=CARD, fg=TXT, selectcolor=BG, anchor="e",
                           activebackground=CARD, activeforeground=ACCENT,
                           font=("Arial", 13), padx=14, pady=10,
                           indicatoron=True).pack(fill="x", pady=5)

    def exam_move(self, d):
        self.ex_ans[self.ex_i] = self.ex_var.get() or None
        nxt = self.ex_i + d
        if nxt < 0:
            return
        if nxt >= len(self.ex_qs):
            self.exam_finish()
            return
        self.ex_i = nxt
        self.exam_render()

    def exam_finish(self):
        if hasattr(self, "ex_var"):
            self.ex_ans[self.ex_i] = self.ex_var.get() or None
        right = sum(1 for q, a in zip(self.ex_qs, self.ex_ans) if a == q.answer)
        wrong = len(self.ex_qs) - right
        pct = round(right / len(self.ex_qs) * 100)
        el = int(time.time() - self.ex_t0)
        pts = sum(q.level * 10 for q, a in zip(self.ex_qs, self.ex_ans)
                  if a == q.answer)
        self.total_points += pts
        self.solved += len(self.ex_qs)
        self.correct_total += right
        acc = round(self.correct_total / self.solved * 100)
        self.lbl_points.config(text=f"إجمالي النقاط: {self.total_points}")
        self.lbl_solved.config(text=f"الأسئلة المحلولة: {self.solved}")
        self.lbl_acc.config(text=f"نسبة الدقة: {acc}%")

        for w in self.exam_frame.winfo_children():
            w.destroy()
        tk.Label(self.exam_frame, text="نتيجة الاختبار", bg=BG, fg=ACCENT,
                 font=("Arial", 22, "bold")).pack(pady=18)
        grid = tk.Frame(self.exam_frame, bg=BG)
        grid.pack(pady=10)
        cells = [("النتيجة", f"{pct}%", GOLD), ("إجابات صحيحة", right, OK),
                 ("إجابات خاطئة", wrong, BAD),
                 ("الوقت", f"{el//60:02d}:{el%60:02d}", ACCENT),
                 ("النقاط المكتسبة", pts, GOLD)]
        for t, v, col in cells:
            c = tk.Frame(grid, bg=CARD, padx=24, pady=16)
            c.pack(side="right", padx=8)
            tk.Label(c, text=t, bg=CARD, fg=TXT, font=("Arial", 10)).pack()
            tk.Label(c, text=v, bg=CARD, fg=col,
                     font=("Arial", 20, "bold")).pack()

        msg = ("ممتاز! إتقان تام 🎉" if pct >= 90 else
               "جيد جداً، واصلي 💪" if pct >= 70 else
               "تحتاجين لمراجعة البطاقات 📘")
        tk.Label(self.exam_frame, text=msg, bg=BG, fg=GOLD,
                 font=("Arial", 15, "bold")).pack(pady=16)
        tk.Button(self.exam_frame, text="إعادة الاختبار", bg=ACCENT,
                  fg="#0f172a", relief="flat", padx=24, pady=8,
                  font=("Arial", 12, "bold"),
                  command=self.exam_home).pack()

    # -------------------- (4) التدريب الموجه --------------------
    def tab_practice(self):
        fr = ttk.Frame(self.nb)
        self.nb.add(fr, text="التدريب الموجّه")
        self.pr_frame = fr

        tk.Label(fr, text="حلّ المسألة، وإذا احتجت مساعدة اضغط «عرض تلميح».",
                 bg=BG, fg=TXT, font=("Arial", 12)).pack(pady=10)

        self.pr_info = tk.Label(fr, text="", bg=BG, fg=GOLD,
                                font=("Arial", 10, "bold"))
        self.pr_info.pack()
        self.pr_q = tk.Label(fr, text="", bg=CARD, fg=ACCENT,
                             font=("Arial", 22, "bold"), pady=24)
        self.pr_q.pack(fill="x", padx=20, pady=12)

        self.pr_entry = tk.Entry(fr, font=("Arial", 15), justify="center",
                                 bg="#334155", fg="white", insertbackground="white")
        self.pr_entry.pack(fill="x", padx=120, ipady=8)
        self.pr_entry.bind("<Return>", lambda e: self.pr_check())

        b = tk.Frame(fr, bg=BG)
        b.pack(pady=14)
        tk.Button(b, text="تحقّق", bg=OK, fg="white", relief="flat", padx=22,
                  pady=6, font=("Arial", 11, "bold"),
                  command=self.pr_check).pack(side="right", padx=6)
        tk.Button(b, text="عرض تلميح", bg=GOLD, fg="#0f172a", relief="flat",
                  padx=22, pady=6, font=("Arial", 11, "bold"),
                  command=self.pr_hint).pack(side="right", padx=6)
        tk.Button(b, text="خطوات الحل", bg=CARD, fg=TXT, relief="flat",
                  padx=22, pady=6, command=self.pr_steps).pack(side="right", padx=6)
        tk.Button(b, text="سؤال جديد", bg=ACCENT, fg="#0f172a", relief="flat",
                  padx=22, pady=6, font=("Arial", 11, "bold"),
                  command=self.pr_new).pack(side="right", padx=6)

        self.pr_msg = tk.Label(fr, text="", bg=BG, fg=TXT,
                               font=("Arial", 12), wraplength=850, justify="right")
        self.pr_msg.pack(pady=10)
        self.pr_new()

    def pr_new(self):
        self.pr_cur = self.rnd.choice(self.bank)
        self.pr_tries = 0
        self.pr_q.config(text=self.pr_cur.expr)
        self.pr_info.config(text=f"{self.pr_cur.category}  |  المستوى "
                                 f"{self.pr_cur.level}")
        self.pr_entry.delete(0, "end")
        self.pr_msg.config(text="اكتب التحليل التام ثم اضغط «تحقّق».", fg=TXT)

    @staticmethod
    def norm(s):
        return (s.replace(" ", "").replace("×", "*").replace("−", "-")
                 .replace("*", "").lower())

    def pr_check(self):
        user = self.pr_entry.get().strip()
        if not user:
            return
        self.pr_tries += 1
        if self.norm(user) == self.norm(self.pr_cur.answer) or \
           self.norm(user) in self.norm(self.pr_cur.answer):
            pts = max(self.pr_cur.level * 10 - (self.pr_tries - 1) * 3, 3)
            self.pr_msg.config(text=f"إجابة صحيحة ✔  (+{pts} نقطة)", fg=OK)
            self.add_score(pts, True)
        else:
            self.pr_msg.config(
                text=f"غير صحيح ✘ — حاولي مرة أخرى. المحاولة رقم {self.pr_tries}",
                fg=BAD)
            if self.pr_tries >= 3:
                self.add_score(0, False)
                self.pr_msg.config(
                    text=f"الحل الصحيح: {self.pr_cur.answer}", fg=GOLD)

    def pr_hint(self):
        self.pr_msg.config(text=f"💡 تلميح: {self.pr_cur.hint}", fg=GOLD)

    def pr_steps(self):
        txt = "\n".join(f"{n+1}. {s}" for n, s in enumerate(self.pr_cur.steps))
        messagebox.showinfo("خطوات الحل", txt + f"\n\nالحل: {self.pr_cur.answer}")

    # -------------------- (5) المحاكاة الهندسية --------------------
    def tab_geometry(self):
        fr = ttk.Frame(self.nb)
        self.nb.add(fr, text="المحاكاة الهندسية")

        tk.Label(fr, text="شاهد هندسياً كيف يتحول اقتطاع المربع b² من a² "
                          "إلى مستطيل أبعاده (a−b)(a+b)",
                 bg=BG, fg=TXT, font=("Arial", 12)).pack(pady=8)

        ctrl = tk.Frame(fr, bg=CARD, pady=10)
        ctrl.pack(fill="x", padx=14)
        self.va = tk.IntVar(value=8)
        self.vb = tk.IntVar(value=3)

        tk.Label(ctrl, text="الضلع الكلي (a):", bg=CARD, fg=TXT,
                 font=("Arial", 11)).grid(row=0, column=2, padx=10, sticky="e")
        tk.Scale(ctrl, from_=2, to=14, orient="horizontal", variable=self.va,
                 bg=CARD, fg=ACCENT, troughcolor=BG, highlightthickness=0,
                 length=280, command=lambda e: self.draw_geo()
                 ).grid(row=0, column=1)

        tk.Label(ctrl, text="الضلع المقتطع (b):", bg=CARD, fg=TXT,
                 font=("Arial", 11)).grid(row=1, column=2, padx=10, sticky="e")
        tk.Scale(ctrl, from_=1, to=13, orient="horizontal", variable=self.vb,
                 bg=CARD, fg=GOLD, troughcolor=BG, highlightthickness=0,
                 length=280, command=lambda e: self.draw_geo()
                 ).grid(row=1, column=1)

        self.geo_canvas = tk.Canvas(fr, bg="#0b1220", height=340,
                                    highlightthickness=0)
        self.geo_canvas.pack(fill="both", expand=True, padx=14, pady=10)

        self.geo_stats = tk.Label(fr, text="", bg=BG, fg=TXT,
                                  font=("Arial", 13, "bold"))
        self.geo_stats.pack(pady=(0, 10))
        self.after(200, self.draw_geo)

    def draw_geo(self):
        c = self.geo_canvas
        c.delete("all")
        a, b = self.va.get(), self.vb.get()
        if b >= a:
            b = a - 1
            self.vb.set(b)
        u = 260 / max(a, 1)
        x0, y0 = 60, 40

        # المربع الكبير a²
        c.create_rectangle(x0, y0, x0 + a * u, y0 + a * u,
                           fill="#1d4ed8", outline=ACCENT, width=2)
        # المربع المقتطع b²
        c.create_rectangle(x0 + (a - b) * u, y0 + (a - b) * u,
                           x0 + a * u, y0 + a * u,
                           fill="#7f1d1d", outline=BAD, width=2)
        c.create_text(x0 + a * u / 2 - 30, y0 + 24, text=f"a² = {a*a}",
                      fill="white", font=("Arial", 13, "bold"))
        c.create_text(x0 + (a - b / 2) * u, y0 + (a - b / 2) * u,
                      text=f"b² = {b*b}", fill="#fecaca",
                      font=("Arial", 11, "bold"))

        # المستطيل المكافئ (a-b)(a+b)
        rx = x0 + a * u + 90
        w, h = (a + b) * u * 0.55, (a - b) * u * 0.9
        c.create_rectangle(rx, y0 + 40, rx + w, y0 + 40 + h,
                           fill="#166534", outline=OK, width=2)
        c.create_text(rx + w / 2, y0 + 40 + h / 2,
                      text=f"(a−b)(a+b) = {(a-b)*(a+b)}",
                      fill="white", font=("Arial", 12, "bold"))
        c.create_text(rx + w / 2, y0 + 24, text=f"العرض = a+b = {a+b}",
                      fill=OK, font=("Arial", 10))
        c.create_text(rx - 20, y0 + 40 + h / 2, text=f"a−b\n= {a-b}",
                      fill=OK, font=("Arial", 10))

        c.create_text(x0 + a * u + 45, y0 + 150, text="=", fill=GOLD,
                      font=("Arial", 30, "bold"))

        self.geo_stats.config(
            text=f"a² = {a*a}   |   b² = {b*b}   |   a² − b² = {a*a - b*b}"
                 f"   |   (a−b)(a+b) = {(a-b)*(a+b)}   ✔ متساويان")


if __name__ == "__main__":
    App().mainloop()
