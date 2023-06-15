from lexer import Token,Lexer
class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
    """next用法的感覺"""
    def eat(self, token_type):
        # 確認當前的 token 是否符合預期的 token_type，若符合則繼續取得下一個 token
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            # 如果不符合則返回錯誤訊息
            raise Exception()
        
    def parse(self):
        node = self.additive_expression()
        return node
    
    def to_string(self, node):
        if isinstance(node, Num):
            return str(node.value)
        elif isinstance(node, BinOp):
          return f"({self.to_string(node.left)} {str(node.op)} {self.to_string(node.right)})"
        elif isinstance(node, BinOp):
            return f"({self.to_string(node.left)} {node.op} {self.to_string(node.right)})"
        elif isinstance(node, Negative):
            return f"-({self.to_string(node.expr)})"
        else:
            raise Exception(f'Invalid syntax tree node: {type(node).__name__}')

    """
    加法表達示
    additive_expression : multiple_expression
                    | additive_expression + multiple_expression
                    | additive_expression - multiple_expression
    """
    def additive_expression(self):
      node = self.multiple_expression()

      while self.current_token.type in ('PLUS', 'MINUS'):
          token = self.current_token
          if token.type == 'PLUS':
              self.eat('PLUS')
          elif token.type == 'MINUS':
              self.eat('MINUS')

          node = BinOp(left=node, op=token.value, right=self.multiple_expression())

      return node
    """
    乘法表達示
    multiple_expression : unary_expression 
                    | multiple_expression * unary_expression 
                    | multiple_expression / unary_expression
    """
    def multiple_expression(self):
        node = self.unary_expression()

        while self.current_token.type in ('MUL', 'DIVIDE'):
            token = self.current_token
            self.eat(token.type)

            # 構建二元操作的節點，包括左操作數、操作符和右操作數
            right_node = self.unary_expression()
            node = BinOp(left=node, op=token.value, right=right_node)

        return node
    """
    一元表達示:
    unary_expression : primary_expression 
                | + unary_expression  
                | - unary_expression  
    """
    def unary_expression(self):
        token = self.current_token
        if token.type == 'PLUS': 
            self.eat(token.type) # 消除'+'號
            node = self.unary_expression()
        elif token.type == 'MINUS': 
            self.eat(token.type) # 消除'-'號
            node = Negative(self.unary_expression())
        else:
            node = self.primary_expression()

        return node
    """
    基礎表達示:
    primary_expression : ( additive_expression ) 
                        | CHAR 
                        | INT  
                        | ID   
    """
    def primary_expression(self):
        token = self.current_token
        if token.type in ('INT', 'CHAR', 'ID'):
            self.eat(token.type)
            return Num(token.value)
        elif token.type == 'LPAREN':
            self.eat('LPAREN')
            node = self.additive_expression()
            self.eat('RPAREN')
            return node
        else:
            return None
class BinOp(): # 二元運算，例如加法、減法、乘法、除法等
    def __init__(self, left, op, right):
        self.left = left # 左操作數
        self.op = op # 運算符
        self.right = right # 右操作數

class Num(object): # 數字常量
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return self.__str__()

class Negative(): # 取負運算，即對一個表達式取負值
    def __init__(self, expr):
        self.expr = expr #代表要取負的表達式

    def __str__(self): # 將表達式以字串形式表示出來
        return f"-({self.expr})"

    def __repr__(self): # 將表達式以字串形式表示出來
        return self.__str__()

"""
使用這些類別可以構建複雜的算術運算表達式
例如 BinOp(Num(5), '+', BinOp(Num(3), '*', Num(2))) 可以表示為 5 + 3 * 2。
這段程式碼主要用於建構一個表示算術運算表達式的數據結構
方便對表達式進行操作和處理。
"""

if __name__ == '__main__':
    head = """
    :::這是佳儀的期末作業
    :::基於期中的架構再加上語法分析
    :::都示一些最最最基本的功能(大概+,-,*,/這樣)
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
    print("========Parser========")
    lexer = Lexer(code)
    parser = Parser(lexer)
    ast = parser.parse()
    result = parser.to_string(ast)
    print(result) 