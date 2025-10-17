# 🔍 Verificador de Integridade de Arquivos

Sistema robusto e profissional para verificação de integridade de arquivos com suporte avançado para formatos Excel, análise multiplataforma e geração de executáveis standalone.

## 🎯 Funcionalidades Principais

### ✨ Verificações Gerais

- **Hash MD5/SHA256** - Detecção precisa de corrupção
- **Acessibilidade** - Verificação de permissões e disponibilidade
- **Metadados** - Tamanho, data de modificação, permissões
- **Status inteligente** - INTACT, CORRUPTED, INACCESSIBLE, UNKNOWN

### 📊 Verificações Específicas por Formato

| Formato                | Verificações                                                                      |
| ---------------------- | --------------------------------------------------------------------------------- |
| **Excel (.xlsx/.xls)** | 🆕 Análise avançada de planilhas, células, dados ausentes, auto-instalação pandas |
| **CSV**                | Formato, encoding, contagem linhas/colunas, detecção separador                    |
| **JSON**               | Sintaxe válida, estrutura hierárquica                                             |
| **PDF**                | Cabeçalho, estrutura, versão PDF                                                  |
| **XML**                | Estrutura bem formada, encoding                                                   |
| **ZIP/RAR**            | Integridade, lista de arquivos                                                    |
| **Python**             | Sintaxe válida (AST), estrutura                                                   |
| **SQL**                | Statements válidos, estrutura básica                                              |
| **Texto**              | Encoding, contagem linhas/caracteres                                              |

### 🚀 Funcionalidades Excel Avançadas ⭐ **NOVO**

- **Auto-detecção de pandas** - Verifica disponibilidade automaticamente
- **Auto-instalação de dependências** - Instala pandas e openpyxl quando necessário
- **Análise multi-planilha** - Examina todas as abas simultaneamente
- **Estatísticas detalhadas**:
  - Contagem de linhas, colunas e células por planilha
  - Detecção e percentual de dados ausentes
  - Tipos de dados por coluna
  - Validação de formato e estrutura
- **Tratamento robusto de erros**:
  - Detecção de arquivos `.xls` renomeados como `.xlsx`
  - Tratamento de erros de estilo (`openpyxl.styles.fills.Fill`)
  - Detecção de arquivos ZIP corrompidos
  - Fallbacks para diferentes engines de leitura

## 🚀 Como Usar

### 🖥️ Interface Interativa (Recomendado)

```bash
# Modo interativo com configuração guiada
python verificador_interativo.py
```

**Recursos da interface:**

- Configuração passo-a-passo
- Validação de parâmetros
- Opções de análise Excel
- Auto-instalação de dependências
- Confirmação antes da execução

### 💻 Linha de Comando

```bash
# Verificar um diretório
python script.py /caminho/para/diretorio

# Verificar múltiplos diretórios
python script.py /dir1 /dir2 /dir3

# Especificar formato de saída
python script.py /diretorio --format json

# Arquivo de saída personalizado
python script.py /diretorio --output relatorio_integridade

# Busca recursiva
python script.py /diretorio --recursive

# Filtrar por tipo de arquivo
python script.py /diretorio --filter "*.xlsx,*.csv"
```

### 🐍 Uso Programático

- **Criar verificador básico**: `checker = FileIntegrityChecker(['/caminho/diretorio'])`

- **Com análise Excel avançada**: `checker = FileIntegrityChecker(['/dir'], auto_install_excel=True)`

- **Executar verificação**: `checker.scan_directories()`

- **Gerar relatório**: `checker.generate_report('meu_relatorio')`

- **Verificar arquivo específico**:
  ```
  resultado = checker.check_file_integrity('/caminho/arquivo.xlsx')
  print(resultado['integrity_status']) # INTACT, CORRUPTED, INACCESSIBLE, UNKNOWN
  ```

# Análise Excel detalhada

```**py**
if 'specific_checks' in resultado:
excel_info = resultado['specific_checks']
print(f"Planilhas: {excel_info.get('sheets_count')}")
print(f"Células analisadas: {excel_info.get('total_cells')}")
```

## 📦 Instalação e Dependências

### Requisitos Mínimos

- **Python 3.6+** (recomendado 3.8+)
- Bibliotecas padrão Python (hashlib, json, csv, pathlib, etc.)

### Dependências Opcionais (Auto-instaladas)

```bash
# Para análise Excel avançada (instalação automática disponível)
pip install pandas openpyxl
```

### Instalação Rápida

```bash
# Clonar repositório
git clone <repository-url>
cd verificar_integridade_arquivos

# Executar diretamente (sem instalação adicional)
python verificador_interativo.py
```

## 🖥️ Executáveis Standalone

### 📦 Pacotes Prontos

- **`VerificadorIntegridade_Excel_20251016_1342.zip`** - Versão final completa
- **`Build_Windows_Excel_20251016_1354.zip`** - Kit para build Windows

### 🪟 Build Windows

```cmd
# Método automático
1. Extrair Build_Windows_Excel_20251016_1354.zip
2. Executar: build_windows_excel.bat

# Método manual
pip install pyinstaller pandas openpyxl
pyinstaller --onefile --name="VerificadorIntegridade_Excel" verificador_interativo.py
```

## 📊 Relatórios de Saída

### Formatos Disponíveis

- **JSON** - Relatório completo com todos os detalhes
- **CSV** - Dados tabulares para análise em planilhas
- **TXT** - Sumário legível para humanos

### Estrutura do Relatório JSON

```json
{
  "summary": {
    "total_files": 150,
    "intact_files": 145,
    "corrupted_files": 3,
    "excel_files": 12,
    "scan_date": "2025-10-17T10:30:00"
  },
  "files": [
    {
      "file_name": "relatorio.xlsx",
      "integrity_status": "INTACT",
      "file_size": 15360,
      "md5_hash": "a1b2c3d4...",
      "specific_checks": {
        "format_valid": true,
        "sheets_count": 3,
        "total_cells": 450,
        "verification_level": "advanced"
      }
    }
  ]
}
```

## 🔍 Status de Integridade

| Status              | Descrição                              | Ação Recomendada     |
| ------------------- | -------------------------------------- | -------------------- |
| **INTACT** ✅       | Arquivo íntegro e funcional            | Nenhuma              |
| **CORRUPTED** ❌    | Arquivo corrompido ou formato inválido | Recuperar de backup  |
| **INACCESSIBLE** 🚫 | Sem permissão ou arquivo não existe    | Verificar permissões |
| **UNKNOWN** ❓      | Status indeterminado                   | Análise manual       |

## 🧪 Exemplos Práticos

### Verificação Rápida

```bash
python verificador_interativo.py
# Siga as instruções na tela
```

### Análise de Múltiplos Diretórios

```bash
python script.py /dados/vendas /dados/estoque /dados/clientes --format json
```

### Análise Excel Específica

```bash
python script.py /planilhas_excel --filter "*.xlsx" --output relatorio_excel
```

## 🔧 Problemas Conhecidos e Soluções

### Excel - Erro "expected openpyxl.styles.fills.Fill"

**Problema**: Arquivo Excel com formatação/estilos complexos

**Solução**: O sistema detecta automaticamente e tenta leitura alternativa

**Status**: Arquivo é válido, mas com formatação não suportada pelo parser

### Excel - Erro "File is not a zip file"

**Problema**: Arquivo `.xlsx` corrompido ou `.xls` renomeado

**Solução**: Sistema identifica o formato real e sugere correções

**Status**: Verificação de cabeçalho binário implementada

### Auto-instalação de Dependências

O sistema pergunta automaticamente se deve instalar pandas/openpyxl quando detecta arquivos Excel.

## 📁 Estrutura do Projeto

```text
verificar_integridade_arquivos/
├── 🔧 CÓDIGO FONTE
│   ├── script.py                           # Engine principal (31KB)
│   ├── verificador_interativo.py          # Interface (19KB)
│   └── README.md                           # Esta documentação
│
├── 🏗️ BUILD WINDOWS
│   ├── build_windows_excel.bat            # Script automático
│   ├── requirements_windows.txt           # Dependências
│   └── verificador_excel_windows.spec     # Config PyInstaller
│
└── 📦 DISTRIBUIÇÃO
    ├── VerificadorIntegridade_Excel_*.zip  # Versão final
    └── Build_Windows_Excel_*.zip           # Kit build Windows
```

## 🚀 Performance

| Cenário                  | Tempo | Funcionalidades      |
| ------------------------ | ----- | -------------------- |
| Arquivo pequeno (<10MB)  | 1-2s  | Análise completa ✓   |
| Arquivo médio (10-100MB) | 3-10s | Análise completa ✓   |
| Arquivo grande (>100MB)  | 1-2s  | Verificação básica ✓ |
| Excel com pandas         | +0.5s | Análise avançada ✓   |

## 🤝 Contribuição

1. Fork do projeto
2. Crie sua feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📞 Suporte

Para reportar bugs ou solicitar funcionalidades:

1. Abra uma issue no GitHub
2. Inclua logs de erro (`file_integrity_check.log`)
3. Descreva o ambiente (OS, Python version)
4. Forneça exemplos de arquivos problemáticos (se possível)

## Casos de Uso Típicos

1. **Auditoria de Integridade**: Verificar se arquivos de backup estão íntegros
2. **Validação Pós-Transferência**: Confirmar que arquivos foram transferidos corretamente
3. **Detecção de Corrupção**: Identificar arquivos corrompidos antes de processamento
4. **Monitoramento de Sistema**: Verificação periódica de integridade de dados
5. **Migração de Dados**: Validar integridade antes e após migração
