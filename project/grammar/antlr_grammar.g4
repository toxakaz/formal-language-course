grammar antlr_grammar;

prog: stmt SEMI prog | EOF;

stmt: var EQUALS expr | PRINT LPAREN expr RPAREN;

var: (CHAR | '_') (CHAR | DIGIT | '_')*?;

val:
	STRING
	| INT
	| BOOL
	| REG
	| CFG
	| LCURLY (val (COMMA val)*)? RCURLY;

expr:
	var
	| val
	| LPAREN expr RPAREN
	| SET_STARTS LPAREN expr COMMA expr RPAREN
	| SET_FINALS LPAREN expr COMMA expr RPAREN
	| ADD_STARTS LPAREN expr COMMA expr RPAREN
	| ADD_FINALS LPAREN expr COMMA expr RPAREN
	| GET_STARTS LPAREN expr RPAREN
	| GET_FINALS LPAREN expr RPAREN
	| GET_REACHABLE LPAREN expr RPAREN
	| GET_VERTICES LPAREN expr RPAREN
	| GET_EDGES LPAREN expr RPAREN
	| GET_LABELS LPAREN expr RPAREN
	| MAP LPAREN lambda_ COMMA expr RPAREN
	| FILTER LPAREN lambda_ COMMA expr RPAREN
	| LOAD LPAREN expr RPAREN
	| NOT expr
	| expr AMPER expr
	| expr DOT expr
	| expr VLINE expr
	| expr ASTER
	| expr IN expr;

lambda_:
	LPAREN lambda_ RPAREN
	| LAMBDA var (COMMA var)*? COLON expr;

SET_STARTS: 'set_starts';
SET_FINALS: 'set_finals';
ADD_STARTS: 'add_starts';
ADD_FINALS: 'add_finals';
GET_STARTS: 'get_starts';
GET_FINALS: 'get_finals';
GET_REACHABLE: 'get_reachable';
GET_VERTICES: 'get_vertices';
GET_EDGES: 'get_edges';
GET_LABELS: 'get_labels';
MAP: 'map';
FILTER: 'filter';
LOAD: 'load';
NOT: 'not';

LAMBDA: 'lambda';

NONZERO: [1-9];
DIGIT: [0-9];
CHAR: [a-z] | [A-Z];
INT: '0' | '-'? NONZERO DIGIT*;
BOOL: 'true' | 'false';
STRING: '"' .*? '"';

REG: 'r' STRING;
CFG: 'c' STRING;

SEMI: ';';
COLON: ':';

LPAREN: '(';
RPAREN: ')';
LCURLY: '{';
RCURLY: '}';

EQUALS: '=';
COMMA: ',';
UNDER: '_';

ASTER: '*';
DOT: '.';
AMPER: '&';
VLINE: '|';
IN: 'in';

PRINT: 'print';
