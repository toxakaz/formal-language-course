# Язык запросов к графам

### Описание AST

```
prog = List<stmt>
stmt =
    bind of var * expr
  | print of expr
val =
    String of string
  | Int of int
  | Bool of bool
  | Reg of string
  | Cfg of string
  | Set of List<val>
expr =
    Var of var                   // переменные
  | Val of val                   // константы
  | Set_start of Set<val> * expr // задать множество стартовых состояний
  | Set_final of Set<val> * expr // задать множество финальных состояний
  | Add_start of Set<val> * expr // добавить состояния в множество стартовых
  | Add_final of Set<val> * expr // добавить состояния в множество финальных
  | Get_start of expr            // получить множество стартовых состояний
  | Get_final of expr            // получить множество финальных состояний
  | Get_reachable of expr        // получить все пары достижимых вершин
  | Get_vertices of expr         // получить все вершины
  | Get_edges of expr            // получить все рёбра
  | Get_labels of expr           // получить все метки
  | Map of lambda * expr         // классический map
  | Filter of lambda * expr      // классический filter
  | Load of path                 // загрузка графа
  | Intersect of expr * expr     // пересечение языков
  | Concat of expr * expr        // конкатенация языков
  | Union of expr * expr         // объединение языков
  | Star of expr                 // замыкание языков (звезда Клини)
lambda = Lambda of List<var> * expr
```

### Описание конкретного синтаксиса языка

```
prog ->
    stmt ';' prog
  | EOF

stmt ->
    var '=' expr
  | 'print' '(' expr ')'

var -> (CHAR | '_') (CHAR | DIGIT | '_')*

val -> STRING | INT | BOOL | REG | CFG | SET

expr ->
    var
  | val
  | '(' expr ')'
  | 'set_starts' '(' expr ',' expr ')'
  | 'set_finals' '(' expr ',' expr ')'
  | 'add_starts' '(' expr ',' expr ')'
  | 'add_finals' '(' expr ',' expr ')'
  | 'get_starts' '(' expr ')'
  | 'get_finals' '(' expr ')'
  | 'get_reachable' '(' expr ')'
  | 'get_vertices' '(' expr ')'
  | 'get_edges' '(' expr ')'
  | 'get_labels' '(' expr ')'
  | 'map' '(' lambda ',' expr ')'
  | 'filter' '(' lambda ',' expr ')'
  | 'load' '(' expr ')'
  | 'not' expr
  | expr '&' expr                       // Intersect
  | expr '.' expr                       // Concat
  | expr '|' expr                       // Union
  | expr '*'                            // Star
  | expr 'in' expr                      // Contains

lambda ->
    '(' lambda ')'
  | 'lambda' var (',' var)* ':' expr

NONZERO -> [1-9]
DIGIT -> [0-9]
CHAR -> [a-z] | [A-Z]

INT -> '0' | '-'? NONZERO DIGIT*
BOOL -> 'true' | 'false'
STRING -> '"' .* '"'

REG -> 'r' STRING
CFG -> 'c' STRING

SET -> '{' val (',' val)* '}'
```

### Пример программы

Загрузить граф bzip, установить стартовыми вершинами 1 - 5, финальными - все. Вывести результат некоторого запроса к нему.
```
g = load("bzip")
g = set_final(get_vertices(g), set_start({1, 2, 3, 5}, g))

r = r"(l . r*)*"

print(g & q)
```
