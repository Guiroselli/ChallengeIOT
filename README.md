Sistema RFID para Mapeamento e Gestão de Motos da Mottu
Este projeto foi desenvolvido como parte do Challenge 2025 - 1º Semestre, focando na seção de DISRUPTIVE ARCHITECTURES: IOT, IOB & GENERATIVE IA. O sistema simula um ambiente de rastreamento RFID para o mapeamento e gestão das motos da Mottu em seus pátios, similar ao sistema Sem Parar utilizado em pedágios.
Conteúdo do Projeto
O projeto é composto pelos seguintes arquivos:
rfid_simulation_corrigido_final.py - Código principal da simulação do sistema RFID
disruptive_architectures.md - Documento teórico sobre IoT, IoB e IA Generativa aplicados ao contexto da Mottu
documentacao_prototipo_rfid.md - Documentação técnica detalhada do protótipo
roteiro_pitch_rfid_mottu.md - Roteiro para o vídeo pitch de 5 minutos
Tecnologias Utilizadas
Linguagens e Bibliotecas
Python 3.x - Linguagem de programação principal
NumPy - Para cálculos numéricos e operações matemáticas
Pandas - Para manipulação e análise de dados
Matplotlib - Para visualização e interface gráfica da simulação
UUID - Para geração de identificadores únicos
Datetime - Para manipulação de datas e horários
Conceitos e Tecnologias Disruptivas
Internet das Coisas (IoT) - Implementada através do sistema RFID para rastreamento de motos
Internet dos Comportamentos (IoB) - Análise de padrões de uso e movimentação das motos
Inteligência Artificial Generativa - Conceitos aplicados para otimização de rotas e previsão de demanda
Estrutura do Sistema
Componentes Principais
Tags RFID - Cada moto possui uma tag RFID única que permite seu rastreamento
Leitores RFID - Posicionados estrategicamente no pátio para detectar as motos
Sistema de Visualização - Interface gráfica que mostra o mapa do pátio e a localização das motos em tempo real
Sistema de Estatísticas - Fornece informações sobre o status das motos e detecções RFID
Áreas do Pátio
Entrada - Área onde as motos entram no pátio
Saída - Área onde as motos saem do pátio
Estacionamento - Área principal onde as motos ficam estacionadas
Manutenção - Área dedicada para motos em manutenção
Status das Motos
Disponível (Verde) - Motos prontas para uso
Reservada (Azul) - Motos já reservadas por clientes
Em Manutenção (Laranja) - Motos em processo de manutenção
Requisitos de Sistema
Para executar a simulação, você precisará:
Python 3.x instalado
Bibliotecas: numpy, pandas, matplotlib
Mínimo de 4GB de RAM recomendado
Resolução de tela mínima de 1280x720 para melhor visualização
Instalação
Certifique-se de ter o Python instalado em seu sistema
Instale as bibliotecas necessárias:
pip install numpy pandas matplotlib
Baixe todos os arquivos do projeto para uma pasta local
Execução
Para iniciar a simulação, execute o seguinte comando no terminal:
python rfid_simulation_corrigido_final.py
A simulação abrirá uma janela mostrando o pátio da Mottu com as motos e leitores RFID. As motos são representadas por quadrados coloridos de acordo com seu status, e os leitores RFID são representados por círculos que indicam seu alcance de detecção.
Funcionalidades
Rastreamento em Tempo Real - Visualize a posição exata de cada moto no pátio
Detecção RFID - Os leitores detectam automaticamente as motos dentro de seu alcance
Estatísticas - Painel com informações sobre o número de motos por status e detecções RFID
Setores - O pátio é dividido em setores (A, B, C, D) para facilitar a localização
Resultados Parciais
A simulação demonstra com sucesso como um sistema RFID pode ser implementado para o mapeamento e gestão das motos da Mottu. Os resultados incluem:
Detecção precisa das motos em diferentes áreas do pátio
Visualização clara do status de cada moto (disponível, reservada, em manutenção)
Estatísticas em tempo real sobre a ocupação do pátio
Demonstração da viabilidade técnica da solução proposta
Próximos Passos
Para uma implementação real, os próximos passos incluiriam:
Integração com sistemas de gestão existentes da Mottu
Implementação de hardware RFID real (tags e leitores)
Desenvolvimento de aplicativo móvel para acesso às informações
Implementação de análise preditiva para otimização de recursos
Contribuições
Este projeto foi desenvolvido como parte do Challenge 2025 - 1º Semestre. As principais contribuições incluem:
Conceito e design do sistema RFID para gestão de frotas
Implementação da simulação em Python
Documentação técnica e teórica
Roteiro para apresentação do projeto
Autores
Desenvolvido pela equipe do Challenge 2025 - 1º Semestre.
