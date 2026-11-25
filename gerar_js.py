import json
import re

# Load parsed json
with open('C:/Users/Gustavo/.gemini/antigravity/scratch/consulta-magistrados-tjgo/dados_tjgo.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Collect all distinct specialties
all_specialties = set()
for item in data:
    for sp in item['especialidades']:
        all_specialties.add(sp)

sorted_specialties = sorted(list(all_specialties))

# Collect comarcas with counts
comarca_counts = {}
for item in data:
    c = item['comarca']
    comarca_counts[c] = comarca_counts.get(c, 0) + 1

sorted_comarcas = sorted(comarca_counts.items(), key=lambda x: (-x[1], x[0]))

# Create JS bundle
js_content = f"""// Base de dados estruturada de Magistrados - TJGO (Atualização: 23 de Novembro de 2026)
window.DADOS_TJGO = {json.dumps(data, ensure_ascii=False, indent=2)};

window.ESPECIALIDADES_LISTA = {json.dumps(sorted_specialties, ensure_ascii=False, indent=2)};

window.COMARCAS_LISTA = {json.dumps([{'nome': c[0], 'qtd': c[1]} for c in sorted_comarcas], ensure_ascii=False, indent=2)};
"""

with open('C:/Users/Gustavo/.gemini/antigravity/scratch/consulta-magistrados-tjgo/dados.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"Gerado dados.js com {len(data)} registros e {len(sorted_specialties)} especialidades distintas!")
