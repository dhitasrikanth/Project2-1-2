# If you haven't read the P2 post in campuswire, read it before you continue.

# If you have working lexer of project 1, then you are good to go, you just
# need few modifications in the lexer. I believe you are better off, if you
# just extend it.

# If you don't have a working lexer for project 1, we have provide a skelton of 
# lexer. You need to complete the functions commented with tokenize.

# newline lexer.
class Token:
    def __init__(self, token_type, value=None):
        self.type = token_type
        self.value = value

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None
        if self.current_char == '\n':  # Skip over newline characters
            self.advance()

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos < len(self.text):
            return self.text[peek_pos]
        else:
            return None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    # implement
    def number(self):
        result = ''
        decimal_count = 0
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                decimal_count += 1
                if decimal_count > 1:
                    break
            result += self.current_char
            self.advance()
        if decimal_count == 0:
            return float(result), 0
        else:
            return float(result), 1

    # implement
    def identifier(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return result

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            elif self.current_char.isdigit():
                res = self.number()
                if res[1] == 1:
                    return Token('FNUMBER', res[0])
                else:
                    return Token('NUMBER', res[0])
            elif self.current_char.isalpha() or self.current_char == '_':
                return self.keyword_or_identifier()
            elif self.current_char == '+' or self.current_char == '-' or self.current_char == '*' or self.current_char == '/':
                return self.operator()
            elif self.current_char == '(' or self.current_char == ')':
                token = Token('PARENTHESIS', self.current_char)
                self.advance()
                return token
            elif self.current_char == '{' or self.current_char == '}':
                token = Token('SCOPE', self.current_char)
                self.advance()
                return token
            elif self.current_char == '\n':  # Change delimiter to newline character
                token = Token('DELIMITER', self.current_char)
                self.advance()
                return token
            elif self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token('OPERATOR', '!=')
                else:
                    self.error()

            elif self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token('OPERATOR', '==')
                else:
                    return Token('OPERATOR', '=')

            elif self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token('OPERATOR', '<=')
                else:
                    return Token('OPERATOR', '<')
            elif self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token('OPERATOR', '>=')
                else:
                    return Token('OPERATOR', '>')
            else:
                self.error()
        return Token('EOF')

    #implement
    def keyword_or_identifier(self):
        identifier = self.identifier()
        if identifier in ['if', 'else', 'while', 'for', 'break', 'continue']:
            return Token(identifier.upper())
        else:
            return Token('IDENTIFIER', identifier)

    #implement
    def operator(self):
        if self.current_char == '+':
            self.advance()
            return Token('OPERATOR', '+')
        elif self.current_char == '-':
            self.advance()
            return Token('OPERATOR', '-')
        elif self.current_char == '*':
            self.advance()
            return Token('OPERATOR', '*')
        elif self.current_char == '/':
            self.advance()
            return Token('OPERATOR', '/')
        else:
            self.error()

# Parse Tree Node definitions.
# Don't need to modify these definitions for the completion of project 2.

# But if you are interested in modifying these definitions for
# learning purposes. Then Don't whatever you want.

class Node:
    pass

class ProgramNode(Node):
    def __init__(self, statements):
        self.statements = statements

class DeclarationNode(Node):
    def __init__(self, identifier, expression, myType):
        self.identifier = identifier
        self.expression = expression
        self.type       = myType

class AssignmentNode(Node):
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

class IfStatementNode(Node):
    def __init__(self, condition, if_block, else_block):
        self.condition = condition
        self.if_block = if_block
        self.else_block = else_block

class WhileLoopNode(Node):
    def __init__(self, condition, loop_block):
        self.condition = condition
        self.loop_block = loop_block

class ConditionNode(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class ArithmeticExpressionNode(Node):
    def __init__(self, operator, left, right, myType):
        self.operator = operator
        self.left = left
        self.right = right
        self.type  = myType

class TermNode(Node):
    def __init__(self, operator, left, right, myType):
        self.operator = operator
        self.left = left
        self.right = right
        self.type  = myType

class FactorNode(Node):
    def __init__(self, value, myType):
        self.value = value
        self.type = myType




# final parser - student copy

# Skelton of Parser class.
# For project 1, we should have implemented parser that returns a string representation.
# For project 2:
  # 1. You have to build the Parse tree with the node definitions given to you. The core
  # logic of how to parse the lanague will not differ, but you to have create Tree node
  # whereever you are creating tuple in the project 1.
  # 2. Implement symbol table and scoping rules. 
  #   Hint: You can use stack to model the nested scopes and a dictionary to store identifiers
  #   and its type.

  # For those who are interested, you call print_parse_tree to view the text representation
  # of Parse Tree.


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        # implement symbol table and scopes
        self.symbol_table_stack = [{}]
        self.messages = []

    def print_parse_tree(self, node, indent=0):
        message = ""
        if isinstance(node, ProgramNode):
            message += '  ' * indent + 'Program\n'
            for statement in node.statements:
                message += self.print_parse_tree(statement, indent + 1)
        elif isinstance(node, DeclarationNode):
            message += '  ' * indent + 'Declaration: ' + node.identifier + '\n'
            message += self.print_parse_tree(node.expression, indent + 1)
        elif isinstance(node, AssignmentNode):
            message += '  ' * indent + 'Assignment: ' + node.identifier + '\n'
            message += self.print_parse_tree(node.expression, indent + 1)
        elif isinstance(node, IfStatementNode):
            message += '  ' * indent + 'If Statement\n'
            message += self.print_parse_tree(node.condition, indent + 1)
            message += '  ' * indent + 'Then Block:\n'
            for statement in node.if_block:
                message += self.print_parse_tree(statement, indent + 2)
            if node.else_block:
                message += '  ' * indent + 'Else Block:\n'
                for statement in node.else_block:
                    message += self.print_parse_tree(statement, indent + 2)
        elif isinstance(node, WhileLoopNode):
            message += '  ' * indent + 'While Loop\n'
            message += self.print_parse_tree(node.condition, indent + 1)
            message += '  ' * indent + 'Loop Block:\n'
            for statement in node.loop_block:
                message += self.print_parse_tree(statement, indent + 2)
        elif isinstance(node, ConditionNode):
            message += '  ' * indent + 'Condition : with operator ' + node.operator + '\n'
            message += '  ' * indent + 'LHS\n'
            message += self.print_parse_tree(node.left, indent + 2)
            message += '  ' * indent + 'RHS\n'
            message += self.print_parse_tree(node.right, indent + 2)
        elif isinstance(node, ArithmeticExpressionNode):
            message += '  ' * indent + 'Arithmetic Expression: ' + node.operator + '\n'
            message += self.print_parse_tree(node.left, indent + 1)
            message += self.print_parse_tree(node.right, indent + 1)
        elif isinstance(node, TermNode):
            message += '  ' * indent + 'Term: ' + node.operator + '\n'
            message += self.print_parse_tree(node.left, indent + 1)
            message += self.print_parse_tree(node.right, indent + 1)
        elif isinstance(node, FactorNode):
            message += '  ' * indent + 'Factor: ' + str(node.value) + '\n'

        return message


    def error(self, message):
        self.messages.append(message)

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f'Expected token of type {token_type}, but found {self.current_token.type}')

    # enter the new scope in the program
    def enter_scope(self, scope_prefix):
        self.symbol_table_stack.append({})

    # leave the current scope
    def leave_scope(self):
        self.symbol_table_stack.pop()

    # return the current scope
    def current_scope(self):
        pass

    def checkVarDeclared(self, identifier):

        #if #implement :
            #self.error(f'Variable {identifier} has already been declared in the current scope')

        pass

    def checkVarUse(self, identifier):
        # check var declared, so we can use it.
        self.error(f'Variable {identifier} has not been declared in the current or any enclosing scopes')

        pass

    # return false when types mismatch, otherwise ret true
    def checkTypeMatch(self, vType, eType, var, exp):
        pass
    # return its type or None if not found
    def getMyType(self, identifier):
      pass

    def parse_program(self):
        statements = []
        while self.current_token.type != 'EOF':
            statements.append(self.parse_statement())
            if self.current_token.type == 'DELIMITER':
                self.eat('DELIMITER')
        return ProgramNode(statements)


    def parse_statement(self):
        pass

    def parse_declaration(self):
        pass

    def parse_assignment(self):
        pass

    def parse_if_statement(self):
        pass

    def parse_while_loop(self):

        #return WhileLoopNode(condition, loop_block)
        pass
    # No need to check type mismatch here.
    def parse_condition(self):

        #return ConditionNode(left, operator, right)
        pass
    def parse_arithmetic_expression(self):
        pass

    def parse_term(self):
        pass

    def parse_factor(self):
        pass

def main():
    text = '''
    float x = 0.234
    int y = 0
    int z = 0
    if x > y then {
      float sum = 10.50
      int cnt   = 20
      if cnt > 0 then {
        int x = 1
        sum   = 2.0 * sum
        x     = x + 1
      }
      x = 10
      while x > 1.9 do {
        z = z + y
        x = x - 1.0
        sum = x + sum
      }
    }
    '''

    lexer = Lexer(text)

    while True:
        token = lexer.get_next_token()
        if token.type == 'EOF':
            break
        print(token.type, token.value)

if __name__ == "__main__":
    main()