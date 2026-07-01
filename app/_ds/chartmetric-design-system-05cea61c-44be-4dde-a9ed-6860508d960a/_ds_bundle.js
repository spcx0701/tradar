/* This file is auto-generated from the design-system bundle. Do not edit by hand. */
/* @ds-bundle: {"format":3,"namespace":"ChartmetricDesignSystem_05cea6","components":[{"name":"Avatar","sourcePath":"components/core/Avatar.jsx"},{"name":"Badge","sourcePath":"components/core/Badge.jsx"},{"name":"Button","sourcePath":"components/core/Button.jsx"},{"name":"IconButton","sourcePath":"components/core/IconButton.jsx"},{"name":"Input","sourcePath":"components/core/Input.jsx"},{"name":"Select","sourcePath":"components/core/Select.jsx"},{"name":"Switch","sourcePath":"components/core/Switch.jsx"},{"name":"Tabs","sourcePath":"components/core/Tabs.jsx"},{"name":"Tag","sourcePath":"components/core/Tag.jsx"},{"name":"MetricStat","sourcePath":"components/data/MetricStat.jsx"},{"name":"PlatformIcon","sourcePath":"components/data/PlatformIcon.jsx"},{"name":"CM_PLATFORMS","sourcePath":"components/data/PlatformIcon.jsx"},{"name":"ScoreRing","sourcePath":"components/data/ScoreRing.jsx"},{"name":"Sparkline","sourcePath":"components/data/Sparkline.jsx"},{"name":"StageBadge","sourcePath":"components/data/StageBadge.jsx"},{"name":"CM_CAREER_STAGES","sourcePath":"components/data/StageBadge.jsx"},{"name":"TrendDelta","sourcePath":"components/data/TrendDelta.jsx"}],"sourceHashes":{"components/core/Avatar.jsx":"3bdd472f844a","components/core/Badge.jsx":"93dcc03ca126","components/core/Button.jsx":"dd19c72e0286","components/core/IconButton.jsx":"dac65360b12a","components/core/Input.jsx":"79f7700ca17b","components/core/Select.jsx":"ac09e5538778","components/core/Switch.jsx":"d56d36443221","components/core/Tabs.jsx":"f1b62cd769be","components/core/Tag.jsx":"4b1bc13b0f5f","components/data/MetricStat.jsx":"55295dfcfc3e","components/data/PlatformIcon.jsx":"f4543d26a88b","components/data/ScoreRing.jsx":"e6c239d4c7b5","components/data/Sparkline.jsx":"12c9704fac89","components/data/StageBadge.jsx":"f79b3afef3fb","components/data/TrendDelta.jsx":"be27e54b4ad8","ui_kits/app/App.jsx":"91cc24a73e39","ui_kits/app/ArtistProfile.jsx":"dfd67beda6cc","ui_kits/app/ChartsScreen.jsx":"6d79f8a1c229","ui_kits/app/Sidebar.jsx":"8452c5c805b5","ui_kits/app/StreamChart.jsx":"6283ec56f817","ui_kits/app/TalentSearch.jsx":"e33c3f628e99","ui_kits/app/TopBar.jsx":"074b315c3283","ui_kits/app/data.js":"9f624c155e67"},"inlinedExternals":[],"unexposedExports":[]} */

(() => {

const __ds_ns = (window.ChartmetricDesignSystem_05cea6 = window.ChartmetricDesignSystem_05cea6 || {});

const __ds_scope = {};

(__ds_ns.__errors = __ds_ns.__errors || []);

// components/core/Avatar.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Artist / entity avatar. Circular by default with optional rank
 * badge and initials fallback. Square variant for tracks/albums.
 */

const STYLE_ID = "cmds-avatar";
if (typeof document !== "undefined" && !document.getElementById(STYLE_ID)) {
  const el = document.createElement("style");
  el.id = STYLE_ID;
  el.textContent = `
.cmds-avatar{position:relative;display:inline-flex;align-items:center;justify-content:center;
  flex:none;overflow:visible;font-family:var(--cm-font-sans);font-weight:var(--cm-fw-semibold);
  color:var(--cm-n-600);background:var(--cm-n-100);}
.cmds-avatar--circle{border-radius:50%;}
.cmds-avatar--square{border-radius:var(--cm-radius-md);}
.cmds-avatar__img{width:100%;height:100%;object-fit:cover;border-radius:inherit;display:block;}
.cmds-avatar__rank{position:absolute;bottom:-4px;right:-4px;min-width:18px;height:18px;padding:0 4px;
  display:inline-flex;align-items:center;justify-content:center;border-radius:var(--cm-radius-pill);
  background:var(--cm-n-900);color:#fff;font-size:10px;font-weight:var(--cm-fw-bold);
  border:2px solid #fff;line-height:1;}
.cmds-avatar--ring{box-shadow:0 0 0 2px #fff,0 0 0 4px var(--cm-blue-400);}
`;
  document.head.appendChild(el);
}
const SIZES = {
  xs: 24,
  sm: 32,
  md: 40,
  lg: 56,
  xl: 72
};
function Avatar({
  src,
  name = "",
  size = "md",
  shape = "circle",
  rank,
  ring = false,
  ...rest
}) {
  const px = SIZES[size] || size;
  const initials = name.split(" ").map(w => w[0]).filter(Boolean).slice(0, 2).join("").toUpperCase();
  const cls = ["cmds-avatar", `cmds-avatar--${shape}`, ring && "cmds-avatar--ring"].filter(Boolean).join(" ");
  return /*#__PURE__*/React.createElement("span", _extends({
    className: cls,
    style: {
      width: px,
      height: px,
      fontSize: Math.round(px * 0.36)
    }
  }, rest), src ? /*#__PURE__*/React.createElement("img", {
    className: "cmds-avatar__img",
    src: src,
    alt: name
  }) : /*#__PURE__*/React.createElement("span", null, initials || "?"), rank != null && /*#__PURE__*/React.createElement("span", {
    className: "cmds-avatar__rank"
  }, rank));
}
Object.assign(__ds_scope, { Avatar });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Avatar.jsx", error: String((e && e.message) || e) }); }

// components/core/Badge.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Status badge / pill. Soft (tinted) by default, or solid.
 * Tones map to the semantic data palette. Optional leading dot.
 */

const STYLE_ID = "cmds-badge";
if (typeof document !== "undefined" && !document.getElementById(STYLE_ID)) {
  const el = document.createElement("style");
  el.id = STYLE_ID;
  el.textContent = `
.cmds-badge{display:inline-flex;align-items:center;gap:5px;font-family:var(--cm-font-sans);
  font-weight:var(--cm-fw-semibold);font-size:var(--cm-fs-micro);line-height:1;
  letter-spacing:.01em;padding:4px 8px;border-radius:var(--cm-radius-pill);
  border:1px solid transparent;white-space:nowrap;}
.cmds-badge__dot{width:6px;height:6px;border-radius:50%;background:currentColor;}
.cmds-badge--neutral{background:var(--cm-n-100);color:var(--cm-n-600);}
.cmds-badge--info{background:var(--cm-info-soft);color:var(--cm-blue-700);}
.cmds-badge--positive{background:var(--cm-positive-soft);color:var(--cm-positive-700);}
.cmds-badge--negative{background:var(--cm-negative-soft);color:var(--cm-negative-700);}
.cmds-badge--warning{background:var(--cm-warning-soft);color:#9A6700;}
.cmds-badge--solid.cmds-badge--neutral{background:var(--cm-n-700);color:#fff;}
.cmds-badge--solid.cmds-badge--info{background:var(--cm-blue-500);color:#fff;}
.cmds-badge--solid.cmds-badge--positive{background:var(--cm-positive);color:#fff;}
.cmds-badge--solid.cmds-badge--negative{background:var(--cm-negative);color:#fff;}
.cmds-badge--solid.cmds-badge--warning{background:var(--cm-warning);color:#fff;}
.cmds-badge--outline{background:transparent;border-color:var(--cm-border-strong);color:var(--cm-n-600);}
`;
  document.head.appendChild(el);
}
function Badge({
  children,
  tone = "neutral",
  solid = false,
  outline = false,
  dot = false,
  ...rest
}) {
  const cls = ["cmds-badge", `cmds-badge--${tone}`, solid && "cmds-badge--solid", outline && "cmds-badge--outline"].filter(Boolean).join(" ");
  return /*#__PURE__*/React.createElement("span", _extends({
    className: cls
  }, rest), dot && /*#__PURE__*/React.createElement("span", {
    className: "cmds-badge__dot",
    "aria-hidden": "true"
  }), children);
}
Object.assign(__ds_scope, { Badge });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Badge.jsx", error: String((e && e.message) || e) }); }

// components/core/Button.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Chartmetric primary action button.
 * Variants: primary (brand blue), secondary (outline), ghost (text),
 * danger. Sizes sm / md / lg. Blue is rationed — primary only for the
 * single most important action in a view.
 */

const STYLE_ID = "cmds-button";
if (typeof document !== "undefined" && !document.getElementById(STYLE_ID)) {
  const el = document.createElement("style");
  el.id = STYLE_ID;
  el.textContent = `
.cmds-btn{
  --_bg:var(--cm-blue-500);--_fg:#fff;--_bd:transparent;--_bgh:var(--cm-blue-600);--_bga:var(--cm-blue-700);
  display:inline-flex;align-items:center;justify-content:center;gap:8px;
  font-family:var(--cm-font-sans);font-weight:var(--cm-fw-semibold);
  border-radius:var(--cm-radius-md);border:1px solid var(--_bd);
  background:var(--_bg);color:var(--_fg);cursor:pointer;white-space:nowrap;
  transition:var(--cm-transition-control);user-select:none;line-height:1;
}
.cmds-btn:hover{background:var(--_bgh);}
.cmds-btn:active{background:var(--_bga);}
.cmds-btn:focus-visible{outline:none;box-shadow:var(--cm-glow-accent);}
.cmds-btn[disabled]{opacity:.45;cursor:not-allowed;}
.cmds-btn--sm{height:30px;padding:0 12px;font-size:var(--cm-fs-sm);}
.cmds-btn--md{height:38px;padding:0 16px;font-size:var(--cm-fs-body);}
.cmds-btn--lg{height:44px;padding:0 22px;font-size:var(--cm-fs-md);}
.cmds-btn--full{width:100%;}
.cmds-btn--secondary{--_bg:#fff;--_fg:var(--cm-n-800);--_bd:var(--cm-border-strong);--_bgh:var(--cm-n-50);--_bga:var(--cm-n-100);}
.cmds-btn--ghost{--_bg:transparent;--_fg:var(--cm-n-700);--_bd:transparent;--_bgh:var(--cm-n-100);--_bga:var(--cm-n-200);}
.cmds-btn--danger{--_bg:var(--cm-negative);--_fg:#fff;--_bgh:var(--cm-negative-700);--_bga:var(--cm-negative-700);}
.cmds-btn__spin{width:14px;height:14px;border-radius:50%;border:2px solid currentColor;border-top-color:transparent;animation:cmds-spin .6s linear infinite;}
@keyframes cmds-spin{to{transform:rotate(360deg);}}
`;
  document.head.appendChild(el);
}
function Button({
  children,
  variant = "primary",
  size = "md",
  fullWidth = false,
  loading = false,
  disabled = false,
  leadingIcon = null,
  trailingIcon = null,
  type = "button",
  ...rest
}) {
  const cls = ["cmds-btn", `cmds-btn--${size}`, variant !== "primary" && `cmds-btn--${variant}`, fullWidth && "cmds-btn--full"].filter(Boolean).join(" ");
  return /*#__PURE__*/React.createElement("button", _extends({
    className: cls,
    type: type,
    disabled: disabled || loading
  }, rest), loading && /*#__PURE__*/React.createElement("span", {
    className: "cmds-btn__spin",
    "aria-hidden": "true"
  }), !loading && leadingIcon, children && /*#__PURE__*/React.createElement("span", null, children), !loading && trailingIcon);
}
Object.assign(__ds_scope, { Button });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Button.jsx", error: String((e && e.message) || e) }); }

// components/core/IconButton.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/** Square icon-only button for toolbars & table rows. Sizes sm/md. */

const STYLE_ID = "cmds-iconbutton";
if (typeof document !== "undefined" && !document.getElementById(STYLE_ID)) {
  const el = document.createElement("style");
  el.id = STYLE_ID;
  el.textContent = `
.cmds-iconbtn{display:inline-flex;align-items:center;justify-content:center;
  border-radius:var(--cm-radius-md);border:1px solid transparent;background:transparent;
  color:var(--cm-n-600);cursor:pointer;transition:var(--cm-transition-control);}
.cmds-iconbtn:hover{background:var(--cm-n-100);color:var(--cm-n-900);}
.cmds-iconbtn:active{background:var(--cm-n-200);}
.cmds-iconbtn:focus-visible{outline:none;box-shadow:var(--cm-glow-accent);}
.cmds-iconbtn[disabled]{opacity:.4;cursor:not-allowed;}
.cmds-iconbtn--sm{width:30px;height:30px;}
.cmds-iconbtn--md{width:38px;height:38px;}
.cmds-iconbtn--outline{border-color:var(--cm-border-strong);background:#fff;}
.cmds-iconbtn--active{background:var(--cm-blue-50);color:var(--cm-blue-600);}
`;
  document.head.appendChild(el);
}
function IconButton({
  children,
  size = "md",
  outline = false,
  active = false,
  label,
  ...rest
}) {
  const cls = ["cmds-iconbtn", `cmds-iconbtn--${size}`, outline && "cmds-iconbtn--outline", active && "cmds-iconbtn--active"].filter(Boolean).join(" ");
  return /*#__PURE__*/React.createElement("button", _extends({
    className: cls,
    "aria-label": label
  }, rest), children);
}
Object.assign(__ds_scope, { IconButton });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/IconButton.jsx", error: String((e && e.message) || e) }); }

// components/core/Input.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/** Text input with optional leading icon and invalid state. */

const STYLE_ID = "cmds-input";
if (typeof document !== "undefined" && !document.getElementById(STYLE_ID)) {
  const el = document.createElement("style");
  el.id = STYLE_ID;
  el.textContent = `
.cmds-field{display:inline-flex;flex-direction:column;gap:6px;font-family:var(--cm-font-sans);}
.cmds-field__label{font-size:var(--cm-fs-sm);font-weight:var(--cm-fw-medium);color:var(--cm-n-700);}
.cmds-input{display:flex;align-items:center;gap:8px;background:#fff;
  border:1px solid var(--cm-border-strong);border-radius:var(--cm-radius-md);
  padding:0 12px;height:38px;transition:var(--cm-transition-control);}
.cmds-input:focus-within{border-color:var(--cm-blue-500);box-shadow:var(--cm-glow-accent);}
.cmds-input--invalid{border-color:var(--cm-negative);}
.cmds-input--invalid:focus-within{box-shadow:0 0 0 3px var(--cm-negative-soft);}
.cmds-input__icon{display:inline-flex;color:var(--cm-n-400);flex:none;}
.cmds-input input{border:0;outline:0;background:transparent;width:100%;
  font:var(--cm-text-body);color:var(--cm-n-900);}
.cmds-input input::placeholder{color:var(--cm-n-400);}
.cmds-input--disabled{background:var(--cm-n-50);opacity:.7;}
.cmds-field__hint{font-size:var(--cm-fs-caption);color:var(--cm-n-500);}
.cmds-field__hint--error{color:var(--cm-negative-700);}
`;
  document.head.appendChild(el);
}
function Input({
  label,
  leadingIcon = null,
  invalid = false,
  disabled = false,
  hint,
  errorText,
  style,
  ...rest
}) {
  const boxCls = ["cmds-input", invalid && "cmds-input--invalid", disabled && "cmds-input--disabled"].filter(Boolean).join(" ");
  return /*#__PURE__*/React.createElement("label", {
    className: "cmds-field",
    style: style
  }, label && /*#__PURE__*/React.createElement("span", {
    className: "cmds-field__label"
  }, label), /*#__PURE__*/React.createElement("span", {
    className: boxCls
  }, leadingIcon && /*#__PURE__*/React.createElement("span", {
    className: "cmds-input__icon"
  }, leadingIcon), /*#__PURE__*/React.createElement("input", _extends({
    disabled: disabled
  }, rest))), invalid && errorText ? /*#__PURE__*/React.createElement("span", {
    className: "cmds-field__hint cmds-field__hint--error"
  }, errorText) : hint ? /*#__PURE__*/React.createElement("span", {
    className: "cmds-field__hint"
  }, hint) : null);
}
Object.assign(__ds_scope, { Input });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Input.jsx", error: String((e && e.message) || e) }); }

// components/core/Select.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/** Styled wrapper over a native <select> with a chevron. */

const STYLE_ID = "cmds-select";
if (typeof document !== "undefined" && !document.getElementById(STYLE_ID)) {
  const el = document.createElement("style");
  el.id = STYLE_ID;
  el.textContent = `
.cmds-select{position:relative;display:inline-flex;align-items:center;background:#fff;
  border:1px solid var(--cm-border-strong);border-radius:var(--cm-radius-md);
  transition:var(--cm-transition-control);font-family:var(--cm-font-sans);}
.cmds-select:focus-within{border-color:var(--cm-blue-500);box-shadow:var(--cm-glow-accent);}
.cmds-select select{appearance:none;border:0;outline:0;background:transparent;cursor:pointer;
  font:var(--cm-text-body);color:var(--cm-n-900);height:38px;padding:0 34px 0 12px;width:100%;}
.cmds-select--sm select{height:30px;font-size:var(--cm-fs-sm);}
.cmds-select__chev{position:absolute;right:11px;pointer-events:none;color:var(--cm-n-500);
  width:14px;height:14px;}
.cmds-select--disabled{background:var(--cm-n-50);opacity:.7;}
`;
  document.head.appendChild(el);
}
function Select({
  children,
  size = "md",
  disabled = false,
  style,
  ...rest
}) {
  const cls = ["cmds-select", size === "sm" && "cmds-select--sm", disabled && "cmds-select--disabled"].filter(Boolean).join(" ");
  return /*#__PURE__*/React.createElement("span", {
    className: cls,
    style: style
  }, /*#__PURE__*/React.createElement("select", _extends({
    disabled: disabled
  }, rest), children), /*#__PURE__*/React.createElement("svg", {
    className: "cmds-select__chev",
    viewBox: "0 0 16 16",
    fill: "none",
    "aria-hidden": "true"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M4 6l4 4 4-4",
    stroke: "currentColor",
    strokeWidth: "1.6",
    strokeLinecap: "round",
    strokeLinejoin: "round"
  })));
}
Object.assign(__ds_scope, { Select });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Select.jsx", error: String((e && e.message) || e) }); }

// components/core/Switch.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/** On/off toggle switch. */

const STYLE_ID = "cmds-switch";
if (typeof document !== "undefined" && !document.getElementById(STYLE_ID)) {
  const el = document.createElement("style");
  el.id = STYLE_ID;
  el.textContent = `
.cmds-switch{display:inline-flex;align-items:center;gap:9px;cursor:pointer;font-family:var(--cm-font-sans);
  font-size:var(--cm-fs-sm);color:var(--cm-n-700);user-select:none;}
.cmds-switch__track{position:relative;width:36px;height:20px;border-radius:var(--cm-radius-pill);
  background:var(--cm-n-300);transition:background var(--cm-dur-fast) var(--cm-ease-standard);flex:none;}
.cmds-switch__thumb{position:absolute;top:2px;left:2px;width:16px;height:16px;border-radius:50%;
  background:#fff;box-shadow:var(--cm-shadow-sm);transition:transform var(--cm-dur-fast) var(--cm-ease-standard);}
.cmds-switch input{position:absolute;opacity:0;width:0;height:0;}
.cmds-switch input:checked + .cmds-switch__track{background:var(--cm-blue-500);}
.cmds-switch input:checked + .cmds-switch__track .cmds-switch__thumb{transform:translateX(16px);}
.cmds-switch input:focus-visible + .cmds-switch__track{box-shadow:var(--cm-glow-accent);}
.cmds-switch--disabled{opacity:.5;cursor:not-allowed;}
`;
  document.head.appendChild(el);
}
function Switch({
  checked,
  defaultChecked,
  onChange,
  label,
  disabled = false,
  ...rest
}) {
  const cls = ["cmds-switch", disabled && "cmds-switch--disabled"].filter(Boolean).join(" ");
  return /*#__PURE__*/React.createElement("label", {
    className: cls
  }, /*#__PURE__*/React.createElement("input", _extends({
    type: "checkbox",
    checked: checked,
    defaultChecked: defaultChecked,
    onChange: onChange,
    disabled: disabled
  }, rest)), /*#__PURE__*/React.createElement("span", {
    className: "cmds-switch__track"
  }, /*#__PURE__*/React.createElement("span", {
    className: "cmds-switch__thumb"
  })), label && /*#__PURE__*/React.createElement("span", null, label));
}
Object.assign(__ds_scope, { Switch });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Switch.jsx", error: String((e && e.message) || e) }); }

// components/core/Tabs.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/** Underline tab bar. Controlled via value/onChange. */

const STYLE_ID = "cmds-tabs";
if (typeof document !== "undefined" && !document.getElementById(STYLE_ID)) {
  const el = document.createElement("style");
  el.id = STYLE_ID;
  el.textContent = `
.cmds-tabs{display:flex;align-items:center;gap:2px;border-bottom:1px solid var(--cm-border);
  font-family:var(--cm-font-sans);overflow-x:auto;}
.cmds-tab{position:relative;display:inline-flex;align-items:center;gap:7px;padding:11px 14px;
  font-size:var(--cm-fs-body);font-weight:var(--cm-fw-medium);color:var(--cm-n-500);
  background:none;border:0;cursor:pointer;white-space:nowrap;transition:color var(--cm-dur-fast) var(--cm-ease-standard);}
.cmds-tab:hover{color:var(--cm-n-800);}
.cmds-tab--active{color:var(--cm-blue-600);font-weight:var(--cm-fw-semibold);}
.cmds-tab--active:after{content:"";position:absolute;left:8px;right:8px;bottom:-1px;height:2px;
  background:var(--cm-blue-500);border-radius:2px 2px 0 0;}
.cmds-tab__count{font-size:var(--cm-fs-micro);font-weight:var(--cm-fw-semibold);color:var(--cm-n-500);
  background:var(--cm-n-100);border-radius:var(--cm-radius-pill);padding:2px 6px;line-height:1;}
.cmds-tab--active .cmds-tab__count{background:var(--cm-blue-50);color:var(--cm-blue-600);}
`;
  document.head.appendChild(el);
}
function Tabs({
  tabs = [],
  value,
  onChange,
  ...rest
}) {
  return /*#__PURE__*/React.createElement("div", _extends({
    className: "cmds-tabs",
    role: "tablist"
  }, rest), tabs.map(t => {
    const key = t.value ?? t.label;
    const active = key === value;
    return /*#__PURE__*/React.createElement("button", {
      key: key,
      role: "tab",
      "aria-selected": active,
      className: ["cmds-tab", active && "cmds-tab--active"].filter(Boolean).join(" "),
      onClick: () => onChange && onChange(key)
    }, t.icon, t.label, t.count != null && /*#__PURE__*/React.createElement("span", {
      className: "cmds-tab__count"
    }, t.count));
  }));
}
Object.assign(__ds_scope, { Tabs });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Tabs.jsx", error: String((e && e.message) || e) }); }

// components/core/Tag.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/** Filter / attribute chip. Optional color dot and removable ✕. */

const STYLE_ID = "cmds-tag";
if (typeof document !== "undefined" && !document.getElementById(STYLE_ID)) {
  const el = document.createElement("style");
  el.id = STYLE_ID;
  el.textContent = `
.cmds-tag{display:inline-flex;align-items:center;gap:6px;font-family:var(--cm-font-sans);
  font-weight:var(--cm-fw-medium);font-size:var(--cm-fs-sm);line-height:1;color:var(--cm-n-700);
  background:#fff;border:1px solid var(--cm-border-strong);border-radius:var(--cm-radius-sm);
  padding:5px 8px;white-space:nowrap;transition:var(--cm-transition-control);}
.cmds-tag--clickable{cursor:pointer;}
.cmds-tag--clickable:hover{background:var(--cm-n-50);border-color:var(--cm-n-400);}
.cmds-tag--selected{background:var(--cm-blue-50);border-color:var(--cm-blue-300);color:var(--cm-blue-700);}
.cmds-tag__dot{width:8px;height:8px;border-radius:2px;flex:none;}
.cmds-tag__x{display:inline-flex;align-items:center;justify-content:center;width:14px;height:14px;
  border-radius:3px;color:var(--cm-n-500);cursor:pointer;font-size:12px;line-height:1;}
.cmds-tag__x:hover{background:var(--cm-n-200);color:var(--cm-n-800);}
`;
  document.head.appendChild(el);
}
function Tag({
  children,
  color,
  selected = false,
  onRemove,
  onClick,
  ...rest
}) {
  const clickable = !!onClick;
  const cls = ["cmds-tag", clickable && "cmds-tag--clickable", selected && "cmds-tag--selected"].filter(Boolean).join(" ");
  return /*#__PURE__*/React.createElement("span", _extends({
    className: cls,
    onClick: onClick
  }, rest), color && /*#__PURE__*/React.createElement("span", {
    className: "cmds-tag__dot",
    style: {
      background: color
    },
    "aria-hidden": "true"
  }), children, onRemove && /*#__PURE__*/React.createElement("span", {
    className: "cmds-tag__x",
    role: "button",
    "aria-label": "Remove",
    onClick: e => {
      e.stopPropagation();
      onRemove(e);
    }
  }, "\u2715"));
}
Object.assign(__ds_scope, { Tag });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Tag.jsx", error: String((e && e.message) || e) }); }

// components/data/PlatformIcon.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Platform marker for Chartmetric's data sources. Renders the real
 * brand glyph as an INLINE SVG (single-path marks from Simple Icons,
 * embedded — no network dependency). Plain (brand-color glyph) or
 * chip (filled brand-color tile with a white glyph).
 */

const PATHS = {
  spotify: "M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z",
  applemusic: "M23.994 6.124a9.23 9.23 0 00-.24-2.19c-.317-1.31-1.062-2.31-2.18-3.043a5.022 5.022 0 00-1.877-.726 10.496 10.496 0 00-1.564-.15c-.04-.003-.083-.01-.124-.013H5.986c-.152.01-.303.017-.455.026-.747.043-1.49.123-2.193.4-1.336.53-2.3 1.452-2.865 2.78-.192.448-.292.925-.363 1.408-.056.392-.088.785-.1 1.18 0 .032-.007.062-.01.093v12.223c.01.14.017.283.027.424.05.815.154 1.624.497 2.373.65 1.42 1.738 2.353 3.234 2.801.42.127.856.187 1.293.228.555.053 1.11.06 1.667.06h11.03a12.5 12.5 0 001.57-.1c.822-.106 1.596-.35 2.295-.81a5.046 5.046 0 001.88-2.207c.186-.42.293-.87.37-1.324.113-.675.138-1.358.137-2.04-.002-3.8 0-7.595-.003-11.393zm-6.423 3.99v5.712c0 .417-.058.827-.244 1.206-.29.59-.76.962-1.388 1.14-.35.1-.706.157-1.07.173-.95.045-1.773-.6-1.943-1.536a1.88 1.88 0 011.038-2.022c.323-.16.67-.25 1.018-.324.378-.082.758-.153 1.134-.24.274-.063.457-.23.51-.516a.904.904 0 00.02-.193c0-1.815 0-3.63-.002-5.443a.725.725 0 00-.026-.185c-.04-.15-.15-.243-.304-.234-.16.01-.318.035-.475.066-.76.15-1.52.303-2.28.456l-2.325.47-1.374.278c-.016.003-.032.01-.048.013-.277.077-.377.203-.39.49-.002.042 0 .086 0 .13-.002 2.602 0 5.204-.003 7.805 0 .42-.047.836-.215 1.227-.278.64-.77 1.04-1.434 1.233-.35.1-.71.16-1.075.172-.96.036-1.755-.6-1.92-1.544-.14-.812.23-1.685 1.154-2.075.357-.15.73-.232 1.108-.31.287-.06.575-.116.86-.177.383-.083.583-.323.6-.714v-.15c0-2.96 0-5.922.002-8.882 0-.123.013-.25.042-.37.07-.285.273-.448.546-.518.255-.066.515-.112.774-.165.733-.15 1.466-.296 2.2-.444l2.27-.46c.67-.134 1.34-.27 2.01-.403.22-.043.442-.088.663-.106.31-.025.523.17.554.482.008.073.012.148.012.223.002 1.91.002 3.822 0 5.732z",
  youtube: "M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z",
  tiktok: "M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z",
  instagram: "M7.0301.084c-1.2768.0602-2.1487.264-2.911.5634-.7888.3075-1.4575.72-2.1228 1.3877-.6652.6677-1.075 1.3368-1.3802 2.127-.2954.7638-.4956 1.6365-.552 2.914-.0564 1.2775-.0689 1.6882-.0626 4.947.0062 3.2586.0206 3.6671.0825 4.9473.061 1.2765.264 2.1482.5635 2.9107.308.7889.72 1.4573 1.388 2.1228.6679.6655 1.3365 1.0743 2.1285 1.38.7632.295 1.6361.4961 2.9134.552 1.2773.056 1.6884.069 4.9462.0627 3.2578-.0062 3.668-.0207 4.9478-.0814 1.28-.0607 2.147-.2652 2.9098-.5633.7889-.3086 1.4578-.72 2.1228-1.3881.665-.6682 1.0745-1.3378 1.3795-2.1284.2957-.7632.4966-1.636.552-2.9124.056-1.2809.0692-1.6898.063-4.948-.0063-3.2583-.021-3.6668-.0817-4.9465-.0607-1.2797-.264-2.1487-.5633-2.9117-.3084-.7889-.72-1.4568-1.3876-2.1228C21.2982 1.33 20.628.9208 19.8378.6165 19.074.321 18.2017.1197 16.9244.0645 15.6471.0093 15.236-.005 11.977.0014 8.718.0076 8.31.0215 7.0301.0839m.1402 21.6932c-1.17-.0509-1.8053-.2453-2.2287-.408-.5606-.216-.96-.4771-1.3819-.895-.422-.4178-.6811-.8186-.9-1.378-.1644-.4234-.3624-1.058-.4171-2.228-.0595-1.2645-.072-1.6442-.079-4.848-.007-3.2037.0053-3.583.0607-4.848.05-1.169.2456-1.805.408-2.2282.216-.5613.4762-.96.895-1.3816.4188-.4217.8184-.6814 1.3783-.9003.423-.1651 1.0575-.3614 2.227-.4171 1.2655-.06 1.6447-.072 4.848-.079 3.2033-.007 3.5835.005 4.8495.0608 1.169.0508 1.8053.2445 2.228.408.5608.216.96.4754 1.3816.895.4217.4194.6816.8176.9005 1.3787.1653.4217.3617 1.056.4169 2.2263.0602 1.2655.0739 1.645.0796 4.848.0058 3.203-.0055 3.5834-.061 4.848-.051 1.17-.245 1.8055-.408 2.2294-.216.5604-.4763.96-.8954 1.3814-.419.4215-.8181.6811-1.3783.9-.4224.1649-1.0577.3617-2.2262.4174-1.2656.0595-1.6448.072-4.8493.079-3.2045.007-3.5825-.006-4.848-.0608M16.953 5.5864A1.44 1.44 0 1 0 18.39 4.144a1.44 1.44 0 0 0-1.437 1.4424M5.8385 12.012c.0067 3.4032 2.7706 6.1557 6.173 6.1493 3.4026-.0065 6.157-2.7701 6.1506-6.1733-.0065-3.4032-2.771-6.1565-6.174-6.1498-3.403.0067-6.156 2.771-6.1496 6.1738M8 12.0077a4 4 0 1 1 4.008 3.9921A3.9996 3.9996 0 0 1 8 12.0077",
  soundcloud: "M23.999 14.165c-.052 1.796-1.612 3.169-3.4 3.169h-8.18a.68.68 0 0 1-.675-.683V7.862a.747.747 0 0 1 .452-.724s.75-.513 2.333-.513a5.364 5.364 0 0 1 2.763.755 5.433 5.433 0 0 1 2.57 3.54c.282-.08.574-.121.868-.12.884 0 1.73.358 2.347.992s.948 1.49.922 2.373ZM10.721 8.421c.247 2.98.427 5.697 0 8.672a.264.264 0 0 1-.53 0c-.395-2.946-.22-5.718 0-8.672a.264.264 0 0 1 .53 0ZM9.072 9.448c.285 2.659.37 4.986-.006 7.655a.277.277 0 0 1-.55 0c-.331-2.63-.256-5.02 0-7.655a.277.277 0 0 1 .556 0Zm-1.663-.257c.27 2.726.39 5.171 0 7.904a.266.266 0 0 1-.532 0c-.38-2.69-.257-5.21 0-7.904a.266.266 0 0 1 .532 0Zm-1.647.77a26.108 26.108 0 0 1-.008 7.147.272.272 0 0 1-.542 0 27.955 27.955 0 0 1 0-7.147.275.275 0 0 1 .55 0Zm-1.67 1.769c.421 1.865.228 3.5-.029 5.388a.257.257 0 0 1-.514 0c-.21-1.858-.398-3.549 0-5.389a.272.272 0 0 1 .543 0Zm-1.655-.273c.388 1.897.26 3.508-.01 5.412-.026.28-.514.283-.54 0-.244-1.878-.347-3.54-.01-5.412a.283.283 0 0 1 .56 0Zm-1.668.911c.4 1.268.257 2.292-.026 3.572a.257.257 0 0 1-.514 0c-.241-1.262-.354-2.312-.023-3.572a.283.283 0 0 1 .563 0Z",
  shazam: "M12 0C5.373 0-.001 5.371-.001 12c0 6.625 5.374 12 12.001 12s12-5.375 12-12c0-6.629-5.373-12-12-12M9.872 16.736c-1.287 0-2.573-.426-3.561-1.281-1.214-1.049-1.934-2.479-2.029-4.024-.09-1.499.42-2.944 1.436-4.067C6.86 6.101 8.907 4.139 8.993 4.055c.555-.532 1.435-.511 1.966.045.53.557.512 1.439-.044 1.971-.021.02-2.061 1.976-3.137 3.164-.508.564-.764 1.283-.719 2.027.049.789.428 1.529 1.07 2.086.844.73 2.51.891 3.553-.043.619-.559 1.372-1.377 1.38-1.386.52-.567 1.4-.603 1.965-.081.565.52.603 1.402.083 1.969-.035.035-.852.924-1.572 1.572-1.005.902-2.336 1.357-3.666 1.357m8.41-.099c-1.143 1.262-3.189 3.225-3.276 3.309-.27.256-.615.385-.96.385-.368 0-.732-.145-1.006-.43-.531-.559-.512-1.439.044-1.971.021-.02 2.063-1.977 3.137-3.166.508-.563.764-1.283.719-2.027-.048-.789-.428-1.529-1.07-2.084-.844-.73-2.51-.893-3.552.044-.621.556-1.373 1.376-1.38 1.384-.521.566-1.399.604-1.966.084-.564-.521-.604-1.404-.082-1.971.034-.037.85-.926 1.571-1.573 1.979-1.778 5.221-1.813 7.227-.077 1.214 1.051 1.935 2.48 2.028 4.025.092 1.497-.419 2.945-1.434 4.068",
  deezer: "M.693 10.024c.381 0 .693-1.256.693-2.807 0-1.55-.312-2.807-.693-2.807C.312 4.41 0 5.666 0 7.217s.312 2.808.693 2.808ZM21.038 1.56c-.364 0-.684.805-.91 2.096C19.765 1.446 19.184 0 18.526 0c-.78 0-1.464 2.036-1.784 5-.312-2.158-.788-3.536-1.325-3.536-.745 0-1.386 2.704-1.62 6.472-.442-1.932-1.083-3.145-1.793-3.145s-1.35 1.213-1.793 3.145c-.242-3.76-.874-6.463-1.628-6.463-.537 0-1.013 1.378-1.325 3.535C6.938 2.036 6.262 0 5.474 0c-.658 0-1.247 1.447-1.602 3.665-.217-1.291-.546-2.105-.91-2.105-.675 0-1.221 2.807-1.221 6.272 0 3.466.546 6.273 1.221 6.273.277 0 .537-.476.736-1.273.32 2.928.996 4.938 1.776 4.938.606 0 1.143-1.204 1.507-3.11.251 3.622.875 6.195 1.602 6.195.46 0 .875-1.023 1.187-2.677C10.142 21.6 11 24 12.004 24c1.005 0 1.863-2.4 2.235-5.822.312 1.654.727 2.677 1.186 2.677.728 0 1.352-2.573 1.603-6.195.364 1.906.9 3.11 1.507 3.11.78 0 1.455-2.01 1.775-4.938.208.797.46 1.273.737 1.273.675 0 1.22-2.807 1.22-6.273-.008-3.457-.553-6.272-1.23-6.272ZM23.307 10.024c.381 0 .693-1.256.693-2.807 0-1.55-.312-2.807-.693-2.807-.381 0-.693 1.256-.693 2.807s.312 2.808.693 2.808Z",
  x: "M14.234 10.162 22.977 0h-2.072l-7.591 8.824L7.251 0H.258l9.168 13.343L.258 24H2.33l8.016-9.318L16.749 24h6.993zm-2.837 3.299-.929-1.329L3.076 1.56h3.182l5.965 8.532.929 1.329 7.754 11.09h-3.182z",
  twitch: "M11.571 4.714h1.715v5.143H11.57zm4.715 0H18v5.143h-1.714zM6 0L1.714 4.286v15.428h5.143V24l4.286-4.286h3.428L22.286 12V0zm14.571 11.143l-3.428 3.428h-3.429l-3 3v-3H6.857V1.714h13.714Z",
  pandora: "M1.882 0v24H8.32a1.085 1.085 0 001.085-1.085v-4.61h1.612c7.88 0 11.103-4.442 11.103-9.636C22.119 2.257 17.247 0 12.662 0H1.882Z"
};
const PLATFORMS = {
  spotify: {
    color: "var(--cm-platform-spotify)",
    name: "Spotify"
  },
  applemusic: {
    color: "var(--cm-platform-applemusic)",
    name: "Apple Music"
  },
  youtube: {
    color: "var(--cm-platform-youtube)",
    name: "YouTube"
  },
  tiktok: {
    color: "var(--cm-platform-tiktok)",
    name: "TikTok"
  },
  instagram: {
    color: "var(--cm-platform-instagram)",
    name: "Instagram"
  },
  soundcloud: {
    color: "var(--cm-platform-soundcloud)",
    name: "SoundCloud"
  },
  shazam: {
    color: "var(--cm-platform-shazam)",
    name: "Shazam"
  },
  deezer: {
    color: "var(--cm-platform-deezer)",
    name: "Deezer"
  },
  x: {
    color: "var(--cm-platform-x)",
    name: "X"
  },
  twitch: {
    color: "var(--cm-platform-twitch)",
    name: "Twitch"
  },
  pandora: {
    color: "var(--cm-platform-pandora)",
    name: "Pandora"
  }
};
const STYLE_ID = "cmds-platformicon";
if (typeof document !== "undefined" && !document.getElementById(STYLE_ID)) {
  const el = document.createElement("style");
  el.id = STYLE_ID;
  el.textContent = `
.cmds-plat{display:inline-flex;align-items:center;justify-content:center;flex:none;vertical-align:middle;}
.cmds-plat--chip{border-radius:var(--cm-radius-sm);}
.cmds-plat svg{display:block;}
`;
  document.head.appendChild(el);
}
function Glyph({
  platform,
  size,
  fill
}) {
  const d = PATHS[platform] || PATHS.spotify;
  return /*#__PURE__*/React.createElement("svg", {
    width: size,
    height: size,
    viewBox: "0 0 24 24",
    fill: fill,
    "aria-hidden": "true"
  }, /*#__PURE__*/React.createElement("path", {
    d: d
  }));
}
function PlatformIcon({
  platform,
  size = 18,
  chip = false,
  ...rest
}) {
  const p = PLATFORMS[platform] || PLATFORMS.spotify;
  if (chip) {
    const pad = Math.round(size * 0.24);
    return /*#__PURE__*/React.createElement("span", _extends({
      className: "cmds-plat cmds-plat--chip",
      title: p.name,
      style: {
        width: size,
        height: size,
        padding: pad,
        background: p.color
      }
    }, rest), /*#__PURE__*/React.createElement(Glyph, {
      platform: platform,
      size: size - pad * 2,
      fill: "#fff"
    }));
  }
  return /*#__PURE__*/React.createElement("span", _extends({
    className: "cmds-plat",
    title: p.name,
    style: {
      width: size,
      height: size
    }
  }, rest), /*#__PURE__*/React.createElement(Glyph, {
    platform: platform,
    size: size,
    fill: p.color
  }));
}
const CM_PLATFORMS = PLATFORMS;
Object.assign(__ds_scope, { PlatformIcon, CM_PLATFORMS });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/data/PlatformIcon.jsx", error: String((e && e.message) || e) }); }

// components/data/ScoreRing.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Score ring — circular 0–100 gauge for Chartmetric scores
 * (CPP / popularity). Color shifts with the value band.
 */

function ScoreRing({
  value = 0,
  max = 100,
  size = 72,
  thickness = 7,
  label,
  color,
  ...rest
}) {
  const v = Math.max(0, Math.min(max, value));
  const pct = v / max;
  const r = (size - thickness) / 2;
  const c = 2 * Math.PI * r;
  const band = color || (pct >= 0.75 ? "var(--cm-stage-superstar)" : pct >= 0.5 ? "var(--cm-blue-500)" : pct >= 0.25 ? "var(--cm-stage-midlevel)" : "var(--cm-n-400)");
  return /*#__PURE__*/React.createElement("span", _extends({
    style: {
      display: "inline-flex",
      flexDirection: "column",
      alignItems: "center",
      gap: 4
    }
  }, rest), /*#__PURE__*/React.createElement("span", {
    style: {
      position: "relative",
      width: size,
      height: size
    }
  }, /*#__PURE__*/React.createElement("svg", {
    width: size,
    height: size,
    style: {
      transform: "rotate(-90deg)"
    }
  }, /*#__PURE__*/React.createElement("circle", {
    cx: size / 2,
    cy: size / 2,
    r: r,
    fill: "none",
    stroke: "var(--cm-n-200)",
    strokeWidth: thickness
  }), /*#__PURE__*/React.createElement("circle", {
    cx: size / 2,
    cy: size / 2,
    r: r,
    fill: "none",
    stroke: band,
    strokeWidth: thickness,
    strokeLinecap: "round",
    strokeDasharray: c,
    strokeDashoffset: c * (1 - pct),
    style: {
      transition: "stroke-dashoffset var(--cm-dur-slower) var(--cm-ease-out)"
    }
  })), /*#__PURE__*/React.createElement("span", {
    style: {
      position: "absolute",
      inset: 0,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      fontFamily: "var(--cm-font-sans)",
      fontWeight: "var(--cm-fw-bold)",
      fontSize: Math.round(size * 0.3),
      fontVariantNumeric: "tabular-nums lining-nums",
      letterSpacing: "-0.02em",
      color: "var(--cm-n-900)"
    }
  }, Math.round(v))), label && /*#__PURE__*/React.createElement("span", {
    style: {
      font: "var(--cm-fw-semibold) var(--cm-fs-micro)/1 var(--cm-font-sans)",
      letterSpacing: "var(--cm-ls-caps)",
      textTransform: "uppercase",
      color: "var(--cm-text-tertiary)"
    }
  }, label));
}
Object.assign(__ds_scope, { ScoreRing });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/data/ScoreRing.jsx", error: String((e && e.message) || e) }); }

// components/data/Sparkline.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Sparkline — compact inline trend line built from a numeric
 * series. Optional area fill and end dot. Auto-colors by net
 * direction unless a color is supplied.
 */

function Sparkline({
  data = [],
  width = 96,
  height = 28,
  color,
  fill = true,
  showDot = true,
  strokeWidth = 1.75,
  ...rest
}) {
  if (!data.length) return /*#__PURE__*/React.createElement("svg", _extends({
    width: width,
    height: height
  }, rest));
  const min = Math.min(...data);
  const max = Math.max(...data);
  const span = max - min || 1;
  const stepX = width / (data.length - 1 || 1);
  const pad = strokeWidth + 1;
  const y = v => height - pad - (v - min) / span * (height - pad * 2);
  const pts = data.map((v, i) => [i * stepX, y(v)]);
  const line = pts.map((p, i) => `${i ? "L" : "M"}${p[0].toFixed(1)} ${p[1].toFixed(1)}`).join(" ");
  const area = `${line} L${width} ${height} L0 ${height} Z`;
  const dir = data[data.length - 1] - data[0];
  const stroke = color || (dir >= 0 ? "var(--cm-positive)" : "var(--cm-negative)");
  const gid = "cmds-spark-" + Math.random().toString(36).slice(2, 8);
  const last = pts[pts.length - 1];
  return /*#__PURE__*/React.createElement("svg", _extends({
    width: width,
    height: height,
    style: {
      display: "block",
      overflow: "visible"
    }
  }, rest), fill && /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("defs", null, /*#__PURE__*/React.createElement("linearGradient", {
    id: gid,
    x1: "0",
    y1: "0",
    x2: "0",
    y2: "1"
  }, /*#__PURE__*/React.createElement("stop", {
    offset: "0%",
    stopColor: stroke,
    stopOpacity: "0.22"
  }), /*#__PURE__*/React.createElement("stop", {
    offset: "100%",
    stopColor: stroke,
    stopOpacity: "0"
  }))), /*#__PURE__*/React.createElement("path", {
    d: area,
    fill: `url(#${gid})`
  })), /*#__PURE__*/React.createElement("path", {
    d: line,
    fill: "none",
    stroke: stroke,
    strokeWidth: strokeWidth,
    strokeLinecap: "round",
    strokeLinejoin: "round"
  }), showDot && /*#__PURE__*/React.createElement("circle", {
    cx: last[0],
    cy: last[1],
    r: strokeWidth + 0.5,
    fill: stroke
  }));
}
Object.assign(__ds_scope, { Sparkline });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/data/Sparkline.jsx", error: String((e && e.message) || e) }); }

// components/data/StageBadge.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Career-stage badge — Chartmetric's artist tiering taxonomy.
 * Stages descend by prestige: legendary → superstar → mainstream
 * → mid-level → developing.
 */

const STAGES = {
  legendary: {
    label: "Legendary",
    color: "var(--cm-stage-legendary)"
  },
  superstar: {
    label: "Superstar",
    color: "var(--cm-stage-superstar)"
  },
  mainstream: {
    label: "Mainstream",
    color: "var(--cm-stage-mainstream)"
  },
  midlevel: {
    label: "Mid-Level",
    color: "var(--cm-stage-midlevel)"
  },
  developing: {
    label: "Developing",
    color: "var(--cm-stage-developing)"
  }
};
const STYLE_ID = "cmds-stagebadge";
if (typeof document !== "undefined" && !document.getElementById(STYLE_ID)) {
  const el = document.createElement("style");
  el.id = STYLE_ID;
  el.textContent = `
.cmds-stage{display:inline-flex;align-items:center;gap:6px;font-family:var(--cm-font-sans);
  font-weight:var(--cm-fw-semibold);font-size:var(--cm-fs-micro);line-height:1;
  padding:5px 9px;border-radius:var(--cm-radius-pill);white-space:nowrap;
  background:var(--cm-n-100);color:var(--cm-n-800);}
.cmds-stage__dot{width:7px;height:7px;border-radius:50%;flex:none;}
.cmds-stage--solid{color:#fff;}
`;
  document.head.appendChild(el);
}
function StageBadge({
  stage = "developing",
  solid = false,
  ...rest
}) {
  const s = STAGES[stage] || STAGES.developing;
  const style = solid ? {
    background: s.color
  } : undefined;
  return /*#__PURE__*/React.createElement("span", _extends({
    className: ["cmds-stage", solid && "cmds-stage--solid"].filter(Boolean).join(" "),
    style: style
  }, rest), !solid && /*#__PURE__*/React.createElement("span", {
    className: "cmds-stage__dot",
    style: {
      background: s.color
    },
    "aria-hidden": "true"
  }), s.label);
}
const CM_CAREER_STAGES = STAGES;
Object.assign(__ds_scope, { StageBadge, CM_CAREER_STAGES });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/data/StageBadge.jsx", error: String((e && e.message) || e) }); }

// components/data/TrendDelta.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Trend delta — signed change with a directional arrow, tabular
 * figures, and semantic color. The single most repeated element
 * in the product (every metric row, every KPI).
 */

const STYLE_ID = "cmds-trenddelta";
if (typeof document !== "undefined" && !document.getElementById(STYLE_ID)) {
  const el = document.createElement("style");
  el.id = STYLE_ID;
  el.textContent = `
.cmds-delta{display:inline-flex;align-items:center;gap:3px;font-family:var(--cm-font-sans);
  font-weight:var(--cm-fw-semibold);font-variant-numeric:tabular-nums lining-nums;
  letter-spacing:-.01em;line-height:1;}
.cmds-delta--sm{font-size:var(--cm-fs-micro);}
.cmds-delta--md{font-size:var(--cm-fs-sm);}
.cmds-delta--lg{font-size:var(--cm-fs-md);}
.cmds-delta--up{color:var(--cm-positive-700);}
.cmds-delta--down{color:var(--cm-negative-700);}
.cmds-delta--flat{color:var(--cm-n-500);}
.cmds-delta__arrow{font-size:.85em;line-height:1;}
.cmds-delta--pill{padding:3px 7px;border-radius:var(--cm-radius-pill);}
.cmds-delta--pill.cmds-delta--up{background:var(--cm-positive-soft);}
.cmds-delta--pill.cmds-delta--down{background:var(--cm-negative-soft);}
.cmds-delta--pill.cmds-delta--flat{background:var(--cm-n-100);}
`;
  document.head.appendChild(el);
}
function TrendDelta({
  value,
  format = "percent",
  size = "md",
  pill = false,
  showArrow = true,
  ...rest
}) {
  const dir = value > 0 ? "up" : value < 0 ? "down" : "flat";
  const arrow = dir === "up" ? "▲" : dir === "down" ? "▼" : "—";
  const abs = Math.abs(value);
  const text = format === "percent" ? `${abs.toLocaleString(undefined, {
    maximumFractionDigits: 1
  })}%` : format === "signed" ? abs.toLocaleString() : abs.toLocaleString();
  const cls = ["cmds-delta", `cmds-delta--${size}`, `cmds-delta--${dir}`, pill && "cmds-delta--pill"].filter(Boolean).join(" ");
  return /*#__PURE__*/React.createElement("span", _extends({
    className: cls
  }, rest), showArrow && /*#__PURE__*/React.createElement("span", {
    className: "cmds-delta__arrow",
    "aria-hidden": "true"
  }, arrow), text);
}
Object.assign(__ds_scope, { TrendDelta });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/data/TrendDelta.jsx", error: String((e && e.message) || e) }); }

// components/data/MetricStat.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * KPI / metric tile — the atomic unit of every Chartmetric
 * dashboard. Label + big tabular value + delta, with optional
 * platform marker and sparkline.
 */

const STYLE_ID = "cmds-metricstat";
if (typeof document !== "undefined" && !document.getElementById(STYLE_ID)) {
  const el = document.createElement("style");
  el.id = STYLE_ID;
  el.textContent = `
.cmds-stat{display:flex;flex-direction:column;gap:6px;font-family:var(--cm-font-sans);min-width:0;}
.cmds-stat__head{display:flex;align-items:center;gap:7px;}
.cmds-stat__label{font-size:var(--cm-fs-caption);font-weight:var(--cm-fw-medium);color:var(--cm-n-500);
  text-transform:none;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.cmds-stat__value{font-weight:var(--cm-fw-bold);font-size:var(--cm-fs-metric);line-height:1;
  color:var(--cm-n-900);font-variant-numeric:tabular-nums lining-nums;letter-spacing:-.02em;}
.cmds-stat__value--md{font-size:var(--cm-fs-xl);}
.cmds-stat__foot{display:flex;align-items:center;gap:8px;}
.cmds-stat__sub{font-size:var(--cm-fs-caption);color:var(--cm-n-500);}
.cmds-stat--card{background:#fff;border:1px solid var(--cm-border);border-radius:var(--cm-radius-xl);
  padding:var(--cm-pad-card);box-shadow:var(--cm-shadow-card);}
`;
  document.head.appendChild(el);
}
function MetricStat({
  label,
  value,
  delta,
  deltaFormat = "percent",
  sub,
  icon = null,
  spark,
  size = "lg",
  card = false,
  ...rest
}) {
  return /*#__PURE__*/React.createElement("div", _extends({
    className: ["cmds-stat", card && "cmds-stat--card"].filter(Boolean).join(" ")
  }, rest), /*#__PURE__*/React.createElement("div", {
    className: "cmds-stat__head"
  }, icon, /*#__PURE__*/React.createElement("span", {
    className: "cmds-stat__label"
  }, label)), /*#__PURE__*/React.createElement("div", {
    className: ["cmds-stat__value", size === "md" && "cmds-stat__value--md"].filter(Boolean).join(" ")
  }, value), /*#__PURE__*/React.createElement("div", {
    className: "cmds-stat__foot"
  }, delta != null && /*#__PURE__*/React.createElement(__ds_scope.TrendDelta, {
    value: delta,
    format: deltaFormat,
    size: "sm",
    pill: true
  }), sub && /*#__PURE__*/React.createElement("span", {
    className: "cmds-stat__sub"
  }, sub), spark && /*#__PURE__*/React.createElement("div", {
    style: {
      marginLeft: "auto"
    }
  }, /*#__PURE__*/React.createElement(__ds_scope.Sparkline, {
    data: spark,
    width: 84,
    height: 26
  }))));
}
Object.assign(__ds_scope, { MetricStat });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/data/MetricStat.jsx", error: String((e && e.message) || e) }); }

// ui_kits/app/App.jsx
try { (() => {
/* Chartmetric app — shell + routing */
function EmptyState({
  label
}) {
  const {
    Icon
  } = window;
  return /*#__PURE__*/React.createElement("div", {
    className: "cm-screen"
  }, window.TopBar && /*#__PURE__*/React.createElement(window.TopBar, {
    title: label
  }), /*#__PURE__*/React.createElement("div", {
    className: "cm-empty"
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "construction",
    size: 40,
    style: {
      color: "var(--cm-n-300)"
    }
  }), /*#__PURE__*/React.createElement("p", null, label, " \u2014 not part of this UI-kit recreation.")));
}
function App() {
  const [route, setRoute] = React.useState("dashboard");
  let content;
  if (route === "dashboard") content = /*#__PURE__*/React.createElement(window.ArtistProfile, null);else if (route === "charts") content = /*#__PURE__*/React.createElement(window.ChartsScreen, null);else if (route === "talent") content = /*#__PURE__*/React.createElement(window.TalentSearch, null);else content = /*#__PURE__*/React.createElement(EmptyState, {
    label: {
      playlists: "Playlists",
      reports: "Reports",
      shortlists: "Shortlists"
    }[route]
  });
  return /*#__PURE__*/React.createElement("div", {
    className: "cm-app"
  }, /*#__PURE__*/React.createElement(window.Sidebar, {
    route: route,
    onNavigate: setRoute
  }), /*#__PURE__*/React.createElement("main", {
    className: "cm-main"
  }, content));
}
Object.assign(window, {
  App
});
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/app/App.jsx", error: String((e && e.message) || e) }); }

// ui_kits/app/ArtistProfile.jsx
try { (() => {
/* Chartmetric app — Artist profile (the signature screen) */
function ArtistProfile() {
  const NS = window.ChartmetricDesignSystem_05cea6;
  const {
    Button,
    IconButton,
    Tag,
    Tabs,
    Avatar,
    MetricStat,
    ScoreRing,
    StageBadge,
    PlatformIcon,
    TrendDelta
  } = NS;
  const {
    TopBar,
    StreamChart,
    Icon
  } = window;
  const a = window.CM_DATA.hero;
  const [tab, setTab] = React.useState("overview");
  const [platform, setPlatform] = React.useState("spotify");
  return /*#__PURE__*/React.createElement("div", {
    className: "cm-screen"
  }, /*#__PURE__*/React.createElement(TopBar, {
    title: a.name,
    crumb: "Artists"
  }), /*#__PURE__*/React.createElement("div", {
    className: "cm-page"
  }, /*#__PURE__*/React.createElement("section", {
    className: "cm-card cm-profile"
  }, /*#__PURE__*/React.createElement(Avatar, {
    src: a.img,
    name: a.name,
    size: 88
  }), /*#__PURE__*/React.createElement("div", {
    className: "cm-profile__id"
  }, /*#__PURE__*/React.createElement("div", {
    className: "cm-profile__namerow"
  }, /*#__PURE__*/React.createElement("h2", {
    className: "cm-profile__name"
  }, a.name), /*#__PURE__*/React.createElement(Icon, {
    name: "verified",
    size: 20,
    fill: 1,
    style: {
      color: "var(--cm-blue-500)"
    }
  })), /*#__PURE__*/React.createElement("div", {
    className: "cm-profile__sub"
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "location_on",
    size: 15,
    style: {
      color: "var(--cm-n-400)"
    }
  }), a.city, ", ", a.country), /*#__PURE__*/React.createElement("div", {
    className: "cm-profile__tags"
  }, a.genres.map(g => /*#__PURE__*/React.createElement(Tag, {
    key: g
  }, g))), /*#__PURE__*/React.createElement("div", {
    className: "cm-profile__badges"
  }, /*#__PURE__*/React.createElement(StageBadge, {
    stage: a.stage
  }), /*#__PURE__*/React.createElement("span", {
    className: "cm-momentum"
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "trending_up",
    size: 14
  }), a.momentum), /*#__PURE__*/React.createElement("span", {
    className: "cm-rank"
  }, "Global rank ", /*#__PURE__*/React.createElement("b", null, "#", a.rank)))), /*#__PURE__*/React.createElement("div", {
    className: "cm-profile__scores"
  }, /*#__PURE__*/React.createElement(ScoreRing, {
    value: a.cmScore,
    label: "CM Score",
    size: 76
  }), /*#__PURE__*/React.createElement(ScoreRing, {
    value: a.popularity,
    label: "Popularity",
    size: 76
  }), /*#__PURE__*/React.createElement(ScoreRing, {
    value: a.engagement,
    label: "Engagement",
    size: 76
  })), /*#__PURE__*/React.createElement("div", {
    className: "cm-profile__actions"
  }, /*#__PURE__*/React.createElement(Button, {
    variant: "primary",
    leadingIcon: /*#__PURE__*/React.createElement(Icon, {
      name: "bookmark_add",
      size: 16
    })
  }, "Shortlist"), /*#__PURE__*/React.createElement(Button, {
    variant: "secondary",
    leadingIcon: /*#__PURE__*/React.createElement(Icon, {
      name: "ios_share",
      size: 16
    })
  }, "Share"), /*#__PURE__*/React.createElement(IconButton, {
    label: "More",
    outline: true
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "more_horiz",
    size: 18
  })))), /*#__PURE__*/React.createElement(Tabs, {
    value: tab,
    onChange: setTab,
    tabs: [{
      label: "Overview",
      value: "overview"
    }, {
      label: "Audience",
      value: "audience"
    }, {
      label: "Playlists",
      value: "playlists",
      count: 218
    }, {
      label: "Charts",
      value: "charts",
      count: 34
    }, {
      label: "Tracks",
      value: "tracks"
    }, {
      label: "Similar",
      value: "similar"
    }]
  }), /*#__PURE__*/React.createElement("section", {
    className: "cm-kpis"
  }, a.kpis.map((k, i) => /*#__PURE__*/React.createElement("div", {
    className: "cm-card cm-kpi",
    key: i
  }, /*#__PURE__*/React.createElement(MetricStat, {
    label: k.label,
    value: k.value,
    delta: k.delta,
    spark: k.spark,
    icon: /*#__PURE__*/React.createElement(PlatformIcon, {
      platform: k.platform,
      size: 15
    })
  })))), /*#__PURE__*/React.createElement("div", {
    className: "cm-cols"
  }, /*#__PURE__*/React.createElement("section", {
    className: "cm-card cm-chartcard"
  }, /*#__PURE__*/React.createElement("div", {
    className: "cm-chartcard__head"
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("span", {
    className: "cm-overline"
  }, "Streaming"), /*#__PURE__*/React.createElement("h3", {
    className: "cm-chartcard__title"
  }, "Spotify streams \xB7 last 30 days")), /*#__PURE__*/React.createElement("div", {
    className: "cm-chartcard__controls"
  }, ["spotify", "youtube", "applemusic"].map(p => /*#__PURE__*/React.createElement("button", {
    key: p,
    className: "cm-chip" + (platform === p ? " is-active" : ""),
    onClick: () => setPlatform(p)
  }, /*#__PURE__*/React.createElement(PlatformIcon, {
    platform: p,
    size: 14
  }), " ", NS.CM_PLATFORMS[p].name)))), /*#__PURE__*/React.createElement("div", {
    className: "cm-chartcard__metric"
  }, /*#__PURE__*/React.createElement("span", {
    className: "cm-numeric",
    style: {
      fontWeight: 800,
      fontSize: 30
    }
  }, "38,204,118"), /*#__PURE__*/React.createElement(TrendDelta, {
    value: 4.3,
    pill: true
  }), /*#__PURE__*/React.createElement("span", {
    className: "cm-chartcard__metriclbl"
  }, "total streams")), /*#__PURE__*/React.createElement(StreamChart, {
    data: a.streamSeries
  })), /*#__PURE__*/React.createElement("aside", {
    className: "cm-side"
  }, /*#__PURE__*/React.createElement("section", {
    className: "cm-card"
  }, /*#__PURE__*/React.createElement("span", {
    className: "cm-overline"
  }, "Noteworthy insights"), /*#__PURE__*/React.createElement("ul", {
    className: "cm-insights"
  }, a.insights.map((ins, i) => /*#__PURE__*/React.createElement("li", {
    key: i,
    className: "cm-insight"
  }, /*#__PURE__*/React.createElement("span", {
    className: "cm-insight__dot cm-insight__dot--" + ins.tone
  }), /*#__PURE__*/React.createElement("span", {
    dangerouslySetInnerHTML: {
      __html: ins.text
    }
  }))))), /*#__PURE__*/React.createElement("section", {
    className: "cm-card cm-release"
  }, /*#__PURE__*/React.createElement("span", {
    className: "cm-overline"
  }, "Latest release"), /*#__PURE__*/React.createElement("div", {
    className: "cm-release__row"
  }, /*#__PURE__*/React.createElement(Avatar, {
    src: a.release.cover,
    name: a.release.title,
    shape: "square",
    size: 56
  }), /*#__PURE__*/React.createElement("div", {
    className: "cm-release__meta"
  }, /*#__PURE__*/React.createElement("div", {
    className: "cm-release__title"
  }, a.release.title), /*#__PURE__*/React.createElement("div", {
    className: "cm-release__sub"
  }, a.release.type, " \xB7 ", a.release.date), /*#__PURE__*/React.createElement("div", {
    className: "cm-release__sub"
  }, "Playlist reach ", /*#__PURE__*/React.createElement("b", null, a.release.playlistReach))), /*#__PURE__*/React.createElement(ScoreRing, {
    value: a.release.score,
    label: "Score",
    size: 58,
    thickness: 6
  }))), /*#__PURE__*/React.createElement("section", {
    className: "cm-card"
  }, /*#__PURE__*/React.createElement("span", {
    className: "cm-overline"
  }, "Top markets"), /*#__PURE__*/React.createElement("ul", {
    className: "cm-markets"
  }, a.markets.map(m => /*#__PURE__*/React.createElement("li", {
    key: m.city,
    className: "cm-market"
  }, /*#__PURE__*/React.createElement("span", {
    className: "cm-market__city"
  }, m.city, " ", /*#__PURE__*/React.createElement("span", {
    className: "cm-market__cc"
  }, m.country)), /*#__PURE__*/React.createElement("span", {
    className: "cm-market__bar"
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: m.pct + "%"
    }
  })), /*#__PURE__*/React.createElement("span", {
    className: "cm-market__val cm-numeric"
  }, (m.listeners / 1e6).toFixed(2), "M")))))))));
}
Object.assign(window, {
  ArtistProfile
});
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/app/ArtistProfile.jsx", error: String((e && e.message) || e) }); }

// ui_kits/app/ChartsScreen.jsx
try { (() => {
/* Chartmetric app — Charts (leaderboard table) */
function ChartsScreen() {
  const NS = window.ChartmetricDesignSystem_05cea6;
  const {
    Avatar,
    StageBadge,
    TrendDelta,
    Sparkline,
    Select,
    Tag,
    Badge
  } = NS;
  const {
    TopBar,
    Icon
  } = window;
  const rows = window.CM_DATA.charts;
  const movement = r => {
    const d = r.prev - r.rank;
    if (d === 0) return /*#__PURE__*/React.createElement("span", {
      className: "cm-move cm-move--flat"
    }, /*#__PURE__*/React.createElement(Icon, {
      name: "remove",
      size: 14
    }));
    if (d > 0) return /*#__PURE__*/React.createElement("span", {
      className: "cm-move cm-move--up"
    }, /*#__PURE__*/React.createElement(Icon, {
      name: "arrow_drop_up",
      size: 18
    }), d);
    return /*#__PURE__*/React.createElement("span", {
      className: "cm-move cm-move--down"
    }, /*#__PURE__*/React.createElement(Icon, {
      name: "arrow_drop_down",
      size: 18
    }), -d);
  };
  return /*#__PURE__*/React.createElement("div", {
    className: "cm-screen"
  }, /*#__PURE__*/React.createElement(TopBar, {
    title: "Charts",
    crumb: "Discover"
  }), /*#__PURE__*/React.createElement("div", {
    className: "cm-page"
  }, /*#__PURE__*/React.createElement("div", {
    className: "cm-filters"
  }, /*#__PURE__*/React.createElement(Tag, {
    color: "var(--cm-platform-spotify)"
  }, "Spotify"), /*#__PURE__*/React.createElement(Select, {
    size: "sm",
    defaultValue: "artists"
  }, /*#__PURE__*/React.createElement("option", {
    value: "artists"
  }, "Artists"), /*#__PURE__*/React.createElement("option", {
    value: "tracks"
  }, "Tracks")), /*#__PURE__*/React.createElement(Select, {
    size: "sm",
    defaultValue: "listeners"
  }, /*#__PURE__*/React.createElement("option", {
    value: "listeners"
  }, "Monthly Listeners"), /*#__PURE__*/React.createElement("option", {
    value: "followers"
  }, "Followers"), /*#__PURE__*/React.createElement("option", {
    value: "score"
  }, "CM Score")), /*#__PURE__*/React.createElement(Select, {
    size: "sm",
    defaultValue: "global"
  }, /*#__PURE__*/React.createElement("option", {
    value: "global"
  }, "\uD83C\uDF0E Global"), /*#__PURE__*/React.createElement("option", {
    value: "us"
  }, "United States"), /*#__PURE__*/React.createElement("option", {
    value: "ng"
  }, "Nigeria")), /*#__PURE__*/React.createElement(Select, {
    size: "sm",
    defaultValue: "28d"
  }, /*#__PURE__*/React.createElement("option", {
    value: "7d"
  }, "7 days"), /*#__PURE__*/React.createElement("option", {
    value: "28d"
  }, "28 days")), /*#__PURE__*/React.createElement("span", {
    className: "cm-filters__spacer"
  }), /*#__PURE__*/React.createElement(Badge, {
    tone: "neutral",
    outline: true
  }, rows.length, " results")), /*#__PURE__*/React.createElement("section", {
    className: "cm-card cm-table"
  }, /*#__PURE__*/React.createElement("div", {
    className: "cm-tr cm-tr--head"
  }, /*#__PURE__*/React.createElement("span", {
    className: "cm-td cm-td--rank"
  }, "#"), /*#__PURE__*/React.createElement("span", {
    className: "cm-td cm-td--move"
  }, "+/\u2212"), /*#__PURE__*/React.createElement("span", {
    className: "cm-td cm-td--artist"
  }, "Artist"), /*#__PURE__*/React.createElement("span", {
    className: "cm-td cm-td--score"
  }, "CM Score"), /*#__PURE__*/React.createElement("span", {
    className: "cm-td cm-td--num"
  }, "Listeners"), /*#__PURE__*/React.createElement("span", {
    className: "cm-td cm-td--delta"
  }, "\u0394 28d"), /*#__PURE__*/React.createElement("span", {
    className: "cm-td cm-td--spark"
  }, "Trend")), rows.map(r => /*#__PURE__*/React.createElement("div", {
    className: "cm-tr",
    key: r.rank
  }, /*#__PURE__*/React.createElement("span", {
    className: "cm-td cm-td--rank cm-numeric"
  }, r.rank), /*#__PURE__*/React.createElement("span", {
    className: "cm-td cm-td--move"
  }, movement(r)), /*#__PURE__*/React.createElement("span", {
    className: "cm-td cm-td--artist"
  }, /*#__PURE__*/React.createElement(Avatar, {
    src: r.img,
    name: r.name,
    size: 36
  }), /*#__PURE__*/React.createElement("span", {
    className: "cm-artistcell"
  }, /*#__PURE__*/React.createElement("span", {
    className: "cm-artistcell__name"
  }, r.name), /*#__PURE__*/React.createElement(StageBadge, {
    stage: r.stage
  }))), /*#__PURE__*/React.createElement("span", {
    className: "cm-td cm-td--score cm-numeric"
  }, /*#__PURE__*/React.createElement("b", null, r.score)), /*#__PURE__*/React.createElement("span", {
    className: "cm-td cm-td--num cm-numeric"
  }, r.listeners), /*#__PURE__*/React.createElement("span", {
    className: "cm-td cm-td--delta"
  }, /*#__PURE__*/React.createElement(TrendDelta, {
    value: r.delta,
    size: "sm"
  })), /*#__PURE__*/React.createElement("span", {
    className: "cm-td cm-td--spark"
  }, /*#__PURE__*/React.createElement(Sparkline, {
    data: r.spark,
    width: 92,
    height: 26
  })))))));
}
Object.assign(window, {
  ChartsScreen
});
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/app/ChartsScreen.jsx", error: String((e && e.message) || e) }); }

// ui_kits/app/Sidebar.jsx
try { (() => {
/* Chartmetric app — dark sidebar nav */
function Icon({
  name,
  size = 20,
  fill = 0,
  style
}) {
  return /*#__PURE__*/React.createElement("span", {
    className: "ms",
    style: {
      fontSize: size,
      fontVariationSettings: `'FILL' ${fill}`,
      ...style
    }
  }, name);
}
const NAV = [{
  id: "dashboard",
  icon: "dashboard",
  label: "Dashboard"
}, {
  id: "charts",
  icon: "leaderboard",
  label: "Charts"
}, {
  id: "talent",
  icon: "travel_explore",
  label: "Talent Discovery"
}, {
  id: "playlists",
  icon: "queue_music",
  label: "Playlists"
}, {
  id: "reports",
  icon: "description",
  label: "Reports"
}, {
  id: "shortlists",
  icon: "bookmark",
  label: "Shortlists"
}];
function Sidebar({
  route,
  onNavigate
}) {
  const D = window.CM_DATA;
  return /*#__PURE__*/React.createElement("aside", {
    className: "cm-sidebar"
  }, /*#__PURE__*/React.createElement("div", {
    className: "cm-sidebar__logo"
  }, /*#__PURE__*/React.createElement("img", {
    src: "https://cdn.sanity.io/images/zdrkqyxr/production-alt/c911082691fc6a026e5f476eee1daf544076bb98-555x100.svg",
    alt: "Chartmetric",
    height: "22"
  })), /*#__PURE__*/React.createElement("nav", {
    className: "cm-nav"
  }, NAV.map(n => /*#__PURE__*/React.createElement("button", {
    key: n.id,
    className: "cm-nav__item" + (route === n.id ? " is-active" : ""),
    onClick: () => onNavigate(n.id)
  }, /*#__PURE__*/React.createElement(Icon, {
    name: n.icon,
    size: 20,
    fill: route === n.id ? 1 : 0
  }), /*#__PURE__*/React.createElement("span", null, n.label)))), /*#__PURE__*/React.createElement("div", {
    className: "cm-nav__section"
  }, "Favorites"), /*#__PURE__*/React.createElement("div", {
    className: "cm-fav"
  }, [["Burna Boy", D.hero.img], ["Ice Spice", ""], ["G.E.M.", ""]].map(([n, img]) => /*#__PURE__*/React.createElement("button", {
    key: n,
    className: "cm-fav__item",
    onClick: () => onNavigate("dashboard")
  }, /*#__PURE__*/React.createElement("span", {
    className: "cm-fav__avatar",
    style: img ? {
      backgroundImage: `url(${img})`
    } : {}
  }, !img && n[0]), /*#__PURE__*/React.createElement("span", null, n)))), /*#__PURE__*/React.createElement("div", {
    className: "cm-sidebar__foot"
  }, /*#__PURE__*/React.createElement("button", {
    className: "cm-nav__item"
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "settings",
    size: 20
  }), /*#__PURE__*/React.createElement("span", null, "Settings")), /*#__PURE__*/React.createElement("div", {
    className: "cm-account"
  }, /*#__PURE__*/React.createElement("span", {
    className: "cm-account__avatar"
  }, "AR"), /*#__PURE__*/React.createElement("div", {
    className: "cm-account__meta"
  }, /*#__PURE__*/React.createElement("div", {
    className: "cm-account__name"
  }, "A&R Studio"), /*#__PURE__*/React.createElement("div", {
    className: "cm-account__plan"
  }, "Premium plan")))));
}
Object.assign(window, {
  Sidebar,
  Icon
});
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/app/Sidebar.jsx", error: String((e && e.message) || e) }); }

// ui_kits/app/StreamChart.jsx
try { (() => {
/* Streaming-over-time area chart (data viz, scales to its container width). */
function StreamChart({
  data = [],
  height = 240,
  color = "var(--cm-blue-500)",
  grad = "cmStreamGrad"
}) {
  const W = 1000,
    H = height;
  const pad = {
    t: 16,
    r: 8,
    b: 26,
    l: 8
  };
  if (!data.length) return /*#__PURE__*/React.createElement("svg", {
    viewBox: `0 0 ${W} ${H}`
  });
  const min = Math.min(...data),
    max = Math.max(...data);
  const span = max - min || 1;
  const stepX = (W - pad.l - pad.r) / (data.length - 1);
  const x = i => pad.l + i * stepX;
  const y = v => pad.t + (1 - (v - min) / span) * (H - pad.t - pad.b);
  const line = data.map((v, i) => `${i ? "L" : "M"}${x(i).toFixed(1)} ${y(v).toFixed(1)}`).join(" ");
  const area = `${line} L${x(data.length - 1)} ${H - pad.b} L${x(0)} ${H - pad.b} Z`;
  const gridY = [0, 0.25, 0.5, 0.75, 1].map(p => pad.t + p * (H - pad.t - pad.b));
  const months = ["", "Wk 1", "Wk 2", "Wk 3", "Now"];
  return /*#__PURE__*/React.createElement("svg", {
    viewBox: `0 0 ${W} ${H}`,
    preserveAspectRatio: "none",
    style: {
      width: "100%",
      height,
      display: "block"
    }
  }, /*#__PURE__*/React.createElement("defs", null, /*#__PURE__*/React.createElement("linearGradient", {
    id: grad,
    x1: "0",
    y1: "0",
    x2: "0",
    y2: "1"
  }, /*#__PURE__*/React.createElement("stop", {
    offset: "0%",
    stopColor: color,
    stopOpacity: "0.20"
  }), /*#__PURE__*/React.createElement("stop", {
    offset: "100%",
    stopColor: color,
    stopOpacity: "0"
  }))), gridY.map((gy, i) => /*#__PURE__*/React.createElement("line", {
    key: i,
    x1: pad.l,
    x2: W - pad.r,
    y1: gy,
    y2: gy,
    stroke: "var(--cm-n-100)",
    strokeWidth: "1",
    vectorEffect: "non-scaling-stroke"
  })), /*#__PURE__*/React.createElement("path", {
    d: area,
    fill: `url(#${grad})`
  }), /*#__PURE__*/React.createElement("path", {
    d: line,
    fill: "none",
    stroke: color,
    strokeWidth: "2.25",
    vectorEffect: "non-scaling-stroke",
    strokeLinejoin: "round",
    strokeLinecap: "round"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: x(data.length - 1),
    cy: y(data[data.length - 1]),
    r: "3.5",
    fill: color
  }), [0, 0.25, 0.5, 0.75, 1].map((p, i) => /*#__PURE__*/React.createElement("text", {
    key: i,
    x: pad.l + p * (W - pad.l - pad.r),
    y: H - 8,
    fill: "var(--cm-n-400)",
    fontSize: "11",
    fontFamily: "var(--cm-font-sans)",
    textAnchor: i === 0 ? "start" : i === 4 ? "end" : "middle"
  }, months[i])));
}
Object.assign(window, {
  StreamChart
});
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/app/StreamChart.jsx", error: String((e && e.message) || e) }); }

// ui_kits/app/TalentSearch.jsx
try { (() => {
/* Chartmetric app — Talent Discovery (A&R card grid) */
function TalentSearch() {
  const NS = window.ChartmetricDesignSystem_05cea6;
  const {
    Avatar,
    StageBadge,
    Badge,
    Tag,
    Sparkline,
    ScoreRing,
    TrendDelta,
    Button,
    Switch
  } = NS;
  const {
    TopBar,
    Icon
  } = window;
  const people = window.CM_DATA.talent;
  return /*#__PURE__*/React.createElement("div", {
    className: "cm-screen"
  }, /*#__PURE__*/React.createElement(TopBar, {
    title: "Talent Discovery",
    crumb: "A&R Tools"
  }), /*#__PURE__*/React.createElement("div", {
    className: "cm-page"
  }, /*#__PURE__*/React.createElement("div", {
    className: "cm-discover-bar"
  }, /*#__PURE__*/React.createElement("div", {
    className: "cm-discover-bar__filters"
  }, /*#__PURE__*/React.createElement(Tag, {
    onRemove: () => {}
  }, "Career: Developing"), /*#__PURE__*/React.createElement(Tag, {
    onRemove: () => {}
  }, "Momentum: Explosive Growth"), /*#__PURE__*/React.createElement(Tag, {
    onRemove: () => {}
  }, "Region: UK & West Africa"), /*#__PURE__*/React.createElement("button", {
    className: "cm-addfilter"
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "add",
    size: 15
  }), " Add filter")), /*#__PURE__*/React.createElement(Switch, {
    label: "Unsigned only",
    defaultChecked: true
  })), /*#__PURE__*/React.createElement("div", {
    className: "cm-talent-grid"
  }, people.map(p => /*#__PURE__*/React.createElement("section", {
    className: "cm-card cm-talentcard",
    key: p.name
  }, /*#__PURE__*/React.createElement("div", {
    className: "cm-talentcard__top"
  }, /*#__PURE__*/React.createElement(Avatar, {
    src: p.img,
    name: p.name,
    size: 52
  }), /*#__PURE__*/React.createElement(ScoreRing, {
    value: p.score,
    label: "CM",
    size: 54,
    thickness: 6
  })), /*#__PURE__*/React.createElement("div", {
    className: "cm-talentcard__name"
  }, p.name), /*#__PURE__*/React.createElement("div", {
    className: "cm-talentcard__loc"
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "public",
    size: 13,
    style: {
      color: "var(--cm-n-400)"
    }
  }), " ", p.country), /*#__PURE__*/React.createElement("div", {
    className: "cm-talentcard__tags"
  }, p.genres.map(g => /*#__PURE__*/React.createElement(Tag, {
    key: g
  }, g))), /*#__PURE__*/React.createElement("div", {
    className: "cm-talentcard__momentum"
  }, /*#__PURE__*/React.createElement(Badge, {
    tone: "positive",
    dot: true
  }, p.momentum), /*#__PURE__*/React.createElement(TrendDelta, {
    value: p.delta,
    size: "sm"
  })), /*#__PURE__*/React.createElement(Sparkline, {
    data: p.spark,
    width: 240,
    height: 34,
    color: "var(--cm-blue-500)"
  }), /*#__PURE__*/React.createElement("div", {
    className: "cm-talentcard__foot"
  }, /*#__PURE__*/React.createElement("span", {
    className: "cm-talentcard__listeners cm-numeric"
  }, p.listeners, " ", /*#__PURE__*/React.createElement("span", null, "listeners")), /*#__PURE__*/React.createElement(Button, {
    size: "sm",
    variant: "secondary",
    leadingIcon: /*#__PURE__*/React.createElement(Icon, {
      name: "bookmark_add",
      size: 14
    })
  }, "Save")))))));
}
Object.assign(window, {
  TalentSearch
});
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/app/TalentSearch.jsx", error: String((e && e.message) || e) }); }

// ui_kits/app/TopBar.jsx
try { (() => {
/* Chartmetric app — top bar with global search ("Add Data"), filters, actions */
function TopBar({
  title,
  crumb
}) {
  const {
    Button,
    IconButton
  } = window.ChartmetricDesignSystem_05cea6;
  const {
    Icon
  } = window;
  const [q, setQ] = React.useState("");
  return /*#__PURE__*/React.createElement("header", {
    className: "cm-topbar"
  }, /*#__PURE__*/React.createElement("div", {
    className: "cm-topbar__left"
  }, crumb && /*#__PURE__*/React.createElement("span", {
    className: "cm-crumb"
  }, crumb, /*#__PURE__*/React.createElement("span", {
    className: "cm-crumb__sep"
  }, "/")), /*#__PURE__*/React.createElement("h1", {
    className: "cm-topbar__title"
  }, title)), /*#__PURE__*/React.createElement("div", {
    className: "cm-search"
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "search",
    size: 18,
    style: {
      color: "var(--cm-n-400)"
    }
  }), /*#__PURE__*/React.createElement("input", {
    value: q,
    onChange: e => setQ(e.target.value),
    placeholder: "Search artists, tracks, playlists, curators\u2026"
  }), /*#__PURE__*/React.createElement("kbd", {
    className: "cm-kbd"
  }, "/")), /*#__PURE__*/React.createElement("div", {
    className: "cm-topbar__actions"
  }, /*#__PURE__*/React.createElement(IconButton, {
    label: "Notifications",
    outline: true
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "notifications",
    size: 18
  })), /*#__PURE__*/React.createElement(IconButton, {
    label: "Help",
    outline: true
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "help",
    size: 18
  })), /*#__PURE__*/React.createElement(Button, {
    variant: "secondary",
    size: "md",
    leadingIcon: /*#__PURE__*/React.createElement(Icon, {
      name: "add",
      size: 16
    })
  }, "Add data")));
}
Object.assign(window, {
  TopBar
});
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/app/TopBar.jsx", error: String((e && e.message) || e) }); }

// ui_kits/app/data.js
try { (() => {
/* Fake Chartmetric data for the UI-kit recreation (not real-time data). */
(function () {
  const series = (start, n, drift, vol) => {
    const out = [start];
    for (let i = 1; i < n; i++) {
      out.push(Math.max(0, out[i - 1] * (1 + drift + Math.sin(i * 1.7) * vol)));
    }
    return out.map(x => Math.round(x));
  };
  const IMG = {
    burna: "https://cdn.sanity.io/images/zdrkqyxr/production-alt/87414e236a14d2849bde5c91482443d8e885b962-657x658.png?rect=100,48,471,610&w=240&h=240&fit=crop",
    gem: "https://cdn.sanity.io/images/zdrkqyxr/production-alt/072a40fa0e06686ee8da5309707073de0f4e7d71-466x603.png?w=240&h=240&fit=crop",
    ice: "https://cdn.sanity.io/images/zdrkqyxr/production-alt/a94ce761830c687fdf6f9219e02bb333291d7f35-708x1024.png?w=240&h=240&fit=crop"
  };
  window.CM_DATA = {
    hero: {
      name: "Burna Boy",
      img: IMG.burna,
      verified: true,
      country: "Nigeria",
      city: "Port Harcourt",
      genres: ["Afrobeats", "Afro-fusion", "Pop"],
      stage: "superstar",
      momentum: "Growth",
      cmScore: 86,
      popularity: 88,
      engagement: 71,
      rank: 142,
      kpis: [{
        platform: "spotify",
        label: "Spotify Followers",
        value: "12.4M",
        delta: 1.8,
        spark: series(900, 12, 0.02, 0.01)
      }, {
        platform: "spotify",
        label: "Monthly Listeners",
        value: "38.2M",
        delta: 4.3,
        spark: series(700, 12, 0.03, 0.02)
      }, {
        platform: "youtube",
        label: "YouTube Subscribers",
        value: "6.91M",
        delta: 0.9,
        spark: series(500, 12, 0.015, 0.01)
      }, {
        platform: "tiktok",
        label: "TikTok Followers",
        value: "4.05M",
        delta: 7.2,
        spark: series(300, 12, 0.05, 0.03)
      }, {
        platform: "instagram",
        label: "Instagram Followers",
        value: "16.8M",
        delta: 1.1,
        spark: series(800, 12, 0.01, 0.01)
      }, {
        platform: "shazam",
        label: "Shazams",
        value: "9.2M",
        delta: -2.4,
        spark: series(600, 12, -0.01, 0.02)
      }],
      streamSeries: series(1200, 30, 0.012, 0.02),
      markets: [{
        city: "Lagos",
        country: "NG",
        listeners: 2_410_000,
        pct: 100
      }, {
        city: "London",
        country: "GB",
        listeners: 1_980_000,
        pct: 82
      }, {
        city: "Paris",
        country: "FR",
        listeners: 1_240_000,
        pct: 51
      }, {
        city: "New York",
        country: "US",
        listeners: 1_090_000,
        pct: 45
      }, {
        city: "Accra",
        country: "GH",
        listeners: 870_000,
        pct: 36
      }],
      insights: [{
        tone: "positive",
        text: "Added to Spotify's <b>Hot Hits USA</b> (2.1M reach)"
      }, {
        tone: "positive",
        text: "TikTok creations up <b>+7.2%</b> week-over-week"
      }, {
        tone: "info",
        text: "New peak: <b>#3</b> on Apple Music Nigeria"
      }, {
        tone: "negative",
        text: "Shazams cooling <b>−2.4%</b> in last 28 days"
      }],
      release: {
        title: "Higher",
        type: "Single",
        date: "2 days ago",
        cover: IMG.burna,
        score: 74,
        playlistReach: "4.1M"
      }
    },
    charts: [{
      rank: 1,
      prev: 1,
      name: "Sabrina Carpenter",
      img: "",
      stage: "superstar",
      score: 94,
      listeners: "61.2M",
      delta: 2.1,
      spark: series(900, 10, 0.02, 0.01)
    }, {
      rank: 2,
      prev: 4,
      name: "Chappell Roan",
      img: "",
      stage: "mainstream",
      score: 91,
      listeners: "44.8M",
      delta: 9.4,
      spark: series(500, 10, 0.06, 0.02)
    }, {
      rank: 3,
      prev: 2,
      name: "Ice Spice",
      img: IMG.ice,
      stage: "mainstream",
      score: 88,
      listeners: "39.1M",
      delta: -1.2,
      spark: series(700, 10, -0.005, 0.02)
    }, {
      rank: 4,
      prev: 7,
      name: "Burna Boy",
      img: IMG.burna,
      stage: "superstar",
      score: 86,
      listeners: "38.2M",
      delta: 4.3,
      spark: series(600, 10, 0.04, 0.02)
    }, {
      rank: 5,
      prev: 3,
      name: "G.E.M.",
      img: IMG.gem,
      stage: "mainstream",
      score: 84,
      listeners: "21.7M",
      delta: -0.6,
      spark: series(550, 10, 0.0, 0.02)
    }, {
      rank: 6,
      prev: 9,
      name: "Tyla",
      img: "",
      stage: "midlevel",
      score: 80,
      listeners: "18.9M",
      delta: 6.7,
      spark: series(300, 10, 0.05, 0.03)
    }, {
      rank: 7,
      prev: 6,
      name: "PinkPantheress",
      img: "",
      stage: "midlevel",
      score: 78,
      listeners: "16.2M",
      delta: 1.0,
      spark: series(400, 10, 0.02, 0.02)
    }, {
      rank: 8,
      prev: 12,
      name: "Artemas",
      img: "",
      stage: "developing",
      score: 71,
      listeners: "11.4M",
      delta: 12.8,
      spark: series(120, 10, 0.09, 0.03)
    }],
    talent: [{
      name: "Odeal",
      img: "",
      country: "GB",
      genres: ["R&B", "Afro-soul"],
      stage: "developing",
      score: 64,
      momentum: "Explosive Growth",
      delta: 18.2,
      listeners: "3.1M",
      spark: series(80, 10, 0.1, 0.03)
    }, {
      name: "Lay Bankz",
      img: "",
      country: "US",
      genres: ["Pop", "Rap"],
      stage: "developing",
      score: 61,
      momentum: "Growth",
      delta: 11.5,
      listeners: "2.7M",
      spark: series(90, 10, 0.07, 0.03)
    }, {
      name: "Dyo",
      img: "",
      country: "NG",
      genres: ["Afrobeats"],
      stage: "developing",
      score: 58,
      momentum: "Explosive Growth",
      delta: 22.4,
      listeners: "1.9M",
      spark: series(60, 10, 0.12, 0.04)
    }, {
      name: "Sienna Spiro",
      img: "",
      country: "GB",
      genres: ["Pop", "Soul"],
      stage: "developing",
      score: 55,
      momentum: "Growth",
      delta: 9.8,
      listeners: "1.4M",
      spark: series(70, 10, 0.06, 0.03)
    }, {
      name: "Kwn",
      img: "",
      country: "US",
      genres: ["Hyperpop"],
      stage: "developing",
      score: 52,
      momentum: "Explosive Growth",
      delta: 27.1,
      listeners: "980K",
      spark: series(40, 10, 0.14, 0.05)
    }, {
      name: "Maya Delilah",
      img: "",
      country: "GB",
      genres: ["Indie", "Soul"],
      stage: "developing",
      score: 49,
      momentum: "Steady",
      delta: 2.3,
      listeners: "760K",
      spark: series(50, 10, 0.02, 0.02)
    }]
  };
})();
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/app/data.js", error: String((e && e.message) || e) }); }

__ds_ns.Avatar = __ds_scope.Avatar;

__ds_ns.Badge = __ds_scope.Badge;

__ds_ns.Button = __ds_scope.Button;

__ds_ns.IconButton = __ds_scope.IconButton;

__ds_ns.Input = __ds_scope.Input;

__ds_ns.Select = __ds_scope.Select;

__ds_ns.Switch = __ds_scope.Switch;

__ds_ns.Tabs = __ds_scope.Tabs;

__ds_ns.Tag = __ds_scope.Tag;

__ds_ns.MetricStat = __ds_scope.MetricStat;

__ds_ns.PlatformIcon = __ds_scope.PlatformIcon;

__ds_ns.CM_PLATFORMS = __ds_scope.CM_PLATFORMS;

__ds_ns.ScoreRing = __ds_scope.ScoreRing;

__ds_ns.Sparkline = __ds_scope.Sparkline;

__ds_ns.StageBadge = __ds_scope.StageBadge;

__ds_ns.CM_CAREER_STAGES = __ds_scope.CM_CAREER_STAGES;

__ds_ns.TrendDelta = __ds_scope.TrendDelta;

})();
