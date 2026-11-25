import csv
import json
import re

def clean_comarca(raw_name):
    raw_name = raw_name.strip()
    cleaned = re.split(r'\(|DJ|Lei|Resolução', raw_name, flags=re.IGNORECASE)[0].strip()
    words = cleaned.split()
    capitalized = " ".join([w.capitalize() if w.lower() not in ['de', 'da', 'do', 'dos', 'das', 'e'] else w.lower() for w in words])
    if capitalized:
        capitalized = capitalized[0].upper() + capitalized[1:]
    return capitalized, raw_name

def clean_entrancia(raw_entrancia):
    s = raw_entrancia.strip()
    if 'Final' in s:
        return 'Entrância Final'
    elif 'Intermedi' in s:
        return 'Entrância Intermediária'
    elif 'Inicial' in s:
        return 'Entrância Inicial'
    return s

def sanitize_magistrate_name(name):
    """
    Remove todos os resíduos de cargos, DJ, Dir. Foro, etc.
    Garante o nome oficial limpo do magistrado.
    """
    if not name:
        return ""
    
    n = name.strip()
    
    # Remove prefixos como 'Resp.', 'Subst.', 'Atuação:'
    n = re.sub(r'^(Resp[\.,]|Subst[\.,]|Atuação:?|e\s+Dir[\.,]\s*Foro)\s*', '', n, flags=re.IGNORECASE)
    
    # Se houver palavras grudadas como 'CAVALARIDIR.' ou 'AMARALDIR.' ou 'OLIVEIRADJ'
    n = re.sub(r'([A-Za-zÀ-ÿ])(DIR\.?|DIRETOR|DJ|JUIZ|PRESIDENTE|AFASTAD|RESP\.)', r'\1 \2', n, flags=re.IGNORECASE)
    
    cut_patterns = [
        r'\bDir[\.]?\s*(do\s+)?Foro\b.*',
        r'\bDiretor[a]?\s*(do\s+)?Foro\b.*',
        r'\bJu[íi]z[a]?\s+Auxiliar\b.*',
        r'\bPresidente\s+de\s+Turma\b.*',
        r'\bAfastad[ao]\b.*',
        r'\bDJ\s*[\d\.\/]+.*',
        r'\bDJ\.?\s*[\d\.\/]+.*',
        r'\bDJ\b.*',
        r'\(DJ\b.*',
        r'\(com\s+atuação\b.*',
        r'\(Com\s+atuação\b.*',
        r'\(Res\b.*',
        r'\(com\s+atua.*',
        r'-\s*DJ.*',
        r'\bSubst\b.*',
        r'\bResp\b.*'
    ]
    
    for pat in cut_patterns:
        n = re.split(pat, n, flags=re.IGNORECASE)[0]
        
    n = re.sub(r'[\-\(\)\.\,\;]+$', '', n)
    n = re.sub(r'\s+', ' ', n).strip()
    n = re.sub(r'^(e\s+)?(Subst\.|Resp\.)\s*', '', n, flags=re.IGNORECASE)
    n = re.sub(r'[\-\(\)\.\,\;]+$', '', n)
    n = re.sub(r'\s+', ' ', n).strip()
    
    return n.upper()

def extract_specialties_from_text(text_lower):
    """
    Extrai especialidades com base ESTRITAMENTE na denominação atual da vara.
    NÃO considera denominação antiga.
    """
    specs = set()
    
    # Fazenda Pública
    if re.search(r'fazenda[s]?\s+p[úu]blica[s]?|faz\.\s*p[úu]b', text_lower):
        specs.add('Fazenda Pública')
        
    # Execução Fiscal
    if 'execu' in text_lower and 'fiscal' in text_lower:
        specs.add('Execução Fiscal')
        
    # Família
    if 'família' in text_lower or 'familia' in text_lower:
        specs.add('Família')
        
    # Sucessões
    if 'sucess' in text_lower:
        specs.add('Sucessões')
        
    # Ambiental
    if 'ambiental' in text_lower or 'amb.' in text_lower:
        specs.add('Ambiental')
        
    # Infância e Juventude
    if any(k in text_lower for k in ['infância', 'infancia', 'juventude', 'infracional']):
        specs.add('Infância e Juventude')
        
    # Violência Doméstica
    if any(k in text_lower for k in ['violência doméstica', 'violencia domestica', 'mulher', '11.340']):
        specs.add('Violência Doméstica')
        
    # Garantias
    if 'garantias' in text_lower or 'custódia' in text_lower or 'custodia' in text_lower:
        specs.add('Garantias')
        
    # Auditoria Militar
    if 'militar' in text_lower:
        specs.add('Auditoria Militar')
        
    # Turma Recursal
    if 'turma recursal' in text_lower:
        specs.add('Turma Recursal')
        
    # Registros Públicos
    if 'registro' in text_lower or 'reg. p' in text_lower or 'reg.p' in text_lower:
        specs.add('Registros Públicos')
        
    # Crime Organizado e Lavagem
    if 'organização criminosa' in text_lower or 'organizacao criminosa' in text_lower or 'lavagem' in text_lower:
        specs.add('Crime Organizado e Lavagem')
        
    # Tribunal do Júri
    if any(k in text_lower for k in ['júri', 'juri', 'dolosos contra a vida']):
        specs.add('Tribunal do Júri')
        
    # Execução Penal
    if any(k in text_lower for k in ['execução penal', 'execuções penais', 'execucao penal', 'execucoes penais', 'medidas alternativas']):
        specs.add('Execução Penal')
        
    # Juizados Especiais
    if 'juizado especial cível' in text_lower or 'juizado cível' in text_lower or 'juizado especial civ' in text_lower or 'juizado civel' in text_lower:
        specs.add('Juizado Especial Cível')
        
    if 'juizado especial criminal' in text_lower or 'juizado criminal' in text_lower or 'juizado especial crim' in text_lower:
        specs.add('Juizado Especial Criminal')
        
    # Juizado da Infância
    if 'juizado da infância' in text_lower or 'juizado da infancia' in text_lower:
        specs.add('Infância e Juventude')

    # Cível
    if 'cível' in text_lower or 'civel' in text_lower or 'cumprimento de sentença' in text_lower or 'arbitragem' in text_lower:
        specs.add('Cível')

    # Criminal
    is_criminal = False
    if 'criminal' in text_lower or 'delitos' in text_lower or 'reclusão' in text_lower or 'reclusao' in text_lower or 'detenção' in text_lower or 'detencao' in text_lower:
        is_criminal = True
    elif 'crime' in text_lower or 'crimes' in text_lower:
        is_criminal = True
    elif 'execução penal' in text_lower or 'execuções penais' in text_lower:
        is_criminal = True
    elif 'garantias' in text_lower:
        is_criminal = True
    elif 'auditoria militar' in text_lower or 'militar' in text_lower:
        is_criminal = True
    elif 'violência doméstica' in text_lower or 'violencia domestica' in text_lower:
        is_criminal = True
    elif 'júri' in text_lower or 'juri' in text_lower:
        is_criminal = True

    if is_criminal:
        specs.add('Criminal')

    return specs

def parse_magistrates(raw_text):
    magistrates = []
    if not raw_text or not raw_text.strip():
        return magistrates
    
    text = raw_text.strip()
    
    if 'Resp.' in text or 'Resp,' in text:
        normalized = re.sub(r'Resp[\.,]', '|||RESP|||', text)
        parts = normalized.split('|||RESP|||')
        
        titular_part = parts[0].strip()
        if titular_part:
            titular_clean = sanitize_magistrate_name(titular_part)
            if len(titular_clean) > 3:
                magistrates.append({
                    'nome': titular_clean,
                    'funcao': 'Titular',
                    'detalhes': titular_part,
                    'competencia': 'Geral da Vara'
                })
                
        for p in parts[1:]:
            p = p.strip()
            if not p:
                continue
            comp_match = re.search(r'\(com atuação na[s]? competência[s]? ([^)]+)\)', p, flags=re.IGNORECASE)
            competencia = comp_match.group(1).strip() if comp_match else 'Geral / Respondente'
            
            resp_clean = sanitize_magistrate_name(p)
            if len(resp_clean) > 2:
                magistrates.append({
                    'nome': resp_clean,
                    'funcao': 'Respondente Designado',
                    'detalhes': p,
                    'competencia': competencia
                })
    else:
        titular_clean = sanitize_magistrate_name(text)
        if len(titular_clean) > 2:
            magistrates.append({
                'nome': titular_clean,
                'funcao': 'Titular',
                'detalhes': text,
                'competencia': 'Geral da Vara'
            })
            
    return magistrates

def process_file(csv_path):
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        all_lines = list(reader)
        
    data_lines = all_lines[2:]
    
    processed = []
    id_counter = 1
    
    for row in data_lines:
        if not row or not any(row):
            continue
        entrancia_raw = row[0] if len(row) > 0 else ''
        comarca_raw = row[1] if len(row) > 1 else ''
        vara_raw = row[2] if len(row) > 2 else ''
        antiga_denom = row[3] if len(row) > 3 else ''
        magistrado_raw = row[4] if len(row) > 4 else ''
        subst_auto = row[5] if len(row) > 5 else ''
        subst_eventual = row[6] if len(row) > 6 else ''
        
        comarca_clean, _ = clean_comarca(comarca_raw)
        entrancia_clean = clean_entrancia(entrancia_raw)
        
        vara_clean = vara_raw.strip()
        vara_display = vara_clean if vara_clean else 'Vara Única / Competência Geral'
        
        # REGRA CRUCIAL: ESPECIALIDADE VEM EXCLUSIVAMENTE DA VARA ATUAL
        specs = set()
        if vara_clean:
            specs = extract_specialties_from_text(vara_clean.lower())
        else:
            comp_matches = re.findall(r'\(com atuação na[s]? competência[s]? ([^)]+)\)', magistrado_raw, flags=re.IGNORECASE)
            if comp_matches:
                for c_str in comp_matches:
                    sub_specs = extract_specialties_from_text(c_str.lower())
                    specs.update(sub_specs)
            else:
                specs.add('Vara Única (Competência Geral)')
                specs.add('Cível')
                specs.add('Criminal')
                specs.add('Família')
                specs.add('Fazenda Pública')
                specs.add('Infância e Juventude')
                
        if not specs:
            specs.add('Geral / Plena')
        
        magistrates = parse_magistrates(magistrado_raw)
        magistrado_principal = magistrates[0]['nome'] if magistrates else sanitize_magistrate_name(magistrado_raw)
        
        entry = {
            'id': id_counter,
            'comarca': comarca_clean,
            'comarca_original': comarca_raw.strip(),
            'entrancia': entrancia_clean,
            'vara': vara_display,
            'vara_original': vara_raw.strip(),
            'antiga_denominacao': antiga_denom.strip(),
            'magistrado_principal': magistrado_principal,
            'magistrados': magistrates,
            'magistrado_raw': magistrado_raw.strip(),
            'substituto_automatico': subst_auto.strip(),
            'substituto_eventual': subst_eventual.strip(),
            'especialidades': sorted(list(specs))
        }
        processed.append(entry)
        id_counter += 1
        
    return processed

if __name__ == '__main__':
    data = process_file('C:/Users/Gustavo/.gemini/antigravity/scratch/consulta-magistrados-tjgo/dados_tjgo.csv')
    print(f"Total registros processados: {len(data)}")
    
    # Audit unique magistrates count
    all_names = set(m['nome'] for d in data for m in d['magistrados'])
    print(f"Total magistrados únicos puros: {len(all_names)}")
    
    with open('C:/Users/Gustavo/.gemini/antigravity/scratch/consulta-magistrados-tjgo/dados_tjgo.json', 'w', encoding='utf-8') as out:
        json.dump(data, out, ensure_ascii=False, indent=2)
    print("Salvo dados_tjgo.json com sucesso!")
