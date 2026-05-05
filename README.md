# echocardiogram-report-assistant

## Português

### Visão geral
Este projeto implementa um **assistente de laudo de ecocardiograma com RAG e lógica clínica estruturada**, desenhado para gerar uma **minuta de laudo pronta para revisão médica**.

O sistema recebe achados estruturados de ecocardiograma, como:
- fração de ejeção;
- tamanho do ventrículo esquerdo;
- função do ventrículo direito;
- função diastólica;
- valvopatias principais;
- derrame pericárdico;

e usa esses dados para:
- classificar a função sistólica do VE;
- montar texto clínico consistente;
- recuperar casos semelhantes;
- sugerir uma minuta de `findings` e `impression`.

O objetivo não é substituir o cardiologista ou ecocardiografista. O objetivo é:
- reduzir tempo de redação;
- melhorar consistência de wording;
- apoiar um fluxo de revisão humana.

### Base pública recomendada
A melhor base pública para a evolução deste projeto é **EchoNet-Dynamic**, porque ela oferece:
- ecocardiogramas em vídeo;
- anotações especializadas;
- `LVEF`, `EDV`, `ESV`;
- tracings do ventrículo esquerdo.

Referências:
- [EchoNet-Dynamic](https://echonet.github.io/dynamic/)
- [ASE chamber quantification guideline](https://www.asecho.org/guideline/cardiac-chamber-quantification-by-echo-in-adults/)

### Por que essa base foi escolhida
Para um sistema de geração assistida de laudo, o melhor primeiro bloco público é uma base que se conecte diretamente com:
- função ventricular;
- estrutura do VE;
- ecocardiografia real;
- futuras estimativas automáticas de FEVE.

EchoNet-Dynamic é muito forte nisso.

### Caminho de evolução
Como expansão visual/segmentação:
- `CAMUS`

### Arquitetura
#### 1. Entrada estruturada
O sistema recebe:
- `indication`
- `lvef_percent`
- `lv_size`
- `rv_function`
- `diastolic_function`
- `mitral_regurgitation`
- `aortic_stenosis`
- `pericardial_effusion`
- `extra_notes`

#### 2. Lógica clínica
Em [clinical_logic.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/echocardiogram-report-assistant/src/clinical_logic.py), o projeto implementa:
- classificação de FEVE;
- sumários estruturados de função sistólica;
- sumários de função diastólica;
- sumários de valvopatias;
- sumário de derrame pericárdico;
- validação explícita dos campos clínicos.

#### 3. Corpus e knowledge base
Em [data_factory.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/echocardiogram-report-assistant/src/data_factory.py), o projeto cria:
- casos locais de eco no estilo de laudos clínicos;
- templates e guidelines curtos;
- referência formal à base pública recomendada.

#### 4. Retrieval
Em [retrieval.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/echocardiogram-report-assistant/src/retrieval.py), cada caso e documento é indexado com:
- `TfidfVectorizer`
- `cosine_similarity`

O espaço de busca mistura:
- indicação;
- FEVE;
- tamanho do VE;
- função do VD;
- disfunção diastólica;
- gravidade valvar;
- derrame pericárdico;
- texto do laudo.

#### 5. Geração da minuta
Em [generation.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/echocardiogram-report-assistant/src/generation.py), o sistema:
- usa resumo clínico estruturado;
- recupera casos e templates semelhantes;
- ancora a redação no caso mais parecido;
- produz `technique`, `findings` e `impression`;
- devolve confiança, referências e evidências.

#### 6. Orquestração
Em [pipeline.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/echocardiogram-report-assistant/src/pipeline.py), o pipeline integra:
- entrada estruturada;
- classificação clínica;
- retrieval;
- geração da minuta.

### Ferramentas e bibliotecas
- `Python`
- `scikit-learn`
  - `TfidfVectorizer`
  - `cosine_similarity`
- `FastAPI`
- `Streamlit`
- `pydantic`
- `unittest`

### Interface
- API em [app.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/echocardiogram-report-assistant/app.py)
- demo em [streamlit_app.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/echocardiogram-report-assistant/streamlit_app.py)

### Execução
```bash
python3 main.py
python3 -m unittest discover -s tests -v
streamlit run streamlit_app.py
uvicorn app:app --reload
```

### Limitações
- ainda não processa vídeo de eco diretamente;
- usa corpus local inspirado em bases públicas;
- não estima FEVE a partir da imagem;
- não substitui revisão médica.

### Próximos passos
- integração com `EchoNet-Dynamic`;
- módulo visual com `PyTorch`/`MONAI`;
- extração automática de FEVE e volumes;
- retrieval multimodal;
- editor clínico com aprovação.

## English

### Overview
This repository implements an **echocardiogram report assistant with RAG and structured clinical logic**, designed to generate a **draft report ready for physician review**.

The system receives structured echocardiographic findings such as:
- ejection fraction;
- left ventricular size;
- right ventricular function;
- diastolic function;
- key valvular lesions;
- pericardial effusion;

and uses them to:
- classify LV systolic function;
- assemble clinically coherent wording;
- retrieve similar cases;
- generate draft `findings` and `impression`.

The goal is not to replace the cardiologist or echocardiographer. The goal is to:
- reduce drafting time;
- improve wording consistency;
- support a human review workflow.

### Recommended public dataset
The strongest public dataset for the next version of this project is **EchoNet-Dynamic**, because it provides:
- echocardiogram videos;
- expert annotations;
- `LVEF`, `EDV`, `ESV`;
- LV tracings.

References:
- [EchoNet-Dynamic](https://echonet.github.io/dynamic/)
- [ASE chamber quantification guideline](https://www.asecho.org/guideline/cardiac-chamber-quantification-by-echo-in-adults/)

### Why this dataset was selected
For an assisted reporting system, the best public starting point is a dataset that connects directly to:
- ventricular function;
- LV structure;
- real echocardiography data;
- future automated ejection fraction estimation.

EchoNet-Dynamic is particularly strong in that space.

### Upgrade path
For visual expansion and segmentation:
- `CAMUS`

### Architecture
#### 1. Structured input
The system receives:
- `indication`
- `lvef_percent`
- `lv_size`
- `rv_function`
- `diastolic_function`
- `mitral_regurgitation`
- `aortic_stenosis`
- `pericardial_effusion`
- `extra_notes`

#### 2. Clinical logic
In [clinical_logic.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/echocardiogram-report-assistant/src/clinical_logic.py), the project implements:
- LVEF classification;
- structured LV systolic summaries;
- diastolic summaries;
- valvular summaries;
- pericardial effusion summaries;
- explicit validation for clinical input fields.

#### 3. Case corpus and knowledge base
In [data_factory.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/echocardiogram-report-assistant/src/data_factory.py), the project builds:
- local echo cases in clinical reporting style;
- lightweight templates and guidelines;
- a formal reference to the recommended public dataset.

#### 4. Retrieval
In [retrieval.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/echocardiogram-report-assistant/src/retrieval.py), each case and knowledge document is indexed with:
- `TfidfVectorizer`
- `cosine_similarity`

The retrieval space mixes:
- indication;
- LVEF;
- LV size;
- RV function;
- diastolic dysfunction;
- valve severity;
- pericardial effusion;
- report text.

#### 5. Draft generation
In [generation.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/echocardiogram-report-assistant/src/generation.py), the system:
- uses structured clinical summaries;
- retrieves similar cases and templates;
- anchors the wording in the nearest case;
- produces `technique`, `findings`, and `impression`;
- returns confidence, references, and supporting evidence.

#### 6. Orchestration
In [pipeline.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/echocardiogram-report-assistant/src/pipeline.py), the pipeline integrates:
- structured input;
- clinical classification;
- retrieval;
- draft generation.

### Tools and libraries
- `Python`
- `scikit-learn`
  - `TfidfVectorizer`
  - `cosine_similarity`
- `FastAPI`
- `Streamlit`
- `pydantic`
- `unittest`

### Interfaces
- API in [app.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/echocardiogram-report-assistant/app.py)
- demo in [streamlit_app.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/echocardiogram-report-assistant/streamlit_app.py)

### Run
```bash
python3 main.py
python3 -m unittest discover -s tests -v
streamlit run streamlit_app.py
uvicorn app:app --reload
```

### Limitations
- no direct echocardiography video processing yet;
- local corpus inspired by public datasets;
- no automatic LVEF estimation from images;
- not a replacement for physician review.

### Next steps
- EchoNet-Dynamic integration;
- visual module with `PyTorch` / `MONAI`;
- automatic LVEF and volume extraction;
- multimodal retrieval;
- physician approval editor.
