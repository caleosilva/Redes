# 1. Introdução

Considerando o crescente interesse na automação de supermercados, impulsionado pelo avanço da tecnologia e o desenvolvimento de conceitos como IoT (Internet of Things), muitas empresas buscam implementar soluções tecnológicas para aprimorar sua eficiência operacional, reduzir custos e oferecer uma experiência de compra melhorada aos clientes.

Nesse contexto, um supermercado localizado em Feira de Santana decidiu investir em um sistema de caixa de supermercado inteligente baseado em tecnologia RFID (Radio Frequency Identification). O objetivo deste projeto é possibilitar a leitura rápida de múltiplos produtos por meio de tags RFID, permitindo a listagem desses produtos e o cálculo do valor total da compra. Isso proporcionará aos clientes uma experiência mais ágil e eficiente no processo de finalização de suas compras.

Para viabilizar essa solução, atribuímos uma TAG exclusiva a cada produto disponível na loja, armazenando informações detalhadas sobre cada item. A implementação desse sistema foi realizada utilizando a linguagem de programação Python na versão 3.11 e suas bibliotecas internas, incluindo threading, socket e http.server. Isso nos permitiu garantir uma implementação eficiente e confiável do sistema.

Além disso, optamos por desenvolver e testar o produto por meio de containers Docker. Utilizamos um protocolo baseado em uma API REST, que foi verificado e testado com a ajuda do software Postman. Para garantir a comunicação eficaz, nossa implementação foi construída sobre a arquitetura de rede baseada na Internet (TCP/IP). Esse conjunto de escolhas tecnológicas e ferramentas nos permitiu criar um sistema sólido e eficiente para atender às necessidades da loja.


# 2. Metodologia

Inicialmente, exploramos diversas arquiteturas de sistema antes de selecionar o modelo que melhor se adequava às nossas necessidades. O design escolhido, representado abaixo, foi o que seguimos para a implementação:

![Logo do Projeto](https://github.com/caleosilva/Redes/raw/main/ArquiteturaProjeto.png)


O sistema inicia com a comunicação entre o leitor RFID e o Caixa, e posteriormente entre o Caixa e o Controller, utilizando o mecanismo de comunicação por Sockets. Essa tecnologia possibilita a troca de dados entre processos em computadores distintos ou no mesmo computador. Através dela, as TAGs RFID lidas pelo Caixa são transmitidas para o Controller, que por sua vez realiza requisições ao Server.

Para lidar eficientemente com múltiplas requisições simultâneas ao Server, adotamos o conceito de Threads, que está intimamente ligado à programação concorrente. As Threads permitem a execução paralela de diferentes partes de um programa.

No contexto do nosso sistema, uma Thread fixa (representada em amarelo) fica encarregada de ouvir as solicitações de conexão do Caixa. Após aceitar uma solicitação, ela cria uma nova Thread dedicada (em verde) para lidar com a comunicação específica desse Caixa. Essa nova Thread é responsável por receber as solicitações, encaminhá-las ao Server e retornar as respostas ao Caixa. Esse mecanismo de Threads otimiza a capacidade de resposta do sistema e o torna eficaz em ambientes com múltiplos pontos de venda.
