from __future__ import annotations

import html
from typing import Any


def _text(value: Any) -> str:
    return html.escape("—" if value is None else str(value), quote=True)


def _value(value: Any) -> str:
    if isinstance(value, dict):
        items = "".join(f"<li><span>{_text(key)}</span><strong>{_text(amount)}</strong></li>" for key, amount in sorted(value.items()))
        return f'<ul class="metric-list">{items}</ul>'
    return f'<p class="metric">{_text(value)}</p>'


def render_dashboard(overview: dict[str, Any], subject: str) -> str:
    counts = overview["status_counts"]
    cards: list[str] = []
    for fact in overview["facts"]:
        evidence = fact["evidence"]
        stale = '<span class="flag">LAST TRUSTED · STALE</span>' if fact["stale"] else ""
        cards.append(
            f'''<article class="card status-{_text(fact["status"]).lower()}">
  <header><div><p class="eyebrow">{_text(fact["classification"])} · {_text(fact["definition_version"])}</p><h2>{_text(fact["title"])}</h2></div><span class="status">{_text(fact["status"])}</span></header>
  {stale}
  {_value(fact["value"])}
  <p class="explanation">{_text(fact["explanation"])}</p>
  <dl>
    <div><dt>Fact</dt><dd>{_text(fact["fact_id"])}</dd></div>
    <div><dt>Cutoff</dt><dd>{_text(fact["cutoff_at"])}</dd></div>
    <div><dt>Observed</dt><dd>{_text(fact["observed_at"])}</dd></div>
    <div><dt>Owner</dt><dd>{_text(fact["source_owner"])}</dd></div>
    <div><dt>Authority</dt><dd>{_text(fact["authority_id"])}</dd></div>
    <div><dt>Reason</dt><dd>{_text(fact["reason_code"])}</dd></div>
    <div><dt>Audit</dt><dd class="hash">{_text(evidence["audit_entry_hash"])}</dd></div>
    <div><dt>Snapshot</dt><dd class="hash">{_text(evidence["snapshot_hash"] or evidence["last_trusted_snapshot_hash"])}</dd></div>
  </dl>
</article>'''
        )
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Project Brain v2 · Boss Dashboard</title>
  <style>
    :root {{ color-scheme: light; font-family: Inter, ui-sans-serif, system-ui, sans-serif; background:#f4f6f8; color:#18202a; }}
    * {{ box-sizing:border-box; }} body {{ margin:0; }} main {{ width:min(1180px,100%); margin:auto; padding:clamp(18px,4vw,48px); }}
    .top {{ display:flex; gap:24px; align-items:flex-end; justify-content:space-between; flex-wrap:wrap; }} h1 {{ font-size:clamp(28px,5vw,54px); margin:.15em 0; letter-spacing:-.04em; }}
    .eyebrow {{ color:#526171; font-size:12px; font-weight:800; letter-spacing:.12em; text-transform:uppercase; }} .warning {{ background:#fff4cf; border:1px solid #e4c44f; padding:12px 16px; border-radius:12px; font-weight:700; }}
    .summary {{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:12px; margin:28px 0; }} .summary div {{ background:white; border:1px solid #dce2e8; border-radius:16px; padding:18px; }} .summary strong {{ display:block; font-size:34px; }}
    .grid {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:18px; }} .card {{ background:white; border:1px solid #dce2e8; border-top:5px solid #7b8794; border-radius:18px; padding:22px; min-width:0; }}
    .status-trusted {{ border-top-color:#138a5b; }} .status-unknown {{ border-top-color:#d39a19; }} .status-no-go {{ border-top-color:#c43b45; }} .card header {{ display:flex; justify-content:space-between; gap:16px; }} h2 {{ margin:.2em 0 .8em; font-size:21px; }}
    .status,.flag {{ height:max-content; border-radius:999px; padding:6px 10px; background:#edf1f4; font-weight:800; font-size:12px; white-space:nowrap; }} .flag {{ display:inline-block; color:#8b5900; background:#fff0c2; }}
    .metric {{ font-size:clamp(34px,7vw,64px); font-weight:850; margin:18px 0; }} .metric-list {{ list-style:none; padding:0; display:grid; gap:7px; }} .metric-list li {{ display:flex; justify-content:space-between; gap:18px; border-bottom:1px solid #edf0f2; padding:8px 0; }}
    .explanation {{ line-height:1.55; color:#394858; min-height:3em; }} dl {{ display:grid; gap:7px; margin:18px 0 0; }} dl div {{ display:grid; grid-template-columns:86px minmax(0,1fr); gap:10px; }} dt {{ color:#667483; }} dd {{ margin:0; overflow-wrap:anywhere; }} .hash {{ font-family:ui-monospace,monospace; font-size:11px; }} footer {{ margin-top:28px; color:#667483; }}
    @media (max-width:760px) {{ .grid {{ grid-template-columns:1fr; }} .summary {{ grid-template-columns:1fr; }} .card header {{ align-items:flex-start; }} }}
    @media (prefers-reduced-motion:reduce) {{ * {{ scroll-behavior:auto !important; }} }}
  </style>
</head>
<body><main>
  <section class="top" aria-labelledby="page-title"><div><p class="eyebrow">Project Brain v2 · M3 candidate</p><h1 id="page-title">Boss Dashboard</h1><p>As of {_text(overview["as_of"])} · Viewer {_text(subject)}</p></div><p class="warning" role="status">Synthetic only · production off · not decision-usable</p></section>
  <section class="summary" aria-label="Evidence status summary"><div><span>Trusted</span><strong>{_text(counts["Trusted"])}</strong></div><div><span>Unknown</span><strong>{_text(counts["Unknown"])}</strong></div><div><span>No-Go</span><strong>{_text(counts["No-Go"])}</strong></div></section>
  <section class="grid" aria-label="Authorized aggregate facts">{''.join(cards)}</section>
  <footer>Generated {_text(overview["generated_at"])} · No row-level drill-down · No export · No source writes</footer>
</main></body></html>'''
