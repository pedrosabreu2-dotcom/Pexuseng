#!/usr/bin/env python3
"""Gera as artes da campanha 'Proteção contra maresia' (HTML -> PNG via Playwright)."""
from pathlib import Path
import json, subprocess

OUT = Path(__file__).resolve().parent.parent / "imagens"
NAVY, GELO, GELO2, AMBAR, NEVOA, ACO = "#0F2340", "#5B95DB", "#2F62A8", "#F29D38", "#EEF3F7", "#5B6B7A"

LOGO = """<svg viewBox="0 0 100 100" width="{s}" height="{s}"><defs><clipPath id="hc{u}"><polygon points="50,9 85.5,29.5 85.5,70.5 50,91 14.5,70.5 14.5,29.5"/></clipPath>
<g id="arm{u}" fill="none" stroke-linecap="round" stroke-width="5"><path d="M50 50V20M50 31L42 23M50 31L58 23M50 41L44.5 35.5M50 41L55.5 35.5"/></g></defs>
<polygon points="50,4 90,27 90,73 50,96 10,73 10,27" fill="none" stroke="{c}" stroke-width="7" stroke-linejoin="round"/>
<g stroke="{c}">""" + "".join(f'<use href="#arm{{u}}" transform="rotate({a} 50 50)"/>' for a in range(0, 360, 60)) + """</g>
<g clip-path="url(#hc{u})"><path d="M84 6L16 94" stroke="#5B95DB" stroke-width="13"/><path d="M84 6L16 94" stroke="#9CC2EE" stroke-width="4"/></g></svg>"""
_u = [0]
def logo(s=64, c="#FFFFFF"):
    _u[0] += 1
    return LOGO.format(s=s, c=c, u=_u[0])

def marca(c="#FFFFFF", sub="#9CC2EE"):
    return f"""<div class="marca">{logo(58, c)}<div><div class="mn" style="color:{c}">PEXUS Engenharia</div>
<div class="ms" style="color:{sub}">Refrigeração e Climatização</div></div></div>"""

# condensadora estilizada (com ou sem corrosão)
def condensadora(w=620, corroida=True):
    rust = ""
    if corroida:
        rust = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#B5562A" opacity="{o}"/>' for x, y, r, o in
                       [(60,70,14,.85),(84,58,8,.7),(70,96,6,.6),(470,250,18,.8),(498,232,9,.7),(452,276,7,.6),(120,268,11,.75),(520,60,10,.7),(300,40,7,.55)])
        rust += '<path d="M30 300 q20 10 40 0 t40 0" stroke="#B5562A" stroke-width="6" fill="none" opacity=".6"/>'
    fins = "".join(f'<line x1="{x}" y1="40" x2="{x}" y2="280" stroke="{"#8E9AA6" if corroida else "#7FA7D6"}" stroke-width="3"/>' for x in range(300, 520, 12))
    return f"""<svg viewBox="0 0 560 330" width="{w}"><rect x="10" y="10" width="540" height="300" rx="22" fill="#E3E8EE" stroke="#B9C3CD" stroke-width="4"/>
<circle cx="170" cy="160" r="112" fill="#CDD5DD" stroke="#9AA6B2" stroke-width="5"/>
<circle cx="170" cy="160" r="24" fill="#8E9AA6"/>
{''.join(f'<path d="M170 160 L{170+100*c:.0f} {160+100*s:.0f}" stroke="#9AA6B2" stroke-width="5"/>' for c, s in [(1,0),(-1,0),(0,1),(0,-1),(.7,.7),(-.7,-.7),(.7,-.7),(-.7,.7)])}
<rect x="290" y="30" width="240" height="260" rx="10" fill="#D7DEE5"/>{fins}{rust}
<rect x="10" y="300" width="540" height="20" rx="6" fill="#9AA6B2"/></svg>"""

ONDAS = f"""<svg viewBox="0 0 1080 160" width="1080" style="position:absolute;left:0;bottom:0"><path d="M0 70 Q90 20 180 70 T360 70 T540 70 T720 70 T900 70 T1080 70 V160 H0Z" fill="{GELO}" opacity=".35"/>
<path d="M0 105 Q90 60 180 105 T360 105 T540 105 T720 105 T900 105 T1080 105 V160 H0Z" fill="{GELO}" opacity=".55"/></svg>"""

FONTS = (Path(__file__).resolve().parent / "fonts").as_uri()
CSS = f"""@font-face{{font-family:'Montserrat';font-weight:600;src:url('{FONTS}/montserrat-latin-600-normal.woff2')}}
@font-face{{font-family:'Montserrat';font-weight:700;src:url('{FONTS}/montserrat-latin-700-normal.woff2')}}
@font-face{{font-family:'Montserrat';font-weight:800;src:url('{FONTS}/montserrat-latin-800-normal.woff2')}}
@font-face{{font-family:'Montserrat';font-weight:900;src:url('{FONTS}/montserrat-latin-900-normal.woff2')}}
@font-face{{font-family:'IBM Plex Sans';font-weight:400;src:url('{FONTS}/ibm-plex-sans-latin-400-normal.woff2')}}
@font-face{{font-family:'IBM Plex Sans';font-weight:500;src:url('{FONTS}/ibm-plex-sans-latin-500-normal.woff2')}}
@font-face{{font-family:'IBM Plex Sans';font-weight:600;src:url('{FONTS}/ibm-plex-sans-latin-600-normal.woff2')}}
@font-face{{font-family:'IBM Plex Mono',monospace;font-weight:500;src:url('{FONTS}/ibm-plex-mono-latin-500-normal.woff2')}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:var(--w);height:var(--h);overflow:hidden;font-family:'IBM Plex Sans',Arial,sans-serif}}
.pg{{position:relative;width:var(--w);height:var(--h);padding:80px 80px;display:flex;flex-direction:column;overflow:hidden}}
.dark{{background:{NAVY};color:#fff}} .light{{background:{NEVOA};color:{NAVY}}}
h1{{font-family:Montserrat,'Helvetica Neue',Arial,sans-serif;font-weight:900;font-size:92px;line-height:1.02;letter-spacing:-2px}}
h2{{font-family:Montserrat,'Helvetica Neue',Arial,sans-serif;font-weight:800;font-size:66px;line-height:1.08;letter-spacing:-1px}}
h3{{font-family:Montserrat,'Helvetica Neue',Arial,sans-serif;font-weight:800;font-size:40px;line-height:1.15}}
p{{font-size:34px;line-height:1.4}}
.tag{{font-family:'IBM Plex Mono',monospace;font-size:26px;letter-spacing:3px;text-transform:uppercase;color:{AMBAR}}}
.amb{{color:{AMBAR}}} .gel{{color:{GELO}}}
.marca{{display:flex;align-items:center;gap:18px}} .mn{{font-family:Montserrat,Arial,sans-serif;font-weight:800;font-size:32px}} .ms{{font-size:22px;letter-spacing:.5px}}
.foot{{margin-top:auto;display:flex;justify-content:space-between;align-items:flex-end}}
.pag{{font-family:'IBM Plex Mono',monospace;font-size:26px;opacity:.7}}
.card{{border-radius:28px;padding:34px 38px;display:flex;gap:28px;align-items:flex-start}}
.n{{flex:none;width:76px;height:76px;border-radius:50%;background:{AMBAR};color:{NAVY};font-family:Montserrat,Arial,sans-serif;font-weight:900;font-size:40px;display:flex;align-items:center;justify-content:center}}
.btn{{display:inline-block;background:{AMBAR};color:{NAVY};font-family:Montserrat,Arial,sans-serif;font-weight:800;font-size:40px;padding:26px 44px;border-radius:999px}}
ul.ck{{list-style:none;display:grid;gap:16px}} ul.ck li{{font-size:31px;line-height:1.3;padding-left:52px;position:relative}}
ul.ck li:before{{content:'';position:absolute;left:0;top:6px;width:30px;height:30px;border-radius:8px;background:{GELO}}}
"""

def page(w, h, cls, body):
    return f"<!doctype html><html><head><meta charset='utf-8'><style>:root{{--w:{w}px;--h:{h}px}}{CSS}</style></head><body><div class='pg {cls}'>{body}</div></body></html>"

F = (1080, 1350); S = (1080, 1920)
pecas = {}

# ---------- POST 1: CARROSSEL ----------
pecas["post1-carrossel-01-capa"] = (F, "dark", f"""{marca()}
<div style="margin-top:70px" class="tag">Mora perto da praia?</div>
<h1 style="margin-top:22px">A maresia está <span class="amb">corroendo</span> o seu ar&#8209;condicionado.</h1>
<div style="margin-top:50px;display:flex;justify-content:center">{condensadora(760)}</div>
<div class="foot" style="position:relative;z-index:2"><p style="font-size:30px;opacity:.85">Arraste para o lado →</p><span class="pag">1/5</span></div>{ONDAS}""")

itens = [("Serpentina", "O sal ataca as aletas de alumínio. Elas esfarelam, o aparelho troca menos calor, gela menos e gasta mais energia."),
         ("Placa eletrônica", "A umidade salina oxida trilhas e conectores. Resultado: erros, desligamentos e placa queimada."),
         ("Gabinete e suporte", "A ferrugem fura a lataria e enfraquece o suporte da condensadora — risco de queda.")]
cards = "".join(f'<div class="card" style="background:#fff;margin-top:26px"><div class="n">{i+1}</div><div><h3>{t}</h3><p style="font-size:29px;margin-top:8px;color:{ACO}">{d}</p></div></div>' for i, (t, d) in enumerate(itens))
pecas["post1-carrossel-02-o-que-o-sal-faz"] = (F, "light", f"""<div class="tag" style="color:{GELO2}">O que o ar salino faz</div>
<h2 style="margin-top:18px">Três partes do aparelho que mais sofrem</h2>{cards}
<div class="foot"><div style="opacity:.9">{marca(NAVY, GELO2)}</div><span class="pag">2/5</span></div>""")

sinais = [("Pontos de ferrugem ou manchas brancas", "no gabinete, nos parafusos e no suporte"),
          ("Aletas escurecidas ou esfarelando", "na parte de trás da condensadora"),
          ("Aparelho gelando menos ou dando erro", "com mais frequência do que antes")]
sc = "".join(f'<div class="card" style="background:rgba(255,255,255,.07);margin-top:24px;border:2px solid rgba(91,149,219,.35)"><div class="n">{i+1}</div><div><h3>{t}</h3><p style="font-size:29px;margin-top:6px;opacity:.8">{d}</p></div></div>' for i, (t, d) in enumerate(sinais))
pecas["post1-carrossel-03-sinais"] = (F, "dark", f"""<div class="tag">Fique de olho</div>
<h2 style="margin-top:18px">3 sinais de que a maresia já chegou no seu aparelho</h2>{sc}
<div class="foot"><p style="font-size:28px;opacity:.8">Viu algum? Não espere a placa queimar.</p><span class="pag">3/5</span></div>""")

pecas["post1-carrossel-04-como-protegemos"] = (F, "light", f"""<div class="tag" style="color:{GELO2}">Proteção anticorrosiva PEXUS</div>
<h2 style="margin-top:18px">Um produto certo para cada parte</h2>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:26px;margin-top:40px">
 <div style="background:#fff;border-radius:28px;padding:36px"><h3>Básica</h3><ul class="ck" style="margin-top:24px">
  <li>Tratamento da ferrugem com zinco</li><li>Verniz isolante na placa</li><li>Graxa dielétrica nos contatos</li><li>Proteção do gabinete</li></ul></div>
 <div style="background:{NAVY};color:#fff;border-radius:28px;padding:36px;position:relative"><div style="position:absolute;top:-22px;right:28px;background:{AMBAR};color:{NAVY};font-family:Montserrat,Arial,sans-serif;font-weight:800;font-size:22px;padding:8px 18px;border-radius:999px">MAIS COMPLETA</div>
  <h3>Completa</h3><ul class="ck" style="margin-top:24px"><li>Tudo da Básica</li><li><b>Revestimento anticorrosivo nas aletas da serpentina</b></li><li>Relatório com fotos antes e depois</li></ul></div>
</div>
<div style="margin-top:44px;display:flex;align-items:center;gap:34px"><div style="flex:none">{condensadora(330, corroida=False)}</div>
<p style="font-size:31px;color:{ACO}">Serviço com <b style="color:{NAVY}">engenheiro mecânico responsável</b> e produtos próprios para ar salino.</p></div>
<div class="foot"><div>{marca(NAVY, GELO2)}</div><span class="pag">4/5</span></div>""")

pecas["post1-carrossel-05-chamada"] = (F, "dark", f"""{marca()}
<h1 style="margin-top:110px;font-size:84px">Proteja <span class="amb">junto com a limpeza</span>.</h1>
<p style="margin-top:30px;opacity:.9">Uma visita só: higienização completa + proteção contra maresia.</p>
<div style="margin-top:60px"><span class="btn">Chame no WhatsApp</span></div>
<p style="margin-top:28px;font-size:28px;opacity:.75">Link na bio · Zona Sul, Barra, Recreio, Ilha e Niterói</p>
<div class="foot" style="position:relative;z-index:2"><span></span><span class="pag">5/5</span></div>{ONDAS}""")

# ---------- POST 2: COMBO ----------
pecas["post2-combo-limpeza-protecao"] = (F, "dark", f"""{marca()}
<div style="margin-top:64px" class="tag">Alta temporada · verão 2026/27</div>
<h1 style="margin-top:20px;font-size:86px">Combo <span class="amb">Limpeza</span><br>+ Proteção<br>contra maresia</h1>
<div style="margin-top:50px;background:rgba(255,255,255,.07);border:2px solid rgba(91,149,219,.4);border-radius:28px;padding:36px 40px">
<ul class="ck"><li>Higienização completa da evaporadora e da condensadora</li><li>Proteção anticorrosiva na mesma visita</li><li>Mais rendimento e mais vida útil para o aparelho</li></ul></div>
<p style="margin-top:36px;font-size:30px;opacity:.85">Agenda com vagas limitadas por semana. Garanta a sua antes do calor apertar.</p>
<div class="foot" style="position:relative;z-index:2"><span class="btn" style="font-size:34px;padding:22px 38px">Agende pelo WhatsApp</span></div>{ONDAS}""")

# ---------- POST 3: DICA ----------
pecas["post3-dica-agua-doce"] = (F, "light", f"""<div class="tag" style="color:{GELO2}">Dica de engenheiro</div>
<h1 style="margin-top:22px;font-size:80px">Mora no litoral? Peça para <span style="color:{GELO2}">lavar a condensadora com água doce</span> a cada 3 a 6 meses.</h1>
<div style="margin-top:44px;display:flex;gap:30px;align-items:center">
 <div style="flex:none;width:150px;height:150px;border-radius:36px;background:{NAVY};display:flex;align-items:center;justify-content:center">{logo(100)}</div>
 <p style="font-size:31px;color:{ACO}">O sal se acumula nas aletas. Uma lavagem em baixa pressão, sem produto ácido, tira esse sal antes que ele corroa o alumínio.</p></div>
<p style="margin-top:36px;font-size:30px"><b>Importante:</b> com o aparelho desligado no disjuntor e por um profissional — jato forte amassa as aletas.</p>
<div class="foot"><div>{marca(NAVY, GELO2)}</div><span class="pag">Salve este post</span></div>""")

# ---------- STORY ----------
pecas["story-caixa-perguntas"] = (S, "dark", f"""{marca()}
<div style="margin-top:150px" class="tag">Avaliação gratuita pelo direct</div>
<h1 style="margin-top:24px;font-size:96px">Seu ar fica de frente para o mar?</h1>
<p style="margin-top:34px;font-size:40px;opacity:.9">Manda uma foto da condensadora que a gente diz se ela já está sofrendo com a maresia.</p>
<div style="margin-top:80px;height:360px;border:4px dashed rgba(255,255,255,.35);border-radius:36px;display:flex;align-items:center;justify-content:center;font-size:30px;opacity:.6">espaço para a caixa de perguntas</div>
<div class="foot" style="position:relative;z-index:2"><span></span></div>{ONDAS}""")

# ---------- CAPA DO REELS ----------
pecas["reels-capa-3-sinais"] = (S, "dark", f"""{marca()}
<div style="margin-top:130px" class="tag">Mora perto da praia?</div>
<h1 style="margin-top:24px;font-size:112px">3 sinais de que a <span class="amb">maresia</span> está acabando com o seu ar</h1>
<div style="margin-top:80px;display:flex;justify-content:center">{condensadora(860)}</div>
<div class="foot" style="position:relative;z-index:2"><span></span></div>{ONDAS}""")

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = Path(__file__).resolve().parent / "_html"; tmp.mkdir(exist_ok=True)
    jobs = []
    for nome, ((w, h), cls, body) in pecas.items():
        f = tmp / f"{nome}.html"; f.write_text(page(w, h, cls, body), encoding="utf-8")
        jobs.append({"html": str(f), "png": str(OUT / f"{nome}.png"), "w": w, "h": h})
    subprocess.run(["node", str(Path(__file__).resolve().parent / "render.js"), json.dumps(jobs)], check=True)

if __name__ == "__main__":
    main()
