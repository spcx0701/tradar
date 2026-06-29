/* 무역풍 Tradewind — 정적 PWA 앱 로직.
   app/data/*.json (파이썬 AI가 미리 구운 결과)만으로 100% 동작한다.
   백엔드(server/main.py)가 있으면 동일 결과를 /api 로도 제공하지만, 데모는 정적으로 완결. */
'use strict';

const S = { catalog: null, forecast: null, radar: null, countries: null, product: null, chat: [] };

const STATUS = {
  surge:   { label: '급등', cls: 'surge',   sky: '☀️' },
  rising:  { label: '상승', cls: 'rising',  sky: '🌤️' },
  stable:  { label: '안정', cls: 'stable',  sky: '⛅' },
  cooling: { label: '둔화', cls: 'cooling', sky: '🌧️' },
  volatile:{ label: '변동', cls: 'volatile',sky: '🌬️' },
};

/* ── 유틸 ───────────────────────────────── */
function flag(cc) {
  if (!cc || cc.length !== 2) return '🏳️';
  return String.fromCodePoint(...[...cc.toUpperCase()].map(c => 0x1f1e6 + c.charCodeAt(0) - 65));
}
function usd(v) {
  v = +v || 0;
  if (v >= 1e8) return (v / 1e8).toFixed(1) + '억$';
  if (v >= 1e6) return (v / 1e6).toFixed(0) + '백만$';
  if (v >= 1e3) return (v / 1e3).toFixed(0) + '천$';
  return v.toFixed(0) + '$';
}
function pct(v) { const n = (v * 100); return (n >= 0 ? '+' : '') + n.toFixed(0) + '%'; }
function deltaCls(v) { return v > 0.02 ? 'up' : v < -0.02 ? 'down' : 'flat'; }
function pname(hs) { const p = S.catalog.products.find(p => p.hs === hs); return p ? p.name_ko : hs; }
function cname(cc) { return (S.catalog.countries[cc]) || cc; }
function statusOf(s) { return STATUS[s] || STATUS.stable; }
function el(id) { return document.getElementById(id); }

/* ── SVG 라인차트(이력 + 예측 밴드) ─────────── */
function chartSVG(months, hist, fcMonths, mean, lo, hi) {
  const back = 18; // 최근 18개월만 표시
  const h0 = hist.slice(-back), m0 = months.slice(-back);
  const allLabels = m0.concat(fcMonths);
  const histPts = h0.map((v, i) => ({ x: i, y: v }));
  const fcStart = h0.length - 1;
  // 예측선은 마지막 실적에서 이어지도록 앵커
  const meanPts = [{ x: fcStart, y: h0[h0.length - 1] }].concat(mean.map((v, i) => ({ x: fcStart + 1 + i, y: v })));
  const hiPts = [{ x: fcStart, y: h0[h0.length - 1] }].concat(hi.map((v, i) => ({ x: fcStart + 1 + i, y: v })));
  const loPts = [{ x: fcStart, y: h0[h0.length - 1] }].concat(lo.map((v, i) => ({ x: fcStart + 1 + i, y: v })));
  const N = allLabels.length - 1;
  const W = 360, H = 168, padL = 6, padR = 6, padT = 12, padB = 20;
  const ys = h0.concat(mean, hi, lo);
  const ymax = Math.max(...ys) * 1.08, ymin = Math.min(...ys, 0) * 0.98;
  const X = x => padL + (x / N) * (W - padL - padR);
  const Y = y => padT + (1 - (y - ymin) / (ymax - ymin || 1)) * (H - padT - padB);
  const line = pts => pts.map((p, i) => (i ? 'L' : 'M') + X(p.x).toFixed(1) + ' ' + Y(p.y).toFixed(1)).join(' ');
  const band = hiPts.map(p => `${X(p.x).toFixed(1)} ${Y(p.y).toFixed(1)}`).join(' L ')
    + ' L ' + loPts.slice().reverse().map(p => `${X(p.x).toFixed(1)} ${Y(p.y).toFixed(1)}`).join(' L ');
  const sepX = X(fcStart);
  const labels = [m0[0], m0[m0.length - 1], fcMonths[fcMonths.length - 1]];
  const labX = [0, fcStart, N];
  return `<svg class="chart" viewBox="0 0 ${W} ${H}" preserveAspectRatio="none" role="img">
    <line x1="${sepX}" y1="${padT}" x2="${sepX}" y2="${H - padB}" stroke="#cbd5e1" stroke-dasharray="3 3"/>
    <text x="${sepX + 4}" y="${padT + 9}" font-size="9" fill="#94a3b8">예측▶</text>
    <path d="M ${band} Z" fill="rgba(18,179,166,.16)" stroke="none"/>
    <path d="${line(histPts)}" fill="none" stroke="#0b5fa5" stroke-width="2.4" stroke-linejoin="round"/>
    <path d="${line(meanPts)}" fill="none" stroke="#12b3a6" stroke-width="2.4" stroke-dasharray="5 4" stroke-linecap="round"/>
    ${meanPts.slice(1).map(p => `<circle cx="${X(p.x).toFixed(1)}" cy="${Y(p.y).toFixed(1)}" r="2.6" fill="#12b3a6"/>`).join('')}
    <circle cx="${X(fcStart).toFixed(1)}" cy="${Y(h0[h0.length-1]).toFixed(1)}" r="3" fill="#0b5fa5"/>
    ${labX.map((lx, i) => `<text x="${X(lx).toFixed(1)}" y="${H - 6}" font-size="9" fill="#94a3b8" text-anchor="${i===0?'start':i===labX.length-1?'end':'middle'}">${labels[i]}</text>`).join('')}
  </svg>
  <div class="legend"><span><i style="background:#0b5fa5"></i>실적</span><span><i style="background:#12b3a6"></i>AI 예측</span><span><i style="background:rgba(18,179,166,.3)"></i>95% 구간</span></div>`;
}

function gaugeSVG(score) {
  const r = 18, c = 2 * Math.PI * r, off = c * (1 - score / 100);
  const col = score >= 70 ? '#16a34a' : score >= 55 ? '#0b5fa5' : '#64748b';
  return `<svg class="gauge" viewBox="0 0 44 44"><circle cx="22" cy="22" r="${r}" fill="none" stroke="#e2e8f0" stroke-width="5"/>
    <circle cx="22" cy="22" r="${r}" fill="none" stroke="${col}" stroke-width="5" stroke-linecap="round"
      stroke-dasharray="${c.toFixed(1)}" stroke-dashoffset="${off.toFixed(1)}" transform="rotate(-90 22 22)"/>
    <text x="22" y="26" text-anchor="middle" font-size="13" font-weight="800" fill="${col}">${Math.round(score)}</text></svg>`;
}

/* ── 홈 ─────────────────────────────────── */
function renderHome() {
  const hs = S.product || S.catalog.products[0].hs;
  S.product = hs;
  // 품목 칩
  el('home-chips').innerHTML = S.catalog.products.map(p =>
    `<button class="chip ${p.hs === hs ? 'active' : ''}" data-hs="${p.hs}">${p.name_ko}</button>`).join('');
  el('home-chips').querySelectorAll('.chip').forEach(b =>
    b.onclick = () => { S.product = b.dataset.hs; renderHome(); });

  const p = S.catalog.products.find(p => p.hs === hs);
  const markets = (S.radar.by_product[hs] || []);
  const top = markets[0];
  const st = statusOf(top ? top.status : 'stable');
  const rising = markets.filter(m => m.status === 'surge' || m.status === 'rising').length;

  el('home-hero').innerHTML = `<div class="weather"><div class="glow"></div>
    <div class="between"><div><h2>${p.name_ko}</h2>
      <span class="pill ${st.cls}" style="background:rgba(255,255,255,.2);color:#fff">${st.sky} ${st.label} 국면</span></div>
      <div class="sky">${st.sky}</div></div>
    <div class="summary">최근 12개월 수출 ${usd(p.latest12_usd)} · 전년 대비 ${pct(p.yoy)}.
      ${top ? `가장 뜨거운 시장은 <b>${cname(top.country)}</b>(기회 ${Math.round(top.opportunity)}점, ${pct(top.fc_growth6)} 전망).` : ''}</div>
    <div class="metrics">
      <div><b>${pct(p.yoy)}</b><span>전년 대비</span></div>
      <div><b>${rising}곳</b><span>상승·급등 시장</span></div>
      <div><b>${markets.length}곳</b><span>분석 시장</span></div>
    </div></div>`;

  el('home-markets').innerHTML = S.radar.top.slice(0, 5).map(m => marketRow(m)).join('');
  bindMarketRows('home-markets');

  if (top) {
    const key = hs + '|' + top.country, s = S.forecast.series[key];
    el('home-forecast').innerHTML =
      `<div class="between" style="margin-bottom:8px"><h3 style="margin:0">${flag(top.country)} ${cname(top.country)} · ${p.name_ko}</h3>
        <span class="pill ${st.cls}">${pct(s.fc6)} 전망</span></div>` +
      chartSVG(S.forecast.months, s.hist, S.forecast.fc_months, s.mean, s.lo, s.hi) +
      `<p class="small muted" style="margin:8px 0 0">AI 예측 적합도(MAPE) ${(s.mape*100).toFixed(1)}% · 월 추세 ${pct(s.trend)} · 변동성 ${s.cv.toFixed(2)}</p>`;
  }
}

function marketRow(m) {
  const st = statusOf(m.status);
  return `<div class="mkt" data-hs="${m.hs}" data-cc="${m.country}">
    <div class="flag">${flag(m.country)}</div>
    <div class="body"><div class="t">${cname(m.country)} · ${m.product || pname(m.hs)}</div>
      <div class="s"><span class="pill ${st.cls}">${st.label}</span> 전년 ${pct(m.yoy)} · 향후 6개월 ${pct(m.fc_growth6)}</div></div>
    <div class="opp">${gaugeSVG(m.opportunity)}<span>기회점수</span></div></div>`;
}
function bindMarketRows(containerId) {
  el(containerId).querySelectorAll('.mkt').forEach(r =>
    r.onclick = () => openReport(r.dataset.hs, r.dataset.cc));
}

/* ── 레이더 ─────────────────────────────── */
let radarCat = '전체';
function renderRadar() {
  const cats = ['전체'].concat(S.catalog.categories || []);
  el('radar-chips').innerHTML = cats.map(c =>
    `<button class="chip ${c === radarCat ? 'active' : ''}" data-cat="${c}">${c}</button>`).join('');
  el('radar-chips').querySelectorAll('.chip').forEach(b =>
    b.onclick = () => { radarCat = b.dataset.cat; renderRadar(); });
  const list = S.radar.top.filter(m => radarCat === '전체' || m.category === radarCat);
  el('radar-list').innerHTML = list.map(marketRow).join('');
  bindMarketRows('radar-list');
  el('radar-risk').innerHTML = S.radar.risk.map(m => {
    return `<div class="mkt" data-hs="${m.hs}" data-cc="${m.country}" style="border-color:#fecaca;background:#fff8f8">
      <div class="flag">${flag(m.country)}</div>
      <div class="body"><div class="t">${cname(m.country)} · ${m.product}</div>
        <div class="s"><span class="pill cooling">둔화 경보</span> 최근 3개월 ${pct(m.growth3)} · 규모 ${usd(m.recent12_usd)}</div></div>
      <div class="opp"><b style="color:#dc2626">${Math.round(m.risk)}</b><span>위험도</span></div></div>`;
  }).join('');
  bindMarketRows('radar-risk');
}

/* ── AI 참모(클라이언트 사이드, 파이썬 advisor 동기화) ── */
const PRODUCT_KW = {
  '1902.30': ['라면','즉석면','면','noodle'], '1212.21': ['김','조미김','마른김','laver','seaweed'],
  '3304.99': ['화장품','뷰티','코스메틱','스킨','beauty'], '2005.99': ['김치','kimchi'],
  '2103.90': ['고추장','장류','소스','양념','sauce'], '1905.31': ['과자','제과','스낵','snack'],
  '2202.99': ['음료','주스','드링크','beverage'], '2208.90': ['소주','술','주류','증류주','soju'],
  '0810.10': ['딸기','strawberry'], '0806.10': ['포도','샤인머스캣','샤인','grape'],
  '1211.20': ['인삼','홍삼','ginseng'], '1901.90': ['즉석밥','떡','쌀가공','가공밥'],
};
const COUNTRY_KW = {
  US:['미국','usa','america'], JP:['일본','japan'], CN:['중국','china'], VN:['베트남','vietnam'],
  TH:['태국','thailand'], ID:['인도네시아','indonesia'], MY:['말레이시아','malaysia'], PH:['필리핀','philippines'],
  TW:['대만','taiwan'], HK:['홍콩','hongkong'], SG:['싱가포르','singapore'], AU:['호주','australia'],
  AE:['아랍에미리트','uae','두바이'], SA:['사우디'], FR:['프랑스','france'], DE:['독일','germany'],
  GB:['영국','uk','england'], NL:['네덜란드'], CA:['캐나다','canada'], MX:['멕시코','mexico'],
  IN:['인도','india'], MN:['몽골'], RU:['러시아','russia'], BR:['브라질','brazil'],
};
function intentOf(q) {
  const s = q.toLowerCase().replace(/\s/g, '');
  let hs = null, cc = null;
  for (const [k, kws] of Object.entries(PRODUCT_KW)) if (kws.some(w => s.includes(w.replace(/\s/g,'')))) { hs = k; break; }
  for (const [k, kws] of Object.entries(COUNTRY_KW)) if (kws.some(w => s.includes(w))) { cc = k; break; }
  let intent;
  if (/(위험|리스크|둔화|조심|경보|빠지)/.test(s)) intent = 'risk';
  else if (cc && hs) intent = 'forecast';
  else if (/(어디|어느나라|추천|유망|확대|신규|뚫)/.test(s) || hs) intent = 'recommend';
  else intent = 'overview';
  return { hs, cc, intent };
}
function advisorAnswer(q) {
  const it = intentOf(q);
  let headline = '', ev = [], chart = null, sug = [];
  if (it.intent === 'forecast' && it.hs && it.cc) {
    const s = S.forecast.series[it.hs + '|' + it.cc];
    if (!s) { headline = `${cname(it.cc)}의 ${pname(it.hs)} 데이터를 찾지 못했어요.`; }
    else {
      const st = statusOf(s.status);
      headline = `${cname(it.cc)} ${pname(it.hs)} 시장은 현재 '${st.label}' 국면입니다. 최근 12개월 수출은 전년 대비 ${pct(s.yoy)}, 향후 6개월은 전년 동기 대비 ${pct(s.fc6)} 전망(월 추세 ${pct(s.trend)}).`;
      ev = [['최근 12개월 수출', usd(s.recent12_usd)], ['전년 대비(YoY)', pct(s.yoy)],
            ['향후 6개월 전망', pct(s.fc6)], ['예측 적합도(MAPE)', (s.mape*100).toFixed(1)+'%'], ['변동성', s.cv.toFixed(2)]];
      chart = { hs: it.hs, cc: it.cc };
      sug = [`${pname(it.hs)} 어디에 더 수출하면 좋을까?`, `${cname(it.cc)}에서 위험한 시장은?`];
    }
  } else if (it.intent === 'recommend') {
    const rows = it.hs ? (S.radar.by_product[it.hs] || []).slice(0, 5) : S.radar.top.slice(0, 6);
    const t = rows[0];
    headline = it.hs
      ? `${pname(it.hs)} 수출을 확대한다면 지금은 '${cname(t.country)}'이 1순위입니다. 기회점수 ${Math.round(t.opportunity)}점, 전년 대비 ${pct(t.yoy)}, 향후 6개월 ${pct(t.fc_growth6)} 전망.`
      : `지금 가장 빠르게 떠오르는 한류 수출 기회는 '${cname(t.country)}의 ${t.product}'입니다 (기회 ${Math.round(t.opportunity)}, YoY ${pct(t.yoy)}).`;
    ev = rows.map((r, i) => [`${i+1}. ${cname(r.country)}${it.hs ? '' : ' · ' + r.product}`,
      `기회 ${Math.round(r.opportunity)} · ${pct(r.yoy)} · ${statusOf(r.status).label}`]);
    if (it.hs) { chart = { hs: it.hs, cc: t.country }; sug = [`${pname(it.hs)} ${cname(t.country)} 수요 예측`, `${pname(it.hs)} 위험 시장은?`]; }
    else sug = ['라면 어디에 수출하면 좋을까?', '위험한 시장 알려줘'];
  } else if (it.intent === 'risk') {
    const rows = S.radar.risk.slice(0, 6); const t = rows[0];
    headline = t ? `리스크 조기경보: '${cname(t.country)}의 ${t.product}'이 식고 있습니다 (최근 3개월 ${pct(t.growth3)}, 규모 ${usd(t.recent12_usd)}). 의존도가 높다면 시장 다변화를 권장합니다.`
      : '현재 규모 있는 시장 중 둔화 경보는 없습니다.';
    ev = rows.map(r => [`⚠ ${cname(r.country)} · ${r.product}`, `3개월 ${pct(r.growth3)} · ${usd(r.recent12_usd)}`]);
    sug = ['떠오르는 시장 추천해줘', '화장품 중국 수요 예측'];
  } else {
    const o = S.radar.top.slice(0, 3);
    headline = `무역풍은 관세청 수출입통계로 한류 품목의 국가별 수요를 예측합니다. 무엇이 궁금하세요? 품목과 나라를 말씀해 보세요.`;
    ev = o.map(r => [`${cname(r.country)} · ${r.product}`, `기회 ${Math.round(r.opportunity)} · ${pct(r.yoy)}`]);
    sug = ['라면 어디에 수출하면 좋을까?', '화장품 미국 수요 예측', '위험한 시장은?'];
  }
  return { headline, ev, chart, sug };
}
function pushBubble(role, html) {
  const b = document.createElement('div');
  b.className = 'bubble ' + role; b.innerHTML = html;
  el('chat').appendChild(b); window.scrollTo(0, document.body.scrollHeight);
}
function askAdvisor(q) {
  if (!q.trim()) return;
  pushBubble('me', q);
  const r = advisorAnswer(q);
  let html = r.headline;
  if (r.chart) { const s = S.forecast.series[r.chart.hs + '|' + r.chart.cc];
    if (s) html += '<div style="margin-top:10px">' + chartSVG(S.forecast.months, s.hist, S.forecast.fc_months, s.mean, s.lo, s.hi) + '</div>'; }
  if (r.ev.length) html += '<div class="evid">' + r.ev.map(e => `<div class="e"><span>${e[0]}</span><b>${e[1]}</b></div>`).join('') + '</div>';
  pushBubble('ai', html);
  renderSuggest(r.sug);
}
function renderSuggest(list) {
  el('advisor-suggest').innerHTML = list.map(q => `<button class="chip" data-q="${q}">${q}</button>`).join('');
  el('advisor-suggest').querySelectorAll('.chip').forEach(b => b.onclick = () => askAdvisor(b.dataset.q));
}
function initAdvisor() {
  if (S.chat.length) return;
  S.chat.push(1);
  pushBubble('ai', '안녕하세요, AI 무역참모 <b>바람이</b>예요. 🌬️\n관세청 수출입통계로 한류 품목의 수출 시장을 분석해 드려요. 품목과 나라를 말씀해 보세요!');
  renderSuggest(['라면 어디에 수출하면 좋을까?', '화장품 미국 수요 예측', '위험한 시장 알려줘']);
}

/* ── 리포트 ─────────────────────────────── */
function renderReportSelectors() {
  el('rep-product').innerHTML = S.catalog.products.map(p => `<option value="${p.hs}">${p.name_ko}</option>`).join('');
  const fill = hs => {
    const ms = (S.radar.by_product[hs] || []);
    el('rep-country').innerHTML = ms.map(m => `<option value="${m.country}">${cname(m.country)} (${statusOf(m.status).label})</option>`).join('');
  };
  fill(el('rep-product').value);
  el('rep-product').onchange = () => { fill(el('rep-product').value); renderReport(); };
  el('rep-country').onchange = renderReport;
  el('report-src').innerHTML = srcHTML();
  renderReport();
}
function renderReport() {
  const hs = el('rep-product').value, cc = el('rep-country').value;
  const s = S.forecast.series[hs + '|' + cc]; if (!s) return;
  const st = statusOf(s.status);
  const sim = (S.radar.by_product[hs] || []).filter(m => m.country !== cc).slice(0, 3)
    .map(m => ({ ...m, hs, product: pname(hs) }));
  el('report-out').innerHTML = `<div class="card">
    <div class="between"><h3 style="margin:0">${flag(cc)} ${cname(cc)} · ${pname(hs)}</h3><span class="pill ${st.cls}">${st.sky} ${st.label}</span></div>
    <div style="margin:12px 0">${chartSVG(S.forecast.months, s.hist, S.forecast.fc_months, s.mean, s.lo, s.hi)}</div>
    <div class="kv">
      <span class="k">최근 12개월 수출</span><span class="v">${usd(s.recent12_usd)}</span>
      <span class="k">전년 대비(YoY)</span><span class="v delta ${deltaCls(s.yoy)}">${pct(s.yoy)}</span>
      <span class="k">향후 6개월 전망(전년 동기 대비)</span><span class="v delta ${deltaCls(s.fc6)}">${pct(s.fc6)}</span>
      <span class="k">월 추세</span><span class="v">${pct(s.trend)}</span>
      <span class="k">기회점수 / 위험도</span><span class="v">${Math.round(s.opportunity)} / ${Math.round(s.risk)}</span>
      <span class="k">예측 적합도(MAPE)</span><span class="v">${(s.mape*100).toFixed(1)}%</span>
    </div>
    <p class="small" style="margin:12px 0 0;padding:10px 12px;background:#f1f7fd;border-radius:10px">
      💡 <b>AI 권고</b> — ${recommend(s, cc, hs)}</p>
  </div>
  <div class="card"><h3>🔁 함께 보면 좋은 시장</h3>${sim.map(marketRow).join('')}</div>`;
  bindMarketRows('report-out');
}
function recommend(s, cc, hs) {
  if (s.status === 'surge') return `${cname(cc)}는 ${pname(hs)}의 급등 시장입니다. 향후 6개월 ${pct(s.fc6)} 성장이 전망되니 물량·마케팅 선제 확대와 현지 유통망 선점을 권장합니다.`;
  if (s.status === 'rising') return `완만한 상승세입니다. ${pct(s.fc6)} 전망에 맞춰 점진적 물량 확대와 신규 채널 테스트가 적절합니다.`;
  if (s.status === 'cooling') return `둔화 신호가 감지됩니다. 재고·선적 계획을 보수적으로 잡고 대체 시장(레이더 추천)으로 다변화하세요.`;
  if (s.status === 'volatile') return `변동성이 큽니다. 환율·계절 영향을 고려해 분할 선적과 헤지를 권장합니다.`;
  return `안정적인 시장입니다. 현 수준 유지하며 떠오르는 인접 시장을 함께 모니터링하세요.`;
}
function srcHTML() {
  return `<b>데이터 출처</b><br>· 관세청 <b>품목별 국가별 수출입실적</b>(공공데이터포털, apis.data.go.kr/1220000/nitemtrade) — 필수<br>
    · 분석 기간 ${S.catalog.meta.period} · ${S.catalog.products.length}개 한류 품목 · ${Object.keys(S.catalog.countries).length}개국<br>
    · 예측·기회점수는 무역풍 자체 개발 <b>국산 AI</b>(계절분해+감쇠추세, numpy)로 산출.<br>
    <span style="color:#94a3b8">${S.catalog.meta.note}</span>`;
}
function openReport(hs, cc) {
  go('report');
  el('rep-product').value = hs;
  el('rep-product').onchange();
  el('rep-country').value = cc; renderReport();
}

/* ── 네비게이션 ─────────────────────────── */
function go(tab) {
  document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
  el('view-' + tab).classList.add('active');
  document.querySelectorAll('.tabbar button').forEach(b => b.classList.toggle('active', b.dataset.tab === tab));
  el('composer').style.display = tab === 'advisor' ? 'block' : 'none';
  if (tab === 'home') renderHome();
  if (tab === 'radar') renderRadar();
  if (tab === 'advisor') initAdvisor();
  if (tab === 'report') { if (!el('rep-product').options.length) renderReportSelectors(); }
  window.scrollTo(0, 0);
}

async function boot() {
  try {
    const [c, f, r] = await Promise.all([
      fetch('data/catalog.json').then(x => x.json()),
      fetch('data/forecast.json').then(x => x.json()),
      fetch('data/radar.json').then(x => x.json()),
    ]);
    S.catalog = c; S.forecast = f; S.radar = r;
    el('databadge').textContent = '관세청 통계 · ' + c.meta.period.split(' ~ ')[1];
    document.querySelectorAll('.tabbar button').forEach(b => b.onclick = () => go(b.dataset.tab));
    document.querySelectorAll('[data-go]').forEach(a => a.onclick = e => { e.preventDefault(); go(a.dataset.go); });
    el('chat-send').onclick = () => { const i = el('chat-input'); askAdvisor(i.value); i.value = ''; };
    el('chat-input').addEventListener('keydown', e => { if (e.key === 'Enter') el('chat-send').click(); });
    renderHome();
    // 딥링크: ?tab=&hs=&cc=&q= (시연·캡처용)
    const q = new URLSearchParams(location.search);
    if (q.get('hs')) S.product = q.get('hs');
    const tab = q.get('tab');
    if (tab) go(tab);
    if (tab === 'report' && q.get('hs') && q.get('cc')) openReport(q.get('hs'), q.get('cc'));
    if (tab === 'advisor' && q.get('q')) setTimeout(() => askAdvisor(q.get('q')), 60);
    if (tab === 'home' || !tab) renderHome();
  } catch (e) {
    document.querySelector('main').innerHTML = '<div class="card">데이터를 불러오지 못했습니다. <code>scripts/build_app_data.py</code>를 실행했는지 확인하세요.<br><small>' + e + '</small></div>';
  }
  if ('serviceWorker' in navigator) navigator.serviceWorker.register('sw.js').catch(() => {});
}
boot();
