# Sistema de Acompanhamento de PTs

Este sistema permite a elaboração de Permissões de Trabalho (PTs), consulta de análises de risco e, futuramente, a elaboração de Análises de Risco (ARs) através de uma interface web moderna que interage com o sistema corporativo, automatizando tarefas repetitivas e facilitando a gestão de segurança operacional.

![Logo Petrobras](static/logo-petrobras.png)

## Visão Geral

O Sistema de Acompanhamento de PTs foi desenvolvido para otimizar o fluxo de trabalho relacionado à emissão de permissões de trabalho e análises de risco, proporcionando:

- Interface web intuitiva e responsiva
- Automação de processos repetitivos
- Consolidação de informações em um único ambiente
- Geração de relatórios e históricos para auditoria

## Requisitos

- **Python 3.8 ou superior**
- **Firefox** (navegador recomendado)
- **Bibliotecas Python** (instaladas automaticamente pelo script de instalação):
  - selenium
  - pandas
  - flask
  - webdriver-manager
  - openpyxl
  - numpy

## Instalação

1. Clone este repositório:
```bash
git clone https://github.com/joaopaulo01/acompanhamento-pts.git
cd acompanhamento-pts
```

2. Execute o script de instalação:
```bash
python install.py
```

3. Configure as credenciais (opcional):
```bash
python configurar_credenciais.py
```

## Uso

1. Execute a aplicação:
```bash
python app.py
```

2. Acesse a interface web em [http://localhost:5000](http://localhost:5000) ou aguarde a abertura automática no navegador padrão.

3. Faça login com suas credenciais corporativas.

4. Na dashboard principal, você terá acesso a todas as funcionalidades do sistema.

## Funcionalidades Principais

### Dashboard
- Visão geral das PTs e ARs em andamento
- Indicadores de desempenho e estatísticas
- Acesso rápido às principais funcionalidades

### Programação
- Programação Semanal das PTs

### Elaboração de PTs
- Preenchimento automático a partir de dados da planilha
- Validação de dados antes da submissão
- Acompanhamento em tempo real do processo de elaboração

### Consulta de ARs
- Busca rápida de ARs por diversos critérios
- Visualização detalhada dos dados da AR
- Exportação de relatórios

### Elaboração de ARs (em desenvolvimento)
- Preenchimento automático a partir de dados da ordem
- Identificação de perigos e medidas de controle
- Interface guiada para garantir conformidade

### Histórico e Relatórios
- Registro completo de atividades
- Relatórios personalizáveis
- Exportação em diversos formatos

## Estrutura de Dados

O arquivo Excel para importação deve conter as seguintes colunas:

| Coluna              | Descrição                                              |
|---------------------|--------------------------------------------------------|
| ESPECIALIDADES      | Especialidades técnicas envolvidas nos trabalhos       |
| Ordem               | Número da ordem de serviço                             |
| Descrição da PT     | Descrição detalhada da permissão de trabalho           |
| LIBRA               | Identificador LIBRA                                    |
| ARO                 | Identificador ARO                                      |
| Número A.R.         | Número da Análise de Risco                             |
| PBS                 | Lista de Procedimentos Básicos de Segurança aplicáveis |
| Tipo PT/PTT         | Tipo de permissão (PT ou PTT)                          |
| Criticidade PMIC    | Nível de criticidade do trabalho                       |
| Gerência Emitente   | Gerência responsável pela emissão                      |
| Operações           | Códigos das operações a serem realizadas               |
| Tipo de Intervenção | Classificação da intervenção (Corretiva/Preventiva)    |
| Forma de Trabalho   | Classificação do trabalho (Quente/Frio)                |

## Arquitetura do Sistema

### Frontend
- Interface web responsiva desenvolvida com HTML5, CSS3 e JavaScript
- Templates Flask para renderização dinâmica
- Feedback visual em tempo real durante operações

### Backend
- Servidor Flask para processamento de requisições
- Módulo de automação Selenium para interação com sistemas corporativos
- Sistema de logs para rastreabilidade

### Automação com Selenium

O sistema utiliza o Selenium WebDriver para automatizar interações com o sistema corporativo:

1. **Login automático**: Acessa o sistema usando as credenciais fornecidas
2. **Navegação inteligente**: Navega pelas páginas necessárias identificando elementos dinamicamente
3. **Preenchimento de formulários**: Preenche automaticamente dados com validação
4. **Captura de resultados**: Extrai informações relevantes para feedback ao usuário

## Estrutura do Projeto

```
acompanhamento-pts/
│
├── app.py                 # Aplicação principal Flask
├── elaborador.py          # Módulo de automação com Selenium
├── install.py             # Script de instalação e configuração
│
├── templates/             # Templates HTML
│   ├── base.html          # Template base com layout comum
│   ├── configuracoes.html # Configurações do sistema
│   ├── consultar_ar.html  # Interface para consulta de ARs
│   ├── dashboard.html     # Dashboard principal
│   ├── elaborar_pts.html  # Interface para elaboração de PTs
│   ├── historico.html     # Histórico de operações
│   ├── index.html         # Página inicial
│   ├── login.html         # Tela de login
│   ├── relatorios.html    # Geração de relatórios
│   └── resultado.html     # Exibição de resultados
│
├── static/                # Arquivos estáticos
│   ├── js/                # Scripts JavaScript
│   │   └── script.js      # Funções JavaScript principais
│   ├── style.css          # Estilos CSS
│   └── logo-petrobras.png # Logotipo
│
├── uploads/               # Diretório para arquivos carregados
└── screenshots/           # Capturas de tela durante a automação
```

## Solução de Problemas

### Erro de login
- Verifique se as credenciais estão corretas e atualizadas
- Confirme se você tem acesso ao sistema corporativo
- Verifique se não há bloqueios de segurança no navegador

### Erro ao carregar planilha
- Certifique-se de que o formato da planilha é compatível (Excel .xlsx ou .xls)
- Verifique se todas as colunas necessárias estão presentes e corretamente formatadas
- Evite caracteres especiais nos cabeçalhos ou dados

### Erro na automação
- Verifique se o Firefox está instalado e atualizado
- Execute `webdriver-manager update` para atualizar o webdriver
- Verifique se há popups ou captchas bloqueando a automação
- Ajuste o tempo de espera se a rede estiver lenta

### Aplicação não abre
- Verifique se a porta 5000 está disponível:
  - Windows: `netstat -ano | findstr 5000`
  - Linux/Mac: `lsof -i:5000`
- Certifique-se de que não há outra instância da aplicação rodando
- Verifique logs para mensagens de erro específicas

## Desenvolvimento Futuro

### Roadmap
- **Integração direta com SAP**: Eliminação da necessidade de importar planilhas Excel
- **Dashboard analítico**: Métricas avançadas e visualizações de dados
- **App mobile**: Versão para dispositivos móveis para consultas em campo
- **Notificações**: Sistema de alertas

### Contribuindo com o Projeto

Para contribuir com o desenvolvimento:

1. Crie um fork do repositório
2. Configure seu ambiente de desenvolvimento:
   ```bash
   python install.py --dev
   ```
3. Implemente suas alterações seguindo as diretrizes de código
4. Adicione testes para novas funcionalidades
5. Envie um pull request detalhado

## Suporte

Em caso de problemas ou dúvidas:
- Abra uma issue no repositório GitHub
- Consulte a documentação interna no diretório `docs/`
- Entre em contato com o desenvolvedor principal: [seu-email@exemplo.com]

## Licença

Este projeto é licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Agradecimentos

- Equipe de SMS da Petrobras pelo suporte técnico
- Contribuidores do projeto Selenium WebDriver
- Comunidade Flask e Python

---

*Desenvolvido por João Paulo Cavalcante - Petrobras, 2025*
