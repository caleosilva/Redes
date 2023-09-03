# 1. Introdução

Considerando o crescente interesse na automação de supermercados, impulsionado pelo avanço da tecnologia e o desenvolvimento de conceitos como IoT (Internet of Things), muitas empresas buscam implementar soluções tecnológicas para aprimorar sua eficiência operacional, reduzir custos e oferecer uma experiência de compra melhorada aos clientes.

Nesse contexto, um supermercado localizado em Feira de Santana decidiu investir em um sistema de caixa de supermercado inteligente baseado em tecnologia RFID (Radio Frequency Identification). O objetivo deste projeto é possibilitar a leitura rápida de múltiplos produtos por meio de tags RFID, permitindo a listagem desses produtos e o cálculo do valor total da compra. Isso proporcionará aos clientes uma experiência mais ágil e eficiente no processo de finalização de suas compras.

Para viabilizar essa solução, atribuímos uma TAG exclusiva a cada produto disponível na loja, armazenando informações detalhadas sobre cada item. A implementação desse sistema foi realizada utilizando a linguagem de programação Python na versão 3.11 e suas bibliotecas internas, incluindo threading, socket e http.server. Isso nos permitiu garantir uma implementação eficiente e confiável do sistema.

Além disso, optamos por desenvolver e testar o produto por meio de containers Docker. Utilizamos um protocolo baseado em uma API REST, que foi verificado e testado com a ajuda do software Postman. Para garantir a comunicação eficaz, nossa implementação foi construída sobre a arquitetura de rede baseada na Internet (TCP/IP). Esse conjunto de escolhas tecnológicas e ferramentas nos permitiu criar um sistema sólido e eficiente para atender às necessidades da loja.


# 2. Metodologia

Inicialmente, exploramos diversas arquiteturas de sistema antes de selecionar o modelo que melhor se adequava às nossas necessidades. O design escolhido, representado abaixo, foi o que seguimos para a implementação:

![Logo do Projeto](https://github.com/caleosilva/Redes/raw/main/ArquiteturaProjeto.png)


O sistema inicia com a comunicação entre o leitor RFID e o Caixa, e posteriormente entre o Caixa e o Controller, utilizando o mecanismo de comunicação por Sockets. Essa tecnologia possibilita a troca de dados entre processos em computadores distintos ou no mesmo computador. Através dela, as TAGs RFID lidas pelo Caixa são transmitidas para o Controller, que por sua vez realiza requisições ao Server.

É importante destacar que, por padrão, a comunicação via socket tem uma limitação no tamanho dos pacotes, permitindo apenas o envio de até 1024 bytes por vez. Essa restrição pode ser problemática quando os dados a serem transmitidos excedem esse limite. Para mitigar esse desafio, foi implementada uma função que lida com a divisão dos dados originais em segmentos de até 1024 bytes. Esses segmentos são então enviados sequencialmente, garantindo que a informação completa seja transmitida e posteriormente reconstituída com sucesso. Essa abordagem permite a transmissão eficiente de dados mais extensos, superando a limitação inerente à comunicação via socket.

Para lidar eficientemente com múltiplas requisições simultâneas ao Server, adotamos o conceito de Threads, que está intimamente ligado à programação concorrente. As Threads permitem a execução paralela de diferentes partes de um programa.

No contexto do nosso sistema, uma Thread fixa (representada em amarelo) fica encarregada de ouvir as solicitações de conexão do Caixa. Após aceitar uma solicitação, ela cria uma nova Thread dedicada (em verde) para lidar com a comunicação específica desse Caixa. Essa nova Thread é responsável por receber as solicitações, encaminhá-las ao Server e retornar as respostas ao Caixa. Esse mecanismo de Threads otimiza a capacidade de resposta do sistema e o torna eficaz em ambientes com múltiplos pontos de venda.

Em relação ao servidor (Server), adotamos a estratégia de utilizar três dicionários distintos para armazenar os dados necessários de forma organizada e eficiente.

No primeiro dicionário, mantemos informações detalhadas sobre os produtos, incluindo seus nomes, quantidades em estoque e valores. O segundo dicionário é responsável por armazenar informações relacionadas a cada caixa, como seu status de ativação, estado de bloqueio e histórico de compras. Por fim, a terceira estrutura é utilizada para rastrear os produtos que estão atualmente sendo processados em tempo real em um caixa.

Para acessar, atualizar ou adicionar informações a esses dicionários, implementamos rotas GET e POST personalizadas que oferecem várias funcionalidades.

No caso das rotas GET, existem seis possibilidades válidas, cada uma com seu propósito específico:

1. GET http://localhost:8000/id: Retorna todos os produtos disponíveis em estoque.
2. GET http://localhost:8000/id/codigoProduto: Retorna os dados de um produto específico com base em seu código.
3. GET http://localhost:8000/caixas: Fornece informações sobre todos os caixas registrados no sistema.
4. GET http://localhost:8000/caixas/codigoCaixa: Retorna os detalhes de um caixa específico com base em seu código.
5. GET http://localhost:8000/produtosCaixa: Mostra os produtos atualmente em processamento em todos os caixas em tempo real.
6. GET http://localhost:8000/produtosCaixa/codigoCaixa: Exibe os produtos que estão sendo processados em um caixa individual em tempo real.

No que diz respeito às rotas POST, existem quatro possibilidades, sendo elas:

1. POST http://localhost:8000/comprar/codigoCaixa: Finaliza a compra de um caixa em específico
2. POST http://localhost:8000/gerenciarCaixa/codigoCaixa: Altera as informações referente ao Caixa.
3. POST http://localhost:8000/adicionarProdutoCaixa/codigoCaixa: Adiciona um produto ao carrinho para ser comprado
4. POST http://localhost:8000/limparCarrinho/codigoCaixa: Limpa o carrinho de um Caixa específico

As requisições HTTP desempenham um papel fundamental no funcionamento deste sistema. As requisições GET permitem a recuperação de informações específicas, enquanto as requisições POST possibilitam a atualização ou adição de novos dados. Isso cria uma interface flexível que permite aos clientes (como caixas e o controller) interagir com o servidor de forma eficaz, executando ações como consulta de produtos, compra, gerenciamento de caixas, adição de produtos a carrinhos e limpeza de carrinhos.

Além disso, para assegurar um funcionamento estável e um controle eficaz das informações, recorreu-se aos princípios da "Zona Crítica", proporcionados pela biblioteca "threading". Por meio dessa abordagem, é possível garantir que apenas um processo tenha acesso a uma área específica em um determinado momento, o que, por sua vez, assegura que o controle de estoque e as atualizações de informações transcorram de maneira eficiente e ordenada.


