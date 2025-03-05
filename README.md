# my-favorite-movies-clean-arch

Ótimo! Com base na estrutura do seu projeto, vamos atualizar o **README** para refletir a refatoração usando **Arquitetura Limpa**.

---

# 🎬 My Favorite Movies - Clean Architecture  

## 📌 **Descrição do Projeto**  

O **My Favorite Movies** é um sistema para gerenciar filmes e séries favoritos, permitindo que os usuários adicionem seus conteúdos preferidos, comentem e acompanhem tendências do cinema e TV. O sistema consome a API do **TMDB (The Movie Database)** para buscar e armazenar informações.  

Este projeto foi refatorado para seguir a **Arquitetura Limpa (Clean Architecture)**, separando as responsabilidades em camadas bem definidas, tornando o código **mais modular, desacoplado e escalável**.  

O backend foi desenvolvido com **FastAPI**, enquanto o frontend é construído em **React**. Para armazenamento de dados, o sistema usa **PostgreSQL** e **Redis** para cache, garantindo alta performance.  

---

## 🚀 **Principais Funcionalidades**  

✅ **Gerenciamento de Filmes e Séries**  
- Adicionar filmes e séries aos favoritos  
- Buscar detalhes na API do TMDB  
- Listar, editar e remover filmes e séries favoritos  

✅ **Comentários**  
- Adicionar, editar e remover comentários em filmes e séries  

✅ **Autenticação & Segurança**  
- Cadastro e login de usuários  
- Tokens JWT para autenticação segura  

✅ **Performance & Cache**  
- Banco de dados **PostgreSQL** para persistência  
- **Redis** para cache de dados, reduzindo requisições à API  

✅ **Arquitetura Modular & Escalável**  
- Implementação baseada em **Arquitetura Limpa (Clean Architecture)**  
- Separação clara entre **Entities, UseCases, Adapters, Infrastructure e API**  

---

## 🏛 **Arquitetura do Projeto (Clean Architecture)**  

A estrutura do projeto segue os princípios da **Arquitetura Limpa**, organizando o código em diferentes camadas:

```
app/
│── adapters/                     # Interfaces com APIs Externas e outros serviços
│   ├── movie_api_adapter.py       # Comunicação com a API do TMDB
│   ├── email_adapter.py           # Serviço de envio de e-mails
│   ├── redis_adapter.py           # Interface para cache no Redis
│
│── api/                           # Interface com o Mundo Externo (FastAPI)
│   ├── dependencies.py            # Injeção de Dependências
│   ├── router.py                  # Registro de todas as rotas
│   ├── v1_endpoints/              # Rotas da API
│       ├── usuario_route.py       # Rotas relacionadas a usuários
│       ├── usuario_conteudos_route.py  # Relacionadas aos conteúdos do usuário
│       ├── comentario_route.py    # Rotas de comentários
│       ├── conteudos_route.py     # Rotas de filmes e séries
│
│── domain/                        # Camada de Regras de Negócio
│   ├── entities/                  # Entidades (Modelos de Domínio)
│   │   ├── user.py
│   │   ├── movie.py
│   │   ├── tv_show.py
│   │   ├── comment.py
│   ├── models/                    # Modelos do Banco de Dados
│   │   ├── User.py
│   │   ├── Movie.py
│   │   ├── TvShows.py
│   │   ├── Comentario.py
│   ├── usecases/                  # Casos de Uso (Regras de Negócio)
│       ├── user_usecase.py
│       ├── movie_usecase.py
│       ├── tv_show_usecase.py
│       ├── comment_usecase.py
│
│── infrastructure/                 # Infraestrutura e Implementações
│   ├── repositories/               # Repositórios (Acesso ao Banco de Dados)
│   │   ├── user_repository.py
│   │   ├── movie_repository.py
│   │   ├── tv_show_repository.py
│   │   ├── comment_repository.py
│   ├── services/                   # Serviços Externos (Autenticação, Email, Segurança)
│   │   ├── auth_service.py
│   │   ├── email_service.py
│   │   ├── security_service.py
│
│── schemas/                        # Esquemas (Pydantic) para validação de dados
│   ├── UsuarioSchemas.py
│   ├── MovieSchemas.py
│   ├── TvShowsSchemas.py
│   ├── ComentarioSchemas.py
│
│── settings/                       # Configurações da Aplicação
│   ├── config.py                   # Configurações globais
│   ├── logs.py                      # Configuração de logging
│
│── main.py                          # Ponto de entrada do FastAPI
│── requirements.txt                  # Dependências do projeto
│── docker-compose.yaml                # Arquivo para rodar os serviços no Docker
│── Makefile                          # Comandos de automação do projeto
│── tests/                            # Testes automatizados
```

---

## 🛠 **Tecnologias Utilizadas**  

### 🔹 **Backend**  
- **FastAPI** - Framework assíncrono para APIs  
- **SQLAlchemy + Alembic** - ORM e Migrações para PostgreSQL  
- **Pydantic** - Validação de dados  
- **JWT (PyJWT)** - Autenticação segura  

### 🔹 **Frontend**  
- **React.js** - Interface do usuário  

### 🔹 **Banco de Dados & Cache**  
- **PostgreSQL** - Banco relacional para persistência  
- **Redis** - Cache para melhorar performance  

### 🔹 **APIs Externas**  
- **TMDB (The Movie Database)** - Busca de filmes e séries  

---

## 📦 **Instalação e Configuração do Ambiente**  

### 📌 **Pré-requisitos**  
Antes de iniciar, **certifique-se de ter instalado**:  
- **Docker & Docker Compose**  
- **Python 3.12+**  

### 🔹 **Passo 1: Clonar o Repositório**  
```sh
git clone https://github.com/vinnieoh/my-favorite-movies.git
cd my-favorite-movies
```

### 🔹 **Passo 2: Criar e Configurar o Arquivo `.env`**  
Copie o arquivo `.env_exemplo_backend` para `.env`:  
```sh
cp ./api/dotenv_files/.env_exemplo_backend ./api/dotenv_files/.env
```
Edite o arquivo e adicione sua **TMDB API Key**:  
```sh
API_MOVIE=<sua_api_key_da_tmdb>
```

### 🔹 **Passo 3: Subir os Serviços com Docker**  
```sh
docker-compose up --build
```
Isso irá:  
✅ Criar e iniciar o banco **PostgreSQL**  
✅ Criar e iniciar o **Redis**  
✅ Criar e iniciar o backend **FastAPI**  
✅ Criar e iniciar o frontend **React**  

Para verificar se o backend está rodando, acesse:  
📍 **http://127.0.0.1:8000/docs**  

---

## 🔧 **Comandos Úteis**  

| Comando | Descrição |
|---------|------------|
| `make dev` | Inicia o servidor FastAPI em modo de desenvolvimento |
| `make test` | Executa os testes automatizados |
| `make lint` | Verifica a qualidade do código com flake8 |
| `make migrate` | Aplica as migrações do banco de dados |

---

## 📝 **Observações**  

- Certifique-se de ter uma **API Key válida da TMDB** para consumir os serviços de filmes e séries.  
- O projeto está configurado para ser executado via **Docker**, facilitando a configuração do ambiente e a implantação.  
- Para modificar regras de negócio, edite os **UseCases** dentro da pasta `app/domain/usecases/`.  

---

## 📜 **Licença**  

Este projeto está licenciado sob a **Licença MIT**. Consulte o arquivo **LICENSE** para obter mais informações.  

🔗 **Repositório GitHub Codigo Original**: [My Favorite Movies](https://github.com/vinnieoh/my-favorite-movies)  

---

Agora o README reflete corretamente a **Arquitetura Limpa** do projeto, destacando a separação de camadas e a organização do código. 🚀🎬