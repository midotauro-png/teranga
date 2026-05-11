import json

LATEST = sorted(__import__('glob').glob('/Users/midoban/teranga/outputs/*/campaign_output.json'))[-1]
print("File:", LATEST)

with open(LATEST) as f:
    d = json.load(f)

outputs = d.get("task_outputs", [])
print(f"Task outputs: {len(outputs)}")
for i, t in enumerate(outputs):
    print(f"\n--- Task {i} (len={len(t)}) ---")
    print("FIRST 300:", repr(t[:300]))
    print("LAST  300:", repr(t[-300:]))
