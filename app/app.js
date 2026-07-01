/* Tradar — 수출 인텔리전스 플랫폼 (정적 SPA)
   app/data/*.json (파이썬 국산 AI가 구운 예측·레이더·스코어)만으로 100% 동작.
   시각화는 ECharts(벤더링), 아이콘은 Material Symbols. */
'use strict';

const S = { cat:null, fc:null, radar:null, tm:null, countries:null,
  view:'command', product:null, country:null, charts:{}, chat:[], mapBy:'category', discFilter:'all' };

const MOM = {
  surge:{ko:'폭발적 성장',cls:'surge'}, rising:{ko:'성장',cls:'rising'}, stable:{ko:'안정',cls:'stable'},
  cooling:{ko:'둔화',cls:'cooling'}, volatile:{ko:'변동성',cls:'volatile'} };
const STAGE = { dominant:'최대시장', core:'주력시장', growing:'성장시장', emerging:'신흥시장', nascent:'초기시장' };
const SUBS = [['demand','수요'],['growth','성장'],['stability','안정성'],['potential','잠재력']];

/* ---------- helpers ---------- */
const $ = s => document.querySelector(s);
const el = (t,c,h)=>{const e=document.createElement(t); if(c)e.className=c; if(h!=null)e.innerHTML=h; return e;};
function flag(cc){ return cc&&cc.length===2 ? String.fromCodePoint(...[...cc.toUpperCase()].map(c=>0x1f1e6+c.charCodeAt(0)-65)) : '🏳️'; }
function usd(v){ v=+v||0; if(v>=1e9)return '$'+(v/1e9).toFixed(2)+'B'; if(v>=1e6)return '$'+(v/1e6).toFixed(1)+'M'; if(v>=1e3)return '$'+(v/1e3).toFixed(0)+'K'; return '$'+v.toFixed(0); }
function usdKo(v){ v=+v||0; if(v>=1e8)return (v/1e8).toFixed(1)+'억$'; if(v>=1e6)return (v/1e6).toFixed(0)+'백만$'; return (v/1e3).toFixed(0)+'천$'; }
function pct(v){ const n=v*100; return (n>=0?'+':'')+n.toFixed(0)+'%'; }
function pct1(v){ const n=v*100; return (n>=0?'+':'')+n.toFixed(1)+'%'; }
function dcls(v){ return v>0.015?'up':v<-0.015?'down':'flat'; }
function delta(v){ return `<span class="delta ${dcls(v)}">${pct(v)}</span>`; }
function pname(hs){ const p=S.cat.products.find(p=>p.hs===hs); return p?p.name_ko:hs; }
function cname(cc){ return (S.cat.countries[cc])||cc; }
function ser(hs,cc){ return S.fc.series[hs+'|'+cc]; }
function scoreColor(s){ return s>=75?'#16B364':s>=60?'#1D68F0':s>=45?'#16A8C8':'#9AA4B2'; }
function yoyColor(y){ // finviz-style heat
  const t=Math.max(-1,Math.min(1,y/0.5));
  if(t>=0){ const a=[0.18+0.72*t]; return `rgba(22,179,100,${a[0].toFixed(2)})`; }
  return `rgba(240,68,59,${(0.18+0.72*-t).toFixed(2)})`;
}
function momTag(m){ const x=MOM[m]||MOM.stable; return `<span class="mom ${x.cls}">${x.ko}</span>`; }
function stageTag(st){ return `<span class="stage ${st}">${STAGE[st]||st}</span>`; }

/* score ring (SVG, brand gradient stroke) */
let RINGID=0;
function ring(score,size=64,label='SCORE'){
  const id='rg'+(RINGID++), r=size/2-6, c=2*Math.PI*r, off=c*(1-score/100);
  const fs=size>=90?26:size>=64?19:15;
  return `<span class="ring" style="width:${size}px;height:${size}px">
    <svg width="${size}" height="${size}"><defs><linearGradient id="${id}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#16C8F5"/><stop offset="0.5" stop-color="#2E6BFF"/><stop offset="1" stop-color="#7A5BF0"/></linearGradient></defs>
      <circle cx="${size/2}" cy="${size/2}" r="${r}" fill="none" stroke="#EDF0F4" stroke-width="6"/>
      <circle cx="${size/2}" cy="${size/2}" r="${r}" fill="none" stroke="url(#${id})" stroke-width="6" stroke-linecap="round"
        stroke-dasharray="${c.toFixed(1)}" stroke-dashoffset="${off.toFixed(1)}" transform="rotate(-90 ${size/2} ${size/2})"/></svg>
    <span class="txt"><b style="font-size:${fs}px">${Math.round(score)}</b><span>${label}</span></span></span>`;
}
function subBars(sub){
  return SUBS.map(([k,ko])=>`<div class="subrow"><span class="k">${ko}</span>
    <span class="track"><span class="fill" style="width:${sub[k]}%"></span></span><span class="v num">${sub[k]}</span></div>`).join('');
}
function sparkline(hist,w=88,h=30,up=true){
  const a=hist.slice(-14), mn=Math.min(...a), mx=Math.max(...a), rng=mx-mn||1;
  const pts=a.map((v,i)=>`${(i/(a.length-1)*w).toFixed(1)},${(h-2-((v-mn)/rng)*(h-4)).toFixed(1)}`).join(' ');
  const col=up?'#16B364':'#F0443B';
  return `<svg class="spark" viewBox="0 0 ${w} ${h}"><polyline points="${pts}" fill="none" stroke="${col}" stroke-width="1.8" stroke-linejoin="round"/></svg>`;
}

/* ---------- ECharts ---------- */
const FONT='Inter, "Noto Sans KR", sans-serif';
function chart(node,opt){ const c=echarts.init(node); c.setOption(opt); S.charts[node.id]=c; return c; }
function trendChart(node,s,months,fcMonths){
  const back=24, hist=s.hist.slice(-back), hm=months.slice(-back);
  const gap=Array(hist.length-1).fill(null);
  const meanFull=[...Array(hist.length-1).fill(null), hist[hist.length-1], ...s.mean];
  const loFull=[...gap, hist[hist.length-1], ...s.lo], hiFull=[...gap, hist[hist.length-1], ...s.hi];
  const x=[...hm,...fcMonths];
  chart(node,{
    grid:{left:8,right:12,top:16,bottom:24,containLabel:true},
    textStyle:{fontFamily:FONT},
    tooltip:{trigger:'axis',axisPointer:{type:'line'},valueFormatter:v=>v==null?'-':usd(v),
      backgroundColor:'#fff',borderColor:'#E1E6EC',textStyle:{color:'#0C0D11',fontSize:12}},
    xAxis:{type:'category',data:x,boundaryGap:false,axisLine:{lineStyle:{color:'#E1E6EC'}},
      axisLabel:{color:'#9AA4B2',fontSize:10,interval:Math.floor(x.length/6)},axisTick:{show:false}},
    yAxis:{type:'value',splitLine:{lineStyle:{color:'#EDF0F4'}},axisLabel:{color:'#9AA4B2',fontSize:10,formatter:v=>usd(v)}},
    series:[
      {name:'예측구간',type:'line',data:hiFull,lineStyle:{opacity:0},stack:'band',symbol:'none',areaStyle:{opacity:0}},
      {name:'lo',type:'line',data:loFull.map((v,i)=>v==null?null:hiFull[i]-v),lineStyle:{opacity:0},stack:'band',symbol:'none',
        areaStyle:{color:'rgba(46,107,255,0.10)'}},
      {name:'실적',type:'line',data:[...hist,...Array(fcMonths.length).fill(null)],smooth:true,symbol:'none',
        lineStyle:{color:'#1D68F0',width:2.4},areaStyle:{color:new echarts.graphic.LinearGradient(0,0,0,1,[{offset:0,color:'rgba(29,104,240,0.16)'},{offset:1,color:'rgba(29,104,240,0)'}])}},
      {name:'AI 예측',type:'line',data:meanFull,smooth:true,symbol:'circle',symbolSize:5,
        lineStyle:{color:'#12b3a6',width:2.4,type:'dashed'},itemStyle:{color:'#12b3a6'}},
    ]
  });
}
function treeChart(node){
  const by=S.mapBy;
  let data;
  if(by==='category'){
    const cats={};
    S.tm.leaves.forEach(l=>{ (cats[l.category]??=[]).push(l); });
    data=Object.entries(cats).map(([c,ls])=>({name:c,children:groupBy(ls,'product')}));
  } else {
    const ctry={};
    S.tm.leaves.forEach(l=>{ (ctry[l.country_name]??=[]).push(l); });
    data=Object.entries(ctry).sort((a,b)=>sum(b[1])-sum(a[1])).slice(0,14)
      .map(([c,ls])=>({name:c,children:ls.map(leafNode)}));
  }
  chart(node,{
    textStyle:{fontFamily:FONT},
    tooltip:{formatter:p=>{const d=p.data; return d.yoy==null?`<b>${p.name}</b>`:
      `<b>${d.pn} · ${d.cn}</b><br/>수출 ${usd(d.value)}<br/>전년 ${pct(d.yoy)} · 스코어 ${d.score}`;},
      backgroundColor:'#fff',borderColor:'#E1E6EC',textStyle:{color:'#0C0D11',fontSize:12}},
    series:[{type:'treemap',roam:false,nodeClick:'link',breadcrumb:{show:false},
      width:'100%',height:'100%',top:2,left:2,right:2,bottom:2,
      itemStyle:{borderColor:'#fff',borderWidth:2,gapWidth:2},
      label:{fontFamily:FONT,fontSize:11,fontWeight:600,color:'#fff',overflow:'truncate'},
      upperLabel:{show:true,height:20,color:'#6B7585',fontWeight:700,fontSize:11},
      levels:[{itemStyle:{borderWidth:3,gapWidth:3,borderColor:'#F6F8FA'},upperLabel:{show:false}},
        {itemStyle:{borderWidth:2,gapWidth:2,borderColorSaturation:0.1},upperLabel:{show:true}},
        {itemStyle:{gapWidth:1}}],
      data}]
  });
}
function groupBy(ls,key){ const g={}; ls.forEach(l=>{(g[l[key]]??=[]).push(l);});
  return Object.entries(g).map(([n,arr])=>({name:n,children:arr.map(leafNode)})); }
function leafNode(l){ return {name:cname(l.country)+(l.product?'':''),value:l.value,itemStyle:{color:yoyColor(l.yoy)},
  yoy:l.yoy,score:l.score,pn:l.product,cn:l.country_name,label:{formatter:`{b}`},
  _hs:l.hs,_cc:l.country}; }
function sum(ls){ return ls.reduce((a,l)=>a+l.value,0); }
function countryBar(node,hs){
  const rows=(S.radar.by_product[hs]||[]).slice(0,8);
  chart(node,{ grid:{left:8,right:16,top:8,bottom:8,containLabel:true},textStyle:{fontFamily:FONT},
    tooltip:{trigger:'axis',valueFormatter:v=>usd(v),backgroundColor:'#fff',borderColor:'#E1E6EC',textStyle:{color:'#0C0D11'}},
    xAxis:{type:'value',axisLabel:{color:'#9AA4B2',fontSize:10,formatter:v=>usd(v)},splitLine:{lineStyle:{color:'#EDF0F4'}}},
    yAxis:{type:'category',inverse:true,data:rows.map(r=>cname(r.country)),axisLabel:{color:'#4B5563',fontSize:11},axisTick:{show:false},axisLine:{show:false}},
    series:[{type:'bar',data:rows.map(r=>({value:r.recent12_usd,itemStyle:{color:r.yoy>0?'#1D68F0':'#CBD2DC',borderRadius:[0,4,4,0]}})),barWidth:'62%'}]});
}

/* ---------- market row ---------- */
function marketRow(m,i){
  const s=ser(m.hs,m.country);
  return `<div class="rrow" data-hs="${m.hs}" data-cc="${m.country}">
    ${i!=null?`<span class="rank num">${i+1}</span>`:''}
    <span class="flag">${flag(m.country)}</span>
    <div class="body"><div class="t">${cname(m.country)} · ${m.product||pname(m.hs)}</div>
      <div class="s">${momTag(m.status)} 전년 ${delta(m.yoy)} · 6M ${delta(m.fc_growth6)}</div></div>
    ${s?sparkline(s.hist,72,26,m.yoy>=0):''}
    <div style="text-align:center;min-width:44px"><div class="num" style="font-size:18px;font-weight:800;color:${scoreColor(m.score||60)}">${Math.round(m.score||60)}</div>
      <div class="overline" style="font-size:9px">SCORE</div></div></div>`;
}
function bindRows(root){ root.querySelectorAll('.rrow[data-hs]').forEach(r=>r.onclick=()=>openScore(r.dataset.hs,r.dataset.cc)); }

/* ---------- views ---------- */
function renderCommand(){
  const v=$('#view-command');
  const total=S.countries.countries.reduce((a,c)=>a+c.latest12_usd,0);
  const surge=S.radar.top.filter(t=>t.status==='surge').length;
  const wYoy=S.cat.products.reduce((a,p)=>a+p.yoy*p.latest12_usd,0)/S.cat.products.reduce((a,p)=>a+p.latest12_usd,0);
  const avgScore=Math.round(S.tm.leaves.reduce((a,l)=>a+l.score,0)/S.tm.leaves.length);
  const top=S.radar.top.slice(0,6), rising=[...S.radar.top].sort((a,b)=>b.growth3-a.growth3).slice(0,5);
  const heating=[...S.tm.leaves].sort((a,b)=>b.growth3-a.growth3).slice(0,5);
  v.innerHTML=`<div class="wrap">
    <div class="page-h"><div><div class="overline">COMMAND CENTER</div><h1>수출 기회 커맨드센터</h1>
      <div class="sub">관세청 수출입통계 · 분석기간 ${S.cat.meta.period} · ${S.cat.products.length}개 한류 품목 × ${Object.keys(S.cat.countries).length}개국</div></div>
      <div class="sp"></div><div class="seg" id="cc-range"><button class="on">최근 12개월</button><button>6개월</button></div></div>
    <div class="grid g-4" style="margin-bottom:16px">
      ${stat('database','분석 수출액 (12M)',usd(total),`<span class="delta ${dcls(wYoy)}">${pct(wYoy)}</span> 전년 대비`)}
      ${stat('trending_up','급등 시장',surge+'곳',`<span class="muted">폭발적 성장 감지</span>`)}
      ${stat('speed','평균 Tradar Score',avgScore,`<span class="muted">시장 매력도 종합</span>`)}
      ${stat('warning','리스크 경보',S.radar.risk.length+'곳',`<span class="muted">둔화 조기경보</span>`)}
    </div>
    <div class="grid g-32">
      <div class="card"><div class="card-h"><span class="overline">TOP OPPORTUNITIES</span><span class="ms muted" style="font-size:18px">bookmark_add</span></div>
        <div class="card-b" style="padding:8px" id="cc-top"></div></div>
      <div style="display:flex;flex-direction:column;gap:16px">
        <div class="card"><div class="card-h"><span class="overline">FASTEST RISING</span></div><div class="card-b" style="padding:8px" id="cc-rising"></div></div>
        <div class="card"><div class="card-h"><span class="overline">RISK ALERTS</span><span class="ms" style="font-size:18px;color:var(--cm-neg)">notifications_active</span></div><div class="card-b" style="padding:8px" id="cc-risk"></div></div>
      </div>
    </div>
    <div class="card mt"><div class="card-h"><span class="overline">MARKETS HEATING UP · 최근 3개월 급상승</span></div>
      <div class="card-b" style="padding:8px" id="cc-heat"></div></div>
  </div>`;
  $('#cc-top').innerHTML=top.map((m,i)=>marketRow(m,i)).join('');
  $('#cc-rising').innerHTML=rising.map(m=>marketRow(m)).join('');
  $('#cc-risk').innerHTML=S.radar.risk.slice(0,5).map(m=>riskRow(m)).join('');
  $('#cc-heat').innerHTML=heating.map(m=>marketRow({...m,status:m.momentum,fc_growth6:m.fc6})).join('');
  bindRows(v);
}
function stat(icon,lbl,val,foot){
  return `<div class="stat"><div class="lbl"><span class="ms">${icon}</span>${lbl}</div>
    <div class="val num">${val}</div><div class="foot">${foot}</div></div>`;
}
function riskRow(m){
  return `<div class="rrow" data-hs="${m.hs}" data-cc="${m.country}">
    <span class="flag">${flag(m.country)}</span>
    <div class="body"><div class="t">${cname(m.country)} · ${m.product}</div>
      <div class="s">${momTag('cooling')} 최근3M ${delta(m.growth3)} · ${usdKo(m.recent12_usd)}</div></div>
    <div style="text-align:center;min-width:40px"><div class="num" style="font-size:17px;font-weight:800;color:var(--cm-neg)">${Math.round(m.risk)}</div><div class="overline" style="font-size:9px">RISK</div></div></div>`;
}

function renderMap(){
  const v=$('#view-map');
  const movers=[...S.tm.leaves].sort((a,b)=>Math.abs(b.growth3)-Math.abs(a.growth3)).slice(0,10);
  v.innerHTML=`<div class="wrap">
    <div class="page-h"><div><div class="overline">MARKET MAP · FINVIZ 스타일</div><h1>마켓맵</h1>
      <div class="sub">타일 크기 = 최근 12개월 수출액 · 색 = 전년 대비 증감(초록 상승 / 빨강 둔화)</div></div>
      <div class="sp"></div><div class="seg" id="map-by"><button data-by="category" class="on">품목별</button><button data-by="country">국가별</button></div></div>
    <div class="grid g-32">
      <div class="card" style="padding:6px"><div id="tm" class="chart" style="height:520px"></div></div>
      <div class="card"><div class="card-h"><span class="overline">TOP MOVERS · 최근 3개월</span></div><div class="card-b" style="padding:8px" id="map-movers"></div></div>
    </div></div>`;
  treeChart($('#tm'));
  $('#tm').__ec=S.charts.tm;
  S.charts.tm.on('click',p=>{ if(p.data&&p.data._hs)openScore(p.data._hs,p.data._cc); });
  $('#map-movers').innerHTML=movers.map(m=>marketRow({...m,status:m.momentum,fc_growth6:m.fc6})).join('');
  bindRows(v);
  $('#map-by').querySelectorAll('button').forEach(b=>b.onclick=()=>{
    S.mapBy=b.dataset.by; $('#map-by').querySelectorAll('button').forEach(x=>x.classList.remove('on')); b.classList.add('on'); treeChart($('#tm'));
    S.charts.tm.on('click',p=>{ if(p.data&&p.data._hs)openScore(p.data._hs,p.data._cc); }); });
}

function openScore(hs,cc){ S.product=hs; S.country=cc; nav('score'); }
function renderScore(){
  const v=$('#view-score');
  if(!S.product){ S.product=S.radar.top[0].hs; S.country=S.radar.top[0].country; }
  const hs=S.product, cc=S.country, s=ser(hs,cc);
  const sim=(S.radar.by_product[hs]||[]).filter(m=>m.country!==cc).slice(0,4);
  const inWl=S.watchlist.some(w=>w===hs+'|'+cc);
  v.innerHTML=`<div class="wrap">
    <div class="page-h">
      <div class="flex" style="gap:14px">
        <span style="font-size:40px">${flag(cc)}</span>
        <div><div class="overline">SCORE PROFILE</div><h1 style="display:flex;align-items:center;gap:10px">${cname(cc)} · ${pname(hs)} ${stageTag(s.stage)}</h1>
          <div class="sub">${momTag(s.status)} · 최근 12개월 수출 ${usdKo(s.recent12_usd)} · 예측 적합도 MAPE ${(s.mape*100).toFixed(1)}%</div></div>
      </div><div class="sp"></div>
      <div class="flex">
        <select class="btn ghost" id="sc-hs" style="height:36px">${S.cat.products.map(p=>`<option value="${p.hs}" ${p.hs===hs?'selected':''}>${p.name_ko}</option>`).join('')}</select>
        <select class="btn ghost" id="sc-cc" style="height:36px">${(S.radar.by_product[hs]||[]).map(m=>`<option value="${m.country}" ${m.country===cc?'selected':''}>${cname(m.country)}</option>`).join('')}</select>
        <button class="btn ${inWl?'primary':'ghost'}" id="sc-wl"><span class="ms">${inWl?'bookmark':'bookmark_add'}</span>${inWl?'저장됨':'워치리스트'}</button>
      </div></div>
    <div class="grid g-4" style="margin-bottom:16px">
      ${stat('speed','전년 대비 (YoY)',pct(s.yoy).replace(/^\+?/,m=>s.yoy>=0?'+':''),momTag(s.status))}
      ${stat('insights','향후 6개월 전망',pct(s.fc6),'<span class="muted">전년 동기 대비</span>')}
      ${stat('show_chart','월 추세',pct1(s.trend),'<span class="muted">계절조정 성장률</span>')}
      ${stat('bar_chart','변동성',s.cv.toFixed(2),'<span class="muted">변동계수(CV)</span>')}
    </div>
    <div class="grid g-23">
      <div class="card pad" style="display:flex;flex-direction:column;align-items:center;gap:14px">
        <div class="overline" style="align-self:flex-start">TRADAR SCORE</div>
        ${ring(s.score,128,'/ 100')}
        <div style="width:100%">${subBars(s.sub)}</div>
      </div>
      <div class="card"><div class="card-h"><span class="overline">EXPORT TREND · 실적 + AI 예측(6개월)</span>
        <span class="tag soft-blue">국산 AI · 계절분해+감쇠추세</span></div>
        <div class="card-b"><div id="sc-trend" class="chart"></div></div></div>
    </div>
    <div class="grid g-2 mt">
      <div class="card"><div class="card-h"><span class="overline">TOP COUNTRIES · ${pname(hs)}</span></div><div class="card-b"><div id="sc-bar" class="chart sm"></div></div></div>
      <div class="card"><div class="card-h"><span class="overline">SIMILAR CLUSTER · 함께 보면 좋은 시장</span></div><div class="card-b" style="padding:8px" id="sc-sim"></div></div>
    </div></div>`;
  trendChart($('#sc-trend'),s,S.fc.months,S.fc.fc_months);
  countryBar($('#sc-bar'),hs);
  $('#sc-sim').innerHTML=sim.map(m=>marketRow({...m})).join('');
  bindRows(v);
  $('#sc-hs').onchange=e=>{ S.product=e.target.value; S.country=(S.radar.by_product[S.product]||[])[0].country; renderScore(); };
  $('#sc-cc').onchange=e=>{ S.country=e.target.value; renderScore(); };
  $('#sc-wl').onclick=()=>{ toggleWatch(hs,cc); renderScore(); };
}

function renderDiscovery(){
  const v=$('#view-discovery');
  const cats=['all',...S.cat.categories], f=S.discFilter;
  let rows=S.tm.leaves.filter(l=>f==='all'||l.category===f).sort((a,b)=>b.score-a.score);
  v.innerHTML=`<div class="wrap">
    <div class="page-h"><div><div class="overline">DISCOVERY · RISING INDEX</div><h1>시장 디스커버리</h1>
      <div class="sub">전 품목×국가 ${S.tm.leaves.length}개 시장을 Tradar Score로 정렬 · 필터로 탐색</div></div></div>
    <div class="flex" style="margin-bottom:14px;gap:8px;flex-wrap:wrap">
      ${cats.map(c=>`<button class="btn ${c===f?'primary':'ghost'} f-cat" data-c="${c}" style="height:32px">${c==='all'?'전체':c}</button>`).join('')}</div>
    <div class="card" style="overflow:hidden">
      <div style="max-height:62vh;overflow:auto"><table class="tbl">
        <thead><tr><th>시장</th><th>단계</th><th>모멘텀</th><th class="r">수출(12M)</th><th class="r">전년</th><th class="r">6M 전망</th><th class="r">Score</th></tr></thead>
        <tbody>${rows.map(l=>`<tr data-hs="${l.hs}" data-cc="${l.country}">
          <td><span style="margin-right:6px">${flag(l.country)}</span>${cname(l.country)} · <b>${l.product}</b></td>
          <td>${stageTag(l.stage)}</td><td>${momTag(l.momentum)}</td>
          <td class="r num">${usd(l.value)}</td><td class="r">${delta(l.yoy)}</td><td class="r">${delta(l.fc6)}</td>
          <td class="r num" style="font-weight:800;color:${scoreColor(l.score)}">${Math.round(l.score)}</td></tr>`).join('')}</tbody>
      </table></div></div></div>`;
  v.querySelectorAll('.f-cat').forEach(b=>b.onclick=()=>{S.discFilter=b.dataset.c; renderDiscovery();});
  v.querySelectorAll('tr[data-hs]').forEach(r=>r.onclick=()=>openScore(r.dataset.hs,r.dataset.cc));
}

function renderWatchlist(){
  const v=$('#view-watchlist');
  const items=S.watchlist.map(w=>{const[hs,cc]=w.split('|'); const l=S.tm.leaves.find(x=>x.hs===hs&&x.country===cc); return l;}).filter(Boolean);
  v.innerHTML=`<div class="wrap"><div class="page-h"><div><div class="overline">WATCHLIST</div><h1>워치리스트</h1>
    <div class="sub">관심 시장을 모아 모멘텀·스코어를 추적합니다</div></div></div>
    ${items.length?`<div class="card"><div class="card-b" style="padding:8px" id="wl-list"></div></div>`:
      `<div class="card"><div class="empty"><span class="ms" style="font-size:38px;color:var(--cm-n-300)">bookmark</span><br>아직 저장한 시장이 없습니다.<br>스코어 화면에서 ‘워치리스트’를 눌러 추가하세요.</div></div>`}</div>`;
  if(items.length){ $('#wl-list').innerHTML=items.map(m=>marketRow({...m,status:m.momentum,fc_growth6:m.fc6})).join(''); bindRows(v); }
}

function renderSettings(){
  const v=$('#view-settings');
  v.innerHTML=`<div class="wrap"><div class="page-h"><div><div class="overline">SETTINGS</div><h1>설정</h1></div></div>
    <div class="grid g-2">
      <div class="card"><div class="card-h"><span class="overline">DATA SOURCES · 데이터 출처</span></div><div class="card-b">
        <div class="flex" style="justify-content:space-between;padding:8px 0"><div><b>관세청 품목별 국가별 수출입실적</b><div class="muted" style="font-size:12px">공공데이터포털 · nitemtrade OpenAPI</div></div><span class="mom surge">연결됨</span></div>
        <div class="hairline"></div>
        <div class="flex" style="justify-content:space-between;padding:8px 0"><div><b>국산 AI 엔진</b><div class="muted" style="font-size:12px">수요예측·조기경보·스코어 (자체 개발)</div></div><span class="mom surge">활성</span></div>
        <div class="hairline"></div>
        <div class="flex" style="justify-content:space-between;padding:8px 0"><div><b>AI 무역참모 LLM</b><div class="muted" style="font-size:12px">국산 LLM(Solar·HyperCLOVA X) 연동 구조</div></div><span class="tag">데모 NLG</span></div>
      </div></div>
      <div class="card"><div class="card-h"><span class="overline">PLAN · 요금제</span></div><div class="card-b">
        <div class="flex" style="gap:14px"><div>${ring(100,72,'PRO')}</div><div><b style="font-size:18px">Tradar Pro</b><div class="muted">전 품목·국가 스코어 무제한 · 조기경보 · AI 상담 무제한</div></div></div>
        <div class="hairline"></div>
        <div class="muted" style="font-size:12px">데이터 기준월 ${S.cat.meta.period.split(' ~ ')[1]} · ${S.cat.meta.note}</div>
      </div></div>
    </div></div>`;
}

/* ---------- AI advisor ---------- */
const PKW={'1902.30':['라면','즉석면','면','noodle'],'1212.21':['김','조미김','마른김','laver','seaweed'],'3304.99':['화장품','뷰티','코스메틱','beauty'],'2005.99':['김치','kimchi'],'2103.90':['고추장','장류','소스','sauce'],'1905.31':['과자','제과','스낵','snack'],'2202.99':['음료','주스','beverage'],'2208.90':['소주','술','주류','soju'],'0810.10':['딸기','strawberry'],'0806.10':['포도','샤인','grape'],'1211.20':['인삼','홍삼','ginseng'],'1901.90':['즉석밥','떡','쌀가공']};
const CKW={US:['미국','usa'],JP:['일본','japan'],CN:['중국','china'],VN:['베트남','vietnam'],TH:['태국','thailand'],ID:['인도네시아'],MY:['말레이시아'],PH:['필리핀'],TW:['대만'],HK:['홍콩'],SG:['싱가포르'],AU:['호주'],AE:['아랍','두바이'],SA:['사우디'],FR:['프랑스'],DE:['독일'],GB:['영국','uk'],NL:['네덜란드'],CA:['캐나다'],MX:['멕시코'],IN:['인도'],MN:['몽골'],RU:['러시아'],BR:['브라질']};
function intent(q){ const s=q.toLowerCase().replace(/\s/g,''); let hs=null,cc=null;
  for(const[k,w]of Object.entries(PKW))if(w.some(x=>s.includes(x.replace(/\s/g,'')))){hs=k;break;}
  for(const[k,w]of Object.entries(CKW))if(w.some(x=>s.includes(x))){cc=k;break;}
  let it; if(/(위험|리스크|둔화|경보|빠지)/.test(s))it='risk'; else if(cc&&hs)it='forecast';
  else if(/(어디|어느나라|추천|유망|확대|신규|뚫)/.test(s)||hs)it='recommend'; else it='overview';
  return{hs,cc,it}; }
function advisorAnswer(q){ const {hs,cc,it}=intent(q); let head='',ev=[],chart=null,sug=[];
  if(it==='forecast'&&hs&&cc){ const s=ser(hs,cc);
    if(!s){head=`${cname(cc)}의 ${pname(hs)} 데이터를 찾지 못했어요.`;}
    else{ head=`${cname(cc)} ${pname(hs)} 시장은 현재 '${MOM[s.status].ko}' 국면입니다. Tradar Score ${Math.round(s.score)}점(${STAGE[s.stage]}), 최근 12개월 수출은 전년 대비 ${pct(s.yoy)}, 향후 6개월은 전년 동기 대비 ${pct(s.fc6)} 전망입니다.`;
      ev=[['Tradar Score',Math.round(s.score)+' / 100'],['최근 12개월 수출',usdKo(s.recent12_usd)],['전년 대비(YoY)',pct(s.yoy)],['향후 6개월 전망',pct(s.fc6)],['예측 적합도(MAPE)',(s.mape*100).toFixed(1)+'%']];
      chart={hs,cc}; sug=[`${pname(hs)} 어디에 더 수출할까?`,`${cname(cc)} 위험 시장은?`]; } }
  else if(it==='recommend'){ const rows=hs?(S.radar.by_product[hs]||[]).slice(0,5):S.radar.top.slice(0,6); const t=rows[0];
    head=hs?`${pname(hs)} 수출 확대라면 지금은 '${cname(t.country)}'이 1순위입니다. Tradar Score ${Math.round(t.score)}점, 전년 ${pct(t.yoy)}, 6개월 ${pct(t.fc_growth6)} 전망.`
      :`지금 가장 유망한 한류 수출 시장은 '${cname(t.country)}의 ${t.product}'입니다 (Score ${Math.round(t.score)}, 전년 ${pct(t.yoy)}).`;
    ev=rows.map((r,i)=>[`${i+1}. ${cname(r.country)}${hs?'':' · '+r.product}`,`Score ${Math.round(r.score)} · ${pct(r.yoy)} · ${MOM[r.status].ko}`]);
    if(hs){chart={hs,cc:t.country};} sug=['위험한 시장 알려줘','화장품 미국 예측']; }
  else if(it==='risk'){ const rows=S.radar.risk.slice(0,6); const t=rows[0];
    head=t?`리스크 조기경보: '${cname(t.country)}의 ${t.product}'이 식고 있습니다 (최근 3개월 ${pct(t.growth3)}, 규모 ${usdKo(t.recent12_usd)}). 의존도가 높다면 시장 다변화를 권장합니다.`:'현재 둔화 경보는 없습니다.';
    ev=rows.map(r=>[`⚠ ${cname(r.country)} · ${r.product}`,`3M ${pct(r.growth3)} · ${usdKo(r.recent12_usd)}`]); sug=['떠오르는 시장 추천','라면 어디에 수출할까?']; }
  else{ const o=S.radar.top.slice(0,3); head=`Tradar는 관세청 수출입통계로 한류 품목의 국가별 시장을 Tradar Score로 평가하고 예측합니다. 품목과 나라를 말씀해 보세요.`;
    ev=o.map(r=>[`${cname(r.country)} · ${r.product}`,`Score ${Math.round(r.score)} · ${pct(r.yoy)}`]); sug=['라면 어디에 수출할까?','화장품 미국 예측','위험한 시장은?']; }
  return {head,ev,chart,sug}; }
function renderAdvisor(){
  const v=$('#view-advisor');
  v.innerHTML=`<div class="chat-wrap"><div class="chat-scroll" id="chat"><div class="chat-inner" id="chat-inner"></div></div>
    <div class="chat-composer"><div class="chat-inner"><div class="suggest" id="sugg"></div>
      <div class="box"><span class="ms muted">auto_awesome</span><input id="chat-in" placeholder="예) 라면 어디에 수출하면 좋을까?" autocomplete="off"><button class="btn primary" id="chat-send" style="height:38px">전송 <span class="ms">arrow_upward</span></button></div></div></div></div>`;
  const inner=$('#chat-inner');
  if(!S.chat.length){ S.chat.push(1);
    bubble('ai',`안녕하세요, AI 무역참모 <b>바람이</b>예요. 🌬️\n관세청 수출입통계로 한류 품목의 수출 시장을 <b>Tradar Score</b>와 예측으로 분석해 드려요. 품목과 나라를 말씀해 보세요!`);
    suggest(['라면 어디에 수출하면 좋을까?','화장품 미국 수요 예측','위험한 시장 알려줘']); }
  else inner.innerHTML=S._chatHtml||'';
  $('#chat-send').onclick=()=>{const i=$('#chat-in'); ask(i.value); i.value='';};
  $('#chat-in').addEventListener('keydown',e=>{if(e.key==='Enter')$('#chat-send').click();});
}
function bubble(role,html){ const c=$('#chat-inner'); const b=el('div','bub '+role,html); c.appendChild(b); S._chatHtml=c.innerHTML; const sc=$('#chat'); sc.scrollTop=sc.scrollHeight; }
function suggest(list){ const s=$('#sugg'); if(!s)return; s.innerHTML=list.map(q=>`<button>${q}</button>`).join(''); s.querySelectorAll('button').forEach(b=>b.onclick=()=>ask(b.textContent)); }
function ask(q){ if(!q.trim())return; bubble('me',q); const r=advisorAnswer(q); let html=r.head;
  if(r.chart){ html+=`<div id="ac${RINGID}" style="height:220px;margin-top:12px"></div>`; }
  if(r.ev.length)html+=`<div class="evid">${r.ev.map(e=>`<div class="e"><span>${e[0]}</span><b>${e[1]}</b></div>`).join('')}</div>`;
  bubble('ai',html);
  if(r.chart){ const node=$('#chat-inner').lastChild.querySelector('div[id^=ac]'); if(node){node.id='ac'+(RINGID++); trendChart(node,ser(r.chart.hs,r.chart.cc),S.fc.months,S.fc.fc_months);} }
  suggest(r.sug); }

/* ---------- watchlist ---------- */
function loadWatch(){ try{S.watchlist=JSON.parse(localStorage.getItem('tdr-wl')||'[]');}catch(e){S.watchlist=[];} updateWlCount(); }
function toggleWatch(hs,cc){ const k=hs+'|'+cc; const i=S.watchlist.indexOf(k); if(i>=0)S.watchlist.splice(i,1); else S.watchlist.push(k);
  localStorage.setItem('tdr-wl',JSON.stringify(S.watchlist)); updateWlCount(); }
function updateWlCount(){ const b=$('#wl-count'); if(!b)return; b.textContent=S.watchlist.length; b.style.display=S.watchlist.length?'inline-block':'none'; }

/* ---------- command palette ---------- */
function openPalette(){ $('#pal-scrim').classList.add('open'); $('#pal').classList.add('open'); const i=$('#pal-input'); i.value=''; palList(''); setTimeout(()=>i.focus(),20); }
function closePalette(){ $('#pal-scrim').classList.remove('open'); $('#pal').classList.remove('open'); }
function palList(q){ q=q.toLowerCase(); const out=[];
  const views=[['space_dashboard','커맨드센터','command'],['grid_view','마켓맵','map'],['insights','스코어 분석','score'],['travel_explore','디스커버리','discovery'],['auto_awesome','AI 무역참모','advisor'],['bookmark','워치리스트','watchlist'],['settings','설정','settings']];
  views.filter(v=>v[1].toLowerCase().includes(q)).forEach(v=>out.push({icon:v[0],name:v[1],meta:'이동',act:()=>nav(v[2])}));
  if(q.length>=1){ S.tm.leaves.filter(l=>(cname(l.country)+l.product).toLowerCase().includes(q)).slice(0,8)
    .forEach(l=>out.push({icon:'insights',name:`${cname(l.country)} · ${l.product}`,meta:`Score ${Math.round(l.score)}`,act:()=>openScore(l.hs,l.country)})); }
  const list=$('#pal-list'); list.innerHTML=out.slice(0,10).map((o,i)=>`<div class="p-item ${i===0?'sel':''}" data-i="${i}"><span class="ms">${o.icon}</span>${o.name}<span class="meta">${o.meta}</span></div>`).join('')||'<div class="empty">결과 없음</div>';
  list.querySelectorAll('.p-item').forEach(it=>it.onclick=()=>{ out[+it.dataset.i].act(); closePalette(); });
  S._pal=out; }

/* ---------- nav / boot ---------- */
function nav(view){ S.view=view;
  document.querySelectorAll('.view').forEach(v=>v.classList.remove('active'));
  $('#view-'+view).classList.add('active');
  document.querySelectorAll('.nav-item').forEach(n=>n.classList.toggle('active',n.dataset.view===view));
  ({command:renderCommand,map:renderMap,score:renderScore,discovery:renderDiscovery,advisor:renderAdvisor,watchlist:renderWatchlist,settings:renderSettings}[view])();
  $('#content').scrollTop=0;
  Object.values(S.charts).forEach(c=>{try{c.resize();}catch(e){}});
}
async function boot(){
  try{
    const [c,f,r,t,ct]=await Promise.all(['catalog','forecast','radar','treemap','countries'].map(n=>fetch('data/'+n+'.json').then(x=>x.json())));
    S.cat=c;S.fc=f;S.radar=r;S.tm=t;S.countries=ct;
    loadWatch();
    document.querySelectorAll('.nav-item').forEach(n=>n.onclick=()=>nav(n.dataset.view));
    $('#search-trigger').onclick=openPalette;
    $('#pal-scrim').onclick=closePalette;
    $('#pal-input').oninput=e=>palList(e.target.value);
    $('#pal-input').onkeydown=e=>{ if(e.key==='Escape')closePalette(); if(e.key==='Enter'&&S._pal&&S._pal[0]){S._pal[0].act();closePalette();} };
    $('#btn-alerts').onclick=()=>nav('command');
    $('#btn-share').onclick=share;
    document.addEventListener('keydown',e=>{ if((e.metaKey||e.ctrlKey)&&e.key.toLowerCase()==='k'){e.preventDefault();openPalette();} });
    window.addEventListener('resize',()=>Object.values(S.charts).forEach(c=>{try{c.resize();}catch(e){}}));
    // 딥링크(시연·캡처용): #view 또는 #score?hs=..&cc=..
    const h=location.hash.slice(1);
    if(h){ const [view,qs]=h.split('?'); const p=new URLSearchParams(qs||'');
      if(p.get('hs')){S.product=p.get('hs');S.country=p.get('cc');}
      if(p.get('q')) S._askOnLoad=p.get('q');
      nav(['command','map','score','discovery','advisor','watchlist','settings'].includes(view)?view:'command');
      if(S._askOnLoad&&view==='advisor') setTimeout(()=>ask(S._askOnLoad),80);
    } else nav('command');
  }catch(e){ $('#content').innerHTML='<div class="wrap"><div class="card pad">데이터를 불러오지 못했습니다. <code>scripts/build_app_data.py</code> 실행을 확인하세요.<br><small>'+e+'</small></div></div>'; }
  if('serviceWorker'in navigator)navigator.serviceWorker.register('sw.js').catch(()=>{});
}
function share(){ const url=location.href; if(navigator.share)navigator.share({title:'Tradar',url}).catch(()=>{}); else{navigator.clipboard&&navigator.clipboard.writeText(url); alert('링크가 복사되었습니다: '+url);} }
boot();
