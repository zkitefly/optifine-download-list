import json

# 读取原始 JSON 文件
with open('index-raw.json', 'r') as f:
    data = json.load(f)

# 删除 file 列表中除了指定属性外的其他属性
for item in data['file']:
    item_keys = list(item.keys())
    for key in item_keys:
        if key not in ['mcversion', 'name', 'ispreview', 'filename', 'forge']:
            del item[key]

# 输出至新的 JSON 文件
with open('index.json', 'w') as f:
    json.dump(data, f)
