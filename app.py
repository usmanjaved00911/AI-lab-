def main():
    print("Dynamic Calculator")
    print("Enter any math expression")
    print("Example: 1 + 2 * 3 - (4 / 2)")
    print("Type 'quit' to exit\n")

    while True:
        user_input = input("Enter expression: ").strip()

        if user_input.lower() == "quit":
            print("Goodbye")
            break

        if not user_input:
            continue

        try:
            result = calculate(user_input)
            print(f"Answer: {result}\n")
        except Exception as e:
            print(f"Error: {str(e)}\n")


def calculate(expr):
    expr = expr.replace(" ", "")
    tokens = tokenize(expr)
    return parse(tokens)


def tokenize(expr):
    tokens = []
    i = 0
    while i < len(expr):
        char = expr[i]
        if char.isdigit() or char == '.':
            num = ""
            while i < len(expr) and (expr[i].isdigit() or expr[i] == '.'):
                num += expr[i]
                i += 1
            tokens.append(float(num))
            i -= 1
        elif char in "+-*/()":
            tokens.append(char)
        else:
            raise ValueError(f"Invalid symbol: {char}")
        i += 1
    return tokens


def parse(tokens):
    index = [0]

    def next_token():
        if index[0] >= len(tokens):
            return None
        return tokens[index[0]]

    def consume():
        token = next_token()
        index[0] += 1
        return token

    def parse_expr():
        left = parse_term()
        while True:
            op = next_token()
            if op == '+':
                consume()
                left += parse_term()
            elif op == '-':
                consume()
                left -= parse_term()
            else:
                break
        return left

    def parse_term():
        left = parse_factor()
        while True:
            op = next_token()
            if op == '*':
                consume()
                left *= parse_factor()
            elif op == '/':
                consume()
                right = parse_factor()
                if right == 0:
                    raise ZeroDivisionError("Can't divide by zero")
                left /= right
            else:
                break
        return left

    def parse_factor():
        token = next_token()
        if isinstance(token, float):
            consume()
            return token
        if token == '(':
            consume()
            result = parse_expr()
            if next_token() != ')':
                raise ValueError("Missing )")
            consume()
            return result
        if token == '-':
            consume()
            return -parse_factor()
        raise ValueError("Invalid expression")

    return parse_expr()


main()