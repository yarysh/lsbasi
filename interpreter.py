import operator

from token import Token, INTEGER, OP, EOF


OP_FUNCS = {
    '+': operator.add,
    '-': operator.sub,
}


class Interpreter:
    def __init__(self, text):
        self.text = text.replace(' ', '')
        self.pos = 0
        self.current_token = None

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        text = self.text
        if self.pos > len(text) - 1:
            return Token(EOF, None)

        current_char = text[self.pos]
        if current_char.isdigit():
            self.pos += 1
            while self.pos < len(text) and text[self.pos].isdigit():
                current_char += text[self.pos]
                self.pos += 1
            token = Token(INTEGER, int(current_char))
            return token

        if current_char in ('+', '-'):
            token = Token(OP, current_char)
            self.pos += 1
            return token

        self.error()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        self.current_token = self.get_next_token()

        left = self.current_token
        self.eat(INTEGER)

        op = self.current_token
        self.eat(OP)

        right = self.current_token
        self.eat(INTEGER)

        func = OP_FUNCS[op.value]
        return func(left.value, right.value)
