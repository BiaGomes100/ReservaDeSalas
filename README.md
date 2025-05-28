Reserva de Salas
Descrição
Este projeto é uma API feita em Flask para gerenciar reservas de salas. Com ela, é possível:

Ver quais salas estão disponíveis;

Fazer uma reserva de sala;

Editar ou cancelar uma reserva;

Cadastrar e autenticar usuários.

O objetivo é facilitar o controle e uso das salas por meio de uma aplicação simples e organizada.

Como executar com Docker
Para rodar o projeto com Docker, siga os passos:

Baixe o repositório do GitHub.

Use o Docker e Docker Compose para montar e subir a aplicação.

Após isso, a API estará disponível localmente para testes e uso.

Com Docker, não é necessário instalar nada manualmente no seu computador — tudo já vem pronto no container.

Arquitetura
O sistema usa microsserviços, ou seja, é dividido em partes menores, cada uma com uma função:

Um serviço cuida da autenticação dos usuários;

Outro serviço gerencia as salas;

E outro é responsável pelas reservas.

Isso facilita a organização e manutenção do projeto.

Integração entre os serviços
Os serviços conversam entre si por meio de requisições HTTP (REST). Por exemplo:

O usuário faz login e recebe um token;

Esse token é usado para acessar os outros serviços, como reservar uma sala;

Os dados são enviados e recebidos no formato JSON.

Essa comunicação entre serviços permite que o sistema funcione de forma integrada e segura.