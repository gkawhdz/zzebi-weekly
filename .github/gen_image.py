import json, os, base64, subprocess, time, urllib.request, concurrent.futures, glob, shutil
key = os.environ.get("OPENAI_API_KEY", "")
before = os.environ.get("BEFORE", "")
def changed():
    try:
        out = subprocess.check_output(["git", "diff", "--name-only", "--diff-filter=AM", before, "HEAD", "--", "req/"]).decode().split()
        if out: return out
    except Exception: pass
    return sorted(glob.glob("req/*.json"))[-1:]
def edit(job):
    # 기준 사진(refs)을 넣어 같은 인물로 생성 — /v1/images/edits (multipart)
    import uuid
    bd = uuid.uuid4().hex; parts = []
    fields = {"model": job.get("model", "gpt-image-1.5"), "prompt": job["prompt"], "size": job.get("size", "1024x1536"),
              "quality": job.get("quality", "medium"), "n": "1", "output_format": job.get("format", "jpeg"),
              "input_fidelity": job.get("fidelity", "high")}
    for k, v in fields.items():
        parts.append(f'--{bd}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
    for r in job["refs"][:4]:
        data = open(r, "rb").read(); mt = "image/png" if r.endswith(".png") else "image/jpeg"
        parts.append(f'--{bd}\r\nContent-Disposition: form-data; name="image[]"; filename="{os.path.basename(r)}"\r\nContent-Type: {mt}\r\n\r\n'.encode() + data + b"\r\n")
    parts.append(f"--{bd}--\r\n".encode())
    return urllib.request.Request("https://api.openai.com/v1/images/edits", data=b"".join(parts),
          headers={"Authorization": "Bearer " + key, "Content-Type": f"multipart/form-data; boundary={bd}"})
def gen(job):
    body = {"model": job.get("model", "gpt-image-1.5"), "prompt": job["prompt"], "size": job.get("size", "1024x1536"),
            "quality": job.get("quality", "medium"), "n": 1, "output_format": job.get("format", "jpeg")}
    req = urllib.request.Request("https://api.openai.com/v1/images/generations", data=json.dumps(body).encode(),
          headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
    if job.get("refs"): req = edit(job)
    last = ""
    for attempt in range(2):
        try:
            with urllib.request.urlopen(req, timeout=240) as r:
                d = json.load(r)
            return job["name"], base64.b64decode(d["data"][0]["b64_json"]), None
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}: {e.read().decode()[:400]}"
        except Exception as e:
            last = str(e)[:400]
        time.sleep(5)
    return job["name"], None, last
# clean results older than 3 days
for d in glob.glob("out/*"):
    if os.path.isdir(d) and time.time() - os.path.getmtime(d) > 3*86400:
        shutil.rmtree(d, ignore_errors=True)
for f in changed():
    rid = os.path.splitext(os.path.basename(f))[0]
    spec = json.load(open(f))
    od = f"out/{rid}"; os.makedirs(od, exist_ok=True)
    status = {"id": rid, "ok": [], "errors": {}}
    if not key:
        status["errors"]["_"] = "OPENAI_API_KEY secret missing"
    else:
        jobs = spec.get("images", [])[:8]
        with concurrent.futures.ThreadPoolExecutor(4) as ex:
            for name, data, err in ex.map(gen, jobs):
                if data:
                    ext = "png" if data[:4] == b"\x89PNG" else "jpg"
                    open(f"{od}/{name}.{ext}", "wb").write(data); status["ok"].append(f"{name}.{ext}")
                else:
                    status["errors"][name] = err
    json.dump(status, open(f"{od}/_done.json", "w"), ensure_ascii=False, indent=1)
    print(json.dumps(status, ensure_ascii=False))
