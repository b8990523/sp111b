# Do_While

## 語法

```
do {
  // 執行動作
} while (條件);
```
###### 此語法再判斷條件是前會先執行一次程式碼，然後才開始判定條件，如果符合則回到原本的地方重複執行，一直到條件為FALSE，動作結束。

## 執行結果
```
PS C:\Users\吳佳儀\OneDrive\文件\系統程式\sp111b\課堂習題\0311\compiler> ./compiler test/dowhile.c
i = 10;
do{
  i = i + 1;
}while (i<20)
========== lex ==============
token=i
token==
token=10
token=;
token=do
token={
token=i
token==
token=i
token=+
token=1
token=;
token=}
token=while
token=(
token=i
token=<
token=20
token=)
========== dump ==============
0:i
1:=
2:10
3:;
4:do
5:{
6:i
7:=
8:i
9:+
10:1
11:;
12:}
13:while
14:(
15:i
16:<
17:20
18:)
============ parse =============
t0 = 10
i = t0
(L0)
t1 = i
t2 = 1
t3 = t1 + t2
i = t3
t4 = i
t5 = 20
t6 = t4 < t5
goto L0
if not T6 goto L1
(L1)
``` 
###### 在test檔中添加一份關於do_while語法的.c檔，驗證更改後的程式碼是否正確。

# Compiler

## 語法

```
PROG = STMTS
BLOCK = { STMTS }
STMTS = STMT*
STMT = WHILE | BLOCK | ASSIGN
WHILE = while (E) STMT
ASSIGN = id '=' E;
E = F (op E)*
F = (E) | Number | Id
```

## 執行結果

```
user@DESKTOP-96FRN6B MINGW64 /d/ccc/book/sp/code/c/02-compiler/03-compiler
$ make clean
rm -f *.o *.exe

user@DESKTOP-96FRN6B MINGW64 /d/ccc/book/sp/code/c/02-compiler/03-compiler
$ make
gcc -std=c99 -O0 lexer.c compiler.c main.c -o compiler

user@DESKTOP-96FRN6B MINGW64 /d/ccc/book/sp/code/c/02-compiler/03-compiler
$ ./compiler test/while.c
while (i<10) i = i + 1;

========== lex ==============
token=while
token=(
token=i
token=<
token=10
token=)
token=i
token==
token=i
token=+
token=1
token=;
========== dump ==============
0:while
1:(
2:i
3:<
4:10
5:)
6:i
7:=
8:i
9:+
10:1
11:;
============ parse =============
(L0)
t0 = i
t1 = 10
t2 = t0 < t1
goto L1 if T2
t3 = i
t4 = 1
t5 = t3 + t4
i = t5
goto L0
(L1)
``` 
