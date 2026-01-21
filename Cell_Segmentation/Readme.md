# Segmentação de Células em Imagens de Microscopia

Projeto de segmentação de células em imagens de microscopia sem contraste de fase utilizando uma arquitetura U-Net reduzida, combinada com Sliced Inference para lidar com forte desbalanceamento espacial dos dados.

# Visão Geral

O projeto tem como objetivo segmentar células provenientes de experimentos de microfluídica, possibilitando análises reológicas baseadas em deformação celular. Devido ao tamanho reduzido das células em relação à imagem completa, foi adotada a técnica de Sliced Inference, que permite aumentar a proporção de pixels relevantes durante o treinamento, resultando em melhorias significativas na qualidade das máscaras preditas.

# Problema

- Imagens ruidosas devido ao aumento de ganho necessário para manter altas taxas de aquisição (FPS) sob limitações de iluminação do microscópio.

- Células ocupando uma fração extremamente pequena da imagem (≈ 0,2% da área total).

- Forte desbalanceamento entre pixels de fundo e objeto, dificultando a aquisição de mascaras com alta qualidade.

# Dados

- Modalidade: Microscopia óptica sem contraste de fase

- Formatos: .png, .tif, .bmp

- Resolução original: 720 × 540 pixels

- Máscaras: Anotação manual binária utilizando o software: <a href="https://github.com/bnsreenu/digitalsreeni-image-annotator">digitalsreeni-image-annotator</a>.

# Metodologia

## Pré-processamento

- Normalização por média e desvio padrão

- Padronização de dimensões via recortes locais

## Data Augmentation

- Rotações

- Flips horizontais e verticais

- Deslocamentos em altura e largura (height/width shift)

## Arquitetura

- U-Net reduzida

- 5 níveis de encoder e decoder

- Número máximo de filtros: 512

## Função de Perda e Métrica

- Função de perda: Dice Loss

- Métrica principal: Dice Coefficient

# Resultados
## Resultados Qualitativos

O Vídeo 1 apresenta uma sequência de imagens adquiridas diretamente do experimento de microfluídica.

<p align="center"> <img src="Figs/gif_run_cell.gif" width="500"> </p> <p align="center"> <em>Vídeo 1 — Sequência temporal de imagens adquiridas diretamente do experimento.</em> </p>

A Figura 1 apresenta um frame bruto e um recorte ampliado de uma célula individual. O contorno em verde corresponde à máscara de referência (ground truth), enquanto o contorno em vermelho indica a segmentação predita pelo modelo.

<p align="center"> <img src="Figs/predic_vs_manual.png" width="500"> </p> <p align="center"> <em>Figura 1 — Frame original do experimento e zoom em uma célula individual.</em> </p>

## Desbalanceamento Espacial

No frame utilizado na Figura 1, a célula ocupa 794 pixels, enquanto a imagem completa contém 388.800 pixels, resultando em uma proporção de apenas 0,20% de área relevante. Esse cenário inviabiliza o treinamento direto em imagens completas mantendo a qualidade das mascara.

Para contornar esse problema, foi utilizada a abordagem de Sliced Inference, ilustrada na Figura 2.

<p align="center"> <img src="https://raw.githubusercontent.com/obss/sahi/main/resources/sahi-sliced-inference-overview.avif" width="500"> </p> <p align="center"> <em> Figura 2 — Pipeline do Sliced Inference: divisão da imagem em patches, inferência local e reconstrução do resultado final. Ref: <a href="https://github.com/obss/sahi">github.com/obss/sahi</a>. </em> </p>

# Construção do Dataset

Foram gerados recortes de 128 × 128 pixels, com as células centralizadas, formando os conjuntos de treino e validação. Essa escolha:

- É compatível com arquiteturas baseadas em downsampling por potências de 2

- Aumentou a proporção de pixels relevantes para aproximadamente 4,85%

- Melhorou significativamente a estabilidade do treinamento

<p align="center"> <img src="Figs/Ori_mask_train.png" width="500"> </p> <p align="center"> <em>Figura 3 — Exemplos de imagens de treino e respectivas máscaras binárias.</em> </p>

## Métricas Quantitativas

Dice médio no conjunto de validação: XX

Distribuição do Dice por imagem

Curvas de treinamento e validação

(Inserir gráficos aqui)