import json,sys
from pathlib import Path
from jsonschema import Draft202012Validator
R=Path(__file__).parent
load=lambda n:json.loads((R/n).read_text(encoding="utf-8"))
def main():
 e=[]
 for s in ("responsibility.v1","state-machines.v1","api-security.v1"):
  e += [s+":"+x.message for x in Draft202012Validator(load(s+".schema.json")).iter_errors(load(s+".json"))]
 st,api,cases=load("state-machines.v1.json"),load("api-security.v1.json"),load("fixtures/cases.v1.json")
 for c in cases["cases"]:
  r="reject";k=c["kind"]
  if k=="transition": r="accept" if [c["from"],c["to"]] in st["machines"][c["machine"]]["transitions"] and c["authorized"] and c["key"] else "reject"
  elif k=="duplicate": r="replay_original" if c["same_payload"] else "conflict"
  elif k=="write": r="accept" if c["key"] else "reject"
  elif k=="envelope": r="accept" if c["request_id"] and c["correlation_id"] else "reject"
  elif k=="scope": r="accept" if c["source"]==api["identity"]["scope_source"] else "reject"
  elif k=="audit": r="reject" if set(c["fields"])&set(api["audit"]["redacted"]) else "accept"
  elif k=="compatibility": r="accept" if c["major_changed"] else "reject"
  if r!=c["expected"]: e.append(c["id"]+f": expected {c['expected']} got {r}")
 if e: print("\n".join("ERROR: "+x for x in e),file=sys.stderr);return 1
 print(f"Protection Mall M1 contracts valid: 3 contracts, {len(cases['cases'])} synthetic cases.");return 0
if __name__=="__main__":raise SystemExit(main())
