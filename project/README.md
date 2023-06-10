## Python的詞法分析器lexer
本程式參考學習至[实现简易的C语言编译器](https://www.jianshu.com/p/6a6379c03d9b)
裡面有加上一些我自己的註解和修改部分

### 前言
當初在訂主題的時候因為發現有些程式在windows上面執行的時候會出狀況，所以就想說那看能不能用python的方式寫一個C語言的編譯器，但因為我還在初學階段，所以期中的部分只能先做出一些簡單的功能

### 程式碼
```python
""" 創建一個用於詞法分析的標記token """
class Token:
    # 設定它的標記種類(type)跟標記值(value)以及標記位置(pos)
    # pos的位置式可選擇的
    def __init__(self, type, value, pos=None):
        # 將傳入的類型和數值賦予token
        self.type = type
        self.value = value
# 代数运算符
PLUS    = 'PLUS'      # 加號
MINUS   = 'MINUS'     # 減號
MUL     = 'MUL'       # 乘號

# 作用域符号
LPAREN  = 'LPAREN'    # 左括號
RPAREN  = 'RPAREN'    # 右括號
BEGIN   = 'BEGIN'     # 開始
END     = 'END'       # 结束

# 符号
ID      = 'ID'        # 標示符
SEMI    = 'SEMI'      # 分號
EOF     = 'EOF'       # 文件结束標誌

# 保留关键字
INT     = 'INT'       # 整数類型
RETURN  = 'RETURN'    # 返回關键字


""" 創建一個詞法分析器Lexer"""
class Lexer:
    def __init__(self, text):
        self.text = text  # 將輸入的字串賦予text
        self.pos = 0      # 將最開始的字串位置設定為0
        self.current_char = self.text[self.pos] # 將current_char設定為text目前的pos位置
        self.line = 1 
        # Ex: int a 
        # self.text = "int a"
        # self.pos = 0
        # self.current_char = text[o] = "i"

    """移动pos指针到下一个位置。"""
    def next(self):
        self.pos += 1
        if self.pos > len(self.text) - 1: 
            self.current_char = None  # 表示文本輸入結束
        else:
            self.current_char = self.text[self.pos]
        if self.current_char == '\n':
            self.line += 1
    """下一個字符"""
    def get_next_token(self):
        while self.current_char is not None:
            # 如果當前字符是空白鍵則呼叫skip_whitespace()函數
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            # 如果當前字符是英文則呼叫identifier()函數
            if self.current_char.isalpha():
                return self.identifier()
            
            # 如果當前字符是數字則呼叫number()函數
            if self.current_char.isdigit():
                return self.number()

            """
            如果當前字符是`+`,`-`,`*`,`(`,`)`,`{`,`}`,`;`
            則呼叫Token將它替換
            """
            if self.current_char == '+':    
                self.next()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.next()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.next()
                return Token(MUL, '*')

            if self.current_char == '(':
                self.next()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.next()
                return Token(RPAREN, ')')

            if self.current_char == '{':
                self.next()
                return Token(BEGIN, '{')

            if self.current_char == '}':
                self.next()
                return Token(END, '}')

            if self.current_char == ';':
                self.next()
                return Token(SEMI, ';')
            self.next()
        # 如果current_char = None 則回傳EOF
        return Token(EOF, None)
    
    """處理當前字符為數字型態的函數"""
    def number(self):
        result = ''
        while self.current_char is not None \
                and self.current_char.isdigit():
            result += self.current_char
            self.next()

        return Token(INT, int(result), self.line) # self.line用來回傳目前的行數
    
    """處理當前字符為空白建的函數"""
    def skip_whitespace(self):
        # isspace contains '', '\n', '\t', etc.
        while self.current_char is not None \
                and self.current_char.isspace():

            self.next()

    """處理當前字符為英文型態的函數"""
    def identifier(self):
        result = ''
        # 確認當前字母是否為英文、數字或底線
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.next()
                                                                         # result.upper() 將result結果轉換成大寫，以助於更能正確的匹配關鍵字
        token = RESERVED_KEYWORDS.get(result.upper(), Token(ID, result)) # Token(ID, result) 這段是當R ESERVED_KEYWORDS.get 沒有找到對應的值，則返回Token(ID, result)
        return token
    
RESERVED_KEYWORDS = {
    'INT': Token('INT', 'int'),
    'RETURN': Token('RETURN', 'return'),
}
```
### 執行方式
1. 可以直接寫在text內容裡面
```python
text = """
#include "sum.h"

int main() {
  int t = sum(10);
  printf("sum(10)=%d\n", t);
}
"""

lexer = Lexer(text)
token = lexer.get_next_token()
index = 0
print(text)
while token.type != 'EOF': # 不能使用 Token.EOF 會找不到
    print(f"{index}:{token.value}")
    token = lexer.get_next_token()
    index += 1
```
```
輸出結果:
#include "sum.h"

int main() {
  int t = sum(10);
  printf("sum(10)=%d
", t);
}

0:include
1:sum
2:h
3:int
4:main
5:(
6:)
7:{
8:int
9:t
10:sum
11:(
12:10
13:)
14:;
15:printf
16:(
17:sum
18:(
19:10
20:)
21:d
22:t
23:)
24:;
25:}
```
2. 也可以用呼叫的方式讀取檔案
```python
filename = "hello.c"

with open(filename, "r") as file:
    code = file.read()

lexer = Lexer(code)
token = lexer.get_next_token()
index = 0 
print(code)
while token.type != 'EOF':
    print(f'{index}:{token.value}')
    token = lexer.get_next_token()
    index += 1
```
```
輸出結果:
#include <stdio.h>

int fibonacci(int i) {
    if (i <= 1) {
        return 1;
    }
    return fibonacci(i-1) + fibonacci(i-2);
}

int main()
{
    int i;
    i = 0;
    while (i <= 10) {
        printf("fibonacci(%2d) = %d\n", i, fibonacci(i));
        i = i + 1;
    }
    return 0;
}

0:include
1:stdio
2:h
3:int
4:fibonacci
5:(
6:int
7:i
8:)
9:{
10:if
11:(
12:i
13:1
14:)
15:{
16:return
17:1
18:;
19:}
20:return
21:fibonacci
22:(
23:i
24:-
25:1
26:)
27:+
28:fibonacci
29:(
30:i
31:-
32:2
33:)
34:;
35:}
36:int
37:main
38:(
39:)
40:{
41:int
42:i
43:;
44:i
45:0
46:;
47:while
48:(
49:i
50:10
51:)
52:{
53:printf
54:(
55:fibonacci
56:(
57:2
58:d
59:)
60:d
61:n
62:i
63:fibonacci
64:(
65:i
66:)
67:)
68:;
69:i
70:i
71:+
72:1
73:;
74:}
75:return
76:0
77:;
78:}
```
### 結語
```python!
當初在執行上面的程式時，其實一直有出現錯誤
不是程式碼停不下來不然就是顯示錯誤
type object 'Token' has no attribute 'EOF'
其中我還發現一個隱藏錯誤在self.line那邊。
-
解決方式:
1.type object 'Token' has no attribute 'EOF'
其實這個問題我處理的最久
因為在Token那邊我明明就有設定EOF的type
但卻一直顯示錯誤，試過很多方式之後才發現要用'EOF'的方式去呼叫他

2. 程式碼停不下來
這個大概是第二久的
原本以為是因為Token 'EOF'那邊的問題
但仔細去看錯誤訊息後發現程式碼試一直停留在get_next_token()
仔細去看之後才發現是這邊出了問題
  if self.current_char == ';':
    self.next()
    return Token(SEMI, ';')
  self.next() --> 原本沒有加，導致程式一直困在while的永久迴圈
# 如果current_char = None 則回傳EOF
return Token(EOF, None)

3. self.line
這個就比較容易解決了，因為當初在設計的時候並沒有設訂self.line的初始值以及他後續的增加方式，所以在number函式return Token(INT, int(result), self.line)的時候就有可能出現問題
```
