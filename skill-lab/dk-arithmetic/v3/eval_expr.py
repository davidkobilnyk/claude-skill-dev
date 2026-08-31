#!/usr/bin/env python3
"""Evaluate a normalized arithmetic expression string with exact rational
arithmetic (no float conversion, so arbitrarily long decimals stay exact).

Grammar: expr := term (('+'|'-') term)*
         term := factor (('*'|'/') factor)*
         factor := '-' factor | '(' expr ')' | NUMBER
NUMBER  := digits ('.' digits)?
"""
import sys
import re
from fractions import Fraction

TOKEN_RE = re.compile(r"\s*(?:(\d+\.\d+|\d+)|([()+\-*/]))")


def tokenize(s):
    tokens = []
    pos = 0
    while pos < len(s):
        m = TOKEN_RE.match(s, pos)
        if not m or m.end() == pos:
            if s[pos:].strip() == "":
                break
            raise ValueError(f"Unexpected character at position {pos}: {s[pos:pos+10]!r}")
        pos = m.end()
        if m.group(1) is not None:
            tokens.append(("NUM", m.group(1)))
        else:
            tokens.append(("OP", m.group(2)))
    return tokens


def decimal_str_to_fraction(s):
    if "." in s:
        int_part, frac_part = s.split(".")
        denom = 10 ** len(frac_part)
        numer = int(int_part or "0") * denom + int(frac_part)
        return Fraction(numer, denom)
    return Fraction(int(s))


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def advance(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def parse_expr(self):
        value = self.parse_term()
        while self.peek() is not None and self.peek()[0] == "OP" and self.peek()[1] in ("+", "-"):
            op = self.advance()[1]
            rhs = self.parse_term()
            value = value + rhs if op == "+" else value - rhs
        return value

    def parse_term(self):
        value = self.parse_factor()
        while self.peek() and self.peek()[0] == "OP" and self.peek()[1] in ("*", "/"):
            op = self.advance()[1]
            rhs = self.parse_factor()
            value = value * rhs if op == "*" else value / rhs
        return value

    def parse_factor(self):
        tok = self.peek()
        if tok is None:
            raise ValueError("Unexpected end of expression")
        if tok[0] == "OP" and tok[1] == "-":
            self.advance()
            return -self.parse_factor()
        if tok[0] == "OP" and tok[1] == "+":
            self.advance()
            return self.parse_factor()
        if tok[0] == "OP" and tok[1] == "(":
            self.advance()
            value = self.parse_expr()
            close = self.advance()
            if close != ("OP", ")"):
                raise ValueError("Expected closing parenthesis")
            return value
        if tok[0] == "NUM":
            self.advance()
            return decimal_str_to_fraction(tok[1])
        raise ValueError(f"Unexpected token: {tok}")


def format_fraction(frac: Fraction) -> str:
    num, den = frac.numerator, frac.denominator
    reduced_den = den
    for p in (2, 5):
        while reduced_den % p == 0:
            reduced_den //= p
    terminates = reduced_den == 1

    sign = "-" if num < 0 else ""
    num = abs(num)

    if terminates:
        scale = 1
        d = den
        while d % 2 == 0:
            d //= 2
            scale *= 5
        while d % 5 == 0:
            d //= 5
            scale *= 2
        scaled_num = num * scale
        scaled_den = den * scale
        decimal_places = len(str(scaled_den)) - 1
        s = str(scaled_num).rjust(decimal_places + 1, "0")
        if decimal_places == 0:
            return f"{sign}{s}"
        int_part = s[:-decimal_places] or "0"
        frac_part = s[-decimal_places:]
        out = f"{sign}{int_part}.{frac_part}"
        if "." in out:
            out = out.rstrip("0").rstrip(".")
        return out if out not in ("", "-") else "0"

    int_part = num // den
    rem = num % den
    digits = []
    for _ in range(6):
        rem *= 10
        digits.append(str(rem // den))
        rem = rem % den
    return f"{sign}{int_part}.{''.join(digits)}... ({num}/{den})"


def main():
    expr = sys.argv[1]
    tokens = tokenize(expr)
    parser = Parser(tokens)
    result = parser.parse_expr()
    print(format_fraction(result))


if __name__ == "__main__":
    main()
