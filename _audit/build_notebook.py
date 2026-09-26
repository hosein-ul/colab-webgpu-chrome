import json, os, sys

base = r"C:\Users\hashe\Documents\deSwap\chrome-colab"
nbpath = os.path.join(base, "colab_chrome_webgpu.ipynb")

nb = json.load(open(nbpath, encoding="utf-8"))
c1 = open(os.path.join(base, "_audit", "cell1_fixed.py"), encoding="utf-8").read()
c2 = open(os.path.join(base, "_audit", "cell2_fixed.py"), encoding="utf-8").read()

def to_src(s):
    return s.splitlines(keepends=True)

assert nb["cells"][1]["cell_type"] == "code", "cell1 mismatch"
assert nb["cells"][2]["cell_type"] == "code", "cell2 mismatch"

nb["cells"][1]["source"] = to_src(c1)
nb["cells"][2]["source"] = to_src(c2)

json.dump(nb, open(nbpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("notebook updated:", nbpath)
print("cells:", len(nb["cells"]))
