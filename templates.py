"""Modelos de arte da página @sintomadegravidez (paleta e logo da marca).

Cada funcao recebe um dicionario com o conteudo (vindo da IA) e devolve o HTML
de cada slide. Os textos sao cortados nos limites abaixo para nao estourar o layout.
"""
import base64
import html as _html
import os
import re

import illustrations

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


def ilus(nome, textos, indice=0):
    """SVG da ilustracao (a IA escolhe o nome; se errar, deduz pelo texto)."""
    svg = illustrations.ILUSTRACOES[illustrations.escolher(nome, *textos, indice=indice)]
    return svg.replace("<svg ", '<svg style="width:100%;height:100%;display:block" ', 1)


def selo_ilus(nome, textos, tamanho, indice=0, fundo="rgba(255,255,255,.78)", anel="rgba(255,255,255,.9)"):
    """Ilustracao dentro de um circulo com anel e confetes."""
    pad = int(tamanho * 0.14)
    return (f'<div style="position:relative;width:{tamanho}px;height:{tamanho}px;flex:none">'
            f'<div style="position:absolute;inset:-16px;border-radius:50%;border:3px dashed {anel}"></div>'
            f'<div style="position:absolute;inset:0;border-radius:50%;background:{fundo};'
            f'box-shadow:0 18px 50px rgba(74,35,64,.16);padding:{pad}px">{ilus(nome, textos, indice)}</div></div>')


def confete(cores=None, n=10, semente=1):
    """Estrelinhas, bolinhas e coracoes espalhados nas bordas (decoracao)."""
    cores = cores or [PINK, BLUE, "#FFD98E", "#FFFFFF"]
    pos = [(7, 18), (92, 12), (86, 40), (4, 52), (94, 66), (10, 82), (88, 90), (50, 4), (30, 94), (72, 96)]
    formas = [
        '<svg viewBox="0 0 20 20" width="{t}" height="{t}"><path d="M10 0l2.6 7.4L20 10l-7.4 2.6L10 20l-2.6-7.4L0 10l7.4-2.6z" fill="{c}"/></svg>',
        '<svg viewBox="0 0 20 20" width="{t}" height="{t}"><circle cx="10" cy="10" r="8" fill="{c}"/></svg>',
        '<svg viewBox="0 0 20 20" width="{t}" height="{t}"><path d="M10 18C2 12 1 6 5 3.6 7.6 2.2 9.6 3.4 10 5.4c.4-2 2.4-3.2 5-1.8 4 2.4 3 8.4-5 14.4z" fill="{c}"/></svg>',
    ]
    out = []
    for k in range(min(n, len(pos))):
        x, y = pos[(k + semente) % len(pos)]
        t = 22 + ((k * 7 + semente * 5) % 5) * 8
        forma = formas[(k + semente) % 3].format(t=t, c=cores[(k + semente) % len(cores)])
        out.append(f'<div style="position:absolute;left:{x}%;top:{y}%;opacity:.85;z-index:0">{forma}</div>')
    return "".join(out)


PADRAO_PONTOS = ("background-image: radial-gradient(rgba(196,82,138,.13) 3.5px, transparent 3.5px);"
                 "background-size: 46px 46px;")

# Mascara de marca aplicada SEMPRE por cima das fotos, para nao parecerem fotos de banco de imagens:
# tom rosado/azulado da marca, trama de pontos, granulacao e moldura fina.
MASCARA_CSS = r"""
.foto { filter: saturate(.8) contrast(1.07) brightness(.97) sepia(.1); }
.tinta { position: absolute; inset: 0; background: linear-gradient(160deg, rgba(244,198,220,.62) 0%, rgba(196,82,138,.30) 48%, rgba(173,220,245,.5) 100%); mix-blend-mode: soft-light; }
.tom { position: absolute; inset: 0; background: rgba(196,82,138,.10); mix-blend-mode: multiply; }
.pontos { position: absolute; inset: 0; background-image: radial-gradient(rgba(255,255,255,.5) 3px, transparent 3.5px); background-size: 46px 46px; -webkit-mask-image: linear-gradient(135deg, #000 0%, transparent 38%); mask-image: linear-gradient(135deg, #000 0%, transparent 38%); }
.graos { position: absolute; inset: 0; opacity: .2; mix-blend-mode: overlay; background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .5 0 0 0 0 .5 0 0 0 0 .5 0 0 0 .9 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>"); }
.moldura { position: absolute; inset: 26px; border: 3px solid rgba(255,255,255,.78); border-radius: 46px; }
"""
# Seta desenhada em SVG (a fonte do servidor nao tem o glifo da seta e mostrava um quadrado vazio).
SETA = ('<svg width="34" height="22" viewBox="0 0 34 22" style="vertical-align:middle;margin-left:8px">'
        '<path d="M2 11h26M20 3l9 8-9 8" fill="none" stroke="currentColor" stroke-width="3.5" '
        'stroke-linecap="round" stroke-linejoin="round"/></svg>')
MASCARA_HTML = ('<div class="tinta"></div><div class="tom"></div><div class="pontos"></div>'
                '<div class="graos"></div><div class="moldura"></div>')


def capa_foto(c, total):
    return f"""
<html><head><meta charset="utf-8"><style>{base_css()}
body {{ background: {WINE}; color: white; }}
.foto {{ position: absolute; inset: 0; background: url('{c.get("foto")}') center/cover no-repeat; }}
.veu {{ position: absolute; inset: 0; background: linear-gradient(180deg, rgba(74,35,64,.55) 0%, rgba(74,35,64,0) 24%, rgba(74,35,64,.35) 44%, rgba(74,35,64,.93) 78%, rgba(74,35,64,.97) 100%); }}
{MASCARA_CSS}
.pill2 {{ padding: 14px 30px; border-radius: 999px; background: {PINK}; color: white; font-size: 28px; font-weight: 700; letter-spacing: 3px; text-transform: uppercase; }}
.base {{ margin-top: auto; }}
h1 {{ font-size: 100px; line-height: 1.04; font-weight: 800; letter-spacing: -2px; text-shadow: 0 4px 24px rgba(0,0,0,.35); }}
h1 span {{ color: #FFC2DE; }}
.sub {{ margin-top: 26px; font-size: 40px; line-height: 1.3; font-weight: 500; opacity: .95; }}
.footer2 {{ margin-top: 40px; display: flex; justify-content: space-between; align-items: center; font-size: 28px; font-weight: 600; }}
</style></head><body>
<div class="slide"><div class="foto"></div><div class="veu"></div>{MASCARA_HTML}
<div class="content">
  <div style="display:flex;justify-content:space-between;align-items:center"><div class="pill2">{esc(cortar(c.get('etiqueta'), 'etiqueta'))}</div>{logo_img(120)}</div>
  <div class="base">
    <h1>{esc(cortar(c.get('capa_titulo'), 'capa_titulo'))} <span>{esc(cortar(c.get('capa_destaque'), 'capa_destaque'))}</span></h1>
    <div class="sub">{esc(cortar(c.get('capa_sub'), 'capa_sub'))}</div>
    <div class="footer2">{handle_html()}<span>Deslize {SETA}</span></div>
  </div>
</div></div></body></html>"""


def capa(c, total):
    if c.get("foto"):
        return capa_foto(c, total)
    textos = [c.get("etiqueta"), c.get("capa_titulo"), c.get("capa_destaque"), c.get("capa_sub")]
    selo = selo_ilus(c.get("capa_ilustracao") or c.get("ilustracao"), textos, 470, indice=0)
    return f"""
<html><head><meta charset="utf-8"><style>{base_css()}
body {{ background: linear-gradient(155deg, #BFE5F9 0%, #F4C6DC 100%); color: {WINE}; }}
.pill2 {{ padding: 14px 30px; border-radius: 999px; background: {WINE}; color: white; font-size: 28px; font-weight: 700; letter-spacing: 3px; align-self: flex-start; text-transform: uppercase; }}
h1 {{ font-size: 108px; line-height: 1.04; font-weight: 800; letter-spacing: -2px; margin-top: 44px; }}
h1 span {{ color: {PINK}; }}
.sub {{ margin-top: 30px; font-size: 40px; line-height: 1.3; font-weight: 500; max-width: 900px; }}
.arte {{ flex: 1; display: flex; align-items: center; justify-content: center; min-height: 0; }}
.footer2 {{ display: flex; justify-content: space-between; align-items: center; font-size: 28px; font-weight: 600; }}
.bigring {{ position: absolute; border-radius: 50%; background: rgba(255,255,255,.28); width: 900px; height: 900px; left: 90px; top: 560px; }}
</style></head><body>
<div class="slide"><div class="bigring"></div>{confete(semente=1)}
<div class="content">
  <div style="display:flex;justify-content:space-between;align-items:center"><div class="pill2">{esc(cortar(c.get('etiqueta'), 'etiqueta'))}</div>{logo_img(120)}</div>
  <h1>{esc(cortar(c.get('capa_titulo'), 'capa_titulo'))} <span>{esc(cortar(c.get('capa_destaque'), 'capa_destaque'))}</span></h1>
  <div class="sub">{esc(cortar(c.get('capa_sub'), 'capa_sub'))}</div>
  <div class="arte">{selo}</div>
  <div class="footer2">{handle_html()}<span>Deslize {SETA}</span></div>
</div></div></body></html>"""


def miolo(c, i, total, item):
    textos = [item.get("titulo"), item.get("frase"), item.get("texto")]
    selo = selo_ilus(item.get("ilustracao") or item.get("icone"), textos, 300, indice=i,
                     fundo=SOFT if i % 2 == 0 else AQUA_SOFT, anel=PINK)
    return f"""
<html><head><meta charset="utf-8"><style>{base_css()}
body {{ background-color: {CREAM}; {PADRAO_PONTOS} }}
.linha {{ display: flex; align-items: center; justify-content: space-between; gap: 30px; margin-top: 34px; }}
.num {{ font-size: 26px; letter-spacing: 4px; font-weight: 700; color: {PINK}; }}
h1 {{ font-size: 80px; line-height: 1.05; color: {WINE}; font-weight: 800; margin-top: 12px; }}
.label {{ margin-top: 24px; font-size: 24px; letter-spacing: 4px; font-weight: 600; color: {PINK}; }}
.quote {{ margin-top: 6px; font-size: 48px; line-height: 1.2; font-weight: 700; font-style: italic; color: {PINK}; }}
.body {{ margin-top: 26px; font-size: 37px; line-height: 1.42; font-weight: 400; }}
.tip {{ margin-top: 30px; background: white; border-left: 12px solid {BLUE}; border-radius: 26px; padding: 26px 34px; font-size: 34px; line-height: 1.38; box-shadow: 0 10px 30px rgba(196,82,138,.14); }}
.tip b {{ color: {PINK}; }}
</style></head><body>
<div class="slide"><div class="blob1"></div><div class="blob2"></div>
<div class="content">
  <div class="top"><span class="pill">{esc(cortar(c.get('etiqueta'), 'etiqueta'))}</span><span class="count">{i:02d}/{total:02d}</span></div>
  <div class="linha"><div style="flex:1"><div class="num">DICA {i - 1:02d}</div><h1>{esc(cortar(item.get('titulo'), 'titulo'))}</h1></div>{selo}</div>
  <div class="label">O QUE O CORPO DIZ</div>
  <div class="quote">“{esc(cortar(item.get('frase'), 'frase'))}”</div>
  <div class="body">{esc(cortar(item.get('texto'), 'texto'))}</div>
  <div class="tip"><b>Ajuda:</b> {esc(cortar(item.get('dica'), 'dica'))}</div>
  <div class="footer">{handle_html()}<span>Deslize {SETA}</span></div>
</div></div></body></html>"""


def alerta(c, i, total):
    itens = [cortar(x, "alerta_item") for x in (c.get("alerta_itens") or [])][:4]
    lis = "".join('<li><span class="n">%d</span><span>%s</span></li>' % (k + 1, esc(t)) for k, t in enumerate(itens))
    selo = selo_ilus("estetoscopio", [], 230, fundo="rgba(255,255,255,.92)", anel=BLUE)
    return f"""
<html><head><meta charset="utf-8"><style>{base_css()}
body {{ background: {SLATE}; color: white; }}
.pill {{ background: {BLUE}; color: {WINE}; }}
.count {{ color: {BLUE}; }}
.linha {{ display: flex; align-items: center; justify-content: space-between; gap: 30px; margin-top: 40px; }}
h1 {{ font-size: 66px; line-height: 1.08; font-weight: 800; flex: 1; }}
h1 span {{ color: {BLUE}; }}
ul {{ list-style: none; margin-top: 36px; }}
li {{ display: flex; gap: 24px; align-items: center; font-size: 34px; line-height: 1.3; background: rgba(255,255,255,.09); border-radius: 24px; padding: 20px 28px; margin-bottom: 16px; }}
.n {{ flex: none; width: 54px; height: 54px; border-radius: 50%; background: {BLUE}; color: {WINE}; font-weight: 800; display: flex; align-items: center; justify-content: center; font-size: 30px; }}
.close {{ margin-top: 14px; margin-bottom: 30px; font-size: 34px; line-height: 1.35; font-weight: 600; color: {SOFT}; }}
.footer {{ color: {BLUE}; }}
.blob1 {{ background: rgba(255,255,255,.06); }} .blob2 {{ background: rgba(255,255,255,.05); }}
</style></head><body>
<div class="slide"><div class="blob1"></div><div class="blob2"></div>
<div class="content">
  <div class="top"><span class="pill">ATENÇÃO</span><span class="count">{i:02d}/{total:02d}</span></div>
  <div class="linha"><h1>Quando é hora de <span>falar com o médico</span></h1>{selo}</div>
  <ul>{lis}</ul>
  <div class="close">Na dúvida, procure atendimento. Perguntar nunca é exagero.</div>
  <div class="footer">{handle_html()}<span>Deslize {SETA}</span></div>
</div></div></body></html>"""


def final(c, i, total):
    return f"""
<html><head><meta charset="utf-8"><style>{base_css()}
body {{ background: linear-gradient(160deg, #F4C6DC 0%, #BFE5F9 100%); color: {WINE}; }}
.pill {{ background: {WINE}; color: white; }}
.count {{ color: {WINE}; }}
h1 {{ font-size: 104px; line-height: 1.04; font-weight: 800; margin-top: 40px; }}
.msg {{ margin-top: 30px; font-size: 44px; line-height: 1.35; font-weight: 500; }}
.cta {{ margin-top: 40px; background: white; color: {WINE}; border-radius: 30px; padding: 34px 40px; font-size: 38px; line-height: 1.35; font-weight: 600; box-shadow: 0 14px 40px rgba(74,35,64,.14); }}
.cta b {{ color: {PINK}; }}
.note {{ margin-top: 26px; font-size: 24px; line-height: 1.4; opacity: .92; }}
.footer {{ color: {WINE}; }}
.blob1 {{ background: rgba(255,255,255,.35); }} .blob2 {{ background: rgba(255,255,255,.3); }}
</style></head><body>
<div class="slide"><div class="blob1"></div><div class="blob2"></div>{confete(semente=4)}
<div class="content">
  <div class="top"><span class="pill">PARA VOCÊ</span><span class="count">{i:02d}/{total:02d}</span></div>
  <div style="margin-top:30px;display:flex;align-items:center;gap:34px">{logo_img(210)}{selo_ilus('abraco', [], 210, fundo='rgba(255,255,255,.7)')}</div>
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


def post_imagem_foto(c):
    html = f"""
<html><head><meta charset="utf-8"><style>{base_css()}
body {{ background: {WINE}; color: {WINE}; }}
.foto {{ position: absolute; inset: 0; background: url('{c.get("foto")}') center 12%/cover no-repeat; }}
.veu {{ position: absolute; inset: 0; background: linear-gradient(180deg, rgba(74,35,64,.5) 0%, rgba(74,35,64,0) 26%, rgba(74,35,64,0) 55%, rgba(74,35,64,.45) 100%); }}
{MASCARA_CSS}
.cartao {{ position: absolute; left: 50px; right: 50px; bottom: 50px; background: rgba(255,255,255,.96); border-radius: 50px; padding: 44px 50px 36px; box-shadow: 0 24px 60px rgba(74,35,64,.35); }}
h1 {{ font-size: 62px; line-height: 1.07; font-weight: 800; color: {WINE}; }}
.texto {{ margin-top: 20px; font-size: 33px; line-height: 1.4; color: {TEXT}; }}
.tip {{ margin-top: 22px; background: {SOFT}; border-left: 10px solid {PINK}; border-radius: 20px; padding: 18px 26px; font-size: 30px; line-height: 1.35; }}
.tip b {{ color: {PINK}; }}
.rod {{ margin-top: 22px; display: flex; justify-content: space-between; align-items: center; font-size: 23px; font-weight: 600; color: {PINK}; }}
.note {{ font-size: 19px; color: {TEXT}; opacity: .7; margin-top: 12px; }}
</style></head><body>
<div class="slide" style="padding:0"><div class="foto"></div><div class="veu"></div>{MASCARA_HTML}
<div style="position:absolute;left:80px;right:80px;top:70px;display:flex;justify-content:space-between;align-items:center;z-index:2"><span class="pill" style="font-size:26px;font-weight:600;letter-spacing:3px">{esc(cortar(c.get('etiqueta'), 'etiqueta'))}</span>{logo_img(104)}</div>
<div class="cartao">
  <h1>{esc(cortar(c.get('titulo'), 'img_titulo'))}</h1>
  <div class="texto">{esc(cortar(c.get('texto'), 'img_texto'))}</div>
  <div class="tip"><b>Dica:</b> {esc(cortar(c.get('dica'), 'img_dica'))}</div>
  <div class="note">{DISCLAIMER_CURTO}</div>
  <div class="rod">{handle_html()}<span></span></div>
</div></div></body></html>"""
    return [(html, 1080, 1350)]


def post_imagem(c):
    if c.get("foto"):
        return post_imagem_foto(c)
    textos = [c.get("etiqueta"), c.get("titulo"), c.get("texto")]
    selo = selo_ilus(c.get("ilustracao"), textos, 330, indice=3, fundo="rgba(255,255,255,.85)", anel=PINK)
    html = f"""
<html><head><meta charset="utf-8"><style>{base_css()}
body {{ background-color: #FBEAF3; background-image: radial-gradient(rgba(196,82,138,.12) 3.5px, transparent 3.5px), linear-gradient(160deg, #F8E1EE 0%, #E3F4FC 100%); background-size: 46px 46px, 100% 100%; color: {WINE}; }}
.linha {{ display: flex; align-items: center; justify-content: space-between; gap: 30px; margin-top: 40px; }}
h1 {{ font-size: 78px; line-height: 1.06; font-weight: 800; flex: 1; }}
.texto {{ margin-top: 40px; font-size: 40px; line-height: 1.45; font-weight: 400; color: {TEXT}; }}
.tip {{ margin-top: 36px; background: white; border-left: 12px solid {BLUE}; border-radius: 26px; padding: 28px 36px; font-size: 36px; line-height: 1.4; box-shadow: 0 10px 30px rgba(196,82,138,.14); }}
.tip b {{ color: {PINK}; }}
.note {{ margin-top: 24px; font-size: 22px; opacity: .85; }}
</style></head><body>
<div class="slide">{confete(semente=2)}
<div class="content">
  <div class="top"><span class="pill">{esc(cortar(c.get('etiqueta'), 'etiqueta'))}</span><span>{logo_img(96)}</span></div>
  <div class="linha"><h1>{esc(cortar(c.get('titulo'), 'img_titulo'))}</h1>{selo}</div>
  <div class="texto">{esc(cortar(c.get('texto'), 'img_texto'))}</div>
  <div class="tip"><b>Dica:</b> {esc(cortar(c.get('dica'), 'img_dica'))}</div>
  <div class="note">{DISCLAIMER_CURTO}</div>
  <div class="footer">{handle_html()}<span></span></div>
</div></div></body></html>"""
    return [(html, 1080, 1350)]


def post_stories_foto(c):
    css = base_css(1920).replace("padding: 80px 90px 70px", "padding: 150px 80px 130px")
    html = f"""
<html><head><meta charset="utf-8"><style>{css}
body {{ background: {WINE}; color: {WINE}; }}
.foto {{ position: absolute; inset: 0; background: url('{c.get("foto")}') center/cover no-repeat; }}
.veu {{ position: absolute; inset: 0; background: linear-gradient(180deg, rgba(74,35,64,.55) 0%, rgba(74,35,64,0) 22%, rgba(74,35,64,0) 50%, rgba(74,35,64,.55) 100%); }}
{MASCARA_CSS}
.pill2 {{ padding: 16px 34px; border-radius: 999px; background: {PINK}; color: white; font-size: 32px; font-weight: 700; letter-spacing: 3px; text-transform: uppercase; }}
.cartao {{ margin-top: auto; background: rgba(255,255,255,.95); border-radius: 56px; padding: 52px 54px 44px; box-shadow: 0 30px 80px rgba(74,35,64,.4); }}
h1 {{ font-size: 76px; line-height: 1.06; font-weight: 800; color: {WINE}; }}
.texto {{ margin-top: 28px; font-size: 40px; line-height: 1.4; font-weight: 500; color: {TEXT}; }}
.rodape {{ margin-top: 28px; font-size: 38px; font-weight: 700; color: {PINK}; }}
.nota {{ margin-top: 20px; font-size: 22px; color: {TEXT}; opacity: .7; }}
.brand {{ margin-top: 26px; font-size: 32px; font-weight: 600; color: white; text-shadow: 0 2px 12px rgba(0,0,0,.4); }}
</style></head><body>
<div class="slide"><div class="foto"></div><div class="veu"></div>{MASCARA_HTML}
<div class="content">
  <div style="display:flex;justify-content:space-between;align-items:center"><div class="pill2">{esc(cortar(c.get('etiqueta'), 'etiqueta'))}</div>{logo_img(140)}</div>
  <div class="cartao">
    <h1>{esc(cortar(c.get('titulo'), 'st_titulo'))}</h1>
    <div class="texto">{esc(cortar(c.get('texto'), 'st_texto'))}</div>
    <div class="rodape">{esc(cortar(c.get('rodape'), 'st_rodape'))}</div>
    <div class="nota">{DISCLAIMER_CURTO}</div>
  </div>
  <div class="brand">{HANDLE}</div>
</div></div></body></html>"""
    return [(html, 1080, 1920)]


def post_stories(c):
    if c.get("foto"):
        return post_stories_foto(c)
    css = base_css(1920).replace("padding: 80px 90px 70px", "padding: 150px 90px 130px")
    textos = [c.get("etiqueta"), c.get("titulo"), c.get("texto")]
    selo = selo_ilus(c.get("ilustracao"), textos, 520, indice=1)
    html = f"""
<html><head><meta charset="utf-8"><style>{css}
body {{ background: linear-gradient(165deg, #BFE5F9 0%, #F4C6DC 100%); color: {WINE}; }}
.bigring {{ position: absolute; border-radius: 50%; background: rgba(255,255,255,.26); width: 1100px; height: 1100px; left: -10px; top: 330px; }}
.pill2 {{ padding: 16px 34px; border-radius: 999px; background: {WINE}; color: white; font-size: 32px; font-weight: 700; letter-spacing: 3px; text-transform: uppercase; }}
.arte {{ margin-top: 40px; display: flex; justify-content: center; }}
h1 {{ margin-top: 70px; font-size: 96px; line-height: 1.06; font-weight: 800; text-align: center; }}
.texto {{ margin-top: 46px; font-size: 46px; line-height: 1.4; font-weight: 500; background: rgba(255,255,255,.76); border-radius: 36px; padding: 40px 44px; }}
.rodape {{ margin-top: 40px; font-size: 40px; font-weight: 700; color: {PINK}; text-align: center; }}
.nota {{ margin-top: auto; font-size: 26px; opacity: .85; }}
.brand {{ margin-top: 22px; display: flex; align-items: center; gap: 18px; font-size: 32px; font-weight: 600; color: {PINK}; }}
</style></head><body>
<div class="slide"><div class="bigring"></div>{confete(semente=3)}
<div class="content">
  <div style="display:flex;justify-content:space-between;align-items:center"><div class="pill2">{esc(cortar(c.get('etiqueta'), 'etiqueta'))}</div>{logo_img(140)}</div>
  <div class="arte">{selo}</div>
  <h1>{esc(cortar(c.get('titulo'), 'st_titulo'))}</h1>
  <div class="texto">{esc(cortar(c.get('texto'), 'st_texto'))}</div>
  <div class="rodape">{esc(cortar(c.get('rodape'), 'st_rodape'))}</div>
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
