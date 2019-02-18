<div style="text-align:center">
    <img alt="Logo" width=256 height=256 src="docs/img/logo.svg" />
</div>

# God

Monitorador de uso de memória e tudo mais.

## Instalação

### Jeito recomendado

Faça download da [última release](releases) e instale usando o
`god-setup.exe`.

### Jeito "hipster"

Esse método requer que você tenha [Python 3.6](https://www.python.org/downloads/release/python-368/)
instalado.

Baixe o código-fonte do God e, na pasta raíz, execute:

```batchfile
pip install --upgrade -r requirements.txt
```

Depois disso o ambiente deve estar pronto. Para rodar o God, execute na pasta
raíz:

```batchfile
python .
```

Rodar isso toda vez é bem chato, mas já que você é hipster deve conseguir criar
um `.cmd` que faça isso pra você. Boa sorte.

## Modo de Uso

Uma vez tendo rodado o God com sucesso, você pode ficar meio perdido. O que fazer
com essa tela preta bonitinha aqui?

O God, além de monitorar o uso de memória do processo selecionado em _background_,
serve como interface de linha de comando para configuração. Para uma lista
completa dos comandos, digite `help` assim que o modo interativo estiver
disponível.
