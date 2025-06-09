import json

with open('1.json', 'r') as f1, open('2.json', 'r') as f2:
    data1 = json.load(f1)
    data2 = json.load(f2)

combined = data1 + data2

with open('id.json', 'w') as f:
    json.dump(combined, f, indent=2)

print("✅ id.json berhasil dibuat dengan gabungan dari 1.json dan 2.json")