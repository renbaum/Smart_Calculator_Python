# write your code here
import re


class Calculator:
    def __init__(self):
        self.set_expression("")

    def set_expression(self, expression: str):
        self.expression = expression
        self.result = 0
        self.tokens = []
        self.operator = []
        self.postfix = []
        

    def calculate(self):
        self.tokenize()
        stack = []
        for token in self.postfix:
            if isinstance(token, int):
                stack.append(token)
            elif self.isvariable(token):
                stack.append(self.getvariable(token))
            elif self.isoperator(token):
                element2 = stack.pop()
                element1 = 0
                if len(stack) > 0:
                    element1 = stack.pop()

                match token:
                    case "+":
                        stack.append(element1 + element2)
                    case "-":
                        stack.append(element1 - element2)

        self.result = stack.pop()


    def tokenize(self) -> bool:
        if not self.expression:
            return False
        pattern = r"([0-9]+)|([-+]+)"
        split = re.findall(pattern, self.expression)
        stack = []
        for token in split:
            number, operator = token
            if number:
                self.postfix.append(int(number))
            elif operator:
                # check if this is a weard one like +-++ or ---
                operator = self.simplify_operator(operator)

                if operator == "(":
                    stack.append(operator)
                elif operator == ")":
                    while len(stack) > 0 and stack[-1] != "(":
                        o = stack.pop()
                        self.postfix.append(o)
                    stack.pop()

                elif len(stack) == 0 or stack[-1] == "(":
                    stack.append(operator)
                elif self.is_higher_precedence(operator, stack[-1]):
                    stack.append(operator)
                else:
                    while len(stack) > 0 and not self.is_higher_precedence(operator, stack[-1]):
                        o = stack.pop()
                        self.postfix.append(o)
                    stack.append(operator)
        while len(stack) > 0:
            self.postfix.append(stack.pop())

    def get_precedence(self, operator):
        match operator:
            case "+"|"-":
                return 1
            case "*"|"/":
                return 2

    def is_higher_precedence(self, operator1, operator2):
        p1 = self.get_precedence(operator1)
        p2 = self.get_precedence(operator2)
        return p1 > p2

    def simplify_operator(self, operator):
        if len(operator) > 1:
            if re.match(r"[-+]+", operator):
                cnt = operator.count("-")
                if cnt % 2 == 0:
                    operator = "+"
                else:
                    operator = "-"
        return operator

    def isvariable(self, token):
        pass

    def getvariable(self, token):
        pass

    def isoperator(self, token):
        if re.match("[+\-*/]", token):
            return True
        return False


if __name__ == "__main__":
    calculator = Calculator()

    while True:
        expression = input()
        match expression:
            case "/exit":
                break
            case "/help":
                print("The program calculates the sum of numbers")
            case _:
                calculator.set_expression(expression)
                calculator.calculate()
                print(calculator.result)

    print("Bye!")