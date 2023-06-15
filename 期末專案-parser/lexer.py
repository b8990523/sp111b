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
DIVIDE = 'DIVIDE'

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
CHAR   = 'CHAR'
# 新增內容
TT_HASH = 'TT_HASH'   # 井字符號
DOT = 'DOT'    # .
Lbrackets = 'Lbrackets' # <
Rbrackets = 'Rbrackets' # >

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

            if self.current_char == '#':
                self.next()
                return Token(TT_HASH, '#')
            if self.current_char == '<':
                self.next()
                return Token(Lbrackets, '<')
            if self.current_char == '>':
                self.next()
                return Token(Rbrackets, '>')
            if self.current_char == '.':
                self.next()
                return Token(DOT, '.')
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
    
    """處理頭文件的函數 #include"""
    def modules(self):
      result = ''
      while self.current_char is not None and self.current_char.isalnum():
          result += self.current_char
          self.next()

      # 处理头文件指令的第一个字符，应该是'#'
      if result == 'include':
          # 解析文件名
          file_name = ''

          # 确认当前字符是否为'<'
          if self.current_char == '<':
              file_name += self.current_char
              self.next()  # 移动到下一个字符

              # 读取到'>'
              while self.current_char is not None and self.current_char != '>':
                  file_name += self.current_char
                  self.next()  # 移动到下一个字符

              # 如果读取到文件名的结尾字符'>'
              if self.current_char == '>':
                  file_name += self.current_char
                  self.next()  # 移动到下一个字符

                  # 返回文件名作为结果
                  return file_name

      # 如果未匹配到头文件指令，则继续处理下一个标记
      return self.get_next_token()

    """處理define函數"""
    def macros(self):
        result = '' 
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char  
            self.next()  # 移動到下一個字符

        if result == 'define':
            literals = self.read_lines().strip()  # 讀取字面值，並去除首尾空格
            marco_name_pattern = re.compile(r'\b\w+(?=[(\s])')  # 確認宏名是什麼
            result = re.search(marco_name_pattern, literals)  # 在程式碼中尋找有無呼叫宏名
            if result is None:
                return None  # 如果找不到宏名則返回空
            """
            什麼是宏名?                      |    marco_name_pattern 是一個正則表達式模式，用於匹配宏名的模式
            宏名其實就是define後面的那個名稱  |    * \b :匹配單詞的開始位置。
            而宏義便是宏名後面的內容          |    * \w+：匹配一個或多個字母、數字或下劃線字符。
            Ex: define macros(self)         |    * (?=[(\s])：使用正向先行斷言，以確保宏名的後面跟著括號或空白字符。
                    |宏名 | 宏名的參數及定義|         
            """
            # 獲取宏名
            macro_name = result.group(0)
            # 在剩餘的字串中獲取宏的參數
            rest_literals = literals[len(macro_name):] #將 literals字串中 macro_name 後面的字串提取出來
            if rest_literals[0] == '(':
                defns_pattern = re.compile(r'(?<=[)]).+') # 同上
                result = re.search(defns_pattern, rest_literals)
                if result is None:
                    return None
                defns = result.group(0)
            else:
                defns = rest_literals
            # 將 rest_literals 從頭到 defns 之前的部分截斷
            rest_literals = rest_literals[:len(rest_literals) - len(defns)]

            args_list = None
            if not rest_literals == '':
                args_list = self.extract_args(rest_literals)  # 提取引數列表 Ex: define ADD(a,b) (a+b)
                                                            #        (a+b) --> self.extract_args --> ['a','b']
            # 替換的標識符
            arg_str = macro_name
            if args_list is not None:
                arg_str += '\(' # 添加左括號
                for i in range(len(args_list)):
                    if i < len(args_list) - 1:
                        arg_str += '\w+,[\s]*' # 為了匹配一個或多個字母、數字或下劃線，後面跟著逗號和可能的空格字符，表示引數的名稱。
                    else:
                        arg_str += '\w+'      # 僅匹配一個或多個字母、數字或下劃線，表示最後一個引數的名稱。
                arg_str += '\)' # 添加右括號

            # 匹配文本中的宏
            macro_pattern = r'\b%s[^\w]' % arg_str # %s是一個佔位符，會被 arg_str 替換 
                                                # \b 表示單詞的邊界，用於確保匹配的是完整的單詞而不是該單詞的一部分。
                                                # [^\w] 表示匹配一個非單詞字符，用於確保宏名後面不是單詞的一部分。
            original_str = self.text[self.pos:]
            result = re.findall(macro_pattern, original_str) # 尋找original_str中是否有對應的宏呼叫
            if len(result) > 0:
                for node in result:
                    macro_defns = defns
                    node_str = node[len(macro_name) + 1:len(node) - 1]  # ADD(3,4) --> (3,4)
                    parms_list = self.extract_args(node_str) # (3,4) --> ['3','4']
                    for k in range(len(parms_list)):
                        macro_defs_parm_pattern = re.compile(r'\b%s\b' % args_list[k]) # args_list[0] -> \ba\b
                                                                                    # args_list[1] -> \bb\b
                        macro_defns = re.sub(macro_defs_parm_pattern, '%s' % parms_list[k], macro_defns) # 將a,b替換成3,4

                    replaces_str = ' {}{}'.format(macro_defns, node[-1])
                    result = re.sub(macro_pattern, replaces_str, original_str, 1)
                    # 重置文本
                    self.text = result
                    original_str = self.text
                self.pos = 0
            return self.get_next_token()  # 獲取下一個標記

    def extract_args(literal):
        literal = literal.lstrip('(')  # 去除開頭的(
        literal = literal.rstrip(')')  # 去除末尾的)
        literal = literal.replace(' ', '')  # 移除空格
        args_pattern = re.compile(r'(?<=,)?(\w+)(?=,)?')  
        args_list = re.findall(args_pattern, literal)  
        return args_list  # 返回引數列表
RESERVED_KEYWORDS = {
        'INT': Token('INT', 'int'),
        'RETURN': Token('RETURN', 'return'),
    }
