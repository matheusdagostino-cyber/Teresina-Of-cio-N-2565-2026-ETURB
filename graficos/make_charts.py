# -*- coding: utf-8 -*-
"""Gera os gráficos do Anexo II da resposta ao Ofício 2565/2026 – ETURB."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
import datetime as dt
import os

OUT = '/home/user/Teresina-Of-cio-N-2565-2026-ETURB/graficos'
os.makedirs(OUT, exist_ok=True)

# paleta validada (dataviz) + ink/chrome para superfície branca de impressão
BLUE, ORANGE, AQUA = '#2a78d6', '#eb6834', '#1baf7a'
INK, INK2, MUTED = '#0b0b0b', '#52514e', '#898781'
GRID, BASE = '#e1e0d9', '#c3c2b7'

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 10,
    'text.color': INK,
    'axes.edgecolor': BASE,
    'axes.labelcolor': INK2,
    'axes.titlesize': 11.5,
    'axes.titleweight': 'bold',
    'axes.titlecolor': INK,
    'xtick.color': MUTED,
    'ytick.color': MUTED,
    'axes.grid': True,
    'grid.color': GRID,
    'grid.linewidth': 0.8,
    'axes.axisbelow': True,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'savefig.dpi': 200,
})

def fmt_br(v, _pos=None):
    s = f'{v:,.0f}'.replace(',', '.')
    return s

def style_ax(ax):
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)
    ax.grid(axis='x', visible=False)

# ---------------------------------------------------------------- Gráfico 1
# Balanço teórico sem evaporação (série cacheada do chart do Ofício 014/2026)
# × volume medido (topografia/drone) × capacidades
meses = []
d = dt.date(2025, 1, 1)
for _ in range(30):
    meses.append(d)
    d = dt.date(d.year + (d.month // 12), (d.month % 12) + 1, 1)

teorico = [None, 1639.2, 2455.2, 2814.7, 3133.0, 3439.4, 3806.3, 4183.4,
           4571.4, 4876.8, 5331.3, 5815.3, 7301.9, 9368.4, 10737.8, 12121.7,
           13099.5, 13765.5, 14080.9, 14458.1, 14846.0, 15151.5, 15605.9,
           16089.9, 17576.5, 19643.1, 21012.5, 22396.3, 23374.1, 24040.1]

med_x = [dt.date(2026, 5, 26), dt.date(2026, 6, 22), dt.date(2026, 7, 13)]
med_y = [11813.72, 10384.72, 10384.72]

fig, ax = plt.subplots(figsize=(9.1, 4.6))
tx = [m for m, v in zip(meses, teorico) if v is not None]
ty = [v for v in teorico if v is not None]
ax.plot(tx, ty, color=BLUE, lw=2, label='Balanço teórico sem evaporação (Ofício nº 014/2026)')
ax.plot(med_x, med_y, 'o', color=ORANGE, ms=8, zorder=5,
        label='Volume medido — topografia/drone')

ax.axhline(26100, color=MUTED, lw=1.4, ls=(0, (5, 4)))
ax.axhline(13600, color=MUTED, lw=1.4, ls=(0, (2, 3)))
ax.text(meses[0], 26100 + 500, 'Capacidade total com a 2ª lagoa (≈ 26.100 m³)',
        fontsize=9, color=INK2)
ax.text(meses[0], 13600 + 500, 'Capacidade da lagoa atual (≈ 13.600 m³)',
        fontsize=9, color=INK2)

ax.annotate('24.040 m³\n(jun/2027)', xy=(tx[-1], ty[-1]), xytext=(-8, -34),
            textcoords='offset points', ha='right', fontsize=9, color=INK2)
ax.annotate('10.384,72 m³ (13/07/2026)', xy=(med_x[-1], med_y[-1]), xytext=(10, -16),
            textcoords='offset points', fontsize=9, color=INK2)

ax.set_ylim(0, 28500)
ax.yaxis.set_major_formatter(FuncFormatter(fmt_br))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))
ax.set_ylabel('Volume (m³)')
ax.set_title('Estoque de percolado: balanço teórico sem evaporação × volume medido')
style_ax(ax)
ax.legend(loc='upper left', bbox_to_anchor=(0.0, 0.86), frameon=False, fontsize=9)
fig.tight_layout()
fig.savefig(f'{OUT}/grafico1_balanco_medicoes.png')
plt.close(fig)

# ---------------------------------------------------------------- Gráfico 2
# Afluente mensal × precipitação (2026) — small multiples, um eixo por medida
m26 = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun']
aflu = [1486.6, 2066.5, 1369.4, 1383.9, 977.8, 666.0]
chuva = [215.0, 497.0, 196.6, 293.8, 73.2, 26.2]

fig, (a1, a2) = plt.subplots(2, 1, figsize=(9.1, 5.4), sharex=True,
                             gridspec_kw={'hspace': 0.42})
a1.bar(m26, aflu, color=BLUE, width=0.62)
a1.set_title('Afluente total à lagoa (percolado + contribuição pluviométrica) — m³/mês')
a1.yaxis.set_major_formatter(FuncFormatter(fmt_br))
a1.set_ylim(0, 2400)
for i, v in enumerate(aflu):
    a1.text(i, v + 55, fmt_br(v), ha='center', fontsize=9, color=INK2)
style_ax(a1)

a2.bar(m26, chuva, color=AQUA, width=0.62)
a2.set_title('Precipitação registrada no aterro — mm/mês')
a2.set_ylim(0, 580)
for i, v in enumerate(chuva):
    a2.text(i, v + 14, f'{v:.0f}', ha='center', fontsize=9, color=INK2)
style_ax(a2)
a2.set_xlabel('2026')

fig.suptitle('Afluente à lagoa e precipitação em 2026 — queda acentuada rumo à estiagem',
             fontsize=11.5, fontweight='bold', y=0.995)
fig.tight_layout(rect=(0, 0, 1, 0.97))
fig.savefig(f'{OUT}/grafico3_afluente_chuva.png')
plt.close(fig)

# ---------------------------------------------------------------- Gráfico 3
# Evolução da cota do nível da lagoa (leituras semanais + medições)
cotas = [
    ('2026-02-10', 171.486), ('2026-02-27', 172.555), ('2026-03-12', 172.838),
    ('2026-03-20', 173.007), ('2026-03-27', 173.011), ('2026-04-02', 173.085),
    ('2026-04-10', 173.237), ('2026-04-17', 173.295), ('2026-04-24', 173.442),
    ('2026-04-30', 173.556), ('2026-05-08', 173.514), ('2026-05-15', 173.504),
    ('2026-05-22', 173.524), ('2026-05-26', 173.510), ('2026-06-22', 173.120),
    ('2026-07-13', 173.120),
]
cx = [dt.date.fromisoformat(a) for a, _ in cotas]
cy = [b for _, b in cotas]

fig, ax = plt.subplots(figsize=(9.1, 4.0))
ax.plot(cx, cy, '-o', color=BLUE, lw=2, ms=5.5)
peak = cy.index(max(cy))
ax.annotate('máxima do período chuvoso: 173,56 m (30/04)', xy=(cx[peak], cy[peak]),
            xytext=(0, 12), textcoords='offset points', ha='center',
            fontsize=9, color=INK2)
ax.annotate('173,12 m (13/07)', xy=(cx[-1], cy[-1]), xytext=(0, -18),
            textcoords='offset points', ha='right', fontsize=9, color=INK2)
ax.set_ylim(171.2, 173.95)
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: f'{v:.1f}'.replace('.', ',')))
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))
ax.set_ylabel('Cota do nível (m)')
ax.set_title('Cota do nível da lagoa em operação — leituras topográficas (fev–jul/2026)')
style_ax(ax)
fig.tight_layout()
fig.savefig(f'{OUT}/grafico2_cota_nivel.png')
plt.close(fig)

print('gerados em', OUT)
for f in sorted(os.listdir(OUT)):
    print(' -', f)
