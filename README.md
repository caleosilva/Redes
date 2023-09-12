<div align="center">
  <h1>
      Relatório do problema 1: Supermercado inteligente
  </h1>

  <h3>
    Georgenes Caleo Silva Pinheiro
  </h3>

  <p>
    Engenharia de Computação – Universidade Estadual de Feira de Santana (UEFS)
    Av. Transnordestina, s/n, Novo Horizonte
    Feira de Santana – BA, Brasil – 44036-900
  </p>

  <center>caleosilva75@gmail.com</center>

</div>





# 1. Introdução

Considerando o crescente interesse na automação de supermercados, impulsionado pelo avanço da tecnologia e o desenvolvimento de conceitos como IoT (Internet of Things), muitas empresas buscam implementar soluções tecnológicas para aprimorar sua eficiência operacional, reduzir custos e oferecer uma experiência de compra melhorada aos clientes.

Nesse contexto, um supermercado localizado em Feira de Santana decidiu investir em um sistema de caixa de supermercado inteligente baseado em tecnologia RFID (Radio Frequency Identification). O objetivo deste projeto é possibilitar a leitura rápida de múltiplos produtos por meio de tags RFID, permitindo a listagem desses produtos e o cálculo do valor total da compra. Isso proporcionará aos clientes uma experiência mais ágil e eficiente no processo de finalização de suas compras.

Para viabilizar essa solução, atribuímos uma TAG exclusiva a cada produto disponível na loja, armazenando informações detalhadas sobre cada item. A implementação desse sistema foi realizada utilizando a linguagem de programação Python na versão 3.11 e suas bibliotecas internas, incluindo threading, socket e http.server. Isso nos permitiu garantir uma implementação eficiente e confiável do sistema.

Além disso, optamos por desenvolver e testar o produto por meio de containers Docker. Utilizamos um protocolo baseado em uma API REST, que foi verificado e testado com a ajuda do software Postman. Para garantir a comunicação eficaz, nossa implementação foi construída sobre a arquitetura de rede baseada na Internet (TCP/IP). Esse conjunto de escolhas tecnológicas e ferramentas nos permitiu criar um sistema sólido e eficiente para atender às necessidades da loja.


# 2. Metodologia

Inicialmente, exploramos diversas arquiteturas de sistema antes de selecionar o modelo que melhor se adequava às nossas necessidades. O design escolhido, representado abaixo, foi o que seguimos para a implementação:

![Logo do Projeto](https://github.com/caleosilva/Redes/raw/main/ArquiteturaRedes.png)


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

# 3. Resultados

Para iniciar o sistema e prepará-lo para o uso pelo usuário final, é necessário executar sequencialmente os componentes principais: Server, Controller, leitor RFID e Caixa. No ambiente do caixa, o funcionário deve identificar qual dos quatro terminais disponíveis será utilizado pelo sensor RFID. Uma vez feita a seleção, o sistema está pronto para uso.

Quanto ao fluxo de operação destinado ao cliente, ele se depara com um menu intuitivo que oferece diversas opções. Isso inclui o início de uma nova compra, onde o cliente pode escolher inserir manualmente o código do produto ou permitir que o leitor RFID faça a identificação automática. Além disso, o cliente pode visualizar os produtos já registrados junto com o valor total, finalizar a compra efetuando o pagamento ou cancelar a operação.

Para o administrador, as funcionalidades estão disponíveis através do software Postman, eliminando a necessidade de uma interface exclusiva. Usando o Postman, o administrador pode acessar informações detalhadas sobre cada caixa, incluindo o status (ativo, bloqueado) e o histórico de compras. Além disso, é possível monitorar as compras em tempo real realizadas em cada caixa e tomar ações como bloquear, desbloquear, ativar ou desativar um terminal, dependendo das necessidades operacionais.

Além disso, é importante mencionar que o sistema foi desenvolvido com grande atenção à robustez e segurança. Todos os possíveis erros e exceções são tratados de maneira adequada, garantindo a estabilidade das operações tanto para os clientes quanto para os funcionários que o utilizam. Qualquer intercorrência, como produtos sem estoque, códigos inválidos ou falhas na comunicação, é detectada e tratada de maneira apropriada, fornecendo ao usuário feedback claro e útil.

No que diz respeito ao controle de estoque, uma funcionalidade crucial do sistema, todas as compras finalizadas resultam na diminuição automática da quantidade de produtos disponíveis. Isso assegura que o estoque da loja seja atualizado em tempo real, evitando situações em que produtos fora de estoque sejam vendidos por engano. A integração perfeita entre o caixa e o controle de estoque é uma das principais vantagens deste sistema, tornando-o uma ferramenta valiosa para gerenciamento eficaz de recursos e para aprimorar a experiência do cliente.

Em resumo, o sistema não apenas oferece uma interface amigável para os clientes efetuarem compras com facilidade, mas também fornece ferramentas poderosas para os administradores monitorarem e gerenciarem eficientemente as operações em vários caixas. Com um foco especial na robustez e na segurança, o sistema se destaca pela capacidade de tratamento de erros e pela atualização automática do estoque, contribuindo para um ambiente de compras eficiente e confiável.

# 4. Conclusão

Ao concluir este projeto, obtivemos valiosas lições sobre a complexa interconexão de sistemas, explorando o funcionamento e a comunicação entre computadores distintos por meio da tecnologia de socket. A integração bem-sucedida do módulo de leitura RFID, em conjunto com as tags RFID UHF, aprimorou nossa compreensão sobre a aplicação prática dessas tecnologias emergentes.

Além disso, ampliamos nossos conhecimentos em diversas áreas de arquitetura de sistemas. Exploramos a arquitetura de Nuvem IoT centralizada, o funcionamento da rede TCP/IP e a administração de contêineres com Docker. Ao desenvolver interfaces de usuário, ganhamos experiência com a implementação de um protocolo baseado em API REST.

Destacamos que todos os requisitos propostos foram atendidos com sucesso. Na interface do caixa, os clientes podem iniciar uma compra, verificar os itens selecionados e concluir a compra efetuando o pagamento. Por sua vez, na interface de administração do supermercado, os gestores podem acessar informações detalhadas sobre os caixas, bloqueá-los ou liberá-los, consultar o histórico de compras e monitorar as transações em tempo real.

Para futuras melhorias no projeto, identificamos duas áreas principais de foco. Primeiramente, há a necessidade de implementar leitores RFID individuais para cada caixa, permitindo a leitura contínua e automática dos produtos em tempo real, sem a necessidade de solicitar a leitura a cada item. Além disso, no lado do servidor, visando escalar o sistema para atender demandas ainda maiores, consideramos a implementação de um buffer de requisições e a adoção de multi-threading para transformar o servidor em uma plataforma de alto desempenho. Essas melhorias proporcionariam uma experiência ainda mais eficaz e escalável aos usuários do sistema.

# Referências

Python threading module: Disponível em: https://docs.python.org/3/library/threading.html. Acesso em: 23 de ago. de 2023

HUNT, John; HUNT, John. Sockets in Python. Advanced Guide to Python 3 Programming, p. 457-470, 2019.

Python http.server module: Disponível em: https://docs.python.org/3/library/http.server.html. Acesso em: 29 de ago. de 2023
