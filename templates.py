"""Modelos de arte da página @sintomadegravidez (paleta e logo da marca).

Cada funcao recebe um dicionario com o conteudo (vindo da IA) e devolve o HTML
de cada slide. Os textos sao cortados nos limites abaixo para nao estourar o layout.
"""
import base64
import html as _html
import os
import re

HANDLE = "@sintomadegravidez"

WINE = "#4A2340"
PINK = "#C4528A"
BLUE = "#ADDCF5"
SOFT = "#F8E1EE"
AQUA_SOFT = "#E3F4FC"
CREAM = "#FDF7FB"
TEXT = "#3B2A3A"
SLATE = "#2B4C66"

DISCLAIMER_CURTO = "Conteúdo informativo. Não substitui o acompanhamento do pré-natal."

LIMITES = {
    "etiqueta": 20,
    "capa_titulo": 44,
    "capa_destaque": 24,
    "capa_sub": 70,
    "titulo": 24,
    "frase": 46,
    "texto": 190,
    "dica": 110,
    "alerta_item": 62,
    "final_titulo": 26,
    "final_msg": 110,
    "img_titulo": 62,
    "img_texto": 230,
    "img_dica": 110,
    "st_titulo": 56,
    "st_texto": 210,
    "st_rodape": 42,
}

# Termos que mandam o post para revisao humana (status "rascunho").
TERMOS_SENSIVEIS = [
    "dosagem", "comprimido", "remédio", "remedio", "medicamento", "tome ", "tomar ",
    "suplemento", "vitamina", "jejum", "emagrec", "garantimos", "resultado garantido", "resultados garantidos",
    "sucesso garantido", "eficácia garantida", "diagnóstico",
    "diagnostico", "aborto", "interromper", "100%", "cura ", "curar",
]

ICONS = {
    "wave": '<svg viewBox="0 0 120 120" width="120" height="120" fill="none" stroke="{c}" stroke-width="9" stroke-linecap="round"><path d="M12 40 q12 -18 24 0 t24 0 t24 0 t24 0"/><path d="M12 68 q12 -18 24 0 t24 0 t24 0 t24 0"/><path d="M12 96 q12 -18 24 0 t24 0 t24 0 t24 0"/></svg>',
    "moon": '<svg viewBox="0 0 120 120" width="120" height="120" fill="{c}"><path d="M78 14 a48 48 0 1 0 28 76 a40 40 0 0 1 -28 -76z"/><circle cx="92" cy="28" r="5"/><circle cx="104" cy="50" r="3.5"/></svg>',
    "heart": '<svg viewBox="0 0 120 120" width="120" height="120" fill="{c}"><path d="M60 104 C14 70 8 40 28 24 C42 13 56 20 60 32 C64 20 78 13 92 24 C112 40 106 70 60 104z"/></svg>',
    "drop": '<svg viewBox="0 0 120 120" width="120" height="120" fill="{c}"><path d="M60 10 C60 10 20 56 20 78 a40 40 0 0 0 80 0 C100 56 60 10 60 10z"/></svg>',
    "smile": '<svg viewBox="0 0 120 120" width="120" height="120" fill="none" stroke="{c}" stroke-width="8" stroke-linecap="round"><circle cx="60" cy="60" r="48"/><circle cx="42" cy="50" r="4" fill="{c}"/><circle cx="78" cy="50" r="4" fill="{c}"/><path d="M36 74 q24 26 48 0"/></svg>',
    "alert": '<svg viewBox="0 0 120 120" width="120" height="120" fill="none" stroke="{c}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"><path d="M60 16 L108 98 H12 Z"/><path d="M60 46 V70"/><circle cx="60" cy="86" r="2" fill="{c}"/></svg>',
}

_LOGO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "logo.png")
try:
    with open(_LOGO_PATH, "rb") as _f:
        LOGO = "data:image/png;base64," + base64.b64encode(_f.read()).decode()
except OSError:
    LOGO = None


def esc(value):
    return _html.escape(str(value or "").strip(), quote=False)


def cortar(texto, chave):
    """Corta no limite, preferindo terminar numa frase ou palavra inteira."""
    t = " ".join(str(texto or "").split())
    n = LIMITES[chave]
    if len(t) <= n:
        return t
    corte = t[:n]
    fim = max(corte.rfind(". "), corte.rfind("! "), corte.rfind("? "))
    if fim >= n * 0.4:
        return corte[: fim + 1]
    if corte.endswith((".", "!", "?")):
        return corte
    if " " in corte[n // 2:]:
        corte = corte[: corte.rfind(" ")]
    return corte.rstrip(" ,;:-") + "…"


def logo_img(size):
    if not LOGO:
        return ""
    return ('<img src="%s" style="width:%dpx;height:%dpx;border-radius:50%%;object-fit:contain;'
            'filter:drop-shadow(0 6px 14px rgba(74,35,64,.22));">' % (LOGO, size, size))


def handle_html():
    return '<span style="display:flex;align-items:center;gap:14px">%s%s</span>' % (logo_img(56), HANDLE)


def icone(nome, cor):
    return ICONS.get(nome, ICONS["heart"]).format(c=cor)


def base_css(altura=1350):
    return f"""
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: 1080px; height: {altura}px; }}
body {{ font-family: 'Poppins', sans-serif; color: {TEXT}; overflow: hidden; }}
.slide {{ position: relative; width: 1080px; height: {altura}px; padding: 80px 90px 70px; display: flex; flex-direction: column; }}
.top {{ display: flex; justify-content: space-between; align-items: center; font-size: 26px; font-weight: 600; letter-spacing: 3px; }}
.pill {{ padding: 12px 26px; border-radius: 999px; background: {PINK}; color: white; text-transform: uppercase; }}
.count {{ color: {PINK}; }}
.footer {{ margin-top: auto; display: flex; justify-content: space-between; align-items: center; font-size: 26px; font-weight: 600; color: {PINK}; }}
.blob1 {{ position: absolute; width: 520px; height: 520px; border-radius: 50%; right: -180px; top: -160px; background: {SOFT}; z-index: 0; }}
.blob2 {{ position: absolute; width: 380px; height: 380px; border-radius: 50%; left: -150px; bottom: 120px; background: {AQUA_SOFT}; z-index: 0; }}
.content {{ position: relative; z-index: 1; display: flex; flex-direction: column; flex: 1; }}
"""


def capa(c, total):
    return f"""
<html><head><meta charset="utf-8"><style>{base_css()}
body {{ background: linear-gradient(155deg, #BFE5F9 0%, #F4C6DC 100%); color: {WINE}; }}
.ring {{ position: absolute; border-radius: 50%; border: 3px solid rgba(255,255,255,.75); }}
.r1 {{ width: 760px; height: 760px; right: -300px; top: 380px; }}
.r2 {{ width: 520px; height: 520px; right: -170px; top: 500px; }}
.dot {{ position: absolute; border-radius: 50%; background: rgba(255,255,255,.55); }}
.pill2 {{ padding: 14px 30px; border-radius: 999px; background: {WINE}; color: white; font-size: 28px; font-weight: 700; letter-spacing: 3px; align-self: flex-start; text-transform: uppercase; }}
.hero {{ margin-top: 150px; }}
h1 {{ font-size: 118px; line-height: 1.04; font-weight: 800; letter-spacing: -2px; }}
h1 span {{ color: {PINK}; }}
.sub {{ margin-top: 48px; font-size: 44px; line-height: 1.35; font-weight: 500; max-width: 920px; }}
.footer2 {{ margin-top: auto; display: flex; justify-content: space-between; font-size: 28px; font-weight: 600; }}
.heart {{ position: absolute; right: 90px; top: 90px; }}
</style></head><body>
<div class="slide"><div class="ring r1"></div><div class="ring r2"></div>
<div class="dot" style="width:90px;height:90px;left:640px;top:760px"></div>
<div class="dot" style="width:46px;height:46px;left:860px;top:690px"></div>
<div class="heart">{logo_img(170) or icone('heart', 'rgba(255,255,255,.9)')}</div>
<div class="content">
  <div class="pill2">{esc(cortar(c.get('etiqueta'), 'etiqueta'))}</div>
  <div class="hero"><h1>{esc(cortar(c.get('capa_titulo'), 'capa_titulo'))} <span>{esc(cortar(c.get('capa_destaque'), 'capa_destaque'))}</span></h1>
  <div class="sub">{esc(cortar(c.get('capa_sub'), 'capa_sub'))}</div></div>
  <div class="footer2">{handle_html()}<span>Deslize &rarr;</span></div>
</div></div></body></html>"""


def miolo(c, i, total, item):
    return f"""
<html><head><meta charset="utf-8"><style>{base_css()}
body {{ background: {CREAM}; }}
.icon {{ width: 190px; height: 190px; border-radius: 50%; background: {PINK}; display: flex; align-items: center; justify-content: center; margin-top: 46px; }}
h1 {{ font-size: 88px; line-height: 1.05; color: {WINE}; font-weight: 800; margin-top: 34px; }}
.label {{ margin-top: 26px; font-size: 24px; letter-spacing: 4px; font-weight: 600; color: {PINK}; }}
.quote {{ margin-top: 8px; font-size: 50px; line-height: 1.2; font-weight: 700; font-style: italic; color: {PINK}; }}
.body {{ margin-top: 30px; font-size: 37px; line-height: 1.45; font-weight: 400; }}
.tip {{ margin-top: 34px; background: white; border-left: 12px solid {BLUE}; border-radius: 26px; padding: 28px 36px; font-size: 34px; line-height: 1.4; box-shadow: 0 10px 30px rgba(232,69,124,.12); }}
.tip b {{ color: {PINK}; }}
</style></head><body>
<div class="slide"><div class="blob1"></div><div class="blob2"></div>
<div class="content">
  <div class="top"><span class="pill">{esc(cortar(c.get('etiqueta'), 'etiqueta'))}</span><span class="count">{i:02d}/{total:02d}</span></div>
  <div class="icon">{icone(item.get('icone'), 'white')}</div>
  <h1>{esc(cortar(item.get('titulo'), 'titulo'))}</h1>
  <div class="label">O QUE O CORPO DIZ</div>
  <div class="quote">“{esc(cortar(item.get('frase'), 'frase'))}”</div>
  <div class="body">{esc(cortar(item.get('texto'), 'texto'))}</div>
  <div class="tip"><b>Ajuda:</b> {esc(cortar(item.get('dica'), 'dica'))}</div>
  <div class="footer">{handle_html()}<span>Deslize &rarr;</span></div>
</div></div></body></html>"""


def alerta(c, i, total):
    itens = [cortar(x, "alerta_item") for x in (c.get("alerta_itens") or [])][:4]
    lis = "".join('<li><span class="n">%d</span><span>%s</span></li>' % (k + 1, esc(t)) for k, t in enumerate(itens))
    return f"""
<html><head><meta charset="utf-8"><style>{base_css()}
body {{ background: {SLATE}; color: white; }}
.pill {{ background: {BLUE}; color: {WINE}; }}
.count {{ color: {BLUE}; }}
.icon {{ width: 150px; height: 150px; border-radius: 50%; background: {BLUE}; display: flex; align-items: center; justify-content: center; margin-top: 36px; }}
.icon svg {{ transform: scale(.85); }}
h1 {{ font-size: 70px; line-height: 1.08; font-weight: 800; margin-top: 26px; }}
h1 span {{ color: {BLUE}; }}
ul {{ list-style: none; margin-top: 32px; }}
li {{ display: flex; gap: 24px; align-items: center; font-size: 34px; line-height: 1.3; background: rgba(255,255,255,.09); border-radius: 24px; padding: 20px 28px; margin-bottom: 16px; }}
.n {{ flex: none; width: 54px; height: 54px; border-radius: 50%; background: {BLUE}; color: {WINE}; font-weight: 800; display: flex; align-items: center; justify-content: center; font-size: 30px; }}
.close {{ margin-top: 14px; margin-bottom: 30px; font-size: 34px; line-height: 1.35; font-weight: 600; color: {SOFT}; }}
.footer {{ color: {BLUE}; }}
.blob1 {{ background: rgba(255,255,255,.06); }} .blob2 {{ background: rgba(255,255,255,.05); }}
</style></head><body>
<div class="slide"><div class="blob1"></div><div class="blob2"></div>
<div class="content">
  <div class="top"><span class="pill">ATENÇÃO</span><span class="count">{i:02d}/{total:02d}</span></div>
  <div class="icon">{icone('alert', SLATE)}</div>
  <h1>Quando é hora de <span>falar com o médico</span></h1>
  <ul>{lis}</ul>
  <div class="close">Na dúvida, procure atendimento. Perguntar nunca é exagero.</div>
  <div class="footer">{handle_html()}<span>Deslize &rarr;</span></div>
</div></div></body></html>"""


def final(c, i, total):
    return f"""
<html><head><meta charset="utf-8"><style>{base_css()}
body {{ background: linear-gradient(160deg, #F4C6DC 0%, #BFE5F9 100%); color: {WINE}; }}
.pill {{ background: {WINE}; color: white; }}
.count {{ color: {WINE}; }}
h1 {{ font-size: 104px; line-height: 1.04; font-weight: 800; margin-top: 50px; }}
.msg {{ margin-top: 36px; font-size: 44px; line-height: 1.35; font-weight: 500; }}
.cta {{ margin-top: 44px; background: white; color: {WINE}; border-radius: 30px; padding: 34px 40px; font-size: 38px; line-height: 1.35; font-weight: 600; }}
.cta b {{ color: {PINK}; }}
.note {{ margin-top: 30px; font-size: 24px; line-height: 1.4; opacity: .92; }}
.footer {{ color: {WINE}; }}
.blob1 {{ background: rgba(255,255,255,.35); }} .blob2 {{ background: rgba(255,255,255,.3); }}
</style></head><body>
<div class="slide"><div class="blob1"></div><div class="blob2"></div>
<div class="content">
  <div class="top"><span class="pill">PARA VOCÊ</span><span class="count">{i:02d}/{total:02d}</span></div>
  <div style="margin-top:36px">{logo_img(240)}</div>
  <h1>{esc(cortar(c.get('final_titulo'), 'final_titulo'))}</h1>
  <div class="msg">{esc(cortar(c.get('final_msg'), 'final_msg'))}</div>
  <div class="cta"><b>Salve</b> este post para reler quando precisar e <b>marque</b> uma mãe que precisa ouvir isso.</div>
  <div class="note">{DISCLAIMER_CURTO}</div>
  <div class="footer">{handle_html()}<span></span></div>
</div></div></body></html>"""


def slides_carrossel(c):
    """Lista de (html, largura, altura) do carrossel."""
    itens = (c.get("itens") or [])[:5]
    total = 1 + len(itens) + 2
    saida = [capa(c, total)]
    for k, item in enumerate(itens, start=2):
        saida.append(miolo(c, k, total, item))
    saida.append(alerta(c, len(itens) + 2, total))
    saida.append(final(c, total, total))
    return [(h, 1080, 1350) for h in saida]


def post_imagem(c):
    html = f"""
<html><head><meta charset="utf-8"><style>{base_css()}
body {{ background: linear-gradient(160deg, #F8E1EE 0%, #E3F4FC 100%); color: {WINE}; }}
.ring {{ position: absolute; border-radius: 50%; border: 3px solid rgba(255,255,255,.8); width: 700px; height: 700px; right: -280px; bottom: 60px; }}
h1 {{ font-size: 90px; line-height: 1.06; font-weight: 800; margin-top: 60px; }}
.texto {{ margin-top: 40px; font-size: 40px; line-height: 1.45; font-weight: 400; color: {TEXT}; }}
.tip {{ margin-top: 40px; background: white; border-left: 12px solid {BLUE}; border-radius: 26px; padding: 30px 38px; font-size: 36px; line-height: 1.4; box-shadow: 0 10px 30px rgba(196,82,138,.14); }}
.tip b {{ color: {PINK}; }}
.note {{ margin-top: 26px; font-size: 22px; opacity: .85; }}
</style></head><body>
<div class="slide"><div class="ring"></div>
<div class="content">
  <div class="top"><span class="pill">{esc(cortar(c.get('etiqueta'), 'etiqueta'))}</span><span>{logo_img(96)}</span></div>
  <h1>{esc(cortar(c.get('titulo'), 'img_titulo'))}</h1>
  <div class="texto">{esc(cortar(c.get('texto'), 'img_texto'))}</div>
  <div class="tip"><b>Dica:</b> {esc(cortar(c.get('dica'), 'img_dica'))}</div>
  <div class="note">{DISCLAIMER_CURTO}</div>
  <div class="footer">{handle_html()}<span></span></div>
</div></div></body></html>"""
    return [(html, 1080, 1350)]


def post_stories(c):
    css = base_css(1920).replace("padding: 80px 90px 70px", "padding: 150px 90px 130px")
    html = f"""
<html><head><meta charset="utf-8"><style>{css}
body {{ background: linear-gradient(165deg, #BFE5F9 0%, #F4C6DC 100%); color: {WINE}; }}
.ring {{ position: absolute; border-radius: 50%; border: 3px solid rgba(255,255,255,.75); }}
.r1 {{ width: 820px; height: 820px; left: -330px; top: 1100px; }}
.r2 {{ width: 560px; height: 560px; right: -200px; top: 420px; }}
.centro {{ margin-top: 70px; display: flex; flex-direction: column; align-items: flex-start; }}
.pill2 {{ padding: 16px 34px; border-radius: 999px; background: {WINE}; color: white; font-size: 32px; font-weight: 700; letter-spacing: 3px; text-transform: uppercase; }}
h1 {{ margin-top: 60px; font-size: 104px; line-height: 1.06; font-weight: 800; }}
.texto {{ margin-top: 56px; font-size: 48px; line-height: 1.42; font-weight: 500; background: rgba(255,255,255,.72); border-radius: 36px; padding: 44px 46px; }}
.rodape {{ margin-top: 56px; font-size: 40px; font-weight: 700; color: {PINK}; }}
.nota {{ margin-top: auto; font-size: 26px; opacity: .85; }}
.brand {{ margin-top: 26px; display: flex; align-items: center; gap: 18px; font-size: 32px; font-weight: 600; color: {PINK}; }}
</style></head><body>
<div class="slide"><div class="ring r1"></div><div class="ring r2"></div>
<div class="content">
  <div style="display:flex;justify-content:space-between;align-items:center"><div class="pill2">{esc(cortar(c.get('etiqueta'), 'etiqueta'))}</div>{logo_img(150)}</div>
  <div class="centro">
    <h1>{esc(cortar(c.get('titulo'), 'st_titulo'))}</h1>
    <div class="texto">{esc(cortar(c.get('texto'), 'st_texto'))}</div>
    <div class="rodape">{esc(cortar(c.get('rodape'), 'st_rodape'))}</div>
  </div>
  <div class="nota">{DISCLAIMER_CURTO}</div>
  <div class="brand">{HANDLE}</div>
</div></div></body></html>"""
    return [(html, 1080, 1920)]


def revisar(conteudo):
    """Devolve os termos sensiveis encontrados em todo o conteudo."""
    partes = []

    def coletar(v):
        if isinstance(v, dict):
            for x in v.values():
                coletar(x)
        elif isinstance(v, list):
            for x in v:
                coletar(x)
        elif isinstance(v, str):
            partes.append(v)

    coletar(conteudo)
    texto = " " + " ".join(partes).lower() + " "
    achados = [t.strip() for t in TERMOS_SENSIVEIS
               if re.search(r"(?<![a-zà-ú])" + re.escape(t.strip()) + r"(?![a-zà-ú])", texto)]
    if re.search(r"\d\s?(mg|mcg|ml)\b", texto):
        achados.append("dose")
    return sorted(set(achados))
