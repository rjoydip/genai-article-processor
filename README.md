# Python Starter

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![image](https://img.shields.io/pypi/v/uv.svg)](https://pypi.python.org/pypi/uv)
[![Checked with pyright](https://microsoft.github.io/pyright/img/pyright_badge.svg)](https://microsoft.github.io/pyright/)
[![CI](https://github.com/rjoydip/genai-article-processor/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/rjoydip/genai-article-processor/actions/workflows/ci.yml)

Building an Application for Processing Old Article Images with AI.

## 🚀 Features

- Docker support
- UV package manager
- Ruff for code formatting and linting
- Pytest for testing

## 📋 Prerequisites

- Python 3.13+
- Docker Desktop
- UV package manager

## Codeflow

```mermaid
graph TD
    A[main.py] --> B[ArticleProcessor]
    B --> C[ArticleProcessorAgent]

    C --> D[Step 1: Extract text from image]
    D --> E[AIProcessor.ask_ai]

    C --> F[Step 2: Parse XML metadata]
    F --> G[XMLParser.parse_xml_metadata]

    C --> H[Step 3: Combined sources]
    H --> I[AIProcessor.ask_ai]
    I --> J[UtilityManager.structure_json]

    C --> K[Step 4: Structure content]
    K --> L[AIProcessor.ask_ai]
    L --> M[UtilityManager.structure_json]

    C --> N[Step 5: Generate HTML]
    N --> O[HTMLProcessor.generate_html]
    O --> P[AIProcessor.ask_ai]

    C --> Q[Step 6: Save results]
    Q --> R[DataSaver.save_processed_data]

    subgraph Components
        E
        G
        J
        M
        P
        R
    end

    subgraph Process Flow
        D --> F --> H --> K --> N --> Q
    end

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style C fill:#bbf,stroke:#333,stroke-width:2px
    style E fill:#bfb,stroke:#333,stroke-width:2px
    style G fill:#bfb,stroke:#333,stroke-width:2px
    style J fill:#bfb,stroke:#333,stroke-width:2px
    style M fill:#bfb,stroke:#333,stroke-width:2px
    style P fill:#bfb,stroke:#333,stroke-width:2px
    style R fill:#bfb,stroke:#333,stroke-width:2px
```

## 🛠 Installation

- Clone the repository:

Install project dependencies:

```bash
uv sync
```

- Pre commit hook install

```bash
uvx pre-commit install
```

## Development

### Local Development

- Run UV application locally:

```bash
uv run main.py -n <INPUT_FILENAME>
# or
uv run main.py --name <INPUT_FILENAME>
```

- Run code formatting and linting:

```bash
uv run ruff format .
# or
uv run ruff check --fix --show-diff-on-failure
```

- Run pre-commit files

```bash
uvx pre-commit run --all-files
```

- Run typechecking:

```bash
uv run pyright
```

- Run tests:

```bash
uv run pytest
```

### Docker Development

Build and run the application in Docker:

```bash
docker build -t app .
docker run -p 8000:8000 app
```

## ⚙️ Configuration

- Project dependencies and settings are managed in `pyproject.toml`
- Ruff is configured for code formatting and linting
- Pytest is set up for testing

## 🧪 Testing

Tests are located in the `tests/` directory. Run the test suite using:

```bash
uv run pytest
```

## 🔍 Project Structure

```txt
genai-article-processor/
├─ .devcontainer/
│  └─ devcontainer.json
├─ .github/
│  ├─ actions/
│  │  └─ setup/
│  │     └─ action.yml
│  ├─ workflows/
│  │  └─ ci.yml
│  └─ dependabot.yml
├─ .vscode/
│  └─ extensions.json
├─ artifacts/
│  ├─ inputs/
│  │  ├─ article.png
│  │  ├─ article.xml
│  │  ├─ Muenchen-award-profile-1.png
│  │  ├─ Muenchen-award-profile-1.xml
│  │  ├─ Muenchen-death-notice-1.png
│  │  └─ Muenchen-newspaper-court-case-listings.png
│  └─ processed_data/
├─ modules/
│  ├─ agent.py
│  ├─ ai_processor.py
│  ├─ data_saver.py
│  ├─ html_processor.py
│  ├─ prompt_manager.py
│  └─ xml_parser.py
├─ tests/
│  └─ test_main.py
├─ .env
├─ .env.example
├─ .gitignore
├─ .pre-commit-config.yaml
├─ .python-version
├─ .tool-versions
├─ config.py
├─ docker-compose.yml
├─ Dockerfile
├─ LICENSE
├─ main.py
├─ pyproject.toml
├─ README.md
├─ utils.py
└─ uv.lock
```

## 👥 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
