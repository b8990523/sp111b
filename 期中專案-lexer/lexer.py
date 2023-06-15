import os
import re
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
DIVIDE  = 'DIVIDE'    # 除號
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
CHAR    = 'CHAR'  

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
            
            if self.current_char == '/':
                self.next()
                return Token(DIVIDE, '/')

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

if __name__ == '__main__':
    head = """
    :::這是佳儀的期中作業
    :::基於Python語法的C語言詞法分析器-lexer
    :::能力不足所以期中只能先做這樣:) 
    """
    print(head)
    filename = input("请输入要编译的.c文件:")
    with open(filename, "r") as file:
        code = file.read()
    lexer = Lexer(code)
    token = lexer.get_next_token()
    index = 0 
    print("========原始代碼========")
    print(code)
    print("========Lexer========")
    while token.type != 'EOF':
        print(f'{index}:{token.value}')
        token = lexer.get_next_token()
        index += 1