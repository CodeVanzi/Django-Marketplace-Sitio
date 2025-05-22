# Marketplace Sítio Nova Esperança & Sistema de Apoio à Decisão - Trabalho de Conclusão de Curso - UNIVESP

**Autores (Grupo PI Atual):** 
CAIO VINÍCIUS CONSTANTE DA SILVA, 
FABIO HIDEO HATAE, 
GABRIELLA FERREIRA, 
GRACIEL COVANZI DE SOUSA, 
RICHARD HATANAKA, 
RODRIGO TROSKAITIS SANTOS, 
ROGERIO NASCIMENTO CAVALIERI, 
VALDEMIR DAMAS DA SILVA

**Orientadora:** Profª Carla Dominique Silva Vasconcelos
**Instituição:** Universidade Virtual do Estado de São Paulo (UNIVESP)
**Cursos:** Ciência de Dados / Engenharia da Computação
**Ano de Conclusão:** 2025

---

## 1. Visão Geral do Projeto

Este repositório contém o código-fonte da aplicação web **Marketplace Sítio Nova Esperança**, uma plataforma robusta desenvolvida em Django. O projeto é o resultado da evolução de múltiplos Projetos Integradores (PI) da UNIVESP, adaptando-se e expandindo-se para atender às crescentes necessidades do Sítio Nova Esperança em diferentes momentos de seu desenvolvimento.

A plataforma atual integra diversas funcionalidades essenciais:
*   Um **marketplace completo** para a comercialização dos produtos do Sítio.
*   Ferramentas de **apoio à decisão** para a gestão da fazenda, incluindo dashboards analíticos.
*   Um **assistente virtual (chatbot)** para suporte técnico especializado.

O sistema foi construído utilizando tecnologias modernas como **Django** para o backend, **Tailwind CSS** para estilização responsiva, e **HTMX** para interações dinâmicas, proporcionando uma experiência de usuário fluida e moderna. A aplicação está configurada para deploy na plataforma **Railway**.

## 2. Contexto e Motivação

O desenvolvimento deste sistema foi impulsionado pelas necessidades identificadas na Fazenda Nova Esperança, um empreendimento focado na produção de cogumelos e outros produtos agrícolas. Os principais desafios que o projeto visa solucionar são:

*   **Para o Sr. Eric (Proprietário):** Facilitar a análise de rentabilidade e o planejamento estratégico da produção através de visualizações de dados de mercado claras e acessíveis.
*   **Para o Sr. Victor e Equipe Técnica:** Fornecer uma ferramenta de consulta rápida e confiável para dúvidas sobre técnicas de cultivo, manejo de pragas, solução de problemas operacionais e outras questões técnicas, otimizando o tempo e a eficiência da equipe.
*   **Para o Sítio Nova Esperança como um todo:** Criar um canal de vendas online direto (marketplace), expandindo o alcance de seus produtos e fortalecendo a marca.

Este projeto visa, portanto, não apenas resolver problemas pontuais, mas também agregar valor estratégico e operacional ao Sítio Nova Esperança.

---

## 3. Funcionalidades Detalhadas

A plataforma Sítio Nova Esperança oferece um conjunto abrangente de funcionalidades:

### 3.1. Módulo de Marketplace e E-commerce
*   **Landing Page:** Página inicial informativa e visualmente atraente para apresentar o Sítio e seus produtos.
*   **Catálogo de Produtos:** Listagem detalhada de produtos, organizados por categorias, com imagens, descrições e preços.
*   **Carrinho de Compras:** Funcionalidade completa para adicionar, remover e atualizar quantidades de produtos no carrinho.
*   **Checkout Seguro:** Processo de finalização de compra intuitivo.
*   **Integração com Stripe:** Sistema de pagamento online robusto, configurado para testes com cartões de crédito (funcionalidade de boleto preparada conforme documentação do Stripe, mas não ativa em produção no momento).
*   **Gerenciamento de Pedidos:** Usuários podem visualizar seu histórico de pedidos. Administradores têm ferramentas para gerenciar todos os pedidos.

### 3.2. Gerenciamento de Usuários e Perfis
*   **Autenticação Completa (Django Allauth):** Cadastro de novos usuários, login (por e-mail), logout seguro.
*   **Recuperação de Senha:** Funcionalidade para usuários redefinirem suas senhas.
*   **Perfil do Usuário:** Área dedicada onde os usuários podem gerenciar suas informações pessoais, múltiplos endereços de entrega, visualizar/atualizar foto de perfil.

### 3.3. Painel de Administração (Acesso Restrito)
*   **Acesso Seguro:** O painel de administração principal do Django está localizado em `/mestre/` para maior segurança.
*   **Admin Honeypot:** Uma "armadilha" configurada no caminho `/admin/` tradicional para detectar e desencorajar tentativas de acesso não autorizado.
*   **Gerenciamento de Conteúdo:**
    *   Cadastro e edição de Produtos (nome, descrição, preço, imagens, estoque).
    *   Gerenciamento de Categorias de produtos.
*   **Gerenciamento de Usuários:** Visualização, criação e edição de usuários, atribuição de permissões (staff, superuser).
*   **Gerenciamento de Pedidos:** Acompanhamento e atualização do status dos pedidos realizados no marketplace.

### 3.4. Módulos de Apoio à Decisão (Acesso Restrito para Staff/Admin)
*   **Dashboard de Commodities (DB Commodities):**
    *   Ferramenta de visualização de dados históricos de preços de diversas commodities agrícolas.
    *   Gráficos interativos gerados com Bokeh, permitindo análise de tendências e variações.
    *   Filtros dinâmicos por ativo, com atualizações de conteúdo via HTMX para uma experiência fluida.
    *   Tabelas de resumo com médias e outras métricas relevantes.
*   **Dashboard de Análise de Mercado de Cogumelos (DB Cogumelos):**
    *   Painel dedicado à análise de dados de uma pesquisa de mercado focada nos principais cogumelos medicinais de interesse (Cordyceps, Reishi, Agaricus, Juba de Leão).
    *   Visualização de preço médio e desvio padrão (+1σ, -1σ) para diferentes apresentações dos cogumelos (extrato, cápsulas, desidratado).
    *   Gráficos comparativos e individuais gerados com Bokeh.
    *   Tabelas de resumo detalhadas por espécie e apresentação.
    *   Interface com sidebar para "filtragem" visual por espécie, utilizando HTMX para carregar dinamicamente os dados e gráficos correspondentes.
*   **Assistente Virtual (Chatbot):**
    *   Interface de chat integrada à plataforma Django, acessível por administradores e staff.
    *   Projetado para responder perguntas técnicas sobre o cultivo de cogumelos, utilizando como base de conhecimento o documento "Produção de Cogumelos por Meio de Tecnologia Chinesa Modificada" (Embrapa).
    *   **Arquitetura:** A interface Django consome uma API Flask externa. Esta API Flask implementa a lógica RAG (Retrieval-Augmented Generation) usando LlamaIndex, embeddings locais (`intfloat/multilingual-e5-large`), e o poder de geração de texto da API do Gemini (Google - modelo `gemini-2.0-flash`).
    *   A comunicação entre Django e a API Flask é protegida por uma chave secreta compartilhada.

---

## 4. Tecnologias e Arquitetura

*   **Framework Backend:** Django 4.2.6 (Python 3.12.2)
*   **Interface do Usuário (Frontend):**
    *   HTML5, CSS3
    *   **Tailwind CSS:** Framework CSS utilitário para design moderno e responsivo.
    *   **HTMX:** Para interações dinâmicas e atualizações parciais da página, especialmente nos dashboards, melhorando a usabilidade e reduzindo a necessidade de JavaScript complexo.
    *   **JavaScript (Vanilla):** Utilizado para funcionalidades específicas do cliente, como a interatividade da interface do chatbot e o toggle de tema claro/escuro.
*   **Banco de Dados:**
    *   Desenvolvimento: SQLite
    *   Produção (Railway): PostgreSQL (configurado via `dj_database_url`)
*   **Visualização de Dados:** Bokeh
*   **Autenticação de Usuários:** Django Allauth
*   **Processamento de Pagamentos:** Stripe
*   **Armazenamento de Mídia (Produção):** Cloudinary (configurado via `cloudinary_storage`)
*   **Segurança:** Django Admin Honeypot, CSRF protection, XSS protection (via Django templates).
*   **Servidor WSGI (Produção):** Gunicorn (implícito pelo Railway ou configurável).
*   **Hospedagem da Aplicação Django:** Railway
*   **API do Chatbot (Serviço Externo):**
    *   Framework: Flask (Python)
    *   RAG: LlamaIndex
    *   Embeddings: `intfloat/multilingual-e5-large` (local na API Flask)
    *   LLM: Google Gemini API (`gemini-2.0-flash`)
    *   Exposição para Desenvolvimento Django: Ngrok (temporário)
    *   Hospedagem Futura Planejada (Chatbot API): Railway

---

## 5. Configuração e Execução do Ambiente de Desenvolvimento

Siga os passos abaixo para configurar e rodar o projeto Django localmente. Este guia assume que a API Flask do chatbot será rodada separadamente (localmente ou via Ngrok).

### 5.1. Pré-requisitos
*   Python (versão 3.10 ou superior recomendado, o projeto usa 3.12.2)
*   Pip (gerenciador de pacotes Python)
*   Git
*   (Opcional, mas recomendado) Um gerenciador de ambiente virtual como `venv`.

### 5.2. Configuração do Projeto Django (Marketplace Sítio Nova Esperança)

1.  **Clonar o Repositório do Projeto Django:**
    ```bash
    git clone https://github.com/CodeVanzi/Django-Marketplace-Sitio
    cd Django-Marketplace-Sitio 
    ```
    (Substitua `Django-Marketplace-Sitio` pelo nome exato da pasta do seu projeto se for diferente).

2.  **Criar e Ativar Ambiente Virtual:**
    Recomenda-se fortemente usar um ambiente virtual para isolar as dependências do projeto.
    ```bash
    python -m venv venv
    ```
    Para ativar o ambiente virtual:
    *   No Windows (PowerShell): `.\venv\Scripts\Activate.ps1`
    *   No Windows (Git Bash ou CMD): `.\venv\Scripts\activate`
    *   No macOS/Linux: `source venv/bin/activate`
    Você deve ver `(venv)` no início do seu prompt do terminal.

3.  **Instalar Dependências Python:**
    Com o ambiente virtual ativado, instale todas as bibliotecas necessárias:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar Variáveis de Ambiente (Arquivo `.env`):**
    *   Na raiz do projeto Django (mesmo nível que `manage.py`), crie um arquivo chamado `.env` ou renomeie o arquivo .env_model para .env
    *   Copie o conteúdo do arquivo `env.example` (se existir) para o `.env` ou adicione as seguintes variáveis, adaptando os valores:

        ```env
        # Django Core
        ENVIRONMENT="development" 
        SECRET_KEY="django_chave_secreta_aqui_trocar_em_producao" 


        # Database (Exemplo para SQLite local, ajuste para PostgreSQL se necessário em dev)
        DATABASE_URL="sqlite:///db.sqlite3"

        # Stripe (Use chaves de TESTE do seu dashboard Stripe)
        STRIPE_API_KEY_PUBLISHABLE="pk_test_xxxxxxxxxxxxxxxxxxxxxxxx"
        STRIPE_API_KEY_HIDDEN="sk_test_xxxxxxxxxxxxxxxxxxxxxxxx"

        # Cloudinary (Opcional para desenvolvimento local, mas necessário se DEFAULT_FILE_STORAGE estiver configurado)
        # CLOUD_NAME="seu_cloud_name"
        # CLOUD_API_KEY="sua_api_key_cloudinary"
        # CLOUD_API_SECRET="sua_api_secret_cloudinary"

        # Configurações de E-mail (Para Allauth - recuperação de senha, etc.)
        # Exemplo para Gmail (requer configuração de "senha de app" no Google)
        # EMAIL_HOST="smtp.gmail.com"
        # EMAIL_PORT=587
        # EMAIL_USE_TLS=True
        # EMAIL_HOST_USER="seu_email@gmail.com"
        # EMAIL_HOST_PASSWORD="sua_senha_de_app_de_16_digitos"

        # URLs e Chaves para a API do Chatbot
        # Se a API Flask rodar localmente na porta 5001:
        CHATBOT_API_URL="http://127.0.0.1:5001/ask" 
        # Se for usar Ngrok, substitua pela URL HTTPS fornecida pelo Ngrok.
        # CHATBOT_API_URL="https://SUA_URL_NGROK.ngrok-free.app/ask"
        CHATBOT_API_SHARED_SECRET="SUA_CHAVE_SECRETA_COMPARTILHADA_DEFINIDA_NO_ENV_DA_API_FLASK"
        ```
    *   **Nota sobre `SECRET_KEY`:** Para produção, use uma chave forte e única gerada (o Django gera uma quando você cria o projeto).
    *   **Nota sobre `DATABASE_URL`:** Se você pretende usar PostgreSQL localmente, ajuste esta URL. Ex: `postgres://USER:PASSWORD@HOST:PORT/DBNAME`.

5.  **Aplicar Migrações do Banco de Dados:**
    Este comando cria as tabelas no seu banco de dados com base nos modelos definidos.
    ```bash
    python manage.py migrate
    ```

6.  **Criar um Superusuário:**
    Este usuário terá acesso total ao painel de administração do Django (`/mestre/`).
    ```bash
    python manage.py createsuperuser
    ```
    Siga as instruções para definir nome de usuário, e-mail e senha.

7.  **Coletar Arquivos Estáticos (Opcional para Desenvolvimento com `DEBUG=True`):**
    Embora o Django sirva arquivos estáticos automaticamente em desenvolvimento quando `DEBUG=True`, é uma boa prática verificar se `collectstatic` funciona. Em produção, este passo é essencial.
    ```bash
    python manage.py collectstatic --noinput
    ```

### 5.3. Configuração da API Flask do Chatbot (Serviço Separado)

A interface do chatbot neste projeto Django consome uma API Flask externa. Siga as instruções abaixo para configurar e rodar esta API.

1.  **(Se ainda não fez) Instalar Ollama (para opção de LLM local na API Flask):**
    *   Acesse [ollama.com](https://ollama.com/) e baixe o instalador para seu sistema operacional.
    *   Execute o instalador. O Ollama geralmente roda como um serviço em segundo plano.
    *   Baixe o modelo LLM configurado para uso local na API Flask (ex: `llama3.2:3b` se você tem um script `localchatbot.py` que o usa):
        ```bash
        ollama pull llama3.2:3b 
        ```
    *   O serviço Ollama deve estar em execução para a API Flask (versão local) funcionar.

2.  **Clonar o Repositório da API Flask do Chatbot:**
    ```bash
    git clone https://github.com/CodeVanzi/Chatbot-TCC-Univesp
    cd Chatbot-TCC-Univesp
    ```

3.  **Configurar Ambiente Virtual e Instalar Dependências (API Flask):**
    Dentro da pasta `Chatbot-TCC-Univesp`:
    ```bash
    python -m venv venv
    # Ativar venv (conforme instruções do seu SO)
    pip install -r requirements.txt 
    ```
    *Nota: O `requirements.txt` da API Flask pode ser diferente do projeto Django.*

4.  **Configurar Arquivo `.env` (API Flask):**
    Na raiz do projeto da API Flask (`Chatbot-TCC-Univesp`), crie um arquivo `.env` com:
    ```env
    GEMINI_API_KEY="SUA_CHAVE_DE_API_DO_GOOGLE_GEMINI_AQUI"
    CHATBOT_API_SHARED_SECRET="MESMA_CHAVE_SECRETA_COMPARTILHADA_DEFINIDA_NO_ENV_DO_DJANGO"
    ```
    *   A `GEMINI_API_KEY` é necessária para o script que usa a API do Gemini (ex: `geminichatbot.py`).
    *   A `CHATBOT_API_SHARED_SECRET` deve ser idêntica à definida no `.env` do projeto Django para que a autenticação funcione.

5.  **Preparar Dados para o Chatbot (PDF):**
    *   Dentro da pasta da API Flask, crie uma subpasta chamada `data` (se não existir).
    *   Coloque o arquivo PDF da Embrapa ("Produção de Cogumelos por Meio de Tecnologia Chinesa Modificada") dentro desta pasta `data/`.

6.  **Gerar Índice de Embeddings (API Flask):**
    *   A API Flask (tanto a versão Gemini quanto a local com Ollama) geralmente cria um índice de embeddings na primeira vez que é executada ou através de um script de pré-processamento. Este passo pode levar algum tempo e requer que o modelo de embedding (`intfloat/multilingual-e5-large`) seja baixado. Certifique-se de que a pasta de destino do índice (ex: `storage_gemini_llm` ou `storage`) tenha permissão de escrita.

### 5.4. Executando os Serviços

Você precisará de pelo menos dois terminais abertos: um para a API Flask e outro para o projeto Django. Se for usar Ngrok, um terceiro terminal.

1.  **Rodar a API Flask do Chatbot:**
    *   Navegue até a pasta da API Flask (`Chatbot-TCC-Univesp`).
    *   Ative o ambiente virtual da API Flask.
    *   Execute o script da API desejada (porta padrão geralmente é 5001):
        ```bash
        # Para usar a API do Gemini (recomendado para performance e deploy futuro)
        python geminichatbot.py 
        
        # OU, para usar o Ollama localmente (requer Ollama rodando com o modelo baixado)
        # python localchatbot.py 
        ```
    *   Mantenha este terminal aberto.

2.  **(Opcional, mas necessário se o Django não estiver na mesma máquina/rede ou para acesso externo durante o desenvolvimento) Rodar Ngrok para a API Flask:**
    *   Abra um novo terminal.
    *   Navegue até onde você extraiu o Ngrok.
    *   Execute (assumindo que a API Flask está na porta 5001):
        ```bash
        ngrok http 5001
        ```
    *   Copie a URL HTTPS fornecida pelo Ngrok (ex: `https://aleatorio.ngrok-free.app`).
    *   Atualize a variável `CHATBOT_API_URL` no arquivo `.env` do seu **projeto Django** para esta URL do Ngrok (ex: `CHATBOT_API_URL="https://aleatorio.ngrok-free.app/ask"`).

3.  **Rodar o Servidor de Desenvolvimento Django:**
    *   Navegue até a pasta do seu projeto Django (`Django-Marketplace-Sitio`).
    *   Ative o ambiente virtual do Django.
    *   Execute:
        ```bash
        python manage.py runserver
        ```
    *   Mantenha este terminal aberto.

### 5.5. Acessando a Aplicação

*   **Aplicação Django Principal:** `http://127.0.0.1:8000/`
*   **Painel de Administração (Real):** `http://127.0.0.1:8000/mestre/`
*   **Admin Honeypot:** `http://127.0.0.1:8000/admin/`
*   **Dashboard de Commodities:** `http://127.0.0.1:8000/commodities/dashboard/` (acesso restrito)
*   **Dashboard de Cogumelos:** `http://127.0.0.1:8000/commodities/db_cogumelos/` ( acesso restrito)
*   **Assistente Virtual (Chatbot):** `http://127.0.0.1:8000/assistente-virtual/` (acesso restrito)
*   **URL de Produção (Railway - PARA AVALIADORES - VER LOGIN E SENHA TEMPORÁRIOS NO ARQUIVO PRINCIPAL DO TCC, EM ANEXOS):** `https://sitionovaesperanca.up.railway.app/`

---

## 6. Estrutura de Deploy (Railway)

A aplicação Django está configurada para deploy na plataforma Railway. Considerações importantes para o deploy:
*   **Variáveis de Ambiente:** Todas as chaves sensíveis (`SECRET_KEY`, `DATABASE_URL`, `CHATBOT_API_URL` apontando para a API do chatbot hospedada, etc.) são configuradas como variáveis de ambiente diretamente no dashboard do Railway.
*   **`Procfile`:** Um `Procfile` é usado para definir os comandos para iniciar o servidor web (Gunicorn) e, se aplicável, rodar migrations.
    ```Procfile
    release: python manage.py migrate
    web: gunicorn marketplace_sitio.wsgi --log-file -
    ```
*   **Banco de Dados:** Railway oferece serviços de PostgreSQL que podem ser facilmente provisionados e conectados à aplicação Django através da variável de ambiente `DATABASE_URL`.
*   **Arquivos Estáticos:** `whitenoise` é utilizado para servir arquivos estáticos em produção. `python manage.py collectstatic` é executado durante o processo de build/release.
*   **API do Chatbot:** Para a versão de produção, a API Flask do chatbot também precisaria ser hospedada (ex: no Railway ou outro serviço) e a `CHATBOT_API_URL` no ambiente de produção do Django apontaria para essa URL hospedada.

---

## 7. Considerações sobre o Desenvolvimento do Chatbot (API Externa)

O componente chatbot deste projeto Django consome uma API Flask separada. Esta API implementa a lógica RAG:
*   **LlamaIndex:** Orquestra o pipeline de RAG.
*   **Embedding:** Utiliza o modelo `intfloat/multilingual-e5-large` (rodando localmente na instância da API Flask) para criar embeddings do documento base (PDF da Embrapa) e das perguntas dos usuários.
*   **LLM:** As perguntas (com contexto recuperado) são enviadas para a API do Google Gemini (modelo `gemini-2.0-flash`) para geração da resposta.
*   **Segurança:** A comunicação entre a app Django e a API Flask é protegida por uma chave secreta compartilhada (`X-API-Key`).

**Opções de Execução da API Flask do Chatbot:**
*   **`geminichatbot.py`:** Utiliza a API do Gemini para LLM e embeddings locais. Ideal para deploy na nuvem e para ter respostas da LMM mais rapidamente, ainda usando recursos locais para o embedding (indexação do documento de referênia).
*   **`localchatbot.py`:** Utiliza Ollama para LLM local (ex: `llama3.2:3b`) e embeddings locais. Útil para desenvolvimento totalmente offline ou para evitar custos de API, mas requer hardware mais robusto e o serviço Ollama em execução.
*   **`geminichatbot_railway.py` (Planejado):** Versão para usar tanto LLM quanto embeddings via API do Gemini, otimizada para deploy em plataformas como Railway, não implementada ainda.

---
