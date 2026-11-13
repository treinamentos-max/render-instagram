# render-instagram

Serviço pequeno que recebe HTML e devolve o link público de uma imagem JPEG (para publicar no Instagram via N8N).
Apaga os arquivos automaticamente após `RETENTION_HOURS` horas (padrão 72).

Variáveis: `TOKEN` (obrigatória, senha do serviço), `PUBLIC_BASE_URL` (endereço público), `RETENTION_HOURS`.
Nenhuma senha fica neste repositório.

Observação para os modelos de arte: use tamanhos fixos em px (ex.: height:1350px), nunca vh/100%, porque a janela de captura é maior que a arte e depois é recortada.
