# Licenciatura em Computação (UFRPE)
Projeto desenvolvido para a disciplina de Arquitetura e Organização de Computadores - 2026.2

Alunos: Túlio Lorca de Araújo Falcão, Henrique Barbosa Mendes e Lucas Thomaz de Santana

# Simulador MIPS - Etapa 1: Desassemblador (Disassembler)

Esta primeira etapa consiste em um desassemblador capaz de converter instruções binárias de 32 bits (representadas em hexadecimal) para a linguagem Assembly MIPS correspondente.

## 📌 Funcionalidades
- Leitura automatizada de arquivos JSON de entrada (`entrada.json`).
- Conversão e alinhamento de instruções Hexadecimais para Binário de 32 bits.
- Suporte a 40 instruções da arquitetura MIPS (Formatos R, I, J e chamada `syscall`).
- Tratamento de extensoes de sinal para valores imediatos negativos.
- Exportação dos resultados desassemblados em formato JSON estruturado (`exemploSaida.json`).

## 📁 Estrutura do Projeto

| Arquivo | Descrição |
| :--- | :--- |
| `app.py` | Orquestrador principal da aplicação. Integra a leitura, conversão e escrita do JSON final. |
| `decodificador.py` | Módulo responsável pelo Input/Output do arquivo `entrada.json`. |
| `instrucoesMips.py` | Núcleo do desassemblador. Contém a tabela de instruções, fatiamento de bits e formatação Assembly. |
| `entrada.json` | Arquivo contendo a lista de palavras em hexadecimal a serem processadas. |
| `exemploSaida.json` | Arquivo gerado contendo o código desmontado e o estado inicial das estruturas. |

## 🚀 Como Executar

### Pré-requisitos
- Python 3.8 ou superior instalado.
