#!/usr/bin/env python3
"""Zzebi.St 위클리 빌더 (v3 · 2026-10-29)

데이터(JSON) → 리포트 HTML(한국어·영어·중국어 전환) → 암호화된 비밀 링크 페이지.

사용법
  python3 tools/build_report.py strings  DATA_DIR            # 번역할 한국어 문구 목록 → DATA_DIR/strings.json
  python3 tools/build_report.py render   DATA_DIR OUT.html   # 평문 리포트(검수·미리보기용, 커밋 금지)
  python3 tools/build_report.py seal     PLAIN.html OUT.html KEY   # 암호화 래퍼 페이지(공개 저장소에 올려도 안전)
  python3 tools/build_report.py pack     DATA_DIR OUT.enc KEY      # 데이터 폴더를 암호화해 저장(수·금 점검용)
  python3 tools/build_report.py unpack   IN.enc DATA_DIR KEY
  python3 tools/build_report.py newkey                         # 새 키(base64url 32바이트)와 새 slug 출력

DATA_DIR 구성: meta.json, look_<id>.json, market.json, img/<id>.jpg, i18n.json({"한국어 문구":{"en":..,"zh":..}})
링크 형식: https://gkawhdz.github.io/zzebi-weekly/r/<slug>/#k=<KEY>  (키는 # 뒤라 서버·저장소에 남지 않음)
"""
import sys, os, json, re, html, base64, io, glob, secrets, tarfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HANGUL = re.compile(r'[가-힣]')
esc = lambda s: html.escape(str(s), quote=True)

# ---------------------------------------------------------------- 번역 등록
class Tr:
    def __init__(self, i18n=None):
        self.keys, self.idx, self.i18n = [], {}, i18n or {}
    def id(self, s):
        if s not in self.idx:
            self.idx[s] = len(self.keys); self.keys.append(s)
        return self.idx[s]
    def __call__(self, s, tag='span', cls=None):
        """한글이 있으면 번역 가능한 span으로 감싸기"""
        s = '' if s is None else str(s)
        c = f' class="{cls}"' if cls else ''
        if not HANGUL.search(s):
            return f'<{tag}{c}>{esc(s)}</{tag}>' if cls or tag != 'span' else esc(s)
        return f'<{tag}{c} data-i="{self.id(s)}">{esc(s)}</{tag}>'
    def attr(self, s):
        """alt 같은 속성용: data-ia 인덱스"""
        s = str(s or '')
        return f'alt="{esc(s)}"' + (f' data-ia="{self.id(s)}"' if HANGUL.search(s) else '')
    def table(self):
        out = {'en': [], 'zh': []}
        for k in self.keys:
            t = self.i18n.get(k, {})
            out['en'].append(t.get('en') or None)
            out['zh'].append(t.get('zh') or None)
        return out

# ---------------------------------------------------------------- 가격 표기
def won_ko(w, approx=False, frm=False):
    if approx and w >= 10000:
        man = w / 10000
        s = f'약 {man:,.0f}만원' if man >= 100 else f'약 {man:,.1f}만원'.replace('.0만', '만')
    else:
        s = f'{w:,}원'
    return s + ('~' if frm else '')

def price(p, T):
    w = int(p.get('won') or 0)
    off = int(p.get('off') or 0)
    ap, fr = bool(p.get('approx')), bool(p.get('from'))
    o = f'<span class="off">{off}%</span>' if off else ''
    return (f'<span class="pr">{o}<span class="won" data-won="{w}" data-ap="{int(ap)}" data-fr="{int(fr)}">'
            f'{esc(won_ko(w, ap, fr))}</span></span>')

def brand_name(p, T, br_cls='br', br_break=True):
    b = p.get('brand') or ''
    n = p.get('name') or ''
    bh = f'<span class="{br_cls}">{T(b)}</span>' if b else ''
    return f'<span class="nm">{bh}{"<br>" if (b and br_break) else (" " if b else "")}{T(n)}</span>'

A = lambda url: f'href="{esc(url)}" target="_blank" rel="noopener"'

# ---------------------------------------------------------------- 이미지
def data_uri(path, width=820, q=82):
    from PIL import Image
    im = Image.open(path).convert('RGB')
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'JPEG', quality=q, optimize=True, progressive=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()

# ---------------------------------------------------------------- 섹션
TIER_TAG = {'lux': '명품', 'mid': '중가', 'value': '가성비'}

def render_look(L, n, T, data_dir, eager):
    img = os.path.join(data_dir, 'img', L['img'])
    src = data_uri(img) if os.path.exists(img) else ''
    h = [f'  <section class="look" id="look-{esc(L["id"])}" aria-labelledby="h-{esc(L["id"])}">',
         '    <div class="look-head">',
         '      <figure class="look-photo">',
         f'        <img src="{src}" {T.attr(L.get("alt",""))} loading="{"eager" if eager else "lazy"}">',
         '        <figcaption>',
         f'          <span class="look-no">{T("해부")} #{esc(L["ep"])} · {T(L.get("city",""))}</span>',
         f'          <h2 id="h-{esc(L["id"])}">{T(L["title"])}</h2>',
         f'          <span class="who">{T(L.get("who",""))}</span>',
         '        </figcaption>',
         f'        <span class="ai-mark">{T("AI 재현 이미지")}</span>',
         '      </figure>',
         '      <div class="look-meta">',
         f'        <p class="point">{T(L.get("point",""))}</p>']
    if L.get('real'):
        h.append(f'        <p class="real"><b>{T("실착 포인트")}</b> {T(L["real"])}</p>')
    h += ['      </div>', '    </div>']
    marks = ['①', '②', '③']
    cores = L.get('cores', [])
    for i, c in enumerate(cores):
        mk = marks[i] if len(cores) > 1 else '·'
        h.append(f'    <h3>{T("핵심 아이템")} {mk} {T(c["h"])}</h3>')
        h.append('    <div class="tiers">')
        for k in ('lux', 'mid', 'value'):
            p = c['tiers'].get(k)
            if not p: continue
            shop = ' · '.join(x for x in [p.get('shop'), p.get('note')] if x)
            h.append(f'      <a class="tier{" lux" if k=="lux" else ""}" {A(p["url"])}>')
            h.append(f'        <span class="tag">{T(TIER_TAG[k])}</span>{brand_name(p, T)}')
            if shop: h.append(f'        <span class="shop">{T(shop)}</span>')
            h.append(f'        {price(p, T)}' + (f'<span class="ovs">{T(p["ovs"])}</span>' if p.get('ovs') else '') + '</a>')
        h.append('    </div>')
    if L.get('with'):
        h.append('    <div class="with">')
        for w in L['with']:
            p = w['p']
            h.append(f'      <a class="item" {A(p["url"])}>')
            h.append(f'        <span class="role">{T(w.get("role",""))}</span>')
            h.append(f'        {brand_name(p, T, br_break=False)}')
            h.append(f'        {price(p, T)}</a>')
        h.append('    </div>')
    h.append('  </section>')
    return '\n'.join(h)

def render_list(items, T, cls='rk'):
    out = [f'      <ol class="{cls}-list">' if cls == 'rk' else '      <ol class="hot-list">']
    for i, p in enumerate(items, 1):
        it, no = ('rk-item', 'rk-no') if cls == 'rk' else ('hot-item', 'hot-rank')
        w = p.get('where') or ''
        num = i
        if cls == 'rk':   # 랭킹은 사이트의 실제 순위를 번호로 (예: '무신사 · 여성 랭킹 2위' → 2)
            m = re.search(r'(\d+)위', w)
            if m:
                num = int(m.group(1)); w = re.sub(r'\s*·?\s*[^·]*\d+위', '', w).strip(' ·')
        where = f'<span class="hot-where">{T(w)}</span>' if w else ''
        b = f'<span class="br">{T(p.get("brand",""))}</span>' if p.get('brand') else ''
        out.append(f'        <li><a class="{it}" {A(p["url"])}>'
                   f'<span class="{no}">{num}</span>'
                   f'<span class="hot-body">{where}<span class="nm">{b}{T(p.get("name",""))}</span></span>'
                   f'{price(p, T)}</a></li>')
    out.append('      </ol>')
    return '\n'.join(out)

LANG_UI = '''<div class="lang" role="group" aria-label="Language">
        <button type="button" data-lang="ko" aria-pressed="true">한국어</button><button type="button" data-lang="en" aria-pressed="false">EN</button><button type="button" data-lang="zh" aria-pressed="false">中文</button>
      </div>'''

LOGO = '''<svg class="logo-mark" viewBox="20 0 580 360" aria-hidden="true"><path d="M310 150 L40 300 c-22 12-14 40 10 40 h520 c24 0 32-28 10-40 L310 150" fill="none" stroke="currentColor" stroke-width="22" stroke-linecap="round" stroke-linejoin="round"/><path d="M310 70 c0-34 26-50 46-50 s44 18 44 44 c0 30-26 38-44 52 L310 150" fill="none" stroke="currentColor" stroke-width="22" stroke-linecap="round" stroke-linejoin="round"/><path d="M310 150 Q296 186 306 214" fill="none" stroke="currentColor" stroke-width="7"/><g transform="rotate(-10 310 262)"><path d="M246 214 h104 l36 34 v70 h-176 v-70 Z" fill="#00A8A8"/><circle cx="310" cy="240" r="11" fill="var(--bg)"/></g></svg>'''

EXTRA_CSS = '''
/* v3.0 · 언어 전환 + 점검 배지 (2026-10-29) */
.brandbar-r{display:flex;align-items:center;gap:10px;flex-wrap:wrap;justify-content:flex-end}
.lang{display:inline-flex;border:1px solid var(--line);border-radius:999px;background:var(--surface);padding:2px}
.lang button{font:inherit;font-size:12.5px;font-weight:700;border:0;background:transparent;color:var(--muted);padding:5px 10px;border-radius:999px;cursor:pointer;min-height:32px}
.lang button[aria-pressed="true"]{background:var(--brand-strong);color:var(--on-brand)}
.lang button:focus-visible{outline:2px solid var(--brand);outline-offset:1px}
.fresh{display:flex;align-items:flex-start;gap:10px;margin:4px 0 0;padding:11px 14px;border-radius:12px;background:var(--surface);border:1px solid var(--line);font-size:13.5px;line-height:1.5;color:var(--muted)}
.fresh::before{content:"";flex:0 0 auto;width:9px;height:9px;margin-top:6px;border-radius:50%;background:var(--brand);box-shadow:0 0 0 4px var(--brand-soft)}
.fresh b{color:var(--ink);font-weight:700}
html[lang="zh-CN"] body{word-break:normal;line-break:strict;font-family:"PingFang SC","Noto Sans SC","Microsoft YaHei",var(--body)}
@media (max-width:460px){.brandbar{flex-wrap:wrap}.adtag{display:none}}
.tabs{position:sticky}.tabs::after{content:"";position:absolute;top:0;right:0;bottom:1px;width:36px;pointer-events:none;background:linear-gradient(to right,transparent,var(--bg))}
.tabs.end::after{opacity:0}
'''

JS = r'''
(function(){
  var d=document.documentElement; d.classList.add('js');
  function hp(){var o={};(location.hash||'').replace(/^#/,'').split('&').forEach(function(kv){var i=kv.indexOf('=');if(i>0)o[kv.slice(0,i)]=decodeURIComponent(kv.slice(i+1));else if(kv)o.t=kv;});return o}
  function setHash(o){var s=[];['k','t','l'].forEach(function(k){if(o[k])s.push(k+'='+encodeURIComponent(o[k]))});try{history.replaceState(null,'','#'+s.join('&'))}catch(_){}}
  /* 탭 */
  var tabs=[].slice.call(document.querySelectorAll('.tabs a'));
  var ids=tabs.map(function(a){return a.getAttribute('data-tab')});
  function show(id,scroll){
    if(ids.indexOf(id)<0) id='women';
    tabs.forEach(function(a){a.setAttribute('aria-selected', a.getAttribute('data-tab')===id?'true':'false')});
    ids.forEach(function(x){var p=document.getElementById(x); if(p) p.classList.toggle('on', x===id)});
    if(scroll){var a=document.getElementById('tabs-top'); var y=a.getBoundingClientRect().top+(window.pageYOffset||d.scrollTop); window.scrollTo(0,Math.max(0,y));}
  }
  tabs.forEach(function(a){a.addEventListener('click',function(e){e.preventDefault(); var id=a.getAttribute('data-tab'); var o=hp(); o.t=id; setHash(o); show(id,true)})});
  [].forEach.call(document.querySelectorAll('a[data-go]'),function(a){a.addEventListener('click',function(e){e.preventDefault();var o=hp();o.t=a.getAttribute('data-go');setHash(o);show(o.t,true)})});
  /* 언어 */
  var I=window.__I18N||{en:[],zh:[]};
  var nodes=[].slice.call(document.querySelectorAll('[data-i]')).map(function(e){return [e,e.textContent]});
  var alts=[].slice.call(document.querySelectorAll('[data-ia]')).map(function(e){return [e,e.getAttribute('alt')]});
  var wons=[].slice.call(document.querySelectorAll('.won[data-won]'));
  var UI={ko:{tabs:null},en:{},zh:{}};
  function fmt(w,ap,fr,l){
    var s;
    if(l==='en'){ s=ap? '≈ ₩'+(w>=1e6?(w/1e6).toFixed(w>=1e7?1:2).replace(/\.?0+$/,'')+'M':Math.round(w/1e3)+'K') : '₩'+w.toLocaleString('en-US'); }
    else if(l==='zh'){ s=ap? '约'+(w/1e4>=100?Math.round(w/1e4):(Math.round(w/1e3)/10))+'万韩元' : w.toLocaleString('en-US')+'韩元'; }
    else { s=ap? '약 '+(w/1e4>=100?Math.round(w/1e4).toLocaleString('ko-KR'):(Math.round(w/1e3)/10))+'만원' : w.toLocaleString('ko-KR')+'원'; }
    return s+(fr?'~':'');
  }
  function lang(l){
    if(['ko','en','zh'].indexOf(l)<0) l='ko';
    d.setAttribute('lang', l==='zh'?'zh-CN':l);
    nodes.forEach(function(p){var i=+p[0].getAttribute('data-i'); var t=(l!=='ko'&&I[l]&&I[l][i])||p[1]; if(p[0].textContent!==t) p[0].textContent=t;});
    alts.forEach(function(p){var i=+p[0].getAttribute('data-ia'); p[0].setAttribute('alt',(l!=='ko'&&I[l]&&I[l][i])||p[1]);});
    wons.forEach(function(e){e.textContent=fmt(+e.getAttribute('data-won'),e.getAttribute('data-ap')==='1',e.getAttribute('data-fr')==='1',l)});
    [].forEach.call(document.querySelectorAll('.lang button'),function(b){b.setAttribute('aria-pressed',b.getAttribute('data-lang')===l?'true':'false')});
    try{localStorage.setItem('zz_lang',l)}catch(_){}
  }
  [].forEach.call(document.querySelectorAll('.lang button'),function(b){b.addEventListener('click',function(){var l=b.getAttribute('data-lang');lang(l);var o=hp();o.l=l==='ko'?'':l;setHash(o)})});
  var o=hp(), saved=null; try{saved=localStorage.getItem('zz_lang')}catch(_){}
  lang(o.l||saved||'ko');
  var ti=document.querySelector('.tabs-in'),tb=document.querySelector('.tabs');function ed(){if(ti&&tb)tb.classList.toggle('end',ti.scrollLeft+ti.clientWidth>=ti.scrollWidth-4)}if(ti){ti.addEventListener('scroll',ed,{passive:true});ed()}
  show(o.t||'',false);
  window.addEventListener('hashchange',function(){var o=hp();show(o.t||'',true)});
})();
'''

def render(data_dir, i18n_path=None):
    meta = json.load(open(os.path.join(data_dir, 'meta.json')))
    mk = json.load(open(os.path.join(data_dir, 'market.json')))
    i18n = {}
    ip = i18n_path or os.path.join(data_dir, 'i18n.json')
    if os.path.exists(ip): i18n = json.load(open(ip))
    T = Tr(i18n)
    looks = {os.path.basename(f)[5:-5]: json.load(open(f)) for f in glob.glob(os.path.join(data_dir, 'look_*.json'))}
    css = open(os.path.join(ROOT, 'tools', 'report_style.css')).read() + EXTRA_CSS
    W = [looks[i] for i in meta['women'] if i in looks]
    M = [looks[i] for i in meta['men'] if i in looks]

    b = []
    b.append('<div class="wrap">\n  <header>\n    <div class="brandbar">')
    b.append(f'      <a class="brand" href="https://www.instagram.com/zzebi.st/" target="_blank" rel="noopener" aria-label="Instagram @zzebi.st">{LOGO}<span class="wordmark">zzebi<em>.st</em></span></a>')
    b.append(f'      <div class="brandbar-r"><span class="adtag">{T("구독자 전용")}</span>{LANG_UI}</div>')
    b.append('    </div>')
    b.append(f'    <p class="masthead">WEEKLY <span>·</span> {T(meta["week"])} · {T(meta["issued"])}</p>')
    b.append(f'    <h1>{T(meta.get("h1a","이번 주 셀럽 스냅,"))}<br>{T(meta.get("h1b","지금 사는 법"))}</h1>')
    b.append(f'    <p class="lead">{T(meta.get("lead","여성·남성 셀럽 스냅을 명품부터 가성비까지 사는 법, 무신사·29CM·지그재그·크림의 이번 주 랭킹과 핫딜, 인기 신발을 메뉴별로 정리했어요."))}</p>')
    b.append(f'    <p class="fresh"><span><b>{T("가격·링크 점검")}</b> {T(meta["checked"])} · {T(meta["next"])}</span></p>')
    b.append('  </header>\n  <div id="tabs-top" aria-hidden="true"></div>')
    b.append('  <nav class="tabs" aria-label="menu">\n    <div class="tabs-in" role="tablist">')
    for tid, lab in [('women', '여성'), ('men', '남성'), ('ranking', '이번 주 랭킹'), ('deals', '핫딜'), ('kream', '크림 신발')]:
        b.append(f'      <a href="#t={tid}" role="tab" data-tab="{tid}">{T(lab)}</a>')
    b.append('    </div>\n  </nav>')

    howto = (f'<ul class="howto"><li><b>{T("명품")}</b> {T("실착 브랜드 또는 같은 급")}</li>'
             f'<li><b>{T("중가")}</b> {T("디자인이 가장 가까운 것")}</li>'
             f'<li><b>{T("가성비")}</b> {T("10만 원 안팎으로 따라 입기")}</li></ul>')
    first = True
    for pid, lab, arr, note in [('women', '여성', W, meta.get('women_note')), ('men', '남성', M, meta.get('men_note'))]:
        b.append(f'  <section class="panel" id="{pid}">')
        b.append(f'    <div class="panel-head"><h2 class="panel-h">{T(f"{lab} 셀럽 스냅 {len(arr)}룩")}</h2>{howto}</div>')
        for i, L in enumerate(arr, 1):
            b.append(render_look(L, i, T, data_dir, first)); first = False
        if note: b.append(f'    <p class="note-m">{T(note)}</p>')
        b.append('  </section>')

    b.append('  <section class="panel" id="ranking">')
    b.append(f'    <div class="panel-head"><h2 class="panel-h">{T("이번 주 랭킹")}</h2><p class="hot-lead">{T(mk.get("ranking_lead",""))}</p></div>')
    b.append('    <div class="rk-grid">')
    for g in mk['ranking']:
        if not g.get('items'): continue
        b.append(f'    <div class="rk">\n      <h3 class="rk-h">{T(g["h"])}</h3>\n{render_list(g["items"], T)}\n    </div>')
    b.append('    </div>\n  </section>')

    b.append('  <section class="panel" id="deals">')
    b.append(f'    <div class="panel-head"><h2 class="panel-h">{T("이번 주 핫딜")}</h2><p class="hot-lead">{T("랭킹·인기 상품 중 할인율이 큰 순서로 골랐어요.")}</p></div>')
    if mk.get('tips'):
        b.append(f'    <aside class="tip"><p class="tip-tag">{T("사기 전에 꼭 보세요")}</p><h3 class="tip-h">{T("이번 주 쇼핑 꿀팁")}</h3><ul class="tip-list">')
        for t in mk['tips']:
            b.append(f'      <li><b>{T(t["b"])}</b> {T(t["t"])}</li>')
        b.append('    </ul></aside>')
    for key, h in [('deals_women', '여성 핫딜 TOP 10'), ('deals_men', '남성 핫딜 TOP 10')]:
        if mk.get(key):
            b.append(f'    <div class="hot">\n      <h3 class="rk-h">{T(h)}</h3>\n{render_list(mk[key], T, "hot")}\n    </div>')
    if mk.get('deals_note'): b.append(f'    <p class="hot-note">{T(mk["deals_note"])}</p>')
    b.append('  </section>')

    b.append('  <section class="panel" id="kream">')
    b.append(f'    <div class="panel-head"><h2 class="panel-h">{T("크림 신발")}</h2><p class="hot-lead">{T(mk.get("kream_lead","한정판 거래 플랫폼 크림(KREAM)에서 지금 가장 인기 있는 신발이에요. 가격은 사이즈마다 달라서 화면에 보이는 최저가 기준이에요."))}</p></div>')
    b.append('    <div class="rk-grid">')
    for g in mk.get('kream', []):
        if not g.get('items'): continue
        b.append(f'    <div class="rk">\n      <h3 class="rk-h">{T(g["h"])}</h3>\n{render_list(g["items"], T)}\n    </div>')
    b.append('    </div>\n  </section>')

    foot = meta.get('footer') or [
        '사진은 실제 셀럽 사진이 아닌 AI로 재현한 이미지예요. 상품은 같은 제품이 아니라 비슷한 디자인으로 고른 대체 상품이며, 명품은 실착 브랜드이거나 같은 급의 비슷한 제품이에요.',
        f'국내 가격은 {meta["checked"]} 각 판매처 표시 기준이며 쿠폰·회원 혜택에 따라 결제가가 다를 수 있고, 해외 가격은 1달러 약 1,400원 등으로 대략 환산했어요. 가격과 재고는 수시로 바뀌어요.',
        '이 리포트의 상품 링크는 제휴 링크가 아니에요.',
        '이 링크는 이번 주 구독자 전용이에요. 매주 월요일 새 리포트가 나오면 지난 링크는 닫혀요.']
    b.append('  <footer>' + ''.join(f'\n    <span>{T(x)}</span>' for x in foot) + '\n    <span>Instagram @zzebi.st</span>\n  </footer>\n</div>')

    title = f'Zzebi.St 위클리 {meta["week"]}'
    body = '\n'.join(b)
    tbl = json.dumps(T.table(), ensure_ascii=False, separators=(',', ':'))
    doc = f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="theme-color" content="#F5F1EA">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex,nofollow">
<title>{esc(title)}</title>
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&display=swap">
<style>{css}</style>
</head>
<body>
{body}
<script>window.__I18N={tbl};</script>
<script>{JS}</script>
</body>
</html>
'''
    return doc, T

# ---------------------------------------------------------------- 암호화
def b64u(b): return base64.urlsafe_b64encode(b).decode().rstrip('=')
def ub64u(s): return base64.urlsafe_b64decode(s + '=' * (-len(s) % 4))

def encrypt(data: bytes, key: str) -> bytes:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    iv = secrets.token_bytes(12)
    return iv + AESGCM(ub64u(key)).encrypt(iv, data, None)

def decrypt(blob: bytes, key: str) -> bytes:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    return AESGCM(ub64u(key)).decrypt(blob[:12], blob[12:], None)

SEAL = '''<!doctype html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex,nofollow">
<meta name="referrer" content="no-referrer">
<meta name="theme-color" content="#F5F1EA">
<title>__TITLE__</title>
<meta property="og:type" content="website"><meta property="og:site_name" content="Zzebi.St 위클리">
<meta property="og:title" content="__TITLE__"><meta property="og:description" content="구독자 전용 · 이번 주 셀럽 스냅, 랭킹·핫딜, 크림 인기 신발">
__OGIMG__<meta name="twitter:card" content="summary_large_image">
<style>body{margin:0;min-height:100vh;display:grid;place-items:center;background:#F5F1EA;color:#141414;font-family:system-ui,-apple-system,"Apple SD Gothic Neo",sans-serif;text-align:center;padding:24px}
@media (prefers-color-scheme:dark){body{background:#111313;color:#F2F1ED}}
.m{max-width:340px;line-height:1.6}.m b{display:block;font-size:20px;margin-bottom:8px}.m a{color:#00A8A8;font-weight:700}
.sp{width:28px;height:28px;border:3px solid #00A8A8;border-right-color:transparent;border-radius:50%;margin:0 auto;animation:r .8s linear infinite}@keyframes r{to{transform:rotate(360deg)}}</style>
</head><body><div class="m" id="m"><div class="sp" aria-label="loading"></div></div>
<script id="c" type="application/octet-stream">__CT__</script>
<script>
(function(){
  function bad(){document.getElementById('m').innerHTML='<b>링크가 닫혔어요</b>이 리포트 링크는 만료됐거나 주소가 잘렸어요.<br>인스타그램 <a href="https://www.instagram.com/zzebi.st/">@zzebi.st</a> 최신 게시물에 \\'리포트\\' 댓글을 남기면 DM으로 이번 주 링크를 보내드려요.<br><br><small>This link has expired. Comment “리포트” on @zzebi.st’s latest post to get this week’s link by DM. · 链接已失效，请在 @zzebi.st 最新帖子下评论“리포트”，通过私信获取本周链接。</small>'}
  var h=(location.hash||'').replace(/^#/,''), k=null;
  h.split('&').forEach(function(p){if(p.indexOf('k=')===0)k=p.slice(2)});
  if(!k||!window.crypto||!crypto.subtle){bad();return}
  function d64(s){s=s.replace(/-/g,'+').replace(/_/g,'/');while(s.length%4)s+='=';var b=atob(s),u=new Uint8Array(b.length);for(var i=0;i<b.length;i++)u[i]=b.charCodeAt(i);return u}
  try{var ct=d64(document.getElementById('c').textContent.trim()),key=d64(k)}catch(e){bad();return}
  crypto.subtle.importKey('raw',key,'AES-GCM',false,['decrypt']).then(function(ck){
    return crypto.subtle.decrypt({name:'AES-GCM',iv:ct.slice(0,12)},ck,ct.slice(12))
  }).then(function(buf){
    var html=new TextDecoder().decode(buf);
    var nd=new DOMParser().parseFromString(html,'text/html');
    var root=document.importNode(nd.documentElement,true);
    document.replaceChild(root,document.documentElement);
    [].forEach.call(root.querySelectorAll('script'),function(old){var s=document.createElement('script');s.textContent=old.textContent;old.parentNode.replaceChild(s,old)});
  }).catch(bad);
})();
</script></body></html>
'''

def seal(plain_path, out_path, key, title='Zzebi.St 위클리', og=None, profile=False):
    ct = encrypt(open(plain_path, 'rb').read(), key)
    ogt = f'<meta property="og:image" content="{esc(og)}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">\n' if og else ''
    src = SEAL
    if profile:
        src = (src.replace("인스타그램 <a href=\"https://www.instagram.com/zzebi.st/\">@zzebi.st</a> 최신 게시물에 \\'리포트\\' 댓글을 남기면 DM으로 이번 주 링크를 보내드려요.",
                           "인스타그램 <a href=\"https://www.instagram.com/zzebi.st/\">@zzebi.st</a> 프로필 링크에서 이번 주 리포트를 볼 수 있어요.")
                  .replace("Comment “리포트” on @zzebi.st’s latest post to get this week’s link by DM.", "This week’s report is in @zzebi.st’s Instagram profile link.")
                  .replace("请在 @zzebi.st 最新帖子下评论“리포트”，通过私信获取本周链接。", "请在 @zzebi.st 的 Instagram 主页链接查看本周报告。"))
    page = (src.replace('__TITLE__', esc(title)).replace('__OGIMG__', ogt)
                .replace('__CT__', base64.b64encode(ct).decode()))
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    open(out_path, 'w').write(page)

def pack(data_dir, out, key):
    b = io.BytesIO()
    with tarfile.open(fileobj=b, mode='w:gz') as tf:
        skip = lambda ti: None if os.path.basename(ti.name).startswith('_') or os.path.basename(ti.name) == 'strings.json' else ti
        tf.add(data_dir, arcname='.', filter=skip)
    open(out, 'wb').write(encrypt(b.getvalue(), key))

def unpack(inp, data_dir, key):
    raw = decrypt(open(inp, 'rb').read(), key)
    os.makedirs(data_dir, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(raw), mode='r:gz') as tf:
        tf.extractall(data_dir, filter='data')

if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: print(__doc__); sys.exit(1)
    cmd = a[0]
    if cmd == 'newkey':
        print(json.dumps({'key': b64u(secrets.token_bytes(32)), 'slug': secrets.token_hex(6)}))
    elif cmd == 'strings':
        doc, T = render(a[1])
        have = {}
        ip = os.path.join(a[1], 'i18n.json')
        if os.path.exists(ip): have = json.load(open(ip))
        todo = [k for k in T.keys if not (have.get(k, {}).get('en') and have.get(k, {}).get('zh'))]
        json.dump(todo, open(os.path.join(a[1], 'strings.json'), 'w'), ensure_ascii=False, indent=0)
        print(f'문구 {len(T.keys)}개 중 번역 필요 {len(todo)}개 → {a[1]}/strings.json')
    elif cmd == 'render':
        doc, T = render(a[1])
        open(a[2], 'w').write(doc)
        miss = sum(1 for x in T.table()['en'] if not x)
        print(f'{a[2]} {len(doc)//1024}KB · 문구 {len(T.keys)}개 · 영어 미번역 {miss}개')
    elif cmd == 'seal':
        og = a[4] if len(a) > 4 else None
        title = a[5] if len(a) > 5 else 'Zzebi.St 위클리'
        seal(a[1], a[2], a[3], title, og); print('sealed', a[2])
    elif cmd == 'pack': pack(a[1], a[2], a[3]); print('packed', a[2])
    elif cmd == 'unpack': unpack(a[1], a[2], a[3]); print('unpacked', a[2])
    else: print(__doc__); sys.exit(1)
