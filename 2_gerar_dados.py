# Uso: python scripts/2_gerar_dados.py   (lê saida/catalogo.csv, grava docs/data.json)
import pandas as pd, json, datetime
df = pd.read_csv('saida/catalogo.csv', dtype=str).fillna('')
d = df[df['direito'] == 'True'].copy()
FONTES = [  # nome no CSV, nome curto, cor da lombada
    ('Minha Biblioteca', 'Minha Biblioteca', '#1F8A70'),
    ('ProView (Revista dos Tribunais)', 'ProView', '#B5392F'),
    ('Springer (UFRGS 2005–2021)', 'Springer', '#6B4FA8'),
    ('Springer Book Archives (CAPES)', 'Springer Arquivo', '#8A6D1F'),
    ('EBSCO (acesso perpétuo)', 'EBSCO', '#C06A12'),
]
idx = {f[0]: i for i, f in enumerate(FONTES)}
livros = []
for r in d.itertuples():
    if r.fonte not in idx or not r.link: continue
    acesso = 'L' if 'login' in r.acesso.lower() else 'R'   # L = login (de qualquer lugar); R = rede UFRGS ou proxy
    assunto = r.assunto or r.area
    livros.append([r.titulo, r.autor, r.editora, r.ano, assunto, idx[r.fonte], acesso, r.link])
out = {'gerado': datetime.date.today().isoformat(),
       'fontes': [{'nome': f[1], 'cor': f[2]} for f in FONTES],
       'livros': livros}
json.dump(out, open('docs/data.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print(len(livros), 'títulos em docs/data.json')
