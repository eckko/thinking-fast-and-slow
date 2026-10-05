import math
from urllib.parse import quote

def enc(svg): return 'url("data:image/svg+xml,' + quote(svg, safe=" /:=,;()'.-_") + '")'
NS = "xmlns='http://www.w3.org/2000/svg'"

# ---------------------------------------------------------------- palettes
# keys: paper card ink mut line acc acc2 hl ok bad part c1 c2 c3 c4 on onh
P = {
 'classic': dict(
  L=dict(paper='#fbf8f1',card='#fbfcfd',ink='#121826',mut='#5b6578',line='#d5dbe5',acc='#2743d6',acc2='#7c5cff',hl='#ffe14d',ok='#1e8a63',bad='#d4452f',part='#b07a00',c1='#ff5d73',c2='#12b5a6',c3='#7c5cff',c4='#ff9f1c',on='#ffffff',onh='#ffffff'),
  D=dict(paper='#10131c',card='#181d2a',ink='#e9ecf4',mut='#9aa4b8',line='#2b3347',acc='#8ea2ff',acc2='#b79bff',hl='#f2d43d',ok='#4fd1a0',bad='#ff8a77',part='#e8b84a',c1='#ff7b8d',c2='#35d0c1',c3='#a08cff',c4='#ffb347',on='#0e1320',onh='#0e1320')),
 'lego': dict(
  L=dict(paper='#fff3c4',card='#ffffff',ink='#1b1b1b',mut='#555555',line='#3a3a3a',acc='#d01012',acc2='#d01012',hl='#ffd500',ok='#00852b',bad='#d01012',part='#b87400',c1='#d01012',c2='#00852b',c3='#0055bf',c4='#f5cd2a',on='#ffffff',onh='#ffffff'),
  D=dict(paper='#17181c',card='#24262c',ink='#f2f2f2',mut='#b0b0b8',line='#5a5c64',acc='#e3363a',acc2='#e3363a',hl='#ffd500',ok='#3ecf6e',bad='#ff6b6b',part='#ffb02e',c1='#ff5a5c',c2='#3ecf6e',c3='#4d94ff',c4='#ffd84a',on='#ffffff',onh='#ffffff')),
 'clay': dict(
  L=dict(paper='#f6e9df',card='#fff6ee',ink='#3b2f2f',mut='#7d6b66',line='#ecd9cc',acc='#ff8a65',acc2='#ffb199',hl='#ffd88a',ok='#3f9f72',bad='#d9564b',part='#b57a14',c1='#f58fa5',c2='#6cc5b8',c3='#9b8cf0',c4='#ffb067',on='#3b1d12',onh='#3b2f2f'),
  D=dict(paper='#2a2220',card='#362c29',ink='#f6e7de',mut='#c3aca2',line='#4a3b36',acc='#ff9a7a',acc2='#ffb89e',hl='#e8b95e',ok='#7dd3a5',bad='#ff8a7d',part='#f0b04a',c1='#ff9db4',c2='#7fd8cb',c3='#b3a6ff',c4='#ffc085',on='#2a1410',onh='#2a1410')),
 'pastel': dict(
  L=dict(paper='#fdf6fb',card='#ffffff',ink='#3d3555',mut='#7b7394',line='#eadcf2',acc='#a78bfa',acc2='#f9a8d4',hl='#fde68a',ok='#2f9e77',bad='#e0527f',part='#a97c0a',c1='#f9a8d4',c2='#99e2d0',c3='#c4b5fd',c4='#ffd08a',on='#2d2547',onh='#3d3555'),
  D=dict(paper='#231d33',card='#2e2745',ink='#f3eefc',mut='#b9afd3',line='#433a63',acc='#b79cff',acc2='#f7a9d6',hl='#f3d673',ok='#7fe0b8',bad='#ff8fb8',part='#f0c15a',c1='#f7a9d6',c2='#86dcc9',c3='#b9a8ff',c4='#ffcf8b',on='#231d33',onh='#231d33')),
 'comic': dict(
  L=dict(paper='#fff3b0',card='#ffffff',ink='#111111',mut='#444444',line='#111111',acc='#e63946',acc2='#e63946',hl='#ffe600',ok='#17874c',bad='#d61f2c',part='#b86800',c1='#e63946',c2='#17a05d',c3='#2b6cff',c4='#ffb703',on='#ffffff',onh='#ffffff'),
  D=dict(paper='#14121f',card='#1e1b30',ink='#fff6d6',mut='#c9c3e0',line='#f5e9a8',acc='#ff5a66',acc2='#ff5a66',hl='#ffe600',ok='#38d985',bad='#ff6b78',part='#ffb02e',c1='#ff5a66',c2='#38d985',c3='#5b8cff',c4='#ffc933',on='#14121f',onh='#14121f')),
 'whiteboard': dict(
  L=dict(paper='#eef1f3',card='#ffffff',ink='#1f2937',mut='#5d6875',line='#3b4452',acc='#2563eb',acc2='#2563eb',hl='#fde047',ok='#15803d',bad='#dc2626',part='#b45309',c1='#dc2626',c2='#16a34a',c3='#2563eb',c4='#f59e0b',on='#ffffff',onh='#ffffff'),
  D=dict(paper='#1d2a25',card='#24352e',ink='#f1f5f2',mut='#b6c4bc',line='#cfe0d6',acc='#7cc4ff',acc2='#7cc4ff',hl='#ffe66d',ok='#8be3a6',bad='#ff9a8f',part='#ffcf70',c1='#ff9a8f',c2='#8be3a6',c3='#7cc4ff',c4='#ffd37a',on='#10201a',onh='#10201a')),
 'anime': dict(
  L=dict(paper='#fff1f8',card='#ffffff',ink='#3b2f55',mut='#7a6a99',line='#f0d4ea',acc='#f2509c',acc2='#8f7dff',hl='#ffe27a',ok='#1f9f80',bad='#e03a5e',part='#a97c0a',c1='#ff6fae',c2='#2fbfb0',c3='#8f7dff',c4='#ffb347',on='#ffffff',onh='#ffffff'),
  D=dict(paper='#1a1530',card='#251e45',ink='#f4eeff',mut='#b8aee0',line='#3f3566',acc='#ff7ab8',acc2='#9d8cff',hl='#ffd966',ok='#5fe0bf',bad='#ff7a93',part='#ffc34d',c1='#ff7ab8',c2='#5ee0d4',c3='#a79bff',c4='#ffbd66',on='#1a1530',onh='#1a1530')),
 'watercolor': dict(
  L=dict(paper='#fbfaf6',card='#fffefb',ink='#2f3a45',mut='#6b7886',line='#dfe6ec',acc='#3f7fb0',acc2='#6fae95',hl='#f7e08a',ok='#3f8f6c',bad='#c85a5a',part='#a8741a',c1='#e58a9b',c2='#6bb7a4',c3='#7f9de0',c4='#eab45f',on='#ffffff',onh='#ffffff'),
  D=dict(paper='#151c24',card='#1d2732',ink='#e8eef4',mut='#a2b1c0',line='#2f3d4c',acc='#7db4e0',acc2='#9ad1b8',hl='#e7cf73',ok='#6fd0a5',bad='#f09090',part='#e6b04d',c1='#f0a0b0',c2='#86d3c0',c3='#9fb4f0',c4='#f2c47a',on='#10202c',onh='#10202c')),
 'university': dict(
  L=dict(paper='#f5efe0',card='#fffdf6',ink='#1f2a44',mut='#5f6882',line='#d8cfb8',acc='#7a1f2b',acc2='#9b2c3a',hl='#f1d27a',ok='#2f6f4e',bad='#a3262f',part='#8f6212',c1='#a3262f',c2='#2f6f4e',c3='#1f3a7a',c4='#b8860b',on='#ffffff',onh='#ffffff'),
  D=dict(paper='#141a2b',card='#1c2438',ink='#efe8d4',mut='#aeb3c6',line='#34405e',acc='#d4a74a',acc2='#e6c26e',hl='#d9b350',ok='#6fc59a',bad='#e57b82',part='#e0b050',c1='#e57b82',c2='#6fc59a',c3='#8fa8e8',c4='#e0b050',on='#141a2b',onh='#141a2b')),
 'professional': dict(
  L=dict(paper='#f4f6f9',card='#ffffff',ink='#111827',mut='#5b6472',line='#dde2ea',acc='#1f5fd1',acc2='#1f5fd1',hl='#fde68a',ok='#15803d',bad='#b91c1c',part='#b45309',c1='#b91c1c',c2='#15803d',c3='#1f5fd1',c4='#b45309',on='#ffffff',onh='#ffffff'),
  D=dict(paper='#0f141b',card='#171d26',ink='#e6eaf0',mut='#98a3b3',line='#2a3342',acc='#5b9cff',acc2='#5b9cff',hl='#d6bf5c',ok='#3fd183',bad='#f87171',part='#fbbf24',c1='#f87171',c2='#3fd183',c3='#5b9cff',c4='#fbbf24',on='#0b1220',onh='#0b1220')),
}

# ---------------------------------------------------------------- shape tokens
FONTS = dict(
 classic=('"Instrument Sans",system-ui,sans-serif','"Source Serif 4",Georgia,serif'),
 lego=('"Fredoka","Trebuchet MS",system-ui,sans-serif','"Fredoka","Trebuchet MS",system-ui,sans-serif'),
 clay=('"Fredoka","Nunito",system-ui,sans-serif','"Fredoka","Nunito",system-ui,sans-serif'),
 pastel=('"Quicksand","Nunito",system-ui,sans-serif','"Quicksand","Nunito",system-ui,sans-serif'),
 comic=('"Comic Neue","Comic Sans MS",system-ui,sans-serif','"Bangers","Impact",system-ui,sans-serif'),
 whiteboard=('"Patrick Hand","Comic Sans MS",system-ui,sans-serif','"Caveat","Patrick Hand",cursive'),
 anime=('"M PLUS Rounded 1c","Nunito",system-ui,sans-serif','"M PLUS Rounded 1c","Nunito",system-ui,sans-serif'),
 watercolor=('"Nunito",system-ui,sans-serif','"Caveat","Nunito",cursive'),
 university=('"EB Garamond",Georgia,serif','"EB Garamond",Georgia,serif'),
 professional=('"Inter",system-ui,sans-serif','"Inter",system-ui,sans-serif'),
)
SHAPE = dict(
 classic=dict(r='16px',rsm='12px',bw='1px',bw2='2px'),
 lego=dict(r='10px',rsm='6px',bw='2px',bw2='3px'),
 clay=dict(r='30px',rsm='22px',bw='0px',bw2='2px'),
 pastel=dict(r='24px',rsm='16px',bw='1px',bw2='2px'),
 comic=dict(r='6px',rsm='4px',bw='3px',bw2='3px'),
 whiteboard=dict(r='255px 22px 225px 22px / 22px 225px 22px 255px',rsm='14px 5px 16px 5px / 5px 16px 5px 14px',bw='2px',bw2='2px'),
 anime=dict(r='20px',rsm='14px',bw='1px',bw2='2px'),
 watercolor=dict(r='22px',rsm='14px',bw='1px',bw2='2px'),
 university=dict(r='6px',rsm='3px',bw='1px',bw2='2px'),
 professional=dict(r='12px',rsm='8px',bw='1px',bw2='1px'),
)
DEF_BTNSH='0 5px 0 color-mix(in srgb,var(--acc) 60%,#000)'
DEF_BTNSHA='0 1px 0 color-mix(in srgb,var(--acc) 60%,#000)'
DEF_PANELSH='0 6px 0 -2px color-mix(in srgb,var(--acc) 10%,transparent),0 14px 30px -18px color-mix(in srgb,var(--acc) 40%,transparent)'
EXTRA_TOK = dict(
 lego=dict(L=dict(btnsh='0 6px 0 #7d0a0b',btnsha='0 2px 0 #7d0a0b',panelsh='0 6px 0 rgba(0,0,0,.28)'),D=dict(btnsh='0 6px 0 #7d1c1e',btnsha='0 2px 0 #7d1c1e',panelsh='0 6px 0 rgba(0,0,0,.5)')),
 clay=dict(L=dict(btnsh='inset -4px -6px 10px rgba(150,70,40,.28),inset 5px 5px 10px rgba(255,255,255,.55),0 12px 18px -8px rgba(200,100,70,.6)',btnsha='inset 4px 5px 10px rgba(150,70,40,.3),inset -3px -3px 8px rgba(255,255,255,.3),0 3px 6px -2px rgba(200,100,70,.4)',panelsh='12px 14px 26px rgba(170,115,85,.28),-9px -9px 22px rgba(255,255,255,.9)'),
           D=dict(btnsh='inset -4px -6px 10px rgba(0,0,0,.28),inset 5px 5px 10px rgba(255,255,255,.22),0 12px 18px -8px rgba(0,0,0,.6)',btnsha='inset 4px 5px 10px rgba(0,0,0,.35),0 3px 6px -2px rgba(0,0,0,.4)',panelsh='10px 12px 26px rgba(0,0,0,.45),-8px -8px 20px rgba(255,255,255,.04)')),
 pastel=dict(L=dict(btnsh='0 5px 0 #7d63d6',btnsha='0 1px 0 #7d63d6',panelsh='0 12px 28px -14px rgba(167,139,250,.6)'),D=dict(btnsh='0 5px 0 #6a50c2',btnsha='0 1px 0 #6a50c2',panelsh='0 12px 28px -14px rgba(0,0,0,.6)')),
 comic=dict(L=dict(btnsh='4px 4px 0 #111',btnsha='1px 1px 0 #111',panelsh='6px 6px 0 #111',press='3px'),D=dict(btnsh='4px 4px 0 #000',btnsha='1px 1px 0 #000',panelsh='6px 6px 0 #000',press='3px')),
 whiteboard=dict(L=dict(btnsh='3px 4px 0 rgba(31,41,55,.55)',btnsha='1px 1px 0 rgba(31,41,55,.55)',panelsh='3px 5px 0 rgba(31,41,55,.22)',press='3px'),D=dict(btnsh='3px 4px 0 rgba(0,0,0,.5)',btnsha='1px 1px 0 rgba(0,0,0,.5)',panelsh='3px 5px 0 rgba(0,0,0,.35)',press='3px')),
 anime=dict(L=dict(btnsh='0 5px 0 #b02a70,inset 0 2px 0 rgba(255,255,255,.55)',btnsha='0 1px 0 #b02a70,inset 0 2px 0 rgba(255,255,255,.4)',panelsh='0 12px 30px -16px rgba(242,80,156,.55)'),D=dict(btnsh='0 5px 0 #a8438a,inset 0 2px 0 rgba(255,255,255,.35)',btnsha='0 1px 0 #a8438a',panelsh='0 12px 30px -16px rgba(0,0,0,.6)')),
 watercolor=dict(L=dict(btnsh='0 8px 18px -8px rgba(63,127,176,.7)',btnsha='0 2px 6px -2px rgba(63,127,176,.6)',panelsh='0 14px 34px -18px rgba(63,127,176,.5)',press='2px'),D=dict(btnsh='0 8px 18px -8px rgba(0,0,0,.7)',btnsha='0 2px 6px -2px rgba(0,0,0,.6)',panelsh='0 14px 34px -18px rgba(0,0,0,.6)',press='2px')),
 university=dict(L=dict(btnsh='0 3px 0 #4a0f18',btnsha='0 1px 0 #4a0f18',panelsh='0 2px 0 #d8cfb8,0 14px 28px -16px rgba(31,42,68,.45)',press='2px'),D=dict(btnsh='0 3px 0 #8a6a1d',btnsha='0 1px 0 #8a6a1d',panelsh='0 2px 0 #34405e,0 14px 28px -16px rgba(0,0,0,.6)',press='2px')),
 professional=dict(L=dict(btnsh='0 1px 2px rgba(16,24,40,.25)',btnsha='0 0 0 rgba(16,24,40,0)',panelsh='0 1px 2px rgba(16,24,40,.06),0 10px 28px -14px rgba(16,24,40,.2)',press='1px'),D=dict(btnsh='0 1px 2px rgba(0,0,0,.5)',btnsha='0 0 0 rgba(0,0,0,0)',panelsh='0 1px 2px rgba(0,0,0,.4),0 10px 28px -14px rgba(0,0,0,.6)',press='1px')),
)

# ---------------------------------------------------------------- icons (24x24)
START = {}
def ico(body): return enc(f"<svg {NS} viewBox='0 0 24 24'>{body}</svg>")
def glyph(theme, kind, f):
    W,C,J = dict(lego=(3.6,'butt','miter'),clay=(4.6,'round','round'),pastel=(3.2,'round','round'),comic=(4.6,'butt','miter'),
                 whiteboard=(2.6,'round','round'),anime=(3.2,'round','round'),watercolor=(3.2,'round','round'),
                 university=(2.6,'butt','miter'),professional=(2.2,'round','round'),classic=(3,'round','round')).get(theme,(3,'round','round'))
    if kind=='next':
        return ico(f"<path d='M4 12h14M12 5l7 7-7 7' fill='none' stroke='{f}' stroke-width='{W}' stroke-linecap='{C}' stroke-linejoin='{J}'/>")
    if kind=='check':
        return ico(f"<path d='M4 12.5l5 5L20 6.5' fill='none' stroke='{f}' stroke-width='{W}' stroke-linecap='{C}' stroke-linejoin='{J}'/>")
    # start
    if theme in START: return ico(f"<g fill='{f}' stroke='{f}'>{START[theme]}</g>")
    g = dict(
     classic=f"<path d='M8 5l12 7-12 7z' fill='{f}' stroke='{f}' stroke-width='2' stroke-linejoin='round'/>",
     lego=f"<rect x='3' y='10' width='18' height='10' rx='1' fill='{f}'/><rect x='6' y='6' width='4' height='4' rx='1' fill='{f}'/><rect x='14' y='6' width='4' height='4' rx='1' fill='{f}'/>",
     clay=f"<path d='M8 5l12 7-12 7z' fill='{f}' stroke='{f}' stroke-width='4' stroke-linejoin='round'/>",
     pastel=f"<path d='M12 21s-8-5.3-8-11a4.5 4.5 0 0 1 8-2.6A4.5 4.5 0 0 1 20 10c0 5.7-8 11-8 11z' fill='{f}'/>",
     comic=f"<path d='M13 2L4 14h7l-1 8 9-12h-7z' fill='{f}'/>",
     whiteboard=f"<path d='M4 20l1.2-5L16 4.2 19.8 8 9 18.8z' fill='{f}'/><path d='M14.5 5.7l3.8 3.8' stroke='{f}' stroke-width='1' opacity='.4'/>",
     anime=f"<path d='M12 2l2.2 7.8L22 12l-7.8 2.2L12 22l-2.2-7.8L2 12l7.8-2.2z' fill='{f}'/>",
     watercolor=f"<path d='M12 3C8 9 6 12 6 15a6 6 0 0 0 12 0c0-3-2-6-6-12z' fill='{f}'/>",
     university=f"<path d='M12 4L1 9l11 5 9-4.1V15h2V9z' fill='{f}'/><path d='M5 12.5V17c0 1.5 3.1 3 7 3s7-1.5 7-3v-4.5l-7 3.2z' fill='{f}'/>",
     professional=f"<circle cx='12' cy='12' r='9' fill='none' stroke='{f}' stroke-width='2'/><path d='M10 8l6 4-6 4z' fill='{f}'/>")[theme]
    return ico(g)

# ---------------------------------------------------------------- mascots (64x64)
def burst(cx,cy,n,r1,r2):
    pts=[]
    for i in range(n*2):
        r=r1 if i%2==0 else r2; a=math.pi*i/n
        pts.append(f"{cx+r*math.cos(a):.1f},{cy+r*math.sin(a):.1f}")
    return ' '.join(pts)
def mas(body): return enc(f"<svg {NS} viewBox='0 0 64 64'>{body}</svg>")
MASC = dict(
 classic=mas("<circle cx='28' cy='34' r='22' fill='none' stroke='#2743d6' stroke-width='2.5'/><circle cx='28' cy='34' r='14' fill='none' stroke='#7c5cff' stroke-width='2.5'/><circle cx='28' cy='34' r='6' fill='#ffe14d'/><g stroke='#ff5d73' stroke-width='3' stroke-linecap='round'><path d='M46 14l14-6M48 24l14-6M50 34l12-4'/></g>"),
 lego=mas("<g stroke='#111' stroke-width='2' stroke-linejoin='round'><g fill='#d01012'><rect x='6' y='40' width='52' height='18' rx='2'/><rect x='6' y='36' width='9' height='4'/><rect x='49' y='36' width='9' height='4'/></g><g fill='#f5cd2a'><rect x='14' y='22' width='36' height='18' rx='2'/><rect x='16' y='18' width='9' height='4'/><rect x='39' y='18' width='9' height='4'/></g><g fill='#0055bf'><rect x='22' y='6' width='20' height='16' rx='2'/><rect x='24' y='2' width='7' height='4'/><rect x='33' y='2' width='7' height='4'/></g></g>"),
 clay=mas("<defs><radialGradient id='a' cx='35%' cy='30%'><stop offset='0' stop-color='#ffd7c8'/><stop offset='1' stop-color='#ff8a65'/></radialGradient><radialGradient id='b' cx='35%' cy='30%'><stop offset='0' stop-color='#c9f1ea'/><stop offset='1' stop-color='#4fb5a6'/></radialGradient><radialGradient id='c' cx='35%' cy='30%'><stop offset='0' stop-color='#ffd3df'/><stop offset='1' stop-color='#f08aa6'/></radialGradient></defs><circle cx='27' cy='38' r='22' fill='url(#a)'/><circle cx='50' cy='50' r='12' fill='url(#b)'/><circle cx='44' cy='15' r='10' fill='url(#c)'/><ellipse cx='19' cy='28' rx='7' ry='4' fill='#fff' opacity='.5' transform='rotate(-30 19 28)'/>"),
 pastel=mas("<path d='M14 46a10 10 0 0 1 2-19.8A14 14 0 0 1 43 24a11 11 0 0 1 3 22z' fill='#fff' stroke='#c4b5fd' stroke-width='3' stroke-linejoin='round'/><path d='M50 6l2.2 5.6 5.6 2.2-5.6 2.2L50 21.6l-2.2-5.6-5.6-2.2 5.6-2.2z' fill='#fcd34d'/><path d='M52 40s-6-4-6-8a3.4 3.4 0 0 1 6-2 3.4 3.4 0 0 1 6 2c0 4-6 8-6 8z' fill='#f9a8d4'/><circle cx='24' cy='38' r='2' fill='#c4b5fd'/><circle cx='34' cy='38' r='2' fill='#c4b5fd'/>"),
 comic=mas(f"<polygon points='{burst(32,32,10,31,19)}' fill='#ffe600' stroke='#111' stroke-width='3' stroke-linejoin='round'/><text x='32' y='38' text-anchor='middle' font-family='Impact,Arial Black,sans-serif' font-size='15' font-weight='900' fill='#e63946' stroke='#111' stroke-width='.8'>QUIZ!</text>"),
 whiteboard=mas("<g transform='rotate(-35 30 26)'><rect x='4' y='20' width='40' height='12' rx='3' fill='#2563eb' stroke='#1f2937' stroke-width='2'/><rect x='44' y='22' width='10' height='8' fill='#1f2937'/><rect x='10' y='20' width='8' height='12' fill='#1f2937' opacity='.18'/></g><path d='M6 56c6-8 10 4 16-2s10-6 16 0 10 4 18-2' fill='none' stroke='#dc2626' stroke-width='3' stroke-linecap='round'/>"),
 anime=mas("<path d='M30 4l5 17 17 5-17 5-5 17-5-17-17-5 17-5z' fill='#ffe27a' stroke='#ff6fae' stroke-width='2.5' stroke-linejoin='round'/><path d='M52 6l2 6 6 2-6 2-2 6-2-6-6-2 6-2z' fill='#8f7dff'/><path d='M46 44c8-4 14 2 10 10-8 4-14-2-10-10z' fill='#ffb7d5'/><path d='M10 50l2 4 4 2-4 2-2 4-2-4-4-2 4-2z' fill='#4fd1c5'/>"),
 watercolor=mas("<defs><filter id='b'><feGaussianBlur stdDeviation='2'/></filter></defs><g filter='url(#b)'><circle cx='24' cy='32' r='17' fill='#7f9de0' fill-opacity='.75'/><circle cx='40' cy='38' r='14' fill='#e58a9b' fill-opacity='.7'/><circle cx='30' cy='48' r='12' fill='#6bb7a4' fill-opacity='.7'/></g><g transform='rotate(40 46 18)'><rect x='43' y='2' width='5' height='26' rx='2' fill='#8a6a3a'/><path d='M43 28h5l-1 8h-3z' fill='#3f7fb0'/></g>"),
 university=mas("<path d='M32 4l22 8v18c0 14-9 24-22 30C19 54 10 44 10 30V12z' fill='#7a1f2b' stroke='#b8860b' stroke-width='3' stroke-linejoin='round'/><path d='M18 26c5-3 10-3 14 0 4-3 9-3 14 0v16c-5-3-10-3-14 0-4-3-9-3-14 0z' fill='#f5efe0' stroke='#b8860b' stroke-width='1.5' stroke-linejoin='round'/><path d='M32 26v16' stroke='#b8860b' stroke-width='1.5'/>"),
 professional=mas("<rect x='8' y='8' width='48' height='48' rx='12' fill='#1f5fd1'/><path d='M20 34l9 9 15-18' fill='none' stroke='#fff' stroke-width='5' stroke-linecap='round' stroke-linejoin='round'/>"),
)

# ---------------------------------------------------------------- backgrounds
def bg_classic(d):
    cs = ('rgba(255,93,115,.16)','rgba(18,181,166,.12)','rgba(255,159,28,.09)','rgba(124,92,255,.16)') if d else ('#ffe0ea','#d9f3ff','#fff0c9','#e6e0ff')
    return (f"radial-gradient(520px 380px at 0% 0%,{cs[0]} 0,transparent 70%) fixed,radial-gradient(560px 420px at 100% 12%,{cs[1]} 0,transparent 70%) fixed,"
            f"radial-gradient(600px 460px at 85% 100%,{cs[2]} 0,transparent 70%) fixed,radial-gradient(520px 420px at 0% 92%,{cs[3]} 0,transparent 70%) fixed,var(--paper)")
def bg_lego(d):
    op = .13 if d else .16; stroke='rgba(255,255,255,.08)' if d else 'rgba(0,0,0,.09)'
    t=(f"<svg {NS} width='120' height='80'><g stroke='{stroke}' stroke-width='2'>"
       f"<rect x='1' y='1' width='58' height='38' fill='#d01012' fill-opacity='{op}'/><rect x='61' y='1' width='58' height='38' fill='#0055bf' fill-opacity='{op}'/>"
       f"<rect x='-29' y='41' width='58' height='38' fill='#00852b' fill-opacity='{op}'/><rect x='31' y='41' width='58' height='38' fill='#f5cd2a' fill-opacity='{op+.07}'/>"
       f"<rect x='91' y='41' width='58' height='38' fill='#00852b' fill-opacity='{op}'/></g><g fill='{stroke}'>"
       + ''.join(f"<circle cx='{x}' cy='{y}' r='6'/>" for x,y in [(20,20),(40,20),(80,20),(100,20),(50,60),(70,60),(10,60),(110,60)]) + "</g></svg>")
    return f"{enc(t)} 0 0/120px 80px fixed,var(--paper)"
def bg_clay(d):
    a,b,c,e = ('#5a3b33','#2f4a47','#58384a','#3d3a5e') if d else ('#ffd9c9','#cdeee8','#ffd6e2','#e1dcff')
    t=(f"<svg {NS} viewBox='0 0 1200 800' preserveAspectRatio='xMidYMid slice'><defs>"
       + ''.join(f"<radialGradient id='{i}' cx='35%' cy='30%'><stop offset='0' stop-color='{col}' stop-opacity='.95'/><stop offset='1' stop-color='{col}' stop-opacity='.55'/></radialGradient>" for i,col in zip('abcd',(a,b,c,e)))
       + "</defs><circle cx='80' cy='90' r='190' fill='url(#a)'/><circle cx='1130' cy='140' r='150' fill='url(#b)'/><circle cx='1060' cy='760' r='230' fill='url(#c)'/><circle cx='120' cy='730' r='160' fill='url(#d)'/><circle cx='620' cy='820' r='110' fill='url(#a)'/></svg>")
    return f"{enc(t)} center/cover no-repeat fixed,var(--paper)"
def bg_pastel(d):
    c1,c2,c3 = ('rgba(255,255,255,.06)','#b79cff','#f7a9d6') if d else ('rgba(255,255,255,.9)','#c4b5fd','#f9a8d4')
    t=(f"<svg {NS} width='220' height='220'><g fill='{c1}'><circle cx='40' cy='50' r='22'/><circle cx='64' cy='44' r='28'/><circle cx='90' cy='54' r='20'/><circle cx='150' cy='170' r='20'/><circle cx='172' cy='164' r='26'/><circle cx='196' cy='174' r='18'/></g>"
       f"<path d='M170 40l3 8 8 3-8 3-3 8-3-8-8-3 8-3z' fill='{c3}' fill-opacity='.7'/><path d='M30 150l2.4 6 6 2.4-6 2.4-2.4 6-2.4-6-6-2.4 6-2.4z' fill='{c2}' fill-opacity='.7'/><circle cx='110' cy='110' r='3' fill='{c2}' fill-opacity='.6'/></svg>")
    grad = 'linear-gradient(160deg,#2a2342,#231d33 60%,#2d2140)' if d else 'linear-gradient(160deg,#fff0f8,#f3eeff 55%,#e9f7ff)'
    return f"{enc(t)} 0 0/220px 220px fixed,{grad} fixed"
def bg_comic(d):
    dot = 'rgba(255,255,255,.08)' if d else 'rgba(0,0,0,.14)'
    g = 'linear-gradient(135deg,#14121f,#231a3d 60%,#2a1830)' if d else 'linear-gradient(135deg,#fff3b0,#ffd6e0 55%,#c9e4ff)'
    return f"radial-gradient(circle at center,{dot} 1.6px,transparent 2.3px) 0 0/14px 14px fixed,{g} fixed"
def bg_whiteboard(d):
    ln='rgba(255,255,255,.05)' if d else 'rgba(37,99,235,.07)'
    g='linear-gradient(180deg,#23342d,#1a2621)' if d else 'linear-gradient(180deg,#fbfcfd,#eef1f3)'
    return f"linear-gradient({ln} 1px,transparent 1px) 0 0/32px 32px fixed,linear-gradient(90deg,{ln} 1px,transparent 1px) 0 0/32px 32px fixed,{g} fixed"
def bg_anime(d):
    s1,s2,s3 = ('#1a1530','#2b1f55','#14284d') if d else ('#ffd9ec','#e6dcff','#d4ecff')
    star = '#ffe27a' if d else '#ffffff'
    stars=''.join(f"<path transform='translate({x} {y}) scale({s})' d='M0 -10l2.4 7.6L10 0 2.4 2.4 0 10-2.4 2.4-10 0l7.6-2.4z' fill='{star}' fill-opacity='{o}'/>" for x,y,s,o in [(140,120,1.6,.9),(1040,90,2,.9),(980,300,1,.8),(220,330,1.1,.8),(600,70,1,.7),(1120,520,1.3,.8),(70,560,1.4,.7)])
    petals=''.join(f"<ellipse cx='{x}' cy='{y}' rx='16' ry='8' fill='#ff9ccb' fill-opacity='{.45 if d else .6}' transform='rotate({r} {x} {y})'/>" for x,y,r in [(300,180,30),(860,140,-20),(1090,330,50),(180,520,-40),(760,640,20),(480,720,60),(1000,700,-30)])
    lines=''.join(f"<line x1='{x}' y1='800' x2='{x+90}' y2='{y}' stroke='#fff' stroke-opacity='{.10 if d else .45}' stroke-width='2'/>" for x,y in [(0,520),(120,560),(240,590),(960,590),(1080,540),(1200,500)])
    t=(f"<svg {NS} viewBox='0 0 1200 800' preserveAspectRatio='xMidYMid slice'><defs><linearGradient id='g' x1='0' y1='0' x2='0.6' y2='1'><stop offset='0' stop-color='{s1}'/><stop offset='.55' stop-color='{s2}'/><stop offset='1' stop-color='{s3}'/></linearGradient></defs><rect width='1200' height='800' fill='url(#g)'/>{lines}{petals}{stars}</svg>")
    return f"{enc(t)} center/cover no-repeat fixed,var(--paper)"
def bg_watercolor(d):
    cols = [('#3f6c9a',.55),('#9a4f66',.5),('#3f7d6c',.5),('#8a7a3a',.4)] if d else [('#8fb8e0',.55),('#f0a8b8',.5),('#a8d8c4',.5),('#f4d58c',.45)]
    t=(f"<svg {NS} viewBox='0 0 1200 800' preserveAspectRatio='xMidYMid slice'><defs><filter id='w' x='-20%' y='-20%' width='140%' height='140%'>"
       "<feTurbulence type='fractalNoise' baseFrequency='.011' numOctaves='3' seed='7' result='n'/><feDisplacementMap in='SourceGraphic' in2='n' scale='110'/><feGaussianBlur stdDeviation='9'/></filter></defs>"
       f"<g filter='url(#w)'><circle cx='120' cy='110' r='230' fill='{cols[0][0]}' fill-opacity='{cols[0][1]}'/><circle cx='1100' cy='160' r='200' fill='{cols[1][0]}' fill-opacity='{cols[1][1]}'/>"
       f"<circle cx='1040' cy='720' r='260' fill='{cols[2][0]}' fill-opacity='{cols[2][1]}'/><circle cx='150' cy='700' r='200' fill='{cols[3][0]}' fill-opacity='{cols[3][1]}'/></g></svg>")
    return f"{enc(t)} center/cover no-repeat fixed,var(--paper)"
def bg_university(d):
    line = 'rgba(143,168,232,.10)' if d else 'rgba(60,80,140,.13)'; mar = 'rgba(229,123,130,.28)' if d else 'rgba(163,38,47,.28)'
    return f"linear-gradient(90deg,transparent 0 52px,{mar} 52px 54px,transparent 54px) fixed,repeating-linear-gradient(transparent 0 31px,{line} 31px 32px) fixed,var(--paper)"
def bg_professional(d):
    dot='rgba(255,255,255,.05)' if d else 'rgba(16,24,40,.07)'
    g='linear-gradient(180deg,#0f141b,#0b1017)' if d else 'linear-gradient(180deg,#f8fafc,#eef2f7)'
    return f"radial-gradient({dot} 1px,transparent 1.3px) 0 0/22px 22px fixed,{g} fixed"
BG = dict(classic=bg_classic,lego=bg_lego,clay=bg_clay,pastel=bg_pastel,comic=bg_comic,whiteboard=bg_whiteboard,anime=bg_anime,watercolor=bg_watercolor,university=bg_university,professional=bg_professional)

# ---------------------------------------------------------------- per-theme extra CSS
EXTRA = dict(
 classic="",
 lego="""
[data-theme=lego] h1{background:none;color:var(--acc);-webkit-text-fill-color:currentColor;text-shadow:2px 2px 0 var(--hl)}
[data-theme=lego] .panel{background-image:radial-gradient(circle at 50% -2px,rgba(0,0,0,.10) 7px,transparent 8px);background-size:34px 14px;background-repeat:repeat-x}
[data-theme=lego] .opt,[data-theme=lego] .btn,[data-theme=lego] .mbtn,[data-theme=lego] .ord,[data-theme=lego] .chip2{box-shadow:0 3px 0 rgba(0,0,0,.18)}
[data-theme=lego] .btn.main,[data-theme=lego] .go{border:2px solid rgba(0,0,0,.35)}
""",
 clay="""
[data-theme=clay] h1{background:none;color:var(--acc);-webkit-text-fill-color:currentColor;text-shadow:2px 3px 0 color-mix(in srgb,var(--acc) 35%,transparent)}
[data-theme=clay] .opt,[data-theme=clay] .btn:not(.main),[data-theme=clay] .mbtn,[data-theme=clay] .ord,[data-theme=clay] .chip2,[data-theme=clay] .fillbox,[data-theme=clay] .seg,[data-theme=clay] select{box-shadow:inset -3px -4px 8px rgba(120,70,40,.10),inset 3px 3px 8px rgba(255,255,255,.65);border-color:transparent}
[data-theme=clay][data-scheme=dark] .opt,[data-theme=clay][data-scheme=dark] .btn:not(.main),[data-theme=clay][data-scheme=dark] .mbtn,[data-theme=clay][data-scheme=dark] .ord,[data-theme=clay][data-scheme=dark] .chip2{box-shadow:inset -3px -4px 8px rgba(0,0,0,.28),inset 3px 3px 8px rgba(255,255,255,.07)}
[data-theme=clay] .opt.right,[data-theme=clay] .opt.wrong{border-color:transparent;outline:3px solid currentColor}
[data-theme=clay] .opt.right{outline-color:var(--ok)}[data-theme=clay] .opt.wrong{outline-color:var(--bad)}
""",
 pastel="""
[data-theme=pastel] h1{background:linear-gradient(90deg,var(--acc),var(--acc2));-webkit-background-clip:text;background-clip:text;color:transparent}
[data-theme=pastel] .question{font-weight:600}
""",
 comic="""
[data-theme=comic] h1{background:none;color:var(--acc);-webkit-text-fill-color:currentColor;-webkit-text-stroke:2px var(--ink);paint-order:stroke fill;text-shadow:3px 3px 0 var(--ink);letter-spacing:.04em;font-weight:400;font-size:2rem}
[data-theme=comic] .chtitle,[data-theme=comic] .verdict,[data-theme=comic] .panel h2,[data-theme=comic] .rpct,[data-theme=comic] .rbadge{font-family:"Bangers","Impact",sans-serif;letter-spacing:.04em;font-weight:400}
[data-theme=comic] .rpct{font-size:5.6rem;text-shadow:4px 4px 0 rgba(0,0,0,.35)}
[data-theme=comic] .question{font-family:"Comic Neue","Comic Sans MS",sans-serif;font-weight:700}
[data-theme=comic] .opt,[data-theme=comic] .mbtn,[data-theme=comic] .ord,[data-theme=comic] .chip2{box-shadow:3px 3px 0 var(--ink)}
[data-theme=comic] .opt:hover:not([disabled]){box-shadow:5px 5px 0 var(--ink)}
[data-theme=comic] .why{border:3px solid var(--ink);border-left-width:3px;border-radius:8px;box-shadow:3px 3px 0 var(--ink)}
[data-theme=comic] .chip,[data-theme=comic] .kind,[data-theme=comic] .vchip,[data-theme=comic] .mini,[data-theme=comic] .streak,[data-theme=comic] .clockpill{border:2px solid var(--ink)}
[data-theme=comic] .btn.main,[data-theme=comic] .go{border:3px solid var(--ink);font-family:"Bangers","Impact",sans-serif;letter-spacing:.05em;font-weight:400;font-size:1.15em}
[data-theme=comic] .rhero{border:3px solid var(--ink);box-shadow:5px 5px 0 var(--ink)}
""",
 whiteboard="""
[data-theme=whiteboard] h1{background:none;color:var(--acc);-webkit-text-fill-color:currentColor;font-size:2.1rem;font-weight:700;text-decoration:underline wavy var(--c1);text-underline-offset:6px;text-decoration-thickness:2px}
[data-theme=whiteboard] .question{font-family:"Caveat","Patrick Hand",cursive;font-size:1.7rem;font-weight:700;line-height:1.5}
[data-theme=whiteboard] .chtitle,[data-theme=whiteboard] .verdict,[data-theme=whiteboard] .panel h2{font-family:"Caveat","Patrick Hand",cursive;font-size:1.35em;font-weight:700}
[data-theme=whiteboard] .btn.main,[data-theme=whiteboard] .go{border:2px solid var(--ink)}
[data-theme=whiteboard] .opt,[data-theme=whiteboard] .mbtn,[data-theme=whiteboard] .ord,[data-theme=whiteboard] .chip2{box-shadow:2px 3px 0 color-mix(in srgb,var(--ink) 25%,transparent)}
""",
 anime="""
[data-theme=anime] h1{background:linear-gradient(90deg,var(--acc),var(--acc2));-webkit-background-clip:text;background-clip:text;color:transparent;font-weight:700}
[data-theme=anime] h1::after{content:" \\2726";-webkit-text-fill-color:var(--c4);color:var(--c4)}
[data-theme=anime] .btn.main,[data-theme=anime] .go{background:linear-gradient(180deg,rgba(255,255,255,.38),rgba(255,255,255,0) 55%),var(--grad)}
[data-theme=anime] .chip{background:linear-gradient(180deg,rgba(255,255,255,.35),rgba(255,255,255,0) 60%),var(--grad)}
[data-theme=anime] .question{font-weight:500}
""",
 watercolor="""
[data-theme=watercolor] h1{background:linear-gradient(90deg,var(--acc),var(--c1) 70%,var(--acc2));-webkit-background-clip:text;background-clip:text;color:transparent;font-size:2.15rem;font-weight:700}
[data-theme=watercolor] .panel{background-image:radial-gradient(120% 90% at 0% 0%,color-mix(in srgb,var(--c3) 12%,transparent),transparent 60%),radial-gradient(120% 90% at 100% 100%,color-mix(in srgb,var(--c1) 12%,transparent),transparent 60%)}
[data-theme=watercolor] .chtitle,[data-theme=watercolor] .verdict,[data-theme=watercolor] .panel h2{font-family:"Caveat","Nunito",cursive;font-size:1.3em;font-weight:700}
[data-theme=watercolor] .question{font-family:"Nunito",sans-serif;font-weight:600}
""",
 university="""
[data-theme=university] h1{background:none;color:var(--acc);-webkit-text-fill-color:currentColor;font-variant:small-caps;letter-spacing:.03em;font-weight:600}
[data-theme=university] .panel{border-style:double;border-width:3px}
[data-theme=university] .btn.main,[data-theme=university] .go{border:1px solid var(--c4)}
[data-theme=university] .question{font-size:1.45rem;line-height:1.55}
[data-theme=university] .chip{background:var(--acc);color:var(--on)}
""",
 professional="""
[data-theme=professional] h1{background:none;color:var(--ink);-webkit-text-fill-color:currentColor;font-weight:650;letter-spacing:-.02em}
[data-theme=professional] .question{font-weight:500;font-size:1.25rem;line-height:1.55}
[data-theme=professional] .opt,[data-theme=professional] .btn,[data-theme=professional] .mbtn{box-shadow:0 1px 2px rgba(16,24,40,.06)}
[data-theme=professional] .btn.main,[data-theme=professional] .go{box-shadow:var(--btn-sh)}
""",
)

# ---------------------------------------------------------------- assemble
import os
HERE = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.dirname(HERE)
exec(open(os.path.join(HERE, 'gen_more.py')).read())
THEMES = ['classic','lego','clay','pastel','comic','whiteboard','anime','watercolor','university','professional']+list(NEW)
out=[]
out.append("""/* themes.css: generated. Theme = [data-theme], light/dark = [data-scheme]. All artwork is original. */
:root{
  --cobalt:var(--acc);
  --cobalt-soft:color-mix(in srgb,var(--acc) 14%,var(--card));
  --hl-soft:color-mix(in srgb,var(--hl) 30%,var(--card));
  --ok-soft:color-mix(in srgb,var(--ok) 16%,var(--card));
  --bad-soft:color-mix(in srgb,var(--bad) 16%,var(--card));
  --part-soft:color-mix(in srgb,var(--part) 18%,var(--card));
  --pink-soft:color-mix(in srgb,var(--c1) 18%,var(--card));
  --teal-soft:color-mix(in srgb,var(--c2) 18%,var(--card));
  --violet-soft:color-mix(in srgb,var(--c3) 18%,var(--card));
  --amber-soft:color-mix(in srgb,var(--c4) 20%,var(--card));
  --grad:linear-gradient(90deg,var(--acc),var(--acc2));
  --btn-sh:""" + DEF_BTNSH + """;
  --btn-sh-a:""" + DEF_BTNSHA + """;
  --panel-sh:""" + DEF_PANELSH + """;
  --press:4px;
}
""")
for t in THEMES:
    for sch,key in (('light','L'),('dark','D')):
        p=P[t][key]; x=EXTRA_TOK.get(t,{}).get(key,{})
        d = key=='D'
        sans,serif = FONTS[t]
        sh=SHAPE[t]
        flat = p['acc']==p['acc2']
        v = {
         '--paper':p['paper'],'--card':p['card'],'--ink':p['ink'],'--mut':p['mut'],'--line':p['line'],'--acc':p['acc'],'--acc2':p['acc2'],
         '--hl':p['hl'],'--ok':p['ok'],'--bad':p['bad'],'--part':p['part'],'--c1':p['c1'],'--c2':p['c2'],'--c3':p['c3'],'--c4':p['c4'],
         '--on':p['on'],'--on-hero':p['onh'],
         '--sans':sans,'--serif':serif,'--r':sh['r'],'--r-sm':sh['rsm'],'--bw':sh['bw'],'--bw2':sh['bw2'],
         '--bg':BG[t](d),'--mascot':MASC[t],
         '--ico-start':glyph(t,'start',p['on']),'--ico-next':glyph(t,'next',p['on']),'--ico-check':glyph(t,'check',p['on']),
         '--btn-sh':x.get('btnsh',DEF_BTNSH),'--btn-sh-a':x.get('btnsha',DEF_BTNSHA),'--panel-sh':x.get('panelsh',DEF_PANELSH),'--press':x.get('press','4px'),
         '--grad':'linear-gradient(var(--acc),var(--acc))' if flat else 'linear-gradient(90deg,var(--acc),var(--acc2))',
        }
        out.append(f":root[data-theme='{t}'][data-scheme='{sch}']{{" + ';'.join(f"{k}:{val}" for k,val in v.items()) + "}\n")
# tiles
for t in THEMES:
    for sch,key in (('light','L'),('dark','D')):
        p=P[t][key]; sh=SHAPE[t]
        sel = f".tile[data-t='{t}']" if key=='L' else f"[data-scheme='dark'] .tile[data-t='{t}']"
        v={'--t-bg':p['paper'],'--t-card':p['card'],'--t-ink':p['ink'],'--t-line':p['line'],'--t-acc':p['acc'],'--t-on':p['on'],'--t-c1':p['c1'],'--t-c2':p['c2'],'--t-c3':p['c3'],'--t-r':sh['rsm'],'--t-bg-art':BG[t](key=='D').replace('var(--paper)',p['paper'])}
        out.append(sel+"{"+';'.join(f"{k}:{val}" for k,val in v.items())+"}\n")
    out.append(f".tile[data-t='{t}'] .tmas{{background-image:{MASC[t]}}}\n")

out.append(r"""
/* ---------- shared rules driven by the tokens ---------- */
body{font-family:var(--sans);color:var(--ink);background:var(--bg);background-color:var(--paper)}
h1{background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.panel{border-width:var(--bw);border-radius:var(--r);box-shadow:var(--panel-sh)}
.rhero{border-radius:var(--r)}
.opt,.btn,.mbtn,.ord,.chip2,.fillbox,.sbox,.mrow,.cue,.confrow,select,.rate button,.seg,.lenrow input,.ordlist,.spool{border-radius:var(--r-sm)}
.opt,.mbtn,.ord,.chip2,.fillbox,.sbox,.mrow{border-width:var(--bw2)}
.go,.btn.main{background:var(--grad);color:var(--on);box-shadow:var(--btn-sh)}
.go{border-radius:var(--r-sm)}
.go:active:not([disabled]),.btn.main:active:not([disabled]){box-shadow:var(--btn-sh-a);transform:translateY(var(--press))}
.seg button[aria-pressed=true],.chip,.mini.on{background:var(--grad);color:var(--on)}
.opt:nth-of-type(1) .k,.opt:nth-of-type(2) .k,.opt:nth-of-type(3) .k,.opt:nth-of-type(4) .k{color:var(--ink)}
.verdict.ok{color:var(--ok)}.verdict.mid{color:var(--part)}.verdict.no{color:var(--bad)}
.cm{color:var(--bad)}.kind{color:var(--ink)}
.streak{background:var(--amber-soft);border-color:var(--c4)}
.q-card{border-color:var(--cobalt-soft)}
.rhero{color:var(--on-hero)}
.v-excellent .rhero{background:linear-gradient(135deg,var(--c4),var(--c1) 60%,var(--c3))}
.v-pass .rhero{background:linear-gradient(135deg,var(--c2),var(--acc))}
.v-fail .rhero{background:linear-gradient(135deg,var(--c1),var(--c4))}
.rbadge{border-color:currentColor}
.vchip.excellent{background:linear-gradient(90deg,var(--c4),var(--c1))}
.vchip.pass{background:var(--ok)}.vchip.fail{background:var(--bad)}
.shead:hover{filter:none;background:var(--cobalt-soft)}

/* picture in the header and a faint stamp on the question card */
.mascot{flex:none;width:58px;height:58px;background:var(--mascot) center/contain no-repeat}
.q-card::after{content:"";position:absolute;right:10px;bottom:10px;width:84px;height:84px;background:var(--mascot) center/contain no-repeat;opacity:.10;pointer-events:none}

/* button icons that follow the theme */
.go::before,.btn.main::after{content:"";display:inline-block;width:1.15em;height:1.15em;vertical-align:-.2em;background-position:center;background-repeat:no-repeat;background-size:contain}
.go::before{background-image:var(--ico-start);margin-right:.5em}
.btn.main::after{background-image:var(--ico-next);margin-left:.5em}
.btn.main.chk::after{background-image:var(--ico-check)}

/* theme picker */
.themebtn{display:inline-flex;align-items:center;gap:8px;background:var(--card);border:var(--bw2) solid var(--line);border-radius:999px;padding:6px 14px;font-size:.88rem;font-weight:600}
.themebtn i{display:block;width:16px;height:16px;border-radius:50%;background:conic-gradient(var(--c1),var(--c4),var(--c2),var(--c3),var(--c1))}
.top .tools2{display:flex;gap:8px;align-items:center}
.playing .themebtn{display:none}
#themePanel h3{font:600 .95rem var(--sans);margin:14px 0 8px}
.tiles{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:10px}
.tile{display:grid;gap:6px;justify-items:center;text-align:center;padding:10px 8px 12px;background:var(--t-bg-art);background-color:var(--t-bg);color:var(--t-ink);border:2px solid var(--t-line);border-radius:var(--t-r)}
.tile .tmas{width:46px;height:46px;background-position:center;background-size:contain;background-repeat:no-repeat}
.tile .tsw{display:flex;gap:4px}.tile .tsw i{width:12px;height:12px;border-radius:50%}
.tile .tsw i:nth-child(1){background:var(--t-c1)}.tile .tsw i:nth-child(2){background:var(--t-c2)}.tile .tsw i:nth-child(3){background:var(--t-c3)}
.tile .tbtn{background:var(--t-acc);color:var(--t-on);border-radius:var(--t-r);padding:3px 12px;font-size:.78rem;font-weight:600}
.tile .tnm{font-weight:600;font-size:.9rem;background:var(--t-card);padding:1px 8px;border-radius:999px}
.tile[aria-pressed=true]{outline:3px solid var(--acc);outline-offset:2px}
.tile:hover{transform:translateY(-2px)}
""")
for t in THEMES[1:]:
    out.append(EXTRA[t])
out.append("""
/* dark: soften the highlighter so light text stays readable */
:root[data-scheme='dark'] .question,:root[data-scheme='dark'] .topic mark{background-image:linear-gradient(transparent 62%,color-mix(in srgb,var(--hl) 32%,transparent) 62%)}
""")
open(os.path.join(SITE,'themes.css'),'w').write(''.join(out))

# ---- themes-list.js: the picker's list of themes, plus the Google Fonts link (single source of truth)
import json
NAMES = dict(classic='Classic',lego='Lego',clay='Clay',pastel='Pastel',comic='Comic book',whiteboard='Whiteboard',anime='Anime',watercolor='Watercolor',university='University',professional='Professional')
NAMES.update({k:v['name'] for k,v in NEW.items()})
GFONTS = {'Instrument Sans':'Instrument+Sans:wght@400;500;600','Source Serif 4':'Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400',
 'Fredoka':'Fredoka:wght@400;500;600','Quicksand':'Quicksand:wght@500;600;700','Comic Neue':'Comic+Neue:wght@400;700','Bangers':'Bangers',
 'Patrick Hand':'Patrick+Hand','Caveat':'Caveat:wght@600','M PLUS Rounded 1c':'M+PLUS+Rounded+1c:wght@400;500;700','Nunito':'Nunito:wght@400;600;700',
 'EB Garamond':'EB+Garamond:wght@400;500;600','Inter':'Inter:wght@400;500;600','Marcellus':'Marcellus','Lora':'Lora:wght@400;600',
 'Cormorant Garamond':'Cormorant+Garamond:wght@500;600','Exo 2':'Exo+2:wght@400;600','Lexend':'Lexend:wght@400;500','Baloo 2':'Baloo+2:wght@400;600',
 'Josefin Sans':'Josefin+Sans:wght@400;600','Barlow':'Barlow:wght@400;600','Barlow Condensed':'Barlow+Condensed:wght@600','Poppins':'Poppins:wght@400;500;600',
 'Playfair Display':'Playfair+Display:wght@500;700','Permanent Marker':'Permanent+Marker'}
import re
used=[]
for t in THEMES:
    for f in FONTS[t]:
        for fam in re.findall(r'"([^"]+)"',f):
            if fam in GFONTS and fam not in used: used.append(fam)
url='https://fonts.googleapis.com/css2?'+'&'.join('family='+GFONTS[f] for f in used)+'&display=swap'
js=("/* themes-list.js: GENERATED by tools/gen_themes.py. Do not edit by hand. */\nwindow.QUIZ_THEMES = "+json.dumps([[t,NAMES[t]] for t in THEMES])+";\n"
    "(function(){var l=document.createElement('link');l.rel='stylesheet';l.href="+json.dumps(url)+";document.head.appendChild(l);})();\n")
open(os.path.join(SITE,'themes-list.js'),'w').write(js)
print('themes.css',len(''.join(out)),'chars;',len(THEMES),'themes;',len(used),'fonts')
