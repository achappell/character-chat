!function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.crossOrigin="anonymous",p.async=!0,p.src=s.api_host.replace(".i.posthog.com","-assets.i.posthog.com")+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+" (stub)"},o="init be fs capture alias people.set people.set_once set_config register unregister opt_out_capturing has_opted_out_capturing opt_in_capturing reset isFeatureEnabled onFeatureFlags getFeatureFlag getFeatureFlagPayload reloadFeatureFlags group updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures getActiveMatchingSurveys getSurveys getNextSurveyStep onSessionId setPersonProperties".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);posthog.init('phc_yjPP45JJRToxqNjjoPZfDeSvAZhxEDhnjpXmaq82Tiue',{api_host:'https://us.i.posthog.com',person_profiles:'identified_only'});

(function () {
  const AVATARS = ['🦊','🐼','🐸','🦄','🐯','🦁','🐻','🐨','🐱','🐶','🐰','🐧','🌟','🦋','🎮'];

  const ls   = k => localStorage.getItem(k) || '';
  const prov = () => ls('cc_provider') || window.CC_PROVIDER || 'anthropic';
  const model= () => ls('cc_local_model') || window.CC_LOCAL_MODEL || 'Local';
  const name = () => ls('cc_profile_name');
  const emo  = () => ls('cc_profile_emoji');

  const isIndex = location.pathname === '/' ||
                  location.pathname.endsWith('/index.html') ||
                  location.pathname.endsWith('/character-chat/');

  // ── Styles ──────────────────────────────────────────────────────────────
  const style = document.createElement('style');
  style.textContent = `
  #sh {
    position: fixed; top: 0; left: 0; right: 0; height: 52px; z-index: 200;
    background: rgba(255,255,255,0.92); backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border-bottom: 1px solid rgba(0,0,0,0.07);
    display: flex; align-items: center; padding: 0 14px; gap: 8px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  }
  #sh-home {
    font-size: 13px; font-weight: 600; color: #5b6ef5;
    background: none; border: none; cursor: pointer;
    text-decoration: none; padding: 6px 8px; border-radius: 8px; flex-shrink: 0;
    display: flex; align-items: center; gap: 3px;
  }
  #sh-home:active { background: #eef0ff; }
  #sh-spacer { flex: 1; }
  #sh-profile {
    display: flex; align-items: center; gap: 5px;
    background: #f0f4ff; border: none; border-radius: 20px;
    padding: 5px 10px 5px 7px; cursor: pointer;
    font-size: 13px; font-weight: 600; color: #1a1a2e;
    white-space: nowrap;
  }
  #sh-profile:active { background: #dde3ff; }
  #sh-provider {
    display: flex; align-items: center; gap: 5px;
    border: none; border-radius: 20px;
    padding: 5px 10px; cursor: pointer;
    font-size: 12px; font-weight: 600;
    text-decoration: none; white-space: nowrap; flex-shrink: 0;
  }
  #sh-provider.cloud { background: #eef0ff; color: #5b6ef5; }
  #sh-provider.local { background: #e8f8f0; color: #16a34a; }
  #sh-provider:active { opacity: 0.75; }

  /* ── Profile popover ── */
  #sh-overlay { display:none; position:fixed; inset:0; z-index:290; }
  #sh-overlay.open { display:block; }
  #sh-pop {
    display:none; position:fixed; top:60px; right:12px; z-index:300;
    background:white; border-radius:20px; padding:18px;
    box-shadow:0 8px 32px rgba(0,0,0,0.15); width:272px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  }
  #sh-pop.open { display:block; }
  #sh-pop h3 { font-size:14px; font-weight:700; margin-bottom:12px; color:#1a1a2e; }
  #sh-av-grid { display:grid; grid-template-columns:repeat(5,1fr); gap:6px; margin-bottom:12px; }
  .sh-av {
    font-size:22px; border:2px solid transparent; border-radius:10px;
    padding:6px 2px; cursor:pointer; text-align:center; background:#f8f9ff;
    transition:transform 0.1s;
  }
  .sh-av.sel { border-color:#5b6ef5; background:#eef0ff; }
  .sh-av:active { transform:scale(0.85); }
  #sh-name-in {
    width:100%; border:1.5px solid #e0e4ff; border-radius:10px;
    padding:10px 12px; font-size:15px; font-family:inherit;
    color:#1a1a2e; background:#f8f9ff; outline:none; margin-bottom:10px;
    text-align:center;
  }
  #sh-name-in:focus { border-color:#5b6ef5; }
  #sh-save {
    width:100%; background:#5b6ef5; border:none; border-radius:10px;
    padding:11px; font-size:14px; font-weight:700; color:white; cursor:pointer;
  }
  #sh-save:active { background:#4454d4; }
  `;
  document.head.appendChild(style);

  // ── DOM ─────────────────────────────────────────────────────────────────
  const header  = document.createElement('div');
  header.id = 'sh';
  document.body.prepend(header);

  const overlay = document.createElement('div');
  overlay.id = 'sh-overlay';
  overlay.onclick = closePopover;
  document.body.appendChild(overlay);

  const pop = document.createElement('div');
  pop.id = 'sh-pop';
  document.body.appendChild(pop);

  // ── Header render ────────────────────────────────────────────────────────
  function render() {
    const n = name(), e = emo(), p = prov();
    const profileLabel = n ? `${e || '👤'} ${n} ✏️` : '+ Your name';
    const provClass  = p === 'anthropic' ? 'cloud' : 'local';
    const provLabel  = p === 'anthropic' ? '☁️ Claude' : `🖥️ ${model()}`;
    const settingsUrl = 'kids-chatbot.html?settings=1';

    header.innerHTML = `
      ${isIndex ? '' : '<a id="sh-home" href="index.html">← Home</a>'}
      <div id="sh-spacer"></div>
      <button id="sh-profile" type="button">${profileLabel}</button>
      <a id="sh-provider" class="${provClass}" href="${settingsUrl}">${provLabel} ⚙️</a>
    `;
    document.getElementById('sh-profile').onclick = openPopover;
  }

  // ── Popover ──────────────────────────────────────────────────────────────
  let _av = '';

  function openPopover() {
    _av = emo() || AVATARS[0];
    pop.innerHTML = `
      <h3>Your profile</h3>
      <div id="sh-av-grid"></div>
      <input id="sh-name-in" type="text" placeholder="Your name…" value="${name()}" maxlength="20" autocomplete="off" autocorrect="off" />
      <button id="sh-save" type="button">Save</button>
    `;
    const grid = document.getElementById('sh-av-grid');
    AVATARS.forEach(em => {
      const b = document.createElement('button');
      b.className = 'sh-av' + (em === _av ? ' sel' : '');
      b.textContent = em; b.type = 'button';
      b.onclick = () => {
        _av = em;
        grid.querySelectorAll('.sh-av').forEach(x => x.classList.remove('sel'));
        b.classList.add('sel');
      };
      grid.appendChild(b);
    });
    document.getElementById('sh-save').onclick = saveProfile;
    document.getElementById('sh-name-in').addEventListener('keydown', e => { if (e.key === 'Enter') saveProfile(); });
    pop.classList.add('open');
    overlay.classList.add('open');
    document.getElementById('sh-name-in').focus();
  }

  function saveProfile() {
    const n = document.getElementById('sh-name-in').value.trim();
    if (n) localStorage.setItem('cc_profile_name', n);
    localStorage.setItem('cc_profile_emoji', _av);
    closePopover();
    render();
    if (typeof updatePickerGreeting === 'function') updatePickerGreeting();
  }

  function closePopover() {
    pop.classList.remove('open');
    overlay.classList.remove('open');
  }

  // ── Public API ───────────────────────────────────────────────────────────
  window.updateSharedHeader = render;
  window.setHeaderVisible   = v => { header.style.display = v ? 'flex' : 'none'; };

  // ── Page padding ─────────────────────────────────────────────────────────
  function applyPadding() {
    if (isIndex) {
      document.body.style.paddingTop = '64px';
    } else {
      const app = document.querySelector('.app');
      if (app) {
        const cur = parseInt(getComputedStyle(app).paddingTop) || 0;
        if (cur < 56) app.style.paddingTop = '56px';
      }
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', applyPadding);
  } else {
    applyPadding();
  }

  render();
})();
