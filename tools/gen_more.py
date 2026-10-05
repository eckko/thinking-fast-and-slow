# Extra themes. exec'd from gen_themes.py (shares its globals: P FONTS SHAPE MASC BG EXTRA START enc NS math)
def _lum(h):
    h=h.lstrip('#'); r,g,b=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    f=lambda c: c/12.92 if c<=.03928 else ((c+.055)/1.055)**2.4
    return .2126*f(r)+.7152*f(g)+.0722*f(b)
def _pal(L,D):
    keys='paper card ink mut line acc acc2 hl c1 c2 c3 c4'.split()
    out={}
    for k,v,(ok,bad,part) in (('L',L,('#1e7f5c','#c8402f','#a15f00')),('D',D,('#5fd6a4','#ff8a7a','#eab64a'))):
        d=dict(zip(keys,v.split())); d.update(ok=ok,bad=bad,part=part)
        on='#ffffff' if _lum(d['acc'])<.30 else ('#101418')
        d['on']=on; d['onh']=on if k=='D' else '#ffffff'
        if k=='L' and _lum(d['c2'])>.45: d['onh']='#16202a'
        out[k]=d
    return out
def _petals(cx,cy,n,rx,ry,dist,fill,op):
    return ''.join(f"<ellipse cx='{cx}' cy='{cy-dist}' rx='{rx}' ry='{ry}' fill='{fill}' fill-opacity='{op}' transform='rotate({360*i/n:.0f} {cx} {cy})'/>" for i in range(n))
def _tile(w,h,body): return f"<svg {NS} width='{w}' height='{h}'>{body}</svg>"
def _bgfn(w,h,body_fn,grad_l,grad_d):
    def f(d):
        t=_tile(w,h,body_fn(d)); g=grad_d if d else grad_l
        return f"{enc(t)} 0 0/{w}px {h}px fixed,{g} fixed"
    return f
def _flat(c1,c2,ang=160): return f"linear-gradient({ang}deg,{c1},{c2})"

NEW = {}   # key -> dict(name, pal, font, r, bg, mascot, start, h1)
def add(key,name,L,D,font,r,bg,mascot,start,h1=''):
    NEW[key]=dict(name=name,pal=_pal(L,D),font=font,r=r,bg=bg,mascot=mascot,start=start,h1=h1)

# 1 VEDIC ---------------------------------------------------------------
add('vedic','Vedic',
 '#fff4de #fffaf0 #3a1d12 #7a5a45 #ecd2a6 #c2410c #a21caf #ffd27a #e2571f #b8860b #7c2d12 #f59e0b',
 '#1f130d #2c1b12 #fbe9d0 #cdb393 #4a3220 #ff9a4d #e08cff #e8b04a #ff8a5c #f0c05a #d9a066 #ffb84d',
 ('"Marcellus","Cormorant Garamond",Georgia,serif','"Marcellus","Cormorant Garamond",Georgia,serif'),
 ('14px','10px'),
 _bgfn(110,110,lambda d:f"<g fill='{'#ffb84d' if d else '#c2410c'}' fill-opacity='{.10 if d else .09}'>{_petals(55,55,8,5,13,15,'#c2410c' if not d else '#ffb84d',.12)}</g><circle cx='55' cy='55' r='4' fill='{'#ffd27a' if d else '#b8860b'}' fill-opacity='.35'/><g fill='{'#ffd27a' if d else '#b8860b'}' fill-opacity='.30'><circle cx='5' cy='5' r='2.2'/><circle cx='105' cy='5' r='2.2'/><circle cx='5' cy='105' r='2.2'/><circle cx='105' cy='105' r='2.2'/><path d='M55 2l4 5-4 5-4-5z'/><path d='M55 98l4 5-4 5-4-5z'/></g>",
   _flat('#fff1d6','#ffe3b8'),_flat('#241610','#1a0f0a')),
 "<path d='M8 44h48c0 10-9 17-24 17S8 54 8 44z' fill='#b45309' stroke='#7c2d12' stroke-width='2.5' stroke-linejoin='round'/><path d='M32 40c-9-7-6-16 0-26 6 10 9 19 0 26z' fill='#ffb84d' stroke='#e2571f' stroke-width='2.5' stroke-linejoin='round'/><path d='M32 36c-4-4-3-8 0-13 3 5 4 9 0 13z' fill='#fff2b0'/><path d='M14 52h36' stroke='#fcd34d' stroke-width='2' stroke-linecap='round'/><circle cx='54' cy='14' r='2.5' fill='#f59e0b'/><circle cx='10' cy='20' r='2' fill='#f59e0b'/>",
 "<path d='M12 21c-3.5-3-4-7-.5-12 1 2 2 3 3 3-.5-3 .5-6 3.5-9 .5 4 3.5 6 3.5 11 0 4-3 7-9.5 7z'/>")

# 2 AYURVEDA ------------------------------------------------------------
add('ayurveda','Ayurveda',
 '#f3f8ee #fcfef9 #1f3324 #5b7060 #d3e2c8 #2f7d4f #b8860b #f2e08a #4f9d69 #c9921a #8a6a3b #7aa84a',
 '#101a13 #172419 #e6f3df #a3bba6 #2c4332 #6fd098 #e6c35a #d9c76a #7fd6a0 #e6b84a #c9a06a #a5d468',
 ('"Lora",Georgia,serif','"Lora",Georgia,serif'),
 ('18px','12px'),
 _bgfn(130,130,lambda d:(lambda g,y:f"<g fill='{g}' fill-opacity='{.16 if d else .18}'><path d='M20 40c18-4 30 6 34 24-18 4-32-6-34-24z'/><path d='M85 100c-14-6-18-22-8-34 12 6 16 22 8 34z'/></g><path d='M20 40q16 10 34 24M85 100q-6-16-8-34' stroke='{g}' stroke-opacity='.3' stroke-width='1.5' fill='none'/><circle cx='100' cy='30' r='4' fill='{y}' fill-opacity='.35'/><circle cx='36' cy='108' r='3' fill='{y}' fill-opacity='.35'/>")('#6fd098' if d else '#2f7d4f','#e6c35a' if d else '#c9921a'),
   _flat('#f4f9ee','#e5f1da'),_flat('#121d15','#0d150f')),
 "<path d='M32 58V30' stroke='#2f7d4f' stroke-width='3' stroke-linecap='round'/><path d='M32 40c-14 0-22-8-24-20 14-1 24 6 24 20z' fill='#4f9d69' stroke='#1f5a37' stroke-width='2.5' stroke-linejoin='round'/><path d='M32 34c12-2 20-9 22-20-13 0-22 7-22 20z' fill='#7aa84a' stroke='#1f5a37' stroke-width='2.5' stroke-linejoin='round'/><path d='M32 52c-10-1-16-6-18-14 10 0 17 5 18 14z' fill='#a5d468' stroke='#1f5a37' stroke-width='2.5' stroke-linejoin='round'/><path d='M50 38c4 6 6 9 0 14-6-5-4-8 0-14z' fill='#f2c94c' stroke='#b8860b' stroke-width='2'/>",
 "<path d='M4 20C4 9 12 3 21 3c0 11-6 18-17 17z'/><path d='M4 20c4-6 8-9 13-12' stroke='#000' stroke-opacity='.25' stroke-width='1.2' fill='none'/>")

# 3 INDIAN HISTORY ------------------------------------------------------
add('history','Indian History',
 '#f7ecdc #fff9ee #2b2233 #6e5d6a #e2cdb0 #9a3412 #1e3a8a #f0cf7a #b45309 #1e3a8a #0f766e #be123c',
 '#18141f #231d2c #f4e7d4 #bdb0b6 #3a3045 #f08a4b #8fa6ff #e0b560 #f59e5c #8fa6ff #4fd1c5 #ff7a96',
 ('"Cormorant Garamond","Georgia",serif','"Cormorant Garamond","Georgia",serif'),
 ('10px','6px'),
 _bgfn(96,120,lambda d:(lambda c:f"<g fill='none' stroke='{c}' stroke-opacity='{.22 if d else .20}' stroke-width='2'><path d='M18 120V66c0-22 30-22 30 0v54'/><path d='M24 120V68c0-15 18-15 18 0v52'/><path d='M66 120V66c0-22 30-22 30 0v54' transform='translate(-18 0)' opacity='0'/></g><g fill='{c}' fill-opacity='.22'><circle cx='33' cy='28' r='3'/><circle cx='80' cy='60' r='2.4'/><path d='M80 20l5 6-5 6-5-6z'/></g>")('#f0c27a' if d else '#9a3412'),
   _flat('#f9efdf','#f0dcc0'),_flat('#1b1622','#130f19')),
 "<path d='M6 58V32c0-6 3-9 6-12 3 3 6 6 6 12v26z' fill='#d97706' stroke='#7c2d12' stroke-width='2.5' stroke-linejoin='round'/><path d='M14 58V38c0-5 4-9 9-9h18c5 0 9 4 9 9v20z' fill='#f2c78b' stroke='#7c2d12' stroke-width='2.5' stroke-linejoin='round'/><path d='M23 58V46c0-6 14-6 14 0v12' fill='#7c2d12'/><path d='M32 29c-8-2-12-6-12-11 8 0 12 4 12 11 0 0 0 0 0 0 0-7 4-11 12-11 0 5-4 9-12 11z' fill='#be123c' stroke='#7c2d12' stroke-width='2' stroke-linejoin='round'/><path d='M32 14V6' stroke='#7c2d12' stroke-width='2.5' stroke-linecap='round'/><path d='M32 6l8 2-8 3z' fill='#1e3a8a'/>",
 "<path d='M3 21V10l9-6 9 6v11h-5v-7a4 4 0 0 0-8 0v7z'/>")

# 4 UNIVERSE ------------------------------------------------------------
def _stars(d):
    c='#ffffff' if d else '#5b4bb8'; o=.55 if d else .30
    pts=[(14,18,1.6),(60,40,1),(98,12,1.2),(120,70,1.8),(34,84,1),(82,104,1.4),(20,128,1.1),(112,130,1)]
    s=''.join(f"<circle cx='{x}' cy='{y}' r='{r}' fill='{c}' fill-opacity='{o}'/>" for x,y,r in pts)
    s+=f"<path d='M70 90l2 6 6 2-6 2-2 6-2-6-6-2 6-2z' fill='{'#ffe27a' if d else '#7c5cff'}' fill-opacity='{.7 if d else .35}'/>"
    return s
add('universe','Universe',
 '#eef0ff #ffffff #1a1740 #5d5f8c #d4d8f5 #4f46e5 #a21caf #ffe27a #7c3aed #0ea5e9 #db2777 #f59e0b',
 '#070816 #0f1130 #e8eaff #a6aad6 #272b5a #8b8cff #f0a6ff #ffd966 #b794ff #4cc9f0 #ff7ac6 #ffc65c',
 ('"Exo 2","Nunito",system-ui,sans-serif','"Exo 2","Nunito",system-ui,sans-serif'),
 ('18px','12px'),
 _bgfn(140,140,_stars,
   "radial-gradient(600px 400px at 85% 0%,#e0d4ff,transparent 70%) fixed,radial-gradient(500px 400px at 0% 100%,#cfe8ff,transparent 70%) fixed,#eef0ff",
   "radial-gradient(700px 500px at 85% 0%,#2b1b6b,transparent 70%) fixed,radial-gradient(600px 500px at 0% 100%,#0b2a5c,transparent 70%) fixed,#070816"),
 "<circle cx='30' cy='34' r='17' fill='#8b5cf6' stroke='#2e1065' stroke-width='2.5'/><path d='M16 28c8 2 20 0 28-4M14 38c10 3 22 0 31-4' stroke='#c4b5fd' stroke-width='3' fill='none' stroke-linecap='round' opacity='.7'/><ellipse cx='30' cy='36' rx='29' ry='8' fill='none' stroke='#fbbf24' stroke-width='4' transform='rotate(-18 30 36)'/><path d='M13 40a17 17 0 0 0 34 -2' fill='none' stroke='#8b5cf6' stroke-width='0'/><circle cx='54' cy='12' r='3' fill='#ffe27a'/><circle cx='8' cy='10' r='2' fill='#ffe27a'/><circle cx='52' cy='56' r='2' fill='#7dd3fc'/>",
 "<circle cx='12' cy='12' r='5.5'/><path d='M2 16c0-3 5-6 10-6.5M22 8c0 3-5 6-10 6.5' fill='none' stroke='currentColor' stroke-width='0'/><ellipse cx='12' cy='12' rx='10.5' ry='3.6' fill='none' stroke-width='2' transform='rotate(-20 12 12)'/>")

# 5 MATHS ---------------------------------------------------------------
add('maths','Maths',
 '#f1f6ff #ffffff #12264a #566b8c #cfdcf2 #1d4ed8 #0891b2 #fde68a #dc2626 #0d9488 #7c3aed #d97706',
 '#0c1a2e #132640 #e6f0ff #9bb3d3 #25405f #6aa2ff #4fd1e6 #f2d46a #ff8a80 #4fd6c4 #b79cff #ffb74d',
 ('"Lexend","Nunito",system-ui,sans-serif','"Lexend","Nunito",system-ui,sans-serif'),
 ('12px','8px'),
 _bgfn(120,120,lambda d:(lambda c,a:f"<path d='M0 0H120M0 40H120M0 80H120M0 120H120M0 0V120M40 0V120M80 0V120M120 0V120' stroke='{c}' stroke-opacity='.16' stroke-width='1' fill='none'/><g stroke='{a}' stroke-opacity='.32' stroke-width='3' stroke-linecap='round' fill='none'><path d='M16 22h14M23 15v14'/><path d='M82 24h14'/><path d='M60 84h16M60 92h16'/><path d='M98 88l12 12M110 88l-12 12'/><path d='M20 90h10M20 100h10M25 86l-6 18' opacity='.0'/></g><path d='M10 70h22M14 70l-2 12M28 70l1 12' stroke='{a}' stroke-opacity='.32' stroke-width='3' stroke-linecap='round' fill='none'/>")('#9bb3d3' if d else '#1d4ed8','#6aa2ff' if d else '#1d4ed8'),
   _flat('#f6f9ff','#e7efff'),_flat('#0d1c31','#09131f')),
 "<rect x='10' y='6' width='44' height='52' rx='8' fill='#1d4ed8' stroke='#12264a' stroke-width='2.5'/><rect x='16' y='12' width='32' height='14' rx='3' fill='#dbeafe' stroke='#12264a' stroke-width='2'/><g fill='#fde68a' stroke='#12264a' stroke-width='1.6'><rect x='16' y='32' width='8' height='8' rx='2'/><rect x='28' y='32' width='8' height='8' rx='2'/><rect x='40' y='32' width='8' height='8' rx='2'/><rect x='16' y='44' width='8' height='8' rx='2'/><rect x='28' y='44' width='8' height='8' rx='2'/></g><rect x='40' y='44' width='8' height='8' rx='2' fill='#f87171' stroke='#12264a' stroke-width='1.6'/><path d='M22 19h6M25 16v6M34 19h8' stroke='#12264a' stroke-width='2' stroke-linecap='round'/>",
 "<path d='M12 3v18M3 12h18' stroke-width='0'/><path d='M10 3h4v7h7v4h-7v7h-4v-7H3v-4h7z'/>")

# 6 VEDIC MATHS ---------------------------------------------------------
add('vmaths','Vedic Maths',
 '#fff6e5 #fffdf7 #2d1b0e #7a5c3c #f1d9b0 #0f766e #c2410c #ffd27a #e2571f #0f766e #7c3aed #d98a00',
 '#1a1410 #271d16 #fdebd0 #cdb496 #46372a #3ccbb9 #ff9a5c #ebb94e #ff9a6a #4fd9c8 #b99cff #ffc35c',
 ('"Baloo 2","Nunito",system-ui,sans-serif','"Baloo 2","Nunito",system-ui,sans-serif'),
 ('16px','10px'),
 _bgfn(120,120,lambda d:(lambda c,a:f"<g fill='none' stroke='{c}' stroke-opacity='.28' stroke-width='1.6'><rect x='10' y='10' width='44' height='44'/><path d='M32 10v44M10 32h44M10 54L54 10M10 32L32 10M32 54L54 32'/></g><g fill='{a}' fill-opacity='.30' font-family='Arial,sans-serif' font-weight='700' font-size='15'><text x='72' y='36'>9</text><text x='92' y='96'>7</text><text x='20' y='104'>3</text><text x='70' y='84'>×</text></g>")('#cdb496' if d else '#0f766e','#ff9a5c' if d else '#c2410c'),
   _flat('#fff8ea','#ffeccb'),_flat('#1c1511','#130e0b')),
 "<rect x='6' y='6' width='52' height='52' rx='5' fill='#fffdf7' stroke='#0f766e' stroke-width='3'/><path d='M32 6v52M6 32h52M6 58L58 6M6 32L32 6M32 58L58 32' stroke='#0f766e' stroke-width='1.8' fill='none'/><g font-family='Arial,sans-serif' font-weight='800' font-size='13' fill='#c2410c'><text x='12' y='24'>9</text><text x='38' y='24'>7</text><text x='12' y='50'>6</text><text x='38' y='50'>4</text></g>",
 "<path d='M3 3h18v18H3z' fill='none' stroke-width='2.4'/><path d='M12 3v18M3 12h18M3 21L21 3' fill='none' stroke-width='2'/>")

# 7 GEOMETRY ------------------------------------------------------------
add('geometry','Geometry',
 '#f8f4ff #ffffff #261a4d #6b5f8f #ddd3f5 #6d28d9 #0e7490 #fde68a #e11d48 #0e7490 #6d28d9 #ea580c',
 '#14102a #1d173b #efe9ff #b1a6d6 #352c5c #a78bfa #5fd3ee #f2d46a #ff7a99 #5fd3ee #b79cff #ffa05c',
 ('"Josefin Sans","Nunito",system-ui,sans-serif','"Josefin Sans","Nunito",system-ui,sans-serif'),
 ('8px','5px'),
 _bgfn(140,140,lambda d:(lambda c,a:f"<g fill='none' stroke='{c}' stroke-opacity='.30' stroke-width='1.8'><path d='M12 52L50 52 31 18z'/><circle cx='100' cy='36' r='22'/><circle cx='100' cy='36' r='3' fill='{c}'/><path d='M100 36L122 36' /><rect x='24' y='92' width='34' height='34'/><path d='M24 92L58 126' stroke-dasharray='4 4'/><path d='M96 112a26 26 0 0 1 32 0' stroke='{a}' stroke-opacity='.4'/></g>")('#b1a6d6' if d else '#6d28d9','#5fd3ee' if d else '#0e7490'),
   _flat('#faf6ff','#ede5ff'),_flat('#15112b','#0e0b1d')),
 "<path d='M6 56L30 8l24 48z' fill='#a78bfa' fill-opacity='.35' stroke='#4c1d95' stroke-width='3' stroke-linejoin='round'/><circle cx='30' cy='36' r='11' fill='none' stroke='#0e7490' stroke-width='3'/><path d='M30 8l-10 26M30 8l10 26' stroke='#4c1d95' stroke-width='2.5' stroke-linecap='round'/><circle cx='30' cy='8' r='3.5' fill='#fbbf24' stroke='#4c1d95' stroke-width='2'/><path d='M44 20a22 22 0 0 1 12 14' fill='none' stroke='#e11d48' stroke-width='2.5' stroke-linecap='round'/>",
 "<path d='M12 3L22 20H2z' fill='none' stroke-width='2.6' stroke-linejoin='round'/><circle cx='12' cy='14' r='3.2'/>")

# 8 SANSKRIT ------------------------------------------------------------
add('sanskrit','Sanskrit',
 '#f6efe0 #fffaf0 #2c1810 #78604a #e3d2b4 #9f1239 #b45309 #f0cf7a #9f1239 #b45309 #166534 #1e40af',
 '#1c1410 #2a1f18 #f6e8d2 #c5b199 #463629 #f2849f #f0b25a #e3b865 #f2849f #f0b25a #6fcf8f #8fb0ff',
 ('"Lora",Georgia,serif','"Lora",Georgia,serif'),
 ('8px','5px'),
 _bgfn(150,90,lambda d:(lambda c:f"<g stroke='{c}' stroke-opacity='.30' stroke-linecap='round' fill='none'><path d='M6 22H144' stroke-width='2.4'/><path d='M14 22v-10M30 22c0 12 10 14 16 6M46 22v14M60 22c-6 0-8 12 2 14M78 22v16M96 22c0 14 12 14 14 4M126 22v14' stroke-width='2.4'/><path d='M6 68H100' stroke-width='2.4'/><path d='M16 68c0 12 10 14 14 4M44 68v14M60 68c-4 12 8 14 12 4M84 68v14' stroke-width='2.4'/></g><circle cx='128' cy='72' r='4' fill='{c}' fill-opacity='.22'/>")('#e3b865' if d else '#9f1239'),
   _flat('#f8f1e3','#efe2c8'),_flat('#1e1612','#150f0c')),
 "<rect x='4' y='14' width='56' height='36' rx='5' fill='#f2d9a0' stroke='#7c2d12' stroke-width='2.5'/><circle cx='11' cy='32' r='2.5' fill='#7c2d12'/><circle cx='53' cy='32' r='2.5' fill='#7c2d12'/><path d='M4 32H60' stroke='#9f1239' stroke-width='1.5' stroke-dasharray='1 3' opacity='.0'/><path d='M18 24h28' stroke='#9f1239' stroke-width='3' stroke-linecap='round'/><path d='M22 24v-6M30 24c0 8 8 9 11 3M41 24v12M22 40c4-3 8-3 12 0' stroke='#9f1239' stroke-width='3' stroke-linecap='round' fill='none'/><path d='M32 50V58M24 56h16' stroke='#7c2d12' stroke-width='2.5' stroke-linecap='round'/>",
 "<path d='M3 5h18M7 5c0 7 5 8 8 3M15 5v12' fill='none' stroke-width='2.4' stroke-linecap='round'/><path d='M5 20h14' stroke-width='2.4' stroke-linecap='round'/>")

# 9 EXERCISE ------------------------------------------------------------
add('exercise','Exercise',
 '#fff2ea #ffffff #1c1917 #6b5f58 #f2d5c4 #ea580c #0f172a #fde047 #ea580c #16a34a #2563eb #dc2626',
 '#14110f #201b18 #f7efe8 #bcaea4 #3d3530 #ff8a3d #fbbf24 #ffe14d #ff8a3d #4ade80 #60a5fa #ff6b6b',
 ('"Barlow","Inter",system-ui,sans-serif','"Barlow Condensed","Barlow",system-ui,sans-serif'),
 ('8px','5px'),
 _bgfn(120,120,lambda d:(lambda c,a:f"<g fill='{c}' fill-opacity='.10'><path d='M0 20L20 0H40L0 60z'/><path d='M60 120L120 60V90L90 120z'/></g><g fill='{a}' fill-opacity='.28'><rect x='24' y='84' width='5' height='20' rx='1.5'/><rect x='30' y='88' width='24' height='4' rx='1'/><rect x='55' y='84' width='5' height='20' rx='1.5'/><rect x='19' y='88' width='4' height='12' rx='1.5'/><rect x='61' y='88' width='4' height='12' rx='1.5'/></g><path d='M84 24l8 6-8 6M96 24l8 6-8 6' fill='none' stroke='{a}' stroke-opacity='.30' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'/>")('#ff8a3d' if d else '#ea580c','#ffb347' if d else '#ea580c'),
   _flat('#fff5ee','#ffe3d1'),_flat('#171210','#0f0c0b')),
 "<g stroke='#1c1917' stroke-width='2.5' stroke-linejoin='round'><rect x='4' y='20' width='8' height='24' rx='2' fill='#dc2626'/><rect x='12' y='24' width='6' height='16' rx='1.5' fill='#f87171'/><rect x='18' y='29' width='28' height='6' rx='2' fill='#9ca3af'/><rect x='46' y='24' width='6' height='16' rx='1.5' fill='#f87171'/><rect x='52' y='20' width='8' height='24' rx='2' fill='#dc2626'/></g><path d='M24 12l-4-6M32 10V3M40 12l4-6' stroke='#ea580c' stroke-width='3' stroke-linecap='round'/>",
 "<rect x='1' y='8' width='3.5' height='8' rx='1'/><rect x='4.5' y='6' width='3' height='12' rx='1'/><rect x='7.5' y='10.5' width='9' height='3' rx='1'/><rect x='16.5' y='6' width='3' height='12' rx='1'/><rect x='19.5' y='8' width='3.5' height='8' rx='1'/>")

# 10 FOOD ---------------------------------------------------------------
add('food','Food',
 '#fff4ee #fffdfb #3a1d1a #7f5a54 #f3d3c8 #dc2626 #ea580c #fde68a #dc2626 #16a34a #ea580c #ca8a04',
 '#1d1311 #2a1c19 #fbece6 #cfb0a8 #4a3029 #ff7a6b #ffb347 #f2cf66 #ff7a6b #5fd67f #ffa05c #f0c04a',
 ('"Nunito","Quicksand",system-ui,sans-serif','"Fredoka","Nunito",system-ui,sans-serif'),
 ('18px','12px'),
 _bgfn(72,72,lambda d:(lambda r,w:f"<rect width='72' height='72' fill='{w}'/><rect width='36' height='72' fill='{r}' fill-opacity='.14'/><rect width='72' height='36' fill='{r}' fill-opacity='.14'/>")('#ff7a6b' if d else '#dc2626','#2a1c19' if d else '#fff7f2'),
   _flat('#fff7f2','#fff7f2'),_flat('#241713','#241713')),
 "<path d='M6 28h52c0 16-10 28-26 28S6 44 6 28z' fill='#f97316' stroke='#7c2d12' stroke-width='2.5' stroke-linejoin='round'/><path d='M12 28c4-10 14-12 20-8 6-4 16-2 20 8' fill='#16a34a' stroke='#14532d' stroke-width='2.5' stroke-linejoin='round'/><circle cx='24' cy='26' r='4' fill='#dc2626'/><circle cx='38' cy='24' r='3.4' fill='#fde68a'/><path d='M22 16c-3-4 3-6 0-10M32 14c-3-4 3-6 0-10M42 16c-3-4 3-6 0-10' fill='none' stroke='#9ca3af' stroke-width='2.4' stroke-linecap='round'/>",
 "<path d='M12 7c3-4 9-3 9 3 0 6-4 11-9 11S3 16 3 10c0-6 6-7 9-3z'/><path d='M12 7c0-2 1-4 4-5' fill='none' stroke-width='2' stroke-linecap='round'/>")

# 11 YOGA ---------------------------------------------------------------
add('yoga','Yoga',
 '#f4f1fb #fdfcff #2a2340 #6a6285 #ddd6f0 #7c6bc4 #d97da8 #f4e0a0 #d97da8 #6fb5a4 #7c6bc4 #e0a458',
 '#171424 #211c33 #eeeaf9 #b0a8cc #3a3354 #a899ee #f0a0c6 #e8d08a #f0a0c6 #86d3c0 #a899ee #f0be76',
 ('"Cormorant Garamond","Nunito",Georgia,serif','"Nunito",system-ui,sans-serif'),
 ('26px','18px'),
 _bgfn(160,160,lambda d:(lambda a,b:f"<g fill='{a}' fill-opacity='.10'><circle cx='36' cy='40' r='30'/><circle cx='120' cy='110' r='36'/></g><g fill='{b}' fill-opacity='.12'>{_petals(120,40,5,6,14,14,b,.0)}</g><path d='M110 40c0-10 6-14 10-18 4 4 10 8 10 18-4 6-16 6-20 0z' fill='{b}' fill-opacity='.20'/><path d='M30 130c4-8 10-10 14-10s10 2 14 10' fill='none' stroke='{a}' stroke-opacity='.3' stroke-width='3' stroke-linecap='round'/>")('#a899ee' if d else '#7c6bc4','#f0a0c6' if d else '#d97da8'),
   _flat('#f6f2fd','#e9f3f0'),_flat('#191528','#101a1a')),
 "<circle cx='32' cy='14' r='7' fill='#f2c4a0' stroke='#4c3a7a' stroke-width='2.5'/><path d='M32 22c-8 0-12 6-12 14v4h24v-4c0-8-4-14-12-14z' fill='#7c6bc4' stroke='#4c3a7a' stroke-width='2.5' stroke-linejoin='round'/><path d='M18 30c-6 6-10 14-8 18M46 30c6 6 10 14 8 18' fill='none' stroke='#4c3a7a' stroke-width='3.5' stroke-linecap='round'/><path d='M8 52c8 6 40 6 48 0-4 6-12 8-24 8S12 58 8 52z' fill='#d97da8' stroke='#4c3a7a' stroke-width='2.5' stroke-linejoin='round'/>",
 "<circle cx='12' cy='5' r='2.8'/><path d='M12 9c-3 0-5 3-5 6v1h10v-1c0-3-2-6-5-6zM3 20c5 3 13 3 18 0-2 3-6 4-9 4s-7-1-9-4z'/>")

# 12 MEDITATION ---------------------------------------------------------
add('meditation','Meditation',
 '#eef6f6 #fbfeff #17323a #547078 #cfe3e6 #0e7490 #6d5fc4 #f0e1a0 #5b9fb0 #7aa89a #8a7fd0 #c9a45a',
 '#0b1618 #12242a #e3f2f4 #9bb8bd #223c43 #5cc8e0 #a89cf0 #e6d490 #7cc4d6 #8cd0bc #a89cf0 #dcb86a',
 ('"Quicksand","Nunito",system-ui,sans-serif','"Quicksand","Nunito",system-ui,sans-serif'),
 ('28px','18px'),
 _bgfn(180,180,lambda d:(lambda c:f"<g fill='none' stroke='{c}' stroke-opacity='.22' stroke-width='1.6'><circle cx='90' cy='90' r='14'/><circle cx='90' cy='90' r='30'/><circle cx='90' cy='90' r='48'/><circle cx='90' cy='90' r='68'/><circle cx='90' cy='90' r='88'/></g>")('#9bb8bd' if d else '#0e7490'),
   _flat('#f1f8f8','#e3eef6'),_flat('#0d1a1d','#0a1215')),
 "<ellipse cx='32' cy='54' rx='22' ry='5' fill='none' stroke='#5b9fb0' stroke-width='2.5'/><ellipse cx='32' cy='54' rx='30' ry='7' fill='none' stroke='#5b9fb0' stroke-width='1.8' opacity='.6'/><ellipse cx='32' cy='46' rx='17' ry='7' fill='#94a3b8' stroke='#334155' stroke-width='2.5'/><ellipse cx='32' cy='33' rx='12' ry='6' fill='#a8b5c4' stroke='#334155' stroke-width='2.5'/><ellipse cx='32' cy='22' rx='8' ry='5' fill='#c0cad6' stroke='#334155' stroke-width='2.5'/><circle cx='32' cy='11' r='3.2' fill='#fbbf24' stroke='#334155' stroke-width='1.8'/>",
 "<ellipse cx='12' cy='19' rx='8' ry='3.4'/><ellipse cx='12' cy='12.5' rx='5.5' ry='3'/><ellipse cx='12' cy='7' rx='3.2' ry='2.4'/>")

# 13 HEALTHY BRAIN ------------------------------------------------------
add('brain','Healthy Brain',
 '#fff1f5 #fffdfe #3a1a30 #7c5870 #f4d3df #db2777 #0d9488 #fde68a #db2777 #0d9488 #7c3aed #ea8a00',
 '#1b0f19 #281623 #fbe8f1 #d0aec0 #47293c #ff7ab8 #4fd9c8 #f2d46a #ff7ab8 #4fd9c8 #b79cff #ffb84d',
 ('"Nunito","Quicksand",system-ui,sans-serif','"Nunito",system-ui,sans-serif'),
 ('22px','14px'),
 _bgfn(150,150,lambda d:(lambda a,b:f"<g stroke='{a}' stroke-opacity='.28' stroke-width='1.8' fill='none'><path d='M20 30L64 52 110 24M64 52L56 110 120 120M56 110L18 128M110 24L128 70 120 120'/></g><g fill='{a}' fill-opacity='.5'><circle cx='20' cy='30' r='5'/><circle cx='64' cy='52' r='6'/><circle cx='110' cy='24' r='4.5'/><circle cx='56' cy='110' r='5'/><circle cx='120' cy='120' r='6'/><circle cx='18' cy='128' r='3.5'/><circle cx='128' cy='70' r='4'/></g><circle cx='64' cy='52' r='11' fill='none' stroke='{b}' stroke-opacity='.4' stroke-width='2'/>")('#ff7ab8' if d else '#db2777','#4fd9c8' if d else '#0d9488'),
   _flat('#fff4f8','#ffe6ef'),_flat('#1d1019','#130a12')),
 "<path d='M32 8c-6-4-16-1-17 8-6 2-9 9-5 15-3 6 0 13 7 15 3 7 12 9 15 3 3 6 12 4 15-3 7-2 10-9 7-15 4-6 1-13-5-15-1-9-11-12-17-8z' fill='#f9a8c9' stroke='#831843' stroke-width='2.5' stroke-linejoin='round'/><path d='M32 10v44' stroke='#831843' stroke-width='2.2' stroke-linecap='round'/><path d='M20 24c4 0 7 3 9 6M44 24c-4 0-7 3-9 6M20 40c4 0 7-2 9-5M44 40c-4 0-7-2-9-5' fill='none' stroke='#831843' stroke-width='2.2' stroke-linecap='round'/><path d='M46 6l1.6 4 4 1.6-4 1.6L46 17l-1.6-3.8-4-1.6 4-1.6z' fill='#fbbf24'/>",
 "<path d='M12 3C8 1 4 4 4.5 8 2 9 2 13 4 14.5 3.5 18 7 20 9.5 18.5c1 2 3.5 2 4.5 0 2.5 1.500 6-.5 5.500-4 2-1.500 2-5.500-.5-6.500C19.500 4 15.500 1 12 3z'/>")

# 14 SOCIAL -------------------------------------------------------------
add('social','Talk to People',
 '#fff7e8 #fffefa #2a2438 #6c6580 #f2e1bf #ea580c #7c3aed #fde68a #ea580c #0891b2 #7c3aed #16a34a',
 '#181522 #231f31 #f3effb #b9b2cf #3b3550 #ff9a5c #b79cff #f2d46a #ff9a5c #4fc9e0 #b79cff #5fd67f',
 ('"Poppins","Nunito",system-ui,sans-serif','"Poppins","Nunito",system-ui,sans-serif'),
 ('22px','14px'),
 _bgfn(150,130,lambda d:(lambda a,b,c:f"<g fill='{a}' fill-opacity='.20'><rect x='14' y='16' width='50' height='30' rx='12'/><path d='M26 44l-4 12 14-12z'/></g><g fill='{b}' fill-opacity='.20'><rect x='84' y='62' width='52' height='32' rx='12'/><path d='M122 92l6 12-16-12z'/></g><g fill='{c}' fill-opacity='.35'><circle cx='28' cy='31' r='2.6'/><circle cx='39' cy='31' r='2.6'/><circle cx='50' cy='31' r='2.6'/><circle cx='100' cy='78' r='2.6'/><circle cx='111' cy='78' r='2.6'/><circle cx='122' cy='78' r='2.6'/></g>")('#ff9a5c' if d else '#ea580c','#b79cff' if d else '#7c3aed','#ffffff' if d else '#2a2438'),
   _flat('#fff9ec','#fdeed2'),_flat('#1a1724','#120f1b')),
 "<rect x='4' y='6' width='36' height='24' rx='10' fill='#ea580c' stroke='#431407' stroke-width='2.5'/><path d='M12 29l-3 11 12-9z' fill='#ea580c' stroke='#431407' stroke-width='2.5' stroke-linejoin='round'/><rect x='24' y='28' width='36' height='24' rx='10' fill='#a78bfa' stroke='#2e1065' stroke-width='2.5'/><path d='M50 51l4 9-12-8z' fill='#a78bfa' stroke='#2e1065' stroke-width='2.5' stroke-linejoin='round'/><g fill='#fff'><circle cx='14' cy='18' r='2.4'/><circle cx='22' cy='18' r='2.4'/><circle cx='30' cy='18' r='2.4'/></g>",
 "<path d='M4 4h16a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-8l-5 4v-4H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z'/>")

# 15 MUSIC --------------------------------------------------------------
add('music','Music',
 '#f6f0ff #ffffff #1f1633 #655a80 #ddd0f2 #7e22ce #db2777 #fde68a #db2777 #0891b2 #7e22ce #ea8a00',
 '#120c1d #1c1430 #f1eafc #b6aad2 #34274f #c084fc #ff7ab8 #f2d46a #ff7ab8 #4fc9e0 #c084fc #ffb84d',
 ('"Playfair Display",Georgia,serif','"Playfair Display",Georgia,serif'),
 ('14px','10px'),
 _bgfn(160,120,lambda d:(lambda c,a:f"<g stroke='{c}' stroke-opacity='.26' stroke-width='1.4'><path d='M0 30H160M0 38H160M0 46H160M0 54H160M0 62H160' fill='none'/></g><g fill='{a}' fill-opacity='.45'><ellipse cx='36' cy='54' rx='6' ry='4.4' transform='rotate(-20 36 54)'/><ellipse cx='70' cy='38' rx='6' ry='4.4' transform='rotate(-20 70 38)'/><ellipse cx='108' cy='46' rx='6' ry='4.4' transform='rotate(-20 108 46)'/></g><g stroke='{a}' stroke-opacity='.45' stroke-width='2'><path d='M41 52V26M75 36V10M113 44V18'/></g><g fill='{a}' fill-opacity='.30'><ellipse cx='40' cy='104' rx='7' ry='5' transform='rotate(-20 40 104)'/></g><path d='M46 102V78l14 4' stroke='{a}' stroke-opacity='.30' stroke-width='2.4' fill='none'/>")('#b6aad2' if d else '#7e22ce','#c084fc' if d else '#7e22ce'),
   _flat('#f8f3ff','#ece2fb'),_flat('#150e22','#0e0917')),
 "<g stroke='#7e22ce' stroke-width='2.5' stroke-linejoin='round' stroke-linecap='round'><ellipse cx='18' cy='48' rx='9' ry='7' fill='#db2777' transform='rotate(-20 18 48)'/><ellipse cx='44' cy='42' rx='9' ry='7' fill='#7e22ce' transform='rotate(-20 44 42)'/><path d='M25 46V14l26-6v32' fill='none'/><path d='M25 14l26-6v9l-26 6z' fill='#fbbf24'/></g>",
 "<path d='M9 17V5l11-2v12' fill='none' stroke-width='2.2' stroke-linejoin='round'/><ellipse cx='6.500' cy='17.500' rx='3.200' ry='2.500'/><ellipse cx='17.500' cy='15.500' rx='3.200' ry='2.500'/>")

# 16 ART ----------------------------------------------------------------
add('art','Art',
 '#fffaf2 #ffffff #231c2e #70657f #eadff0 #e11d48 #2563eb #fde047 #e11d48 #16a34a #2563eb #f59e0b',
 '#171320 #221c2f #f6f0fb #bcb2cc #3a3150 #ff6b8a #6ea0ff #ffe14d #ff6b8a #4ade80 #6ea0ff #ffb84d',
 ('"Nunito",system-ui,sans-serif','"Permanent Marker","Caveat",cursive'),
 ('20px','12px'),
 _bgfn(200,200,lambda d:(lambda o:f"<g fill-opacity='{.28 if d else .26}'><circle cx='36' cy='40' r='18' fill='#e11d48'/><circle cx='64' cy='28' r='7' fill='#e11d48'/><circle cx='150' cy='62' r='22' fill='#2563eb'/><circle cx='122' cy='84' r='6' fill='#2563eb'/><circle cx='60' cy='140' r='20' fill='#f59e0b'/><circle cx='96' cy='160' r='8' fill='#f59e0b'/><circle cx='160' cy='158' r='16' fill='#16a34a'/><circle cx='176' cy='128' r='5' fill='#16a34a'/><circle cx='20' cy='178' r='6' fill='#7c3aed'/></g>")(0),
   _flat('#fffaf2','#fff0e0'),_flat('#181421','#100c18')),
 "<path d='M32 6C14 6 4 18 4 31c0 14 12 25 26 25 5 0 6-4 3-7-3-4 0-8 5-8h8c8 0 14-5 14-12C60 16 48 6 32 6z' fill='#f5deb3' stroke='#4a2f1b' stroke-width='2.5' stroke-linejoin='round'/><circle cx='18' cy='26' r='5' fill='#e11d48' stroke='#4a2f1b' stroke-width='1.8'/><circle cx='30' cy='17' r='5' fill='#fde047' stroke='#4a2f1b' stroke-width='1.8'/><circle cx='44' cy='20' r='5' fill='#2563eb' stroke='#4a2f1b' stroke-width='1.8'/><circle cx='47' cy='34' r='4.6' fill='#16a34a' stroke='#4a2f1b' stroke-width='1.8'/><circle cx='20' cy='41' r='4.6' fill='#fff' stroke='#4a2f1b' stroke-width='1.8'/>",
 "<path d='M12 2C7 2 2 6 2 12c0 5 4 9 9 9 2 0 2-1.500 1-2.500-1-1.500 0-3 2-3h3c3 0 5-2 5-5 0-4-4-8-10-8z'/>")

# ---- register into the main tables
for k,v in NEW.items():
    P[k]=v['pal']; FONTS[k]=v['font']
    SHAPE[k]=dict(r=v['r'][0],rsm=v['r'][1],bw='1px',bw2='2px')
    MASC[k]=mas(v['mascot']); BG[k]=v['bg']; START[k]=v['start']
    EXTRA[k]=(f"[data-theme={k}] h1{{background:none;color:var(--acc);-webkit-text-fill-color:currentColor;font-family:var(--serif);font-weight:700}}\n"
              f"[data-theme={k}] .chtitle,[data-theme={k}] .verdict,[data-theme={k}] .panel h2{{font-family:var(--serif)}}\n"+v['h1'])
