<!-- metadados do objeto -->
| Metadata | Value   |
| -------- | ------- |
| object   | content |
| id       |         |

# Visualizando dados da depuração

Enquanto estamos usando o _debugger_, o VSCode nos apresenta algumas janelas extras na lateral esquerda que serão muito úteis na investigação de nossos bugs:

<iframe src="https://player.vimeo.com/video/515406420" width="640" height="360" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe>

- `VARIABLES` (variáveis)
- `CALL STACK` (pilha de chamadas)
- `WATCH` (inspeção)
- `BREAKPOINTS` (pontos de parada)

Além disso também será possível utilizar o `DEBUG CONSOLE` que veremos em breve!

## Janela `VARIABLES` (variáveis)

Nessa janela poderemos ver todas as variáveis e seus valores no contexto atual da aplicação.

No nosso exemplo, não vemos nenhum valor inicialmente pois o breakpoint está na função `main()` e, no momento do breakpoint, nenhuma variável foi criada ainda.
<!-- metadados do objeto -->

Assim que decidimos executar a linha atual (com `F10` ou `F11`), a variável `input_list` aparecerá na janela `VARIABLES` com seu valor: `[1, 2, 3, 4, 5]`. Ela fica dentro de `Locals` pois é uma variável do escopo da função atual.

Dentro de `Globals` não há nada aparente porque não criamos nenhuma variável no escopo global, mas se expandirmos `function variables` poderemos ver as funções que declaramos (e importamos) no nosso arquivo e seus respectivos metadados como `__name__`, `__doc__` e `__annotations__`.

Para ver mais detalhes sobre a variável, clique no símbolo de `>` à esquerda do nome. Como estamos olhando para uma lista do Python, é mostrado o valor armazenado em cada índice e também seu tamanho (representado em `len()`). Incrível, né?! 🤩

Dentro de `special variables` ficam os métodos e atributos "mágicos" (_magic methods_ ou _dunder methods_) daquele objeto, como `__str__`, `__class__` e `__contains__`.

Dentro de `function variables`, veremos os métodos padrões daquele objeto, como `append`, `remove` e `count`.

![VSCode debug: janela de variáveis](/certificacoes/eletiva-python/secao-01_debug-com-python/dia-1_estrategias-de-debug-com-python/conteudo/licao-03_visualizando-dados-da-depuracao/img/vscode-debug-variables.png)

## Janela `CALL STACK` (pilha de chamadas)

Aqui podemos ver, no ponto da execução do debug, qual é a **pilha de chamadas** da nossa aplicação. Em outras palavras, essa janela mostra quais funções/métodos/módulos foram chamados para que a execução chegasse até a linha atual.

No momento atual do nosso exemplo, temos a seguinte pilha:

- `main . . . . . . . . example.py [15:1]`
- `<module> . . . . . . example.py [19:1]`

A forma de ler isso é:

> A execução começou no arquivo `example.py` no escopo global `<module>` e seguiu até a linha `19` desse arquivo. A função `main` no arquivo `example.py` foi chamada e seguiu até a linha `15` desse arquivo.

Agora, vamos observar o que acontece quando avançamos com execução avançando para a próxima chamada de função. Para isso, utilize o "_step into_" (atalho `F11`) para que o _debugger_ **entre** na função `map_factorial`.

Opa! 👀

A função `map_factorial` foi **empilhada** na nossa pilha de chamadas, e agora temos:

- `map_factorial  . . . example.py [5:1]`
- `main . . . . . . . . example.py [15:1]`
- `<module> . . . . . . example.py [19:1]`

Juntando tudo, podemos interpretar que:

> A execução começou no arquivo `example.py` no escopo global `<module>` e seguiu até a linha `19` desse arquivo. A função `main` no arquivo `example.py` foi chamada e seguiu até a linha `15` desse arquivo. **A função `map_factorial` no arquivo `example.py` foi chamada e seguiu até a linha `5` desse arquivo.**

Ah, repare que a janela `VARIABLES` também mudou! Agora já não vemos mais a variável `input_list`, e temos o valor de `numbers` (parâmetro recebido pela função `map_factorial`).

## Janela `WATCH` (inspeção)

Essa janela mostra resultados de **qualquer expressão em Python** que desejarmos "vigiar"!

Por exemplo, podemos inspecionar o resultado de `sum(result)`. Assim, para cada avanço do _debugger_ a janela `WATCH` nos mostrará a soma de todos os elementos dentro da variável `result`. Para isso, basta clicar no sinal de ➕ no cabeçalho da janela e definir as expressões que desejar (como na imagem a seguir)

![VSCode debug: janela de watch](/certificacoes/eletiva-python/secao-01_debug-com-python/dia-1_estrategias-de-debug-com-python/conteudo/licao-03_visualizando-dados-da-depuracao/img/vscode-debug-watch.png)

Repare que, para o nosso exemplo, a variável `result` ainda não foi definida então o resultado da expressão `sum(result)` é um `NameError`.

Se avançarmos na execução com "_step into_" (atalho `F11`), veremos que o valor da expressão será atualizado a medida que o conteúdo de `result` é alterado quando passamos pela linha `result.append(factorial(num))`. Os valores que veremos são: `0`, `1`, `3`, `9`, `33` e por fim `153`.

Viu que a janela `VARIABLES` foi alterando seus valores? A medida que avançamos, `result` teve seu valor preenchido e a variável `num` (_auxiliar do `for`_) foi sendo alterada a cada iteração!

Quando a função `map_factorial` retornar, `sum(result)` terá novamente um `NameError` pois a variável `result` deixa de existir no escopo da execução.
