# Livros de Direito na UFRGS (Biblioteca do CAAR)

Site estático: `docs/index.html` + `docs/data.json`. Sem servidor, sem banco, sem senha.

## Ver no seu computador
    cd docs
    python3 -m http.server 8000
Abra http://localhost:8000. (Abrir o index.html direto não funciona: o navegador bloqueia a leitura do data.json.)

## Publicar no GitHub Pages
1. Crie um repositório no GitHub (ex.: `biblioteca-caar`) e suba esta pasta:
       git init && git add . && git commit -m "primeira versão"
       git branch -M main
       git remote add origin https://github.com/SEU-USUARIO/biblioteca-caar.git
       git push -u origin main
2. No GitHub: Settings > Pages > Source: "Deploy from a branch", branch `main`, pasta `/docs`.
3. O endereço sai em alguns minutos: https://SEU-USUARIO.github.io/biblioteca-caar/

## Atualizar a lista (a Minha Biblioteca muda todo mês)
1. Baixe as listas no Document@ (Aquisição e assinatura de e-books) e coloque em `dados/`, com estes nomes:
   `Acervo-MB-AAAAMM.xlsx`, `ProView_LibraryList_*.xlsx`, `SpringerNatureBooks_UFRGS.xlsx`,
   `SpringerNature_Books_CAPES.xlsx`, `EbooksUFRGS-Wiley_acessoperpetuo.xlsx`, `EBSCOebooks_UFRGS2024.xlsx`, `IEEE.xlsx`.
2. `pip install pandas openpyxl`
3. `python3 scripts/1_montar_catalogo.py` (gera saida/catalogo.csv)
4. `python3 scripts/2_gerar_dados.py` (gera docs/data.json)
5. `git add docs/data.json && git commit -m "atualiza lista" && git push`

## Antes de divulgar
- Esperar a resposta da Biblioteca da Faculdade de Direito sobre republicar as listas de títulos.
- Testar o acesso ao ProView (rede UFRGS ou proxy) com um link de título e ajustar o texto da seção "Como abrir os livros" no index.html.
- Conferir uma amostra de links de cada coleção.
- Trocar o rodapé se o projeto passar a ser oficialmente do CAAR.

## Próximos passos possíveis
Adicionar Wiley, IEEE e outras áreas (o catálogo completo está em saida/catalogo.csv); para 149 mil títulos, trocar a busca por Pagefind.
