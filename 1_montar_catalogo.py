import pandas as pd, re, os, glob, warnings; warnings.filterwarnings('ignore')
# Uso: coloque as planilhas baixadas do Document@ na pasta dados/ e rode: python scripts/1_montar_catalogo.py
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
U='dados/'
MB=sorted(glob.glob(U+'Acervo-MB-*.xlsx'))[-1]  # pega a lista mais recente da Minha Biblioteca
def isbn(x): return re.sub(r'[^0-9Xx]','',str(x)) if pd.notna(x) else ''
def s(x): return '' if pd.isna(x) else str(x).strip()
ACC={'MB':'Login institucional (de qualquer lugar)','PV':'Rede UFRGS ou proxy','SP':'Rede UFRGS, proxy ou login institucional','WI':'Rede UFRGS ou proxy','EB':'Login institucional','IE':'Rede UFRGS ou login institucional'}
recs=[]
# Minha Biblioteca
mb=pd.read_excel(MB,sheet_name='Ativos',dtype=str)
for _,r in mb.iterrows():
    t=s(r['TÍTULO'])+(': '+s(r['SUBTÍTULO']) if s(r['SUBTÍTULO']) else '')
    aut=s(r['AUTOR (A)']) or s(r['ORGANIZADOR (A)'])
    ed=s(r['EDIÇÃO']); ed='' if ed in ('0','') else ed
    obs=''
    if s(r['MOTIVO DA REMOÇÃO']): obs='Sai do acervo em '+s(r['DATA DE REMOÇÃO'])[:10]
    recs.append(dict(fonte='Minha Biblioteca',tipo='Livro',titulo=t,autor=aut,editora=s(r['EDITORA/SELO']),ano=s(r['ANO DE PUBLICAÇÃO']),edicao=ed,isbn=isbn(r['ISBN']),area=s(r['ÁREA DO CONHECIMENTO']),assunto=s(r['SUBÁREA DO CONHECIMENTO']),idioma='Português',link=s(r['URL']),acesso=ACC['MB'],situacao_link='Oficial (lista do fornecedor)',direito=s(r['ÁREA DO CONHECIMENTO'])=='Direito',criterio='Área = Direito',obs=obs))
# ProView
pv=pd.read_excel(U+'ProView_LibraryList_21112022.xlsx',dtype=str).sort_values('Published Date',ascending=False).drop_duplicates('Static Link')
for _,r in pv.iterrows():
    recs.append(dict(fonte='ProView (Revista dos Tribunais)',tipo='Periódico' if s(r['Type'])=='Periodical' else 'Livro',titulo=s(r['Title']),autor=s(r['Author']).replace('\n','; '),editora=s(r['Publisher']),ano=s(r['Published Date'])[:4],edicao='',isbn=isbn(r['ISBN']),area='Direito',assunto=s(r['Subject']),idioma='Português',link=s(r['Static Link']),acesso=ACC['PV'],situacao_link='Oficial (lista do fornecedor)',direito=True,criterio='Coleção jurídica',obs='Lista de nov/2022: pode ter títulos que saíram ou faltar novos'))
# Springer
LAWKW=re.compile(r'\b(law|laws|legal|jurisprud\w*|justice|courts?|constitution\w*|criminal|criminolog\w*|arbitration|human rights|lawyers?|judicial|judges?|legislation|treaty|treaties)\b',re.I)
for f,col in [('SpringerNatureBooks_UFRGS.xlsx','Springer (UFRGS 2005–2021)'),('SpringerNature_Books_CAPES.xlsx','Springer Book Archives (CAPES)')]:
    sp=pd.read_excel(U+f,dtype=str)
    for _,r in sp.iterrows():
        c=s(r['eBook Collection: English Name']); t=s(r['Book Title'])
        if c=='Law and Criminology': d,crit=True,'Coleção Law and Criminology'
        elif c in ('Humanities, Social Sciences and Law','Social Sciences','Political Science and International Studies') and LAWKW.search(t): d,crit=True,'Palavra-chave jurídica no título'
        else: d,crit=False,''
        recs.append(dict(fonte=col,tipo='Livro',titulo=t,autor=s(r['Author']),editora=s(r['Imprint']),ano=s(r['Copyright Year']),edicao='',isbn=isbn(r['Electronic ISBN']),area=c,assunto='',idioma=s(r['Language']),link=s(r['DOI URL']),acesso=ACC['SP'],situacao_link='Oficial (DOI da lista)',direito=d,criterio=crit,obs=''))
# Wiley
w=pd.read_excel(U+'EbooksUFRGS-Wiley_acessoperpetuo.xlsx',dtype=str).dropna(subset=['Product Name'])
w=w[w['Product Code'].str.match(r'^\d{13}$',na=False)]
for _,r in w.iterrows():
    recs.append(dict(fonte='Wiley',tipo='Livro',titulo=s(r['Product Name']).title(),autor='',editora='Wiley',ano=s(r['Year']),edicao='',isbn=s(r['Product Code']),area=s(r['OBOOK Subject']).title(),assunto='',idioma='EN',link='https://onlinelibrary.wiley.com/doi/book/10.1002/'+s(r['Product Code']),acesso=ACC['WI'],situacao_link='Montado pelo ISBN (a testar)',direito=False,criterio='',obs=''))
# EBSCO
e=pd.read_excel(U+'EBSCOebooks_UFRGS2024.xlsx',sheet_name='Planilha2',dtype=str); e.columns=[c.strip() for c in e.columns]
for _,r in e.iterrows():
    t=s(r['Title'])+(': '+s(r['Subtitle']) if s(r['Subtitle']) else '')
    an=s(r['Product ID/AN']); law=s(r['BISAC subject']).upper().startswith('LAW')
    recs.append(dict(fonte='EBSCO (acesso perpétuo)',tipo='Livro',titulo=t,autor=s(r['Author']),editora=s(r['Publisher']),ano=s(r['Publication year']),edicao=s(r['Edition']),isbn=isbn(s(r['eISBN']).split(',')[0]),area=s(r['BISAC subject']),assunto='',idioma=s(r['Language']),link=f'https://search.ebscohost.com/login.aspx?direct=true&db=nlebk&AN={an}&site=ehost-live' if an else '',acesso=ACC['EB'],situacao_link='Montado pelo AN (a testar)',direito=law,criterio='BISAC = LAW' if law else '',obs=''))
# IEEE
ie=pd.read_excel(U+'IEEE.xlsx',dtype=str)
for _,r in ie.iterrows():
    recs.append(dict(fonte='IEEE',tipo='Livro',titulo=s(r['Título']),autor=s(r['Autor']).rstrip('.'),editora='IEEE',ano=s(r['Ano']).strip('[]'),edicao='',isbn='',area='Engenharia / Computação',assunto='',idioma='EN',link=s(r['Link']).replace('http://','https://'),acesso=ACC['IE'],situacao_link='Oficial (lista da UFRGS)',direito=False,criterio='',obs=''))
df=pd.DataFrame(recs)
df=df[df.titulo!='']
df.insert(0,'id',[f'T{i:06d}' for i in range(1,len(df)+1)])
os.makedirs('saida',exist_ok=True)
df.to_csv('saida/catalogo.csv',index=False,encoding='utf-8-sig')
print(len(df),'títulos gravados em saida/catalogo.csv (Direito:',int(df.direito.sum()),')')
