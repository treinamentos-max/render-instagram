"""Biblioteca de ilustracoes (estilo plano, paleta da marca) para as artes.

Cada ilustracao e um SVG 400x400. A IA escolhe o nome que combina com o assunto;
se o nome vier errado, `escolher` procura por palavras-chave no texto do slide.
"""
import re
import unicodedata

W = "#4A2340"   # vinho
P = "#C4528A"   # rosa
B = "#ADDCF5"   # azul bebe
S = "#F8E1EE"   # rosa claro
A = "#E3F4FC"   # azul claro
Y = "#FFD98E"   # amarelo suave
WH = "#FFFFFF"


def _svg(corpo):
    return '<svg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">%s</svg>' % corpo


ILUSTRACOES = {}


def _reg(nome, corpo):
    ILUSTRACOES[nome] = _svg(corpo)


_reg("mamadeira", f"""
<rect x="150" y="150" width="100" height="200" rx="34" fill="{WH}" stroke="{W}" stroke-width="10"/>
<rect x="150" y="215" width="100" height="135" rx="30" fill="{B}"/>
<rect x="150" y="150" width="100" height="200" rx="34" fill="none" stroke="{W}" stroke-width="10"/>
<g stroke="{W}" stroke-width="7" stroke-linecap="round"><path d="M200 240h30M200 270h22M200 300h30"/></g>
<rect x="136" y="124" width="128" height="40" rx="16" fill="{P}" stroke="{W}" stroke-width="10"/>
<path d="M168 124 q0 -62 32 -62 q32 0 32 62z" fill="{S}" stroke="{W}" stroke-width="10" stroke-linejoin="round"/>
<circle cx="316" cy="96" r="10" fill="{Y}"/><circle cx="92" cy="170" r="8" fill="{P}"/><circle cx="326" cy="300" r="7" fill="{B}"/>
""")

_reg("carrinho", f"""
<path d="M70 210 a110 110 0 0 1 220 0z" fill="{P}" stroke="{W}" stroke-width="10" stroke-linejoin="round"/>
<path d="M70 210h280v26a36 36 0 0 1 -36 36h-110a134 134 0 0 1 -134 -62z" fill="{B}" stroke="{W}" stroke-width="10" stroke-linejoin="round"/>
<path d="M290 210l50 -92" fill="none" stroke="{W}" stroke-width="12" stroke-linecap="round"/>
<path d="M326 112h40" stroke="{W}" stroke-width="14" stroke-linecap="round"/>
<circle cx="130" cy="316" r="30" fill="{Y}" stroke="{W}" stroke-width="10"/>
<circle cx="296" cy="316" r="30" fill="{Y}" stroke="{W}" stroke-width="10"/>
<circle cx="150" cy="150" r="10" fill="{WH}"/><circle cx="90" cy="86" r="8" fill="{P}"/><circle cx="330" cy="236" r="0" fill="{P}"/>
""")

_reg("berco", f"""
<rect x="60" y="150" width="280" height="150" rx="22" fill="{A}" stroke="{W}" stroke-width="10"/>
<g stroke="{W}" stroke-width="10" stroke-linecap="round"><path d="M110 150v150M160 150v150M210 150v150M260 150v150M310 150v150"/></g>
<rect x="46" y="120" width="308" height="34" rx="16" fill="{P}" stroke="{W}" stroke-width="10"/>
<path d="M60 300v46M340 300v46" stroke="{W}" stroke-width="14" stroke-linecap="round"/>
<path d="M130 120 q70 -80 140 0" fill="none" stroke="{W}" stroke-width="10" stroke-linecap="round"/>
<path d="M200 64 l7 15 17 2 -12 12 3 17 -15 -8 -15 8 3 -17 -12 -12 17 -2z" fill="{Y}" stroke="{W}" stroke-width="6" stroke-linejoin="round"/>
""")

_reg("body", f"""
<path d="M130 70 q70 50 140 0 l70 50 -40 56 -30 -18 v108 q0 40 -30 56 h-30 q-30 -16 -30 -56 v-108 l-30 18 -40 -56z" fill="{S}" stroke="{W}" stroke-width="10" stroke-linejoin="round"/>
<path d="M130 70 q70 50 140 0" fill="none" stroke="{P}" stroke-width="10"/>
<path d="M200 190 c-30 -22 -40 -48 -18 -58 c10 -4 18 2 18 12 c0 -10 8 -16 18 -12 c22 10 12 36 -18 58z" fill="{P}"/>
<circle cx="88" cy="310" r="9" fill="{Y}"/><circle cx="318" cy="320" r="7" fill="{B}"/>
""")

_reg("chupeta", f"""
<circle cx="200" cy="108" r="58" fill="none" stroke="{P}" stroke-width="22"/>
<path d="M92 214 q108 -64 216 0 q-20 50 -108 50 q-88 0 -108 -50z" fill="{B}" stroke="{W}" stroke-width="10" stroke-linejoin="round"/>
<circle cx="200" cy="222" r="22" fill="{WH}" stroke="{W}" stroke-width="8"/>
<path d="M172 262 q-8 70 28 78 q36 -8 28 -78z" fill="{S}" stroke="{W}" stroke-width="10" stroke-linejoin="round"/>
<circle cx="326" cy="86" r="9" fill="{Y}"/><circle cx="76" cy="320" r="8" fill="{P}"/>
""")

_reg("estetoscopio", f"""
<path d="M110 70v100a90 90 0 0 0 180 0V70" fill="none" stroke="{W}" stroke-width="14" stroke-linecap="round"/>
<circle cx="110" cy="62" r="16" fill="{B}" stroke="{W}" stroke-width="8"/>
<circle cx="290" cy="62" r="16" fill="{B}" stroke="{W}" stroke-width="8"/>
<path d="M200 260v30" stroke="{W}" stroke-width="14" stroke-linecap="round"/>
<path d="M200 290 q0 50 60 50" fill="none" stroke="{W}" stroke-width="14" stroke-linecap="round"/>
<circle cx="288" cy="318" r="42" fill="{P}" stroke="{W}" stroke-width="10"/>
<path d="M288 336 c-18 -13 -24 -28 -11 -34 c6 -2 11 1 11 7 c0 -6 5 -9 11 -7 c13 6 7 21 -11 34z" fill="{WH}"/>
<circle cx="70" cy="200" r="8" fill="{Y}"/>
""")

_reg("calendario", f"""
<rect x="60" y="86" width="280" height="250" rx="30" fill="{WH}" stroke="{W}" stroke-width="10"/>
<path d="M60 150h280" stroke="{W}" stroke-width="10"/>
<path d="M60 116a30 30 0 0 1 30 -30h220a30 30 0 0 1 30 30v34H60z" fill="{P}" stroke="{W}" stroke-width="10" stroke-linejoin="round"/>
<g stroke="{W}" stroke-width="14" stroke-linecap="round"><path d="M130 62v44M270 62v44"/></g>
<g fill="{B}"><circle cx="112" cy="196" r="12"/><circle cx="166" cy="196" r="12"/><circle cx="220" cy="196" r="12"/><circle cx="112" cy="250" r="12"/><circle cx="166" cy="250" r="12"/><circle cx="112" cy="300" r="12"/><circle cx="166" cy="300" r="12"/></g>
<path d="M274 256 c-26 -18 -34 -40 -16 -48 c8 -3 16 2 16 10 c0 -8 8 -13 16 -10 c18 8 10 30 -16 48z" fill="{P}"/>
""")

_reg("mala", f"""
<path d="M150 120v-30a22 22 0 0 1 22 -22h56a22 22 0 0 1 22 22v30" fill="none" stroke="{W}" stroke-width="12"/>
<rect x="60" y="116" width="280" height="206" rx="30" fill="{P}" stroke="{W}" stroke-width="10"/>
<rect x="60" y="196" width="280" height="30" fill="{S}" stroke="{W}" stroke-width="8"/>
<rect x="176" y="186" width="48" height="50" rx="12" fill="{Y}" stroke="{W}" stroke-width="8"/>
<path d="M110 322v22M290 322v22" stroke="{W}" stroke-width="14" stroke-linecap="round"/>
<path d="M104 160l8 14 16 2 -12 11 3 16 -15 -8 -15 8 3 -16 -12 -11 16 -2z" fill="{WH}"/>
<circle cx="318" cy="70" r="9" fill="{B}"/>
""")

_reg("coracao_pulso", f"""
<path d="M200 332 C74 238 52 150 106 100 C146 64 192 82 200 130 C208 82 254 64 294 100 C348 150 326 238 200 332z" fill="{P}" stroke="{W}" stroke-width="10" stroke-linejoin="round"/>
<path d="M62 200h70l24 -46 40 96 28 -62 18 22h96" fill="none" stroke="{WH}" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>
<circle cx="330" cy="64" r="10" fill="{Y}"/><circle cx="70" cy="320" r="8" fill="{B}"/>
""")

_reg("agua", f"""
<path d="M104 96h192l-20 236a24 24 0 0 1 -24 22h-104a24 24 0 0 1 -24 -22z" fill="{WH}" stroke="{W}" stroke-width="10" stroke-linejoin="round"/>
<path d="M114 190h172l-10 142a24 24 0 0 1 -24 22h-104a24 24 0 0 1 -24 -22z" fill="{B}"/>
<path d="M104 96h192l-20 236a24 24 0 0 1 -24 22h-104a24 24 0 0 1 -24 -22z" fill="none" stroke="{W}" stroke-width="10" stroke-linejoin="round"/>
<path d="M200 214 c-26 32 -34 50 -22 68 c12 16 40 16 52 0 c12 -18 4 -36 -30 -68z" fill="{WH}" opacity=".9"/>
<path d="M330 80 c-14 20 -18 30 -10 40 c8 9 24 9 32 0 c8 -10 2 -20 -22 -40z" fill="{P}"/>
<circle cx="72" cy="150" r="8" fill="{Y}"/>
""")

_reg("fruta", f"""
<path d="M200 130 C120 84 56 140 74 232 C90 316 150 352 200 332 C250 352 310 316 326 232 C344 140 280 84 200 130z" fill="{P}" stroke="{W}" stroke-width="10" stroke-linejoin="round"/>
<path d="M200 130 q4 -50 38 -70" fill="none" stroke="{W}" stroke-width="12" stroke-linecap="round"/>
<path d="M226 78 q50 -34 92 6 q-46 34 -92 -6z" fill="{B}" stroke="{W}" stroke-width="10" stroke-linejoin="round"/>
<path d="M112 196 q-12 40 8 74" fill="none" stroke="{WH}" stroke-width="12" stroke-linecap="round" opacity=".8"/>
<circle cx="64" cy="94" r="9" fill="{Y}"/>
""")

_reg("lua_sono", f"""
<path d="M246 56 a150 150 0 1 0 100 212 a120 120 0 0 1 -100 -212z" fill="{Y}" stroke="{W}" stroke-width="10" stroke-linejoin="round"/>
<path d="M170 190 q18 14 36 0" fill="none" stroke="{W}" stroke-width="9" stroke-linecap="round"/>
<circle cx="146" cy="226" r="14" fill="{P}" opacity=".6"/>
<path d="M318 90 l7 15 17 2 -12 12 3 17 -15 -8 -15 8 3 -17 -12 -12 17 -2z" fill="{B}" stroke="{W}" stroke-width="6" stroke-linejoin="round"/>
<path d="M92 80 l5 10 11 1 -8 8 2 11 -10 -5 -10 5 2 -11 -8 -8 11 -1z" fill="{P}"/>
""")

_reg("gestante", f"""
<circle cx="170" cy="86" r="42" fill="{S}" stroke="{W}" stroke-width="10"/>
<path d="M130 70 q10 -46 66 -34 q-6 24 -34 30z" fill="{W}"/>
<path d="M150 130 q-34 50 -26 122 l10 90 h70 l-8 -80 q70 -10 74 -86 q-4 -64 -62 -66 q-40 -8 -58 20z" fill="{P}" stroke="{W}" stroke-width="10" stroke-linejoin="round"/>
<circle cx="236" cy="226" r="58" fill="{P}" stroke="{W}" stroke-width="10"/>
<path d="M236 252 c-18 -13 -24 -28 -11 -34 c6 -2 11 1 11 7 c0 -6 5 -9 11 -7 c13 6 7 21 -11 34z" fill="{WH}"/>
<circle cx="326" cy="90" r="10" fill="{Y}"/><circle cx="76" cy="200" r="8" fill="{B}"/>
""")

_reg("abraco", f"""
<path d="M150 322 C46 244 30 168 76 126 C110 96 148 110 150 150 C152 110 190 96 224 126 C270 168 254 244 150 322z" fill="{P}" stroke="{W}" stroke-width="10" stroke-linejoin="round"/>
<path d="M286 262 C228 220 218 178 244 156 C262 140 284 146 286 168 C288 146 310 140 328 156 C354 178 344 220 286 262z" fill="{B}" stroke="{W}" stroke-width="10" stroke-linejoin="round"/>
<circle cx="316" cy="70" r="10" fill="{Y}"/><circle cx="70" cy="64" r="8" fill="{S}"/>
""")

_reg("ultrassom", f"""
<rect x="52" y="76" width="296" height="250" rx="34" fill="{W}"/>
<path d="M200 118 L98 290 a190 190 0 0 0 204 0z" fill="{B}" stroke="{WH}" stroke-width="8" stroke-linejoin="round"/>
<path d="M142 250 q0 -62 58 -62 q58 0 58 60 q0 36 -44 38 q-30 2 -32 -24 q0 -22 22 -22" fill="none" stroke="{WH}" stroke-width="12" stroke-linecap="round"/>
<circle cx="226" cy="232" r="9" fill="{P}"/>
<circle cx="316" cy="110" r="9" fill="{P}"/><circle cx="82" cy="110" r="9" fill="{Y}"/>
<rect x="170" y="338" width="60" height="16" rx="8" fill="{W}"/>
""")

_reg("sapatinho", f"""
<path d="M84 280 V150 q0 -28 28 -28 h56 q16 0 16 18 q4 44 62 56 q86 18 86 62 v24z" fill="{B}" stroke="{W}" stroke-width="10" stroke-linejoin="round"/>
<path d="M70 280h276v22a24 24 0 0 1 -24 24H94a24 24 0 0 1 -24 -24z" fill="{WH}" stroke="{W}" stroke-width="10" stroke-linejoin="round"/>
<path d="M84 150h100" stroke="{P}" stroke-width="14" stroke-linecap="round"/>
<g fill="{P}"><circle cx="196" cy="196" r="9"/><circle cx="236" cy="214" r="9"/></g>
<path d="M118 214 c-22 -16 -28 -34 -12 -40 c8 -3 14 2 14 8 c0 -6 6 -11 14 -8 c16 6 8 24 -16 40z" fill="{WH}"/>
<circle cx="326" cy="92" r="10" fill="{Y}"/><circle cx="64" cy="76" r="8" fill="{P}"/>
""")

_reg("ursinho", f"""
<circle cx="112" cy="104" r="38" fill="{P}" stroke="{W}" stroke-width="10"/><circle cx="288" cy="104" r="38" fill="{P}" stroke="{W}" stroke-width="10"/>
<circle cx="112" cy="104" r="16" fill="{S}"/><circle cx="288" cy="104" r="16" fill="{S}"/>
<circle cx="200" cy="170" r="104" fill="{S}" stroke="{W}" stroke-width="10"/>
<ellipse cx="200" cy="200" rx="48" ry="38" fill="{WH}" stroke="{W}" stroke-width="8"/>
<circle cx="200" cy="190" r="12" fill="{W}"/>
<path d="M200 202v14 M180 222 q20 14 40 0" fill="none" stroke="{W}" stroke-width="8" stroke-linecap="round"/>
<circle cx="158" cy="150" r="10" fill="{W}"/><circle cx="242" cy="150" r="10" fill="{W}"/>
<path d="M150 276 q50 36 100 0 l22 70 h-144z" fill="{B}" stroke="{W}" stroke-width="10" stroke-linejoin="round"/>
<path d="M200 292 l14 -14 v28z M200 292 l-14 -14 v28z" fill="{P}"/>
""")

_reg("direitos", f"""
<path d="M200 60v250" stroke="{W}" stroke-width="12" stroke-linecap="round"/>
<path d="M110 322h180" stroke="{W}" stroke-width="16" stroke-linecap="round"/>
<path d="M82 108h236" stroke="{W}" stroke-width="12" stroke-linecap="round"/>
<circle cx="200" cy="64" r="16" fill="{Y}" stroke="{W}" stroke-width="8"/>
<path d="M82 108l-46 108h92z" fill="{B}" stroke="{W}" stroke-width="9" stroke-linejoin="round"/>
<path d="M318 108l-46 108h92z" fill="{P}" stroke="{W}" stroke-width="9" stroke-linejoin="round"/>
<path d="M36 216 a46 22 0 0 0 92 0z" fill="{WH}" stroke="{W}" stroke-width="9" stroke-linejoin="round"/>
<path d="M272 216 a46 22 0 0 0 92 0z" fill="{WH}" stroke="{W}" stroke-width="9" stroke-linejoin="round"/>
""")

_reg("prancheta", f"""
<rect x="86" y="70" width="228" height="272" rx="28" fill="{WH}" stroke="{W}" stroke-width="10"/>
<rect x="144" y="46" width="112" height="52" rx="18" fill="{P}" stroke="{W}" stroke-width="10"/>
<g stroke="{B}" stroke-width="12" stroke-linecap="round"><path d="M176 170h110M176 224h110M176 278h80"/></g>
<path d="M120 170l12 12 22 -24M120 224l12 12 22 -24M120 278l12 12 22 -24" fill="none" stroke="{P}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
<circle cx="338" cy="320" r="9" fill="{Y}"/>
""")

_reg("relogio", f"""
<circle cx="200" cy="210" r="132" fill="{WH}" stroke="{W}" stroke-width="12"/>
<circle cx="200" cy="210" r="104" fill="{A}"/>
<path d="M200 210V130M200 210l56 32" fill="none" stroke="{W}" stroke-width="14" stroke-linecap="round"/>
<circle cx="200" cy="210" r="12" fill="{P}"/>
<path d="M96 80 q-30 8 -34 44 M304 80 q30 8 34 44" fill="none" stroke="{P}" stroke-width="14" stroke-linecap="round"/>
<g fill="{W}"><circle cx="200" cy="120" r="5"/><circle cx="200" cy="300" r="5"/><circle cx="110" cy="210" r="5"/><circle cx="290" cy="210" r="5"/></g>
""")

_reg("lotus", f"""
<path d="M200 300 C140 262 134 190 200 120 C266 190 260 262 200 300z" fill="{P}" stroke="{W}" stroke-width="10" stroke-linejoin="round"/>
<path d="M190 296 C112 290 64 236 70 168 C140 176 184 226 190 296z" fill="{S}" stroke="{W}" stroke-width="10" stroke-linejoin="round"/>
<path d="M210 296 C288 290 336 236 330 168 C260 176 216 226 210 296z" fill="{S}" stroke="{W}" stroke-width="10" stroke-linejoin="round"/>
<path d="M120 318h160" stroke="{B}" stroke-width="14" stroke-linecap="round"/>
<circle cx="330" cy="90" r="10" fill="{Y}"/><circle cx="76" cy="104" r="8" fill="{B}"/>
""")

_reg("escudo", f"""
<path d="M200 50 L318 94 v90 c0 80 -52 124 -118 156 c-66 -32 -118 -76 -118 -156 V94z" fill="{B}" stroke="{W}" stroke-width="10" stroke-linejoin="round"/>
<path d="M200 292 c-48 -34 -64 -70 -34 -84 c14 -6 28 2 34 16 c6 -14 20 -22 34 -16 c30 14 14 50 -34 84z" fill="{P}" stroke="{W}" stroke-width="8" stroke-linejoin="round"/>
<path d="M200 90v50M175 115h50" stroke="{WH}" stroke-width="12" stroke-linecap="round"/>
<circle cx="344" cy="60" r="9" fill="{Y}"/>
""")

_reg("conversa", f"""
<path d="M62 96 h200 a34 34 0 0 1 34 34 v76 a34 34 0 0 1 -34 34 h-110 l-52 44 v-44 h-38 a34 34 0 0 1 -34 -34 v-76 a34 34 0 0 1 34 -34z" fill="{P}" stroke="{W}" stroke-width="10" stroke-linejoin="round"/>
<path d="M250 230 h54 a34 34 0 0 1 34 34 v34 a34 34 0 0 1 -34 34 h-20 l-30 34 v-34 h-4 a34 34 0 0 1 -34 -34 v-34 a34 34 0 0 1 34 -34z" fill="{B}" stroke="{W}" stroke-width="10" stroke-linejoin="round"/>
<path d="M158 196 c-28 -20 -36 -44 -18 -52 c8 -3 16 2 18 10 c2 -8 10 -13 18 -10 c18 8 10 32 -18 52z" fill="{WH}"/>
<circle cx="64" cy="320" r="8" fill="{Y}"/>
""")

_reg("flor", f"""
<g fill="{P}" stroke="{W}" stroke-width="8">
<circle cx="200" cy="104" r="48"/><circle cx="276" cy="160" r="48"/><circle cx="248" cy="246" r="48"/>
<circle cx="152" cy="246" r="48"/><circle cx="124" cy="160" r="48"/></g>
<circle cx="200" cy="190" r="50" fill="{Y}" stroke="{W}" stroke-width="8"/>
<path d="M200 296v70" stroke="{W}" stroke-width="12" stroke-linecap="round"/>
<path d="M200 340 q-50 -4 -64 -40 q44 -2 64 40z" fill="{B}" stroke="{W}" stroke-width="8" stroke-linejoin="round"/>
""")

_reg("coracao", f"""
<path d="M200 340 C60 240 36 140 96 92 C142 56 192 76 200 128 C208 76 258 56 304 92 C364 140 340 240 200 340z" fill="{P}" stroke="{W}" stroke-width="10" stroke-linejoin="round"/>
<path d="M112 138 q10 -30 40 -32" fill="none" stroke="{WH}" stroke-width="12" stroke-linecap="round" opacity=".8"/>
<circle cx="338" cy="64" r="10" fill="{Y}"/><circle cx="66" cy="296" r="9" fill="{B}"/>
""")

_reg("estrela", f"""
<path d="M200 54 l40 84 92 12 -68 64 18 92 -82 -46 -82 46 18 -92 -68 -64 92 -12z" fill="{Y}" stroke="{W}" stroke-width="10" stroke-linejoin="round"/>
<circle cx="70" cy="90" r="9" fill="{P}"/><circle cx="332" cy="318" r="9" fill="{B}"/>
""")

# Palavras-chave (sem acento) -> ilustracao, usadas quando a IA erra o nome.
PALAVRAS = [
    (("mamadeira", "amament", "leite", "mama"), "mamadeira"),
    (("enxoval", "roupinha", "body", "roupa"), "body"),
    (("carrinho", "passeio", "bebe conforto"), "carrinho"),
    (("berco", "quarto", "decoracao"), "berco"),
    (("chupeta",), "chupeta"),
    (("consulta", "medic", "pre-natal", "prenatal", "exame", "sinais", "alerta", "sintoma"), "estetoscopio"),
    (("calendario", "semana", "trimestre", "data", "mes "), "calendario"),
    (("mala", "maternidade", "hospital", "parto"), "mala"),
    (("batimento", "pressao", "coracao"), "coracao_pulso"),
    (("agua", "hidrata"), "agua"),
    (("aliment", "fruta", "nutri", "comida", "refeic", "enjoo", "nausea"), "fruta"),
    (("sono", "dormir", "noite", "descanso", "inson"), "lua_sono"),
    (("barriga", "gestante", "gravidez", "corpo"), "gestante"),
    (("ultrassom", "ecografia", "morfologico"), "ultrassom"),
    (("sapato", "pezinho", "meia"), "sapatinho"),
    (("ursinho", "brinquedo", "presente", "cha de bebe"), "ursinho"),
    (("direito", "lei ", "licenca", "trabalho", "estabilidade", "salario"), "direitos"),
    (("plano", "lista", "check", "organiza", "documento"), "prancheta"),
    (("tempo", "contracao", "hora", "rotina"), "relogio"),
    (("emocion", "ansied", "relax", "respira", "bem-estar", "bem estar", "mental", "calma", "estresse"), "lotus"),
    (("protec", "seguranca", "cuidado", "prevenc"), "escudo"),
    (("apoio", "conversa", "parceir", "familia", "rede de"), "conversa"),
    (("amor", "vinculo", "afeto", "abraco", "mae e bebe"), "abraco"),
]

PADRAO = ["coracao", "estrela", "flor", "abraco"]


def _norm(t):
    t = unicodedata.normalize("NFKD", str(t or "").lower())
    return "".join(ch for ch in t if not unicodedata.combining(ch))


def escolher(nome, *textos, indice=0):
    """Devolve o nome de uma ilustracao valida: usa o da IA, ou deduz pelo texto."""
    n = _norm(nome).strip().replace(" ", "_")
    if n in ILUSTRACOES:
        return n
    corpo = " " + " ".join(_norm(t) for t in textos) + " "
    for chaves, ilus in PALAVRAS:
        if any(k in corpo for k in chaves):
            return ilus
    return PADRAO[indice % len(PADRAO)]


def desenho(nome, *textos, indice=0, tamanho=400):
    svg = ILUSTRACOES[escolher(nome, *textos, indice=indice)]
    return svg.replace("<svg ", '<svg width="%d" height="%d" ' % (tamanho, tamanho), 1)


def nomes():
    return sorted(ILUSTRACOES)
