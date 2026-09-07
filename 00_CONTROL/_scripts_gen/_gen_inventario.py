import csv, os, datetime

ROOT = '.'
rows = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d != '.mimosa']
    for fn in filenames:
        full = os.path.join(dirpath, fn).replace(chr(92), '/')
        p = full[2:] if full.startswith('./') else full
        st = os.stat(full)
        fecha = datetime.datetime.fromtimestamp(st.st_mtime).strftime('%Y-%m-%d')
        size = st.st_size
        low = p.lower()
        name = fn

        if p.startswith('MARC'): proj = 'MARC'
        elif p.startswith('AURORA'): proj = 'AURORA'
        elif p.startswith('AUDITORIA_GLOBAL'): proj = 'COMPARTIDO'
        elif 'Chat de WhatsApp con +34' in p: proj = 'COMPARTIDO'
        else: proj = 'INFRA'

        if '+34 722 39 89 89' in p: persona = 'Aurora'
        elif 'aurora' in low and 'marc' not in low: persona = 'Aurora'
        elif p.startswith('MARC') or 'chat de whatsapp con marc' in low: persona = 'Marc'
        elif p.startswith('AUDITORIA_GLOBAL'): persona = 'Agente (auditoría)'
        else: persona = 'Sebastián/Compartido'

        ext = name.rsplit('.', 1)[-1].lower() if '.' in name else ''
        tipos = {'pdf': 'PDF', 'docx': 'DOCX', 'xlsx': 'XLSX', 'md': 'Markdown', 'txt': 'Texto',
                 'opus': 'Audio OPUS', 'wav': 'Audio WAV', 'mp3': 'Audio MP3', 'jpg': 'Imagen',
                 'jpeg': 'Imagen', 'png': 'Imagen', 'mp4': 'Vídeo', 'csv': 'CSV', 'db': 'Base de datos',
                 'json': 'Config', 'mjs': 'Script', 'bak': 'Backup', 'zip': 'ZIP', 'agent': 'Agent def'}
        tipo = tipos.get(ext, ext.upper() or 'Otro')

        if size == 0:
            cat = 'F'
        elif any(k in name for k in ['Doc1_', 'Doc2_', 'Doc3_', 'Plan_Marc_Operativo', 'Oferta_Colaboracion',
                                     'Info básic', 'DOC-20260812', 'IE6', 'IMPODERATE', 'Despierta', 'GEMINI',
                                     'Documento_Alineacion', 'Marc.pdf', 'CV_SEBASTIAN']):
            cat = 'A'
        elif 'chat de whatsapp' in low and ext in ('txt', 'opus', 'wav', 'mp3', 'zip'):
            cat = 'B'
        elif 'transcript' in low:
            cat = 'B'
        elif ext in ('jpg', 'jpeg', 'png', 'mp4'):
            cat = 'C'
        elif 'auditoria' in low or p.startswith('AUDITORIA_GLOBAL') or 'MARC_Proyecto_Entrega' in p \
                or name in ('AGENTS.md', '01_PROMPTS_PARA_AGENTES.md', 'MANIFIESTO_WORKSPACE.md') \
                or name.startswith('ENTREGA_MENSAJE'):
            cat = 'D'
        elif ext in ('db', 'json', 'mjs', 'bak', 'csv', 'gitignore', 'agent') or '.github' in p or ext == '':
            cat = 'E'
        else:
            cat = 'D' if ext == 'md' else 'C' if ext == 'pdf' else 'E'

        if '+34 722 39 89 89' in p:
            sens = 'ALTA [CREDENCIALES SENSIBLES DETECTADAS]'
        elif any(k in low for k in ['contrato', 'ie6', 'oferta_colaboracion', 'cv_sebastian']):
            sens = 'ALTA (contractual/personal)'
        elif 'chat de whatsapp' in low:
            sens = 'MEDIA-ALTA (conversación personal)'
        else:
            sens = 'MEDIA' if cat in ('A', 'B') else 'BAJA'

        rows.append([name, p, tipo, size, fecha, proj, persona, cat, sens])

rows.sort(key=lambda r: r[1])
with open('00_CONTROL/INVENTARIO_COMPLETO.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['archivo', 'ruta', 'tipo', 'tamaño_bytes', 'fecha_mod', 'proyecto', 'persona', 'categoria_A_F', 'sensibilidad'])
    w.writerows(rows)

from collections import Counter
print('Total:', len(rows))
print('Por categoría:', dict(sorted(Counter(r[7] for r in rows).items())))
print('Por proyecto:', dict(sorted(Counter(r[5] for r in rows).items())))
print('Vacíos (0 bytes):')
for r in rows:
    if r[3] == 0:
        print('  -', r[1])
print('Sensibilidad ALTA:', sum(1 for r in rows if r[8].startswith('ALTA')))
