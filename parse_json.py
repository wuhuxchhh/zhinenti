import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

os.chdir(r'C:\zhinenti')
with open('deepseek_data-2026-05-15/conversations.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

conv = data[103]
print(f'Title: {conv["title"]}')
print(f'Date: {conv["inserted_at"]}')

mapping = conv.get('mapping', {})

def traverse(node_id, visited=None):
    if visited is None:
        visited = set()
    if node_id in visited:
        return []
    visited.add(node_id)

    node = mapping.get(node_id)
    if not node:
        return []

    result = []
    msg = node.get('message')
    if msg and msg.get('fragments'):
        frags = msg['fragments']
        for f in frags:
            content = f.get('content', '')
            if content:
                result.append({
                    'type': f['type'],
                    'content': content
                })

    children = node.get('children', [])
    for child_id in sorted(children):
        result.extend(traverse(child_id, visited))

    return result

root_id = mapping['root']['children'][0] if 'root' in mapping and mapping['root']['children'] else None
if root_id:
    messages = traverse(root_id)
    print(f'Total fragments: {len(messages)}')
    print('='*80)

    for i, msg in enumerate(messages):
        label = 'USER' if msg['type'] == 'REQUEST' else 'AI'
        print(f'\n--- [{i}] {label} ---')
        content = msg['content']
        if len(content) > 3000:
            print(content[:3000])
            print(f'\n... [truncated at 3000, total {len(content)}]')
        else:
            print(content)
