# RELATÓRIO - Laboratório de Concorrência e Gargalos em Servidores TCP

Aluna: Paloma Dias de Carvalho

## Questão 1 — Backlog e Recusa de Conexões

O clientenervoso.py apresentou falhas (ConnectionRefusedError ou Timeout) ao testar o servergargalo.py, mas obteve sucesso imediato contra o server.py.

*Motivo Técnico:*
Teste com clientenervoso.py (10 clientes simultâneos)

Executando com servergargalo.py (listen(1))

Apenas 2 clientes conseguiram estabelecer conexão.

Os outros 8 receberam timeout (no Windows não foi gerado ConnectionRefusedError).

Executando com server.py (modelo multithread)

Os 10 clientes conectaram com sucesso.

Foram criadas 10 threads simultâneas para atendimento.

O parâmetro listen(backlog) determina quantas conexões podem permanecer na fila de espera do TCP antes de serem efetivamente aceitas pelo método accept().

No caso do servergargalo.py, configurado com listen(1) e contendo um processamento bloqueante de 5 segundos, o servidor demora a retornar ao accept(). Isso faz com que a fila de conexões pendentes se esgote rapidamente. Como consequência, no Windows, as conexões permanecem aguardando a conclusão do handshake TCP até atingirem o tempo limite, resultando em timeout para os clientes (configurados com 2 segundos).

Já no server.py, o backlog padrão é significativamente maior (aproximadamente 128). Além disso, cada nova conexão é imediatamente delegada a uma thread separada, permitindo que o loop principal continue executando o accept() quase sem interrupções. Isso impede o acúmulo excessivo de conexões na fila e evita o esgotamento do backlog.

O comportamento distinto entre sistemas operacionais, conforme previsto no roteiro, foi confirmado: no Windows os clientes experimentaram timeout, enquanto em ambientes Linux seria mais provável ocorrer diretamente um ConnectionRefusedError.

## Questão 2 — Custo de Recursos: Threads vs. Event Loop

Com base no número máximo de threads simultâneas que você observou no server.py (via threading.active_count()), explique a diferença no consumo de memória e no uso de CPU entre a abordagem Multithread e a abordagem Assíncrona.

 *Resultados observados:*
No modelo multithread (server.py), foram criadas 10 threads para atendimento dos clientes, além da thread principal, totalizando 11 threads em execução.

Já no modelo assíncrono (server_async.py), apenas uma única thread foi utilizada, o Event Loop, responsável por gerenciar simultaneamente as 10 conexões por meio de corrotinas.

Análise de Consumo de Recursos

### Memória

No modelo multithread, cada thread reserva aproximadamente 1 MB de memória para stack. Assim, 10 threads adicionais representam cerca de 10 MB consumidos apenas para estrutura de execução.

No modelo assíncrono, há somente uma thread ativa e múltiplas corrotinas, que são estruturas muito mais leves (aproximadamente 1 a 2 KB cada). O consumo total permanece na faixa de 1 a 2 MB.

Isso significa que o modelo assíncrono pode consumir até dez vezes menos memória para a mesma carga de conexões.

### Processamento (CPU)

No servidor multithread, o sistema operacional realiza constantes trocas de contexto entre threads. Cada context switch envolve salvar e restaurar registradores da CPU, além de possíveis invalidações de cache, gerando um custo estimado entre 1 e 10 microssegundos por troca.

No servidor assíncrono, não há troca de contexto entre threads. A alternância ocorre de forma cooperativa entre corrotinas, sob controle do Event Loop do Python, o que torna o processo significativamente mais leve e eficiente.

### Escalabilidade

Em um cenário com 1000 conexões simultâneas:

O modelo multithread poderia consumir aproximadamente 1 GB de memória apenas com stacks de threads, além de sofrer degradação significativa de desempenho devido ao grande número de trocas de contexto.

O modelo assíncrono manteria o consumo de memória na faixa de 2 a 3 MB, com desempenho mais estável, já que não depende da criação massiva de threads nem da intervenção intensiva do escalonador do sistema operacional.

### Conclusão

Para aplicações predominantemente I/O-bound, como servidores de rede, o modelo assíncrono tende a ser mais eficiente: utiliza menos memória, reduz o overhead de troca de contexto e apresenta melhor escalabilidade sob alta concorrência.

O modelo multithread, por outro lado, é mais indicado para cenários CPU-bound que demandam paralelismo real de processamento.

# Caso Desafio

<img width="1282" height="885" alt="Desafio_extra" src="https://github.com/user-attachments/assets/eab0997b-ff81-4cd3-830c-a49d4c149ef2" />

<img width="1257" height="912" alt="Desafio_extra_01" src="https://github.com/user-attachments/assets/c06091bf-c8b2-45d5-a6d7-cfd6239a8bad" />

<img width="1252" height="910" alt="Desafio_extra_02" src="https://github.com/user-attachments/assets/a86f4fb4-e2eb-4ef7-96ce-1bc5e5aa6f85" />

# EVIDÊNCIA DOS TESTES

*1.1 Servidor bloqueante:*
<img width="1257" height="390" alt="1 1 Servidor Bloqueante" src="https://github.com/user-attachments/assets/bf504f09-f5bc-4f8b-9d0c-eef5049ea2c0" />

*1.2 Comportamento do backlog:*
<img width="1262" height="645" alt="1 2 Comportamente do Backlog" src="https://github.com/user-attachments/assets/3c9b8fdc-6481-40f8-a9eb-30e2d19a0c3a" />

*2.1 Servidor Multithread:*
<img width="1251" height="883" alt="2 1 Servidor Multithread" src="https://github.com/user-attachments/assets/b115f137-1a69-412c-8bec-5506c611a7d0" />

*3.3 Validação*
<img width="1262" height="908" alt="3 3 Validação" src="https://github.com/user-attachments/assets/8fa7e1ba-df13-4c60-adcf-916f3584acff" />

