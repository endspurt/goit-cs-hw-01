# Токени
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f"Token({self.type}, {self.value})"

# Лексер
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def advance(self):
        # Переміщуємо позицію вперед та оновлюємо поточний символ
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Кінець вводу
        else:
            self.current_char = self.text[self.pos]

    def get_next_token(self):
        # Основний метод для отримання наступного токена
        while self.current_char is not None:
            if self.current_char.isdigit():
                return self.integer()
            if self.current_char == '+':
                self.advance()
                return Token('PLUS', '+')
            if self.current_char == '-':
                self.advance()
                return Token('MINUS', '-')
            if self.current_char == '*':
                self.advance()
                return Token('MUL', '*')
            if self.current_char == '/':
                self.advance()
                return Token('DIV', '/')
            if self.current_char == '(':
                self.advance()
                return Token('LPAREN', '(')
            if self.current_char == ')':
                self.advance()
                return Token('RPAREN', ')')
            self.advance()
        return Token('EOF', None)

    def integer(self):
        # Читаємо ціле число
        num = ''
        while self.current_char is not None and self.current_char.isdigit():
            num += self.current_char
            self.advance()
        return Token('INTEGER', int(num))

# Парсер
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type):
        # Перевіряємо тип токена і переходимо до наступного
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise Exception('Invalid Syntax')

    def factor(self):
        # Обробка чисел і виразів у дужках
        token = self.current_token
        if token.type == 'INTEGER':
            self.eat('INTEGER')
            return token.value
        elif token.type == 'LPAREN':
            self.eat('LPAREN')
            result = self.expr()
            self.eat('RPAREN')
            return result

    def term(self):
        # Обробка множення і ділення
        result = self.factor()
        while self.current_token.type in ('MUL', 'DIV'):
            token = self.current_token
            if token.type == 'MUL':
                self.eat('MUL')
                result *= self.factor()
            elif token.type == 'DIV':
                self.eat('DIV')
                result /= self.factor()
        return result

    def expr(self):
        # Обробка додавання і віднімання
        result = self.term()
        while self.current_token.type in ('PLUS', 'MINUS'):
            token = self.current_token
            if token.type == 'PLUS':
                self.eat('PLUS')
                result += self.term()
            elif token.type == 'MINUS':
                self.eat('MINUS')
                result -= self.term()
        return result

# Інтерпретатор
class Interpreter:
    def __init__(self, parser):
        self.parser = parser

    def interpret(self):
        # Основний метод для інтерпретації виразу
        return self.parser.expr()

# Тестування
lexer = Lexer("(2 + 3) * 4 / 2")
parser = Parser(lexer)
interpreter = Interpreter(parser)
result = interpreter.interpret()
print(result)  # Очікуваний результат: 10.0
