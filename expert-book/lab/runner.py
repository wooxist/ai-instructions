#!/usr/bin/env python3
import subprocess as sp, json, pathlib, sys

def sh(cmd):
    return sp.run(cmd, shell=True, check=True, capture_output=True, text=True)

def ensure_dirs():
    for d in ['data/raw','data','logs','.cache','schemas','scripts']:
        pathlib.Path(d).mkdir(parents=True, exist_ok=True)

def write_samples():
    p = pathlib.Path('data/raw/sample1.txt')
    if not p.exists():
        p.write_text("AI instruction design can be automated into reliable workflows using schemas, runners, and validation.")
    p2 = pathlib.Path('data/raw/sample2.txt')
    if not p2.exists():
        p2.write_text("Power users orchestrate CLI tools and editors to turn prompts into reproducible pipelines.")

def main():
    ensure_dirs()
    write_samples()

    print("==> prepare")
    sh("python3 scripts/prepare_inputs.py data/raw > data/inputs.jsonl")

    print("==> generate")
    out = sh("python3 scripts/auto_generate.py --in data/inputs.jsonl")
    pathlib.Path('logs/generate.jsonl').write_text(out.stdout)
    pathlib.Path('.cache/last.out').write_text(out.stdout)

    print("==> verify")
    ver = sh("python3 scripts/verify.py --schema schemas/output.schema.json --input .cache/last.out")
    pathlib.Path('logs/verify.jsonl').write_text(ver.stdout)

    print("==> route")
    rt = sh("python3 scripts/route.py logs/verify.jsonl")
    pathlib.Path('logs/route_summary.json').write_text(rt.stdout)
    route = json.loads(rt.stdout)
    print(f"accept_rate={route.get('accept_rate')}")

    if route.get('accept_rate', 0) >= 0.9:
        print("==> apply")
        # dump individual outputs for demo
        outs = []
        for i, line in enumerate(out.stdout.splitlines()):
            p = pathlib.Path(f".cache/out_{i}.json")
            p.write_text(line)
            outs.append(str(p))
        sh("python3 scripts/apply_changes.py " + " ".join(outs))
    else:
        print("apply skipped (low accept rate)")

if __name__ == '__main__':
    try:
        main()
    except sp.CalledProcessError as e:
        sys.stdout.write(e.stdout)
        sys.stderr.write(e.stderr)
        sys.exit(e.returncode)
