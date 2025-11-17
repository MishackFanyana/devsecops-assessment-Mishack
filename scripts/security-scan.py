
import argparse, os, re, json, math
from pathlib import Path

SIGNATURES = {
    "aws_access_key_id": re.compile(r"AKIA[0-9A-Z]{16}"),
    "aws_secret": re.compile(r"(?i)aws_secret_access_key['\"]?\s*[:=]\s*['\"][A-Za-z0-9/+=]{40}"),
    "api_key": re.compile(r"(?i)(api[-_]?key)[\"' ]*[:=][\"' ]*([A-Za-z0-9\-_]{16,})"),
    "private_key": re.compile(r"-----BEGIN (RSA )?PRIVATE KEY-----"),
    "jwt": re.compile(r"[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+")
}

def entropy(s):
    if not s: return 0
    probs = [float(s.count(c)) / len(s) for c in set(s)]
    return -sum([p * math.log2(p) for p in probs])

def scan_file(path):
    findings = []
    try:
        text = path.read_text(errors="ignore")
    except:
        return findings

    for name, sig in SIGNATURES.items():
        for m in sig.finditer(text):
            findings.append({
                "type": name,
                "match": m.group(0),
                "path": str(path),
                "confidence": 0.9
            })

    for m in re.finditer(r"[A-Za-z0-9/+=]{20,}", text):
        token = m.group(0)
        if entropy(token) > 4.5:
            findings.append({
                "type": "high_entropy",
                "match": token,
                "entropy": entropy(token),
                "path": str(path),
                "confidence": 0.85
            })
    return findings

def scan_dir(root):
    results = []
    for f in Path(root).rglob("*"):
        if f.is_file():
            res = scan_file(f)
            results.extend(res)
    return results

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--path", default=".")
    p.add_argument("--format", default="text", choices=["json","text"])
    args = p.parse_args()

    results = scan_dir(args.path)
    summary = {
        "findings": results,
        "count": len(results),
        "decision": "fail" if len(results) > 0 else "pass"
    }

    if args.format == "json":
        print(json.dumps(summary, indent=2))
    else:
        print(f"Findings: {summary['count']}")
        print(f"Decision: {summary['decision']}")

if __name__ == "__main__":
    main()

