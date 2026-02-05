# 📊 Análise das Notas de Corte do Vestibular da UnB

Este projeto tem como objetivo analisar a evolução das **notas de corte do vestibular da Universidade de Brasília (UnB)** ao longo dos anos, com foco nos **20 cursos mais concorridos**. A pesquisa busca identificar padrões, tendências e níveis de competitividade, oferecendo insights úteis tanto para candidatos quanto para análises educacionais mais amplas.

O projeto combina **análise de dados em Python (Jupyter Notebook)** com uma **interface web em Next.js**, permitindo que os resultados sejam explorados de forma clara, visual e interativa.

---

## 🎯 Pergunta de Pesquisa

**Como as notas de corte do vestibular da UnB evoluíram ao longo dos anos para os 20 cursos mais concorridos?**

---

## 🔍 Subperguntas

- Quais são os 20 cursos mais concorridos da UnB considerando a média histórica da nota de corte?
- Esses cursos estão se tornando mais difíceis ao longo do tempo?
- Quais cursos apresentam maior volatilidade nas notas de corte?
- Existe tendência de alta, queda ou estabilidade nas notas?
- Qual seria uma “nota segura” para aprovação em cada curso?

---

## 🧠 Motivação

A nota de corte é um dos principais referenciais utilizados por candidatos ao vestibular para avaliar suas chances de aprovação. Apesar disso, muitas análises se baseiam apenas em **um único ano**, ignorando variações históricas e tendências.

Este projeto busca preencher essa lacuna por meio de uma análise histórica estruturada, permitindo uma visão mais realista e informada sobre a competitividade dos cursos da UnB.

---

## 🗂️ Escopo da Análise

- **Instituição:** Universidade de Brasília (UnB)
- **Processo seletivo:** Vestibular tradicional
- **Modalidade:** Ampla concorrência
- **Cursos analisados:** Top 20 mais concorridos
- **Período:** Múltiplos anos (a definir conforme disponibilidade dos dados)

---

## 🧪 Metodologia

O projeto será desenvolvido em duas grandes etapas:

### 1️⃣ Análise de Dados (Jupyter Notebook)
Responsável por:
- Coleta e organização dos dados
- Limpeza e padronização
- Análise exploratória
- Cálculo de métricas estatísticas
- Geração de visualizações
- Exportação de dados processados (`JSON` / `CSV`)

Métricas utilizadas:
- Média e mediana das notas de corte
- Desvio padrão (volatilidade)
- Tendência temporal (regressão linear)
- Percentil 75 (estimativa de “nota segura”)

---

### 2️⃣ Visualização Web (Next.js)
Responsável por:
- Apresentar os resultados da pesquisa
- Exibir gráficos interativos
- Mostrar rankings e tendências
- Facilitar a interpretação dos dados

O site consumirá **dados estáticos gerados pelo notebook**, garantindo separação clara entre análise e interface.

---

## 📈 Visualizações Planejadas

- Evolução temporal das notas de corte por curso
- Ranking dos cursos mais concorridos
- Comparação de volatilidade entre cursos
- Distribuição das notas (boxplots)
- Destaque de tendências de alta ou estabilidade

---

## 🚀 Possíveis Extensões Futuras

- Comparação com o PAS
- Inclusão de outras modalidades (cotas)
- Modelo preditivo para estimar notas de corte futuras
- Simulador de chances de aprovação
- Expansão para outras universidades

---

## 🛠️ Tecnologias Utilizadas

- **Python** (pandas, numpy, matplotlib, seaborn)
- **Jupyter Notebook**
- **Next.js**
- **TypeScript**
- **Recharts / Chart.js**
- **Git & GitHub**

---

## 📌 Status do Projeto

🟡 Em planejamento  
- [x] Definição do escopo  
- [x] Definição das perguntas de pesquisa  
- [ ] Coleta dos dados  
- [ ] Análise exploratória  
- [ ] Desenvolvimento do site  

---

## 👤 Autor

**Gabriel Caixeta Romero**  
Estudante de Engenharia de Computação – UnB  
Desenvolvedor Full Stack e entusiasta de análise de dados, machine learning e sistemas educacionais.

---

## 📄 Licença

Este projeto é de caráter educacional e analítico. Os dados utilizados são de fontes públicas.