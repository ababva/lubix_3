import os
import argparse
import enum
from typing import List, Dict
import re

stack = []


class Token(enum.Enum):
    CONST = 1
    DICT = 2


class Dictionary:
    def __init__(self, items: List[Dict[int, any]]):
        self.l = items


class Const:
    def __init__(self, value: any):
        self.value = value


class Variable:
    def __init__(self, name: str, value: any, type: Token):
        self.name = name
        self.value = value
        self.closed = False
        self.type = type

    def close(self):
        self.closed = True


# имя входа и выхода
def parse_args():
    parser = argparse.ArgumentParser(description='bububu')
    parser.add_argument('--input', type=str, help='input file')
    parser.add_argument('--output', type=str, help='output file')
    args = parser.parse_args()
    return args


def parse_dict_row(line):
    if '([' in line:
        line = line[line.index('(['):]
    line = line.strip('])')
    line = line.strip('([')
    line = line.strip()
    vars = [parse_row(i) for i in line.split(',')]
    return vars


def show(l):
    for i in l:
        print(i.__dict__)
        if i.type == Token.DICT:
            show(i.value.l)
        if i.type == Token.CONST:
            print(i.value.value)


def parse_row(line):
    if line == '':
        return
    line = line.strip()
    line = line.strip(',')
    assignment = re.match(r'(?<![\(\[])[_a-z]+(?=[ ]*:.*)', line)
    # получаем значение
    embed = re.match(r'(?<![\(\[])[_a-z]+[ ]*:[ ]*', line)  # проверяем есть ли присвоение
    if not embed:
        value = line
    else:
        value = line[embed.span()[1]:]
    if re.match(r'(\(\[.*\]\))|(\(\[.+)|(.+\]\))', value):
        value = Dictionary(parse_dict_row(value))  # для словаря
        if embed:
            return Variable(assignment.group(0), value, Token.DICT)
        else:
            return value
    else:
        value = Const(eval(substitute(value, stack)))  # для выражения с константой
        if embed:
            return Variable(assignment.group(0), value, Token.CONST)
        else:
            return value


def substitute(line, stack):
    print(stack)
    print(line)
    for i in range(len(stack)):
        if stack[i].type == Token.CONST:
            line = line.replace(stack[i].name, str(stack[i].value.value))
    return line


# здесь магия
def tokenize(file):
    for line in file:
        line = line.strip()
        if line == '':
            continue
        stack.append(parse_row(line))


# очевидно
def load_file(i):
    try:
        with open(i, 'r') as f:
            return f.readlines()
    except FileNotFoundError:
        print('File not found')
        exit(1)


def process(output, o, item, depth=0):
    print(item)
    if item.type == Token.CONST:
        output += '    '*depth + f'<var name="{item.name}">' + str(item.value.value) + '</var>\n'
        return output
    if item.type == Token.DICT:
        output += '    '*depth + f'<dict name="{item.name}">\n'
        for i in item.value.l:
            output = process(output, o, i, depth+1)
        output += '    '*depth + '</dict>\n'
        return output


def save_file(o, s):
    try:
        with open(o, 'w') as f:
            f.write(s)
    except Exception as e:
        print('error saving file')
        print(e)
        exit(1)


def main():
    # i, o = parse_args()
    i, o = "test1.txt", "test1-out.xml"
    file = load_file(i)
    tokenize(file)
    show(stack)
    xml = ''
    for i in stack:
        xml = process(xml, o, i)
    save_file(o, xml)


if __name__ == '__main__':
    main()
