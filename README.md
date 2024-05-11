# Suporte ERP com Transcrição de Áudio

Este projeto fornece uma solução automatizada para ajudar equipes de suporte de sistemas ERP através da transcrição automática de áudios enviados pelos usuários. Utilizando a Gemini AI, o sistema transcreve áudios recebidos e fornece um breve resumo e análise de sentimentos sobre os comentários dos usuários.

## Como Funciona

O sistema integra um endpoint que recebe links para arquivos de áudio e retorna a transcrição textual do áudio, junto com um resumo do conteúdo e uma análise de sentimentos. Esse processo auxilia na rápida compreensão das questões relatadas pelos usuários, permitindo que a equipe de suporte atue de forma mais eficaz e informada.

### Exemplo de Requisição

O endpoint espera receber uma requisição JSON no seguinte formato:

```json
{
  "fileUrl": "https://nfedovale1.s3-us-west-2.amazonaws.com/crm/7/ogg663ccf6bb5a8c.ogg",
  "idTicket": "123",
  "idMensagem": "12345"
}
```
### Resposta Esperada

Após o processamento, o endpoint retorna uma resposta JSON que inclui a transcrição do áudio, a análise de sentimentos, e informações adicionais:

```json
{
  "audioToText": "Por causa do meu, eu não tinha o relatório não batia com o físico, sempre eu tinha que ir lá e resolver esse negócio lá no inventário, entendeu? Então era por isso que estava acontecendo. Agora o que que eu vou fazer? Eu vou tirar um relatório inteirinho, vou conferir tudo de novo, vou arrumar tudo de novo, meu estoque, aí daqui para frente não vai ter mais como eu, é, não vou conseguir fazer mais inventário, quer dizer, o inventário não vai existir mais, entendeu? Aí acho que vai, agora vai dar certo, mas qualquer coisa eu volto a te ligar, bom? Muito obrigada, viu?",
  "emotionAudio": "## Comentário Geral e Sentimento do Usuário\n\nO áudio descreve a frustração de uma usuária com o sistema ERP, especificamente com divergências entre o relatório de estoque e o estoque físico. Ela relata ter que constantemente corrigir as informações no sistema, o que sugere um problema recorrente e trabalhoso.\n\nPara solucionar o problema, ela decidiu realizar uma revisão completa do estoque, conferindo e atualizando as informações no sistema. A expectativa é que, após essa revisão, o problema seja resolvido e ela não precise mais realizar ajustes manuais no inventário.\n\n## Sentimento\n\nO sentimento predominante no áudio é de **frustração** e **exaustão**. A usuária demonstra estar cansada de ter que lidar com esse problema recorrente no sistema. Apesar disso, também há um tom de **esperança** e **otimismo** em relação à solução que ela encontrou, acreditando que a revisão completa do estoque resolverá o problema definitivamente.",
  "idMessage": "12345",
  "idTicket": "123",
  "status": 200
}
```

### Requisitos
+ Python 3.8 ou superior.
+ Bibliotecas: Flask, Requests, outras dependências listadas no requirements.txt.
