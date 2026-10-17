import React, { useEffect, useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { Search, ShoppingBag, Store, UserRound, LogOut, Package, Tag, ArrowLeft, Plus, X, Menu, LoaderCircle, CircleAlert, CheckCircle2 } from 'lucide-react';
import './styles.css';

const API = '/api';
function readToken(){ return localStorage.getItem('market_access') || ''; }
async function api(path, options={}) {
  const headers = {'Content-Type':'application/json', ...(options.headers||{})};
  const token = readToken();
  if(token) headers.Authorization = `Bearer ${token}`;
  const response = await fetch(`${API}${path}`, {...options, headers});
  const raw = await response.text();
  let data = null; try { data = raw ? JSON.parse(raw) : null; } catch { data = raw; }
  if(!response.ok) {
    if(response.status===401) throw new Error('برای این عملیات وارد حساب کاربری شوید.');
    const message = typeof data === 'object' && data ? Object.entries(data).map(([k,v])=>`${k}: ${Array.isArray(v)?v.join(' '):v}`).join(' | ') : `خطای ${response.status}`;
    throw new Error(message || 'درخواست انجام نشد');
  }
  return data;
}
function App(){
  const [page,setPage]=useState('products');
  const [products,setProducts]=useState([]);
  const [categories,setCategories]=useState([]);
  const [sellers,setSellers]=useState([]);
  const [orders,setOrders]=useState([]);
  const [offers,setOffers]=useState([]);
  const [query,setQuery]=useState('');
  const [loading,setLoading]=useState(true);
  const [error,setError]=useState('');
  const [notice,setNotice]=useState('');
  const [token,setToken]=useState(readToken());
  const [modal,setModal]=useState('');
  const [selected,setSelected]=useState(null);
  const [busy,setBusy]=useState(false);
  const [mobileNav,setMobileNav]=useState(false);
  const [cart,setCart]=useState(()=>{try{return JSON.parse(localStorage.getItem('market_cart')||'[]')}catch{return[]}});
  const [form,setForm]=useState({});
  const [username,setUsername]=useState('');
  const [password,setPassword]=useState('');
  const [categoryFilter,setCategoryFilter]=useState('all');
  const [tab,setTab]=useState('all');

  const load=async()=>{
    setLoading(true); setError('');
    const jobs=[
      api('/products/').then(d=>setProducts(Array.isArray(d)?d:(d.results||[]))).catch(e=>setError(e.message)),
      api('/categories/').then(d=>setCategories(Array.isArray(d)?d:(d.results||[]))).catch(()=>setCategories([])),
      api('/seller-profiles/').then(d=>setSellers(Array.isArray(d)?d:(d.results||[]))).catch(()=>setSellers([])),
    ];
    if(readToken()){
      jobs.push(api('/order/').then(d=>setOrders(Array.isArray(d)?d:(d.results||[]))).catch(()=>setOrders([])));
      jobs.push(api('/offers/').then(d=>setOffers(Array.isArray(d)?d:(d.results||[]))).catch(()=>setOffers([])));
    }
    await Promise.all(jobs); setLoading(false);
  };
  useEffect(()=>{load()},[]);
  useEffect(()=>{localStorage.setItem('market_cart',JSON.stringify(cart))},[cart]);
  const filtered=useMemo(()=>products.filter(p=>(`${p.title||''} ${p.description||''}`).toLowerCase().includes(query.toLowerCase()) && (categoryFilter==='all'||String(p.category)===String(categoryFilter))),[products,query,categoryFilter]);
  const notify=(s)=>{setNotice(s);setTimeout(()=>setNotice(''),3500)};
  const updateForm=(k,v)=>setForm(p=>({...p,[k]:v}));
  const login=async(e)=>{e.preventDefault();setBusy(true);setError('');try{const d=await api('/access/',{method:'POST',body:JSON.stringify({username,password})});localStorage.setItem('market_access',d.access);localStorage.setItem('market_refresh',d.refresh);setToken(d.access);setModal('');setPassword('');notify('با موفقیت وارد شدی');await load()}catch(e){setError(e.message)}finally{setBusy(false)}};
  const logout=()=>{localStorage.removeItem('market_access');localStorage.removeItem('market_refresh');setToken('');setOrders([]);setOffers([]);notify('از حساب خارج شدی')};
  const submitCreate=async(e)=>{e.preventDefault();setBusy(true);setError('');try{
    let path='',body={...form};
    if(modal==='product'){path='/products/';body={title:form.title,description:form.description,category:Number(form.category)}}
    if(modal==='seller'){path='/seller-profiles/';body={store_name:form.store_name,description:form.description}}
    if(modal==='category'){path='/categories/';body={name:form.name,description:form.description||''}}
    if(modal==='offer'){path='/offers/';body={...form}}
    await api(path,{method:'POST',body:JSON.stringify(body)});setModal('');setForm({});notify('با موفقیت ثبت شد');await load();
  }catch(e){setError(e.message)}finally{setBusy(false)}};
  const createOrder=async(product)=>{if(!token){setModal('login');return}setSelected(product);setModal('order');setForm({product:product.id||'',quantity:1})};
  const sendOrder=async(e)=>{e.preventDefault();setBusy(true);setError('');try{await api('/order/',{method:'POST',body:JSON.stringify(form)});setModal('');notify('سفارش ثبت شد');await load()}catch(e){setError(e.message)}finally{setBusy(false)}};
  const addToCart=(p)=>{setCart(old=>[...old,{...p,cartId:Date.now()+Math.random()}]);notify('به سبد خرید اضافه شد')};
  const nav=[['products','محصولات',Package],['sellers','فروشگاه‌ها',Store],['offers','پیشنهادها',Tag],['orders','سفارش‌های من',ShoppingBag]];
  const openModal=(name)=>{setError('');setForm({});setModal(name)};
  const categoryName=(id)=>categories.find(c=>String(c.id)===String(id))?.name || `دسته ${id??'عمومی'}`;
  return <div className="app-shell">
    <header className="topbar"><button className="icon-btn mobile-only" onClick={()=>setMobileNav(!mobileNav)}><Menu/></button><button className="brand" onClick={()=>setPage('products')}><span className="brand-mark">M</span><span>MARKET<small>بازار تو، انتخاب تو</small></span></button>
      <div className="searchbox"><Search size={19}/><input value={query} onChange={e=>setQuery(e.target.value)} placeholder="دنبال چی می‌گردی؟"/></div>
      <div className="top-actions"><button className="icon-btn cart-btn" onClick={()=>setPage('cart')} aria-label="سبد خرید"><ShoppingBag/><span className="count">{cart.length}</span></button>{token?<button className="user-btn" onClick={logout}><LogOut size={17}/> خروج</button>:<button className="primary-btn login-btn" onClick={()=>openModal('login')}><UserRound size={17}/> ورود</button>}</div>
    </header>
    <div className="hero"><div className="hero-copy"><span className="eyebrow">MARKETPLACE · بازار آنلاین</span><h1>چیزی که می‌خوای،<br/><em>همین‌جاست.</em></h1><p>محصولات رو کشف کن، فروشگاهت رو بساز و خریدت رو ساده‌تر انجام بده.</p><button className="light-btn" onClick={()=>{setPage('products');document.getElementById('catalog')?.scrollIntoView({behavior:'smooth'})}}>دیدن محصولات <ArrowLeft size={17}/></button></div><div className="hero-art"><div className="orb orb-one"/><div className="orb orb-two"/><div className="floating-card card-a"><span className="mini-icon">✦</span><div><b>انتخاب هوشمند</b><small>چیزی برای هر سلیقه</small></div></div><div className="shopping-illustration"><ShoppingBag size={102} strokeWidth={1.15}/><span className="spark spark1">✦</span><span className="spark spark2">✧</span></div><div className="floating-card card-b"><span className="green-dot"/> تجربه خرید ساده</div></div></div>
    <main className="main-layout"><aside className={`sidebar ${mobileNav?'show':''}`}><div className="side-label">منوی اصلی</div>{nav.map(([id,label,Icon])=><button key={id} className={`nav-item ${page===id?'active':''}`} onClick={()=>{setPage(id);setMobileNav(false)}}><Icon size={19}/>{label}{id==='cart'&&<span>{cart.length}</span>}</button>)}<button className={`nav-item ${page==='cart'?'active':''}`} onClick={()=>setPage('cart')}><ShoppingBag size={19}/>سبد خرید <span>{cart.length}</span></button><div className="side-divider"/><div className="side-label">مدیریت فروشگاه</div><button className="nav-item" onClick={()=>token?openModal('seller'):openModal('login')}><Store size={19}/>ساخت فروشگاه</button><button className="nav-item" onClick={()=>token?openModal('product'):openModal('login')}><Plus size={19}/>افزودن محصول</button><div className="sidebar-bottom"><div className="help-mark">?</div><b>کمکی لازم داری؟</b><p>برای مدیریت فروشگاه ابتدا وارد حساب شو.</p>{!token&&<button onClick={()=>openModal('login')}>ورود به حساب <ArrowLeft size={15}/></button>}</div></aside>
      <section className="content" id="catalog"><div className="section-head"><div><span className="section-kicker">برای تو آماده شده</span><h2>{page==='products'?'محصولات منتخب':page==='sellers'?'فروشگاه‌های بازار':page==='offers'?'پیشنهادهای ویژه':page==='orders'?'سفارش‌های من':page==='cart'?'سبد خرید':'بازار'}</h2><p>{page==='products'?'محصولات رو بگرد و انتخابت رو پیدا کن.':'همه چیز رو یک‌جا مدیریت کن.'}</p></div>{page==='products'&&<button className="outline-btn" onClick={()=>openModal('category')}><Plus size={16}/> دسته جدید</button>}</div>
      {page==='products'&&<><div className="filter-row"><div className="chips"><button className={categoryFilter==='all'?'chip selected':'chip'} onClick={()=>setCategoryFilter('all')}>همه محصولات</button>{categories.map((c,i)=><button key={c.id||i} className={String(categoryFilter)===String(c.id)?'chip selected':'chip'} onClick={()=>setCategoryFilter(String(c.id))}>{c.name}</button>)}</div><span className="result-count">{filtered.length} محصول</span></div>
        {loading?<div className="loading"><LoaderCircle className="spin"/> در حال دریافت محصولات...</div>:error&&!products.length?<div className="empty"><CircleAlert/><h3>ارتباط با API برقرار نشد</h3><p>{error}</p><button className="primary-btn" onClick={load}>تلاش دوباره</button></div>:filtered.length?<div className="product-grid">{filtered.map((p,i)=><article className="product-card" key={p.id||i}><div className={`product-visual visual-${i%6}`}><span className="product-category">{categoryName(p.category)}</span><div className="product-symbol">{['◈','✳','⬡','◉','✦','◇'][i%6]}</div><button className="quick-add" onClick={()=>addToCart(p)} title="افزودن به سبد"><Plus size={19}/></button></div><div className="product-info"><span className="product-overline">MARKET SELECTION</span><h3>{p.title}</h3><p>{p.description||'توضیحی برای این محصول ثبت نشده است.'}</p><div className="product-foot"><span className="no-price">قیمت در اطلاعات API ثبت نشده</span><button onClick={()=>createOrder(p)} className="buy-btn">ثبت سفارش <ArrowLeft size={15}/></button></div></div></article>)}</div>:<div className="empty"><Package/><h3>هنوز محصولی ثبت نشده</h3><p>اگر به حساب کاربری دسترسی داری، اولین محصول رو اضافه کن.</p><button className="primary-btn" onClick={()=>token?openModal('product'):openModal('login')}><Plus size={16}/> افزودن محصول</button></div>}</>}
      {page==='sellers'&&<div className="seller-grid">{sellers.length?sellers.map((s,i)=><article className="seller-card" key={s.id||i}><div className="seller-avatar"><Store/></div><div><h3>{s.store_name}</h3><p>{s.description||'فروشگاه فعال در بازار MARKET'}</p><small>شناسه فروشگاه: {s.id}</small></div></article>):<div className="empty"><Store/><h3>فروشگاهی برای نمایش نیست</h3><p>برای دیدن فروشگاه‌ها وارد حساب شو یا بعداً دوباره امتحان کن.</p></div>}</div>}
      {page==='offers'&&<div className="simple-list">{offers.length?offers.map((o,i)=><article className="list-card" key={o.id||i}><div className="list-icon"><Tag/></div><div><b>{o.title||`پیشنهاد شماره ${o.id||i+1}`}</b><p>{o.description||JSON.stringify(o)}</p></div></article>):<div className="empty"><Tag/><h3>پیشنهادی موجود نیست</h3><p>برای نمایش پیشنهادها باید وارد حساب شده باشی و داده‌ای در API ثبت شده باشد.</p><button className="primary-btn" onClick={()=>token?openModal('offer'):openModal('login')}>افزودن پیشنهاد</button></div>}</div>}
      {page==='orders'&&<div className="simple-list">{!token?<div className="empty"><UserRound/><h3>برای دیدن سفارش‌ها وارد شو</h3><button className="primary-btn" onClick={()=>openModal('login')}>ورود</button></div>:orders.length?orders.map((o,i)=><article className="list-card" key={o.id||i}><div className="list-icon"><ShoppingBag/></div><div><b>سفارش #{o.id||i+1}</b><p>{JSON.stringify(o)}</p></div><span className="status-pill">{o.status||'ثبت‌شده'}</span></article>):<div className="empty"><Package/><h3>هنوز سفارشی نداری</h3><p>وقتی سفارشی ثبت کنی، اینجا نمایش داده می‌شه.</p></div>}</div>}
      {page==='cart'&&<div className="cart-panel">{cart.length? <>{cart.map((p,i)=><div className="cart-line" key={p.cartId}><div className="cart-thumb">{['◈','✳','⬡'][i%3]}</div><div className="cart-title"><b>{p.title}</b><small>{categoryName(p.category)}</small></div><button className="icon-btn" onClick={()=>setCart(c=>c.filter(x=>x.cartId!==p.cartId))}><X/></button></div>)}<div className="cart-note">برای ثبت سفارش، هر محصول را از دکمه «ثبت سفارش» ارسال کن؛ API فعلی برای ساخت سفارش ممکن است شناسه‌های خاصی نیاز داشته باشد.</div><button className="primary-btn" onClick={()=>{setPage('products');notify('برای ثبت سفارش، محصول را انتخاب کن')}}>ادامه خرید <ArrowLeft size={17}/></button><button className="text-btn" onClick={()=>setCart([])}>خالی کردن سبد</button></>:<div className="empty"><ShoppingBag/><h3>سبدت فعلاً خالیه</h3><p>محصولات مورد علاقه‌ات رو به سبد اضافه کن.</p><button className="primary-btn" onClick={()=>setPage('products')}>رفتن به محصولات</button></div>}</div>}
      </section></main>
    <footer className="footer"><div className="brand footer-brand"><span className="brand-mark">M</span><span>MARKET<small>بازار تو، انتخاب تو</small></span></div><span>بازار آنلاین MARKET · ساخته‌شده با Django و React</span><a href="/admin/" target="_blank" rel="noreferrer">مدیریت سایت</a></footer>
    {notice&&<div className="toast"><CheckCircle2 size={18}/>{notice}</div>}
    {modal&&<div className="modal-backdrop" onClick={()=>{setModal('');setError('')}}><section className="modal" onClick={e=>e.stopPropagation()}><button className="modal-close" onClick={()=>setModal('')}><X/></button><span className="section-kicker">MARKET ACCOUNT</span><h2>{({login:'ورود به حساب کاربری',product:'افزودن محصول',seller:'ساخت فروشگاه',category:'ساخت دسته‌بندی',offer:'ثبت پیشنهاد',order:'ثبت سفارش'})[modal]||'ادامه'}</h2><p className="modal-sub">{modal==='login'?'با اطلاعات حساب Django خود وارد شو.':'اطلاعات رو وارد کن تا به API ارسال بشه.'}</p>{error&&<div className="error-box"><CircleAlert size={17}/>{error}</div>}
      {modal==='login'?<form onSubmit={login} className="form-stack"><label>نام کاربری<input required value={username} onChange={e=>setUsername(e.target.value)} autoComplete="username"/></label><label>رمز عبور<input required type="password" value={password} onChange={e=>setPassword(e.target.value)} autoComplete="current-password"/></label><button disabled={busy} className="primary-btn full-btn">{busy?'در حال ورود...':'ورود'}</button></form>:
      modal==='order'?<form onSubmit={sendOrder} className="form-stack"><label>شناسه محصول<input required value={form.product||''} onChange={e=>updateForm('product',e.target.value)}/></label><label>تعداد<input type="number" min="1" required value={form.quantity||1} onChange={e=>updateForm('quantity',Number(e.target.value))}/></label><p className="form-hint">ساختار دقیق سفارش به Serializer بک‌اند بستگی دارد؛ در صورت خطا، پیام API نمایش داده می‌شود.</p><button disabled={busy} className="primary-btn full-btn">{busy?'در حال ثبت...':'ثبت سفارش'}</button></form>:
      <form onSubmit={submitCreate} className="form-stack">{modal==='product'&&<><label>نام محصول<input required value={form.title||''} onChange={e=>updateForm('title',e.target.value)}/></label><label>توضیحات<textarea required value={form.description||''} onChange={e=>updateForm('description',e.target.value)}/></label><label>دسته‌بندی<select required value={form.category||''} onChange={e=>updateForm('category',e.target.value)}><option value="">انتخاب کن</option>{categories.map(c=><option value={c.id} key={c.id}>{c.name}</option>)}</select></label></>}
      {modal==='seller'&&<><label>نام فروشگاه<input required value={form.store_name||''} onChange={e=>updateForm('store_name',e.target.value)}/></label><label>توضیحات<textarea value={form.description||''} onChange={e=>updateForm('description',e.target.value)}/></label></>}
      {modal==='category'&&<><label>نام دسته‌بندی<input required value={form.name||''} onChange={e=>updateForm('name',e.target.value)}/></label><label>توضیحات<textarea value={form.description||''} onChange={e=>updateForm('description',e.target.value)}/></label></>}
      {modal==='offer'&&<><label>عنوان پیشنهاد<input required value={form.title||''} onChange={e=>updateForm('title',e.target.value)}/></label><label>توضیحات<textarea value={form.description||''} onChange={e=>updateForm('description',e.target.value)}/></label><label>شناسه محصول<input value={form.product||''} onChange={e=>updateForm('product',e.target.value)}/></label></>}
      <button disabled={busy} className="primary-btn full-btn">{busy?'در حال ارسال...':'ثبت اطلاعات'}</button></form>}</section></div>}
  </div>
}
createRoot(document.getElementById('root')).render(<App/>);
