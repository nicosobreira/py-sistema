# Sistema

> Tarefa de Programação Estruturada

Criar um sistema administrativo para uma faculdade. Ele deverá **cadastrar alunos por curso**, assim como manegar as **disciplinas** de cada curso.

## Área do Aluno

- Dados pessoais
    - Únicos
        - CPF, Email, Telefone
    - Outros
        - Nome, Endereço
- Prontuário
- Código do curso

### Incluir

Incluir um novo aluno no sistema.

- Incrementar o prontuário
- Verificar se não há repetição de informações pessoais únicas, como: CPF, email, telefone, etc.

### Excluir

- Não pode diminuir o prontuário, só aumentar!

### Alterar

### Buscar

- Por **todas** os valores

## Área do Curso

- Código
- Nome
- Semestres

### Exibir

- Mostrar todos os alunos matriculados no curso

## Disciplinas

- ID
- Nome
- Carga Horária
- Código do Curso
- Semestre (validar se o curso tem a quantidade de semetres)

### Buscar

- Por semestre
- Por curso
