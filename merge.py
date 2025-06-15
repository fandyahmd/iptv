import json

with open('1.json', 'r') as f1, open('add.json', 'r') as f2, open('2.json', 'r') as f3:
    data1 = json.load(f1)
    data2 = json.load(f2)
    data3 = json.load(f3)

combined = data1 + data2 + data3

with open('id.json', 'w') as f:
    json.dump(combined, f, indent=2)

print("✅ id.json created!")