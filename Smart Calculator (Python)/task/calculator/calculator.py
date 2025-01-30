# write your code here
import re


class Calculator:
    def __init__(self):
        self.set_expression("")
        self.variables = {}

    def set_expression(self, expression: str):
        self.expression = expression
        self.result = 0
        self.tokens = []
        self.operator = []
        self.postfix = []
        
    def check_for_assignment_to_variable(self) -> str:
        if len(self.postfix) < 2:
            return ""
        if self.postfix[1] == "=" and self.isvariable(self.postfix[0]):
            result = self.postfix.pop(0)
            self.postfix.pop(0)
            return result

    def calculate(self):
        assignto = ""
        self.tokenize()
        stack = []

        try:
            # check if there is an assignemend to a variable
            assignto = self.check_for_assignment_to_variable()

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
                        case "*":
                            stack.append(element1 * element2)
                        case "/":
                            stack.append(element1 / element2)
                        case "^":
                            stack.append(element1 ** element2)
                else:
                    raise ValueError("Invalid expression")

            if len(stack) > 1:
                raise ValueError("Invalid expression")
            self.result = stack.pop()

            if assignto:
                self.variables[assignto] = self.result
                self.result = None
        except ValueError as e:
            if assignto:
                raise ValueError(f"Invalid assignment")
            else:
                raise e

    def ends_with_operator(self):
        operator = {"+", "-", "/", "*", "="}
        return self.expression and self.expression[-1] in operator

    def tokenize(self) -> bool:
        if not self.expression:
            raise ValueError("Invalid expression")
        if self.ends_with_operator():
            raise ValueError("Invalid expression")
        pattern = r"([0-9]+)|([*\/^\-+]+)|(=)|([A-Za-z0-9]+)|([()])"
        split = re.findall(pattern, self.expression)
        stack = []
        for token in split:
            number, operator, assign, variable, parenthesis = token
            if number:
                if not number.isnumeric():
                    raise ValueError("Invalid expression")
                self.postfix.append(int(number))
            elif parenthesis:
                if parenthesis == "(":
                    stack.append(parenthesis)
                elif parenthesis == ")":
                    try:
                        while len(stack) > 0 and stack[-1] != "(":
                            o = stack.pop()
                            self.postfix.append(o)
                        stack.pop()
                    except Exception:
                        raise ValueError("Invalid expression")
            elif operator:
                # check if this is a weard one like +-++ or ---
                operator = self.simplify_operator(operator)
                if len(stack) == 0 or stack[-1] == "(":
                    stack.append(operator)
                elif self.is_higher_precedence(operator, stack[-1]):
                    stack.append(operator)
                else:
                    while len(stack) > 0 and not self.is_higher_precedence(operator, stack[-1]):
                        o = stack.pop()
                        self.postfix.append(o)
                    stack.append(operator)
            elif assign:
                if len(self.postfix) != 1:
                    raise ValueError("Invalid assignment")
                self.postfix.append(assign)
            elif variable:
                self.postfix.append(variable)

        while len(stack) > 0:
            self.postfix.append(stack.pop())

    def get_precedence(self, operator):
        match operator:
            case "+"|"-":
                return 1
            case "*"|"/":
                return 2
            case "^":
                return 3

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
        if len(operator) > 1:
            raise ValueError("Invalid expression")
        return operator

    def isvariable(self, token):
        if not re.search("[A-Za-z]+", token):
            return False
        if re.search("[0-9]", token):
            raise ValueError("Invalid identifier")
        return True


    def getvariable(self, token):
        if token in self.variables:
            return self.variables[token]
        else:
            raise ValueError("Unknown variable")

    def isoperator(self, token):
        if re.match("[+\-*/^]", token):
            return True
        return False


if __name__ == "__main__":
    calculator = Calculator()

    while True:
        try:
            expression = input()
            if expression.startswith("/"):
                if expression not in ["/help", "/exit"]:
                    raise ValueError("Unknown command")

            match expression:
                case "/exit":
                    break
                case "/help":
                    print("The program calculates the sum of numbers")
                case _:
                    calculator.set_expression(expression)
                    calculator.calculate()
                    if calculator.result is not None:
                        print(calculator.result)
        except ValueError as e:
            print(e)

    print("Bye!")