# Sistema de Consulta de Magistrados — TJGO

Sistema de pesquisa, filtragem avançada e integração com e-mail para o quadro de magistrados do **Tribunal de Justiça do Estado de Goiás (TJGO)**, baseado nos dados atualizados em 23 de novembro de 2026.

---

## 🌟 Funcionalidades Principais

1. **Filtros Avançados Multidimensionais**:
   - **Por Comarca / Cidade**: Seleção entre todas as 116 comarcas do estado de Goiás com contagem de varas por município.
   - **Por Entrância**: Filtragem entre Entrância Final, Intermediária e Inicial.
   - **Por Especialidade / Matéria da Vara**: Chips clicáveis combináveis:
     - *Cível, Criminal, Família, Sucessões, Fazenda Pública, Execução Fiscal, Ambiental, Infância e Juventude, Violência Doméstica, Juizado Especial Cível, Juizado Especial Criminal, Tribunal do Júri, Execução Penal, Garantias, Auditoria Militar, Turmas Recursais, Registros Públicos*.
   - **Por Situação Funcional**: Titulares em exercício vs. Respondentes / Designados.
   - **Busca Rápida Global**: Procura em tempo real por nome do juiz, vara, comarca, atos do DJ ou regras de substituição.

2. **Atualização Dinâmica de Planilha (Botão de Upload)**:
   - **Upload de Novos Dados (.csv)**: Botão no cabeçalho *"Atualizar Planilha"* que permite carregar qualquer nova versão da planilha do TJGO via arquivo ou arrastar e soltar (*drag & drop*).
   - **Parsing e Higienização em Tempo Real**: Aplica automaticamente as regras de higienização de nomes, exclusão de antigas denominações e classificação por matérias no próprio navegador.
   - **Persistência Local (Offline)**: Salva a base customizada no navegador (`localStorage`), mantendo-a disponível mesmo após recarregar a página.
   - **Restaurar Padrão**: Permite alternar de volta para a base oficial de Novembro/2026 com um clique.

3. **Integração Completa com Gmail & E-mail Institucional**:
   - **Seleção em Lote**: Marque magistrados individualmente ou use o botão *"Selecionar Filtrados"* para marcar grupos inteiros com 1 clique.
   - **Copiar para Gmail (`virgula`)**: Copia os nomes separados por vírgula (`NOME 1, NOME 2, ...`), pronto para colar no campo de busca do Gmail ou nos destinatários, **sem nenhuma repetição**.
   - **Cópia em Linhas**: Ideal para planilhas e anotações.
   - **Sugestão de E-mails Institucionais**: Gera automaticamente o formato `@tjgo.jus.br` baseado no nome oficial do magistrado.
   - **Abrir Busca no Gmail**: Botão direto que abre uma nova aba no Gmail com a busca parametrizada dos magistrados selecionados.
   - **Exportar Seleção para CSV**: Download de arquivo `.csv` compatível com Excel e Google Sheets (UTF-8 com BOM).

4. **Escala de Substituição Legal**:
   - Visualização imediata do Substituto Automático e Substituto Eventual para conferência rápida de impedimento, suspeição e plantão.

---

## 🚀 Como Executar

O sistema foi concebido como uma **Single Page Application (SPA)** de alta performance, sem necessidade de servidores complexos ou dependências pesadas:

1. Acesse a pasta:
   ```
   C:\Users\Gustavo\.gemini\antigravity\scratch\consulta-magistrados-tjgo\
   ```
2. Dê um duplo-clique no arquivo:
   ```
   index.html
   ```
   Ele abrirá diretamente em qualquer navegador moderno (Chrome, Edge, Firefox, Brave, etc.) com todos os 458 registros e 425 magistrados prontos para uso instantâneo e offline.

---

## 📊 Estrutura dos Arquivos

- `index.html`: Interface web completa, responsiva, estilizada com Tailwind CSS e ícones Lucide.
- `dados.js`: Base de dados estruturada em JavaScript com os 458 registros, 19 especialidades e 116 comarcas.
- `dados_tjgo.json`: Base em formato JSON limpo e estruturado.
- `dados_tjgo.csv`: Cópia fiel da planilha original para referência histórica.
- `processar_dados.py`: Script Python responsável pela limpeza e normalização dos dados.
- `gerar_js.py`: Script que empacota os dados para a interface web.
