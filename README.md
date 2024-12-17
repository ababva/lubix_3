# Задание №3
Разработать инструмент командной строки для учебного конфигурационного
языка, синтаксис которого приведен далее. Этот инструмент преобразует текст из
входного формата в выходной. Синтаксические ошибки выявляются с выдачей
сообщений.
Входной текст на учебном конфигурационном языке принимается из
файла, путь к которому задан ключом командной строки. Выходной текст на
языке xml попадает в стандартный вывод.
Однострочные комментарии:
// Это однострочный комментарий
Словари:
([
 имя : значение,
 имя : значение,
 имя : значение,
 ...
])
Имена:
[_a-z]+
Значения:
• Числа.
• Словари.
Объявление константы на этапе трансляции:
имя: значение
Вычисление константного выражения на этапе трансляции (инфиксная
форма), пример:
?(имя + 1)
6
Результатом вычисления константного выражения является значение.
Для константных вычислений определены операции и функции:
1. Сложение.
2. Вычитание.
3. Умножение.
4. Деление.
5. pow().
Все конструкции учебного конфигурационного языка (с учетом их
возможной вложенности) должны быть покрыты тестами. Необходимо показать 3
примера описания конфигураций из разных предметных областей.
# Установка
```git clone https://github.com/ababva/lubix_3```
# Запуск 
## Запуск программы
```python main.py```
Запускается изначальный файл, который создан на основе выданного задания.
![image](https://github.com/user-attachments/assets/74f788cf-6633-429f-b791-1bb83952bf8a)

## Запуск программы
```python tests.py```
# Тесты
## Парсинг одиночной константы
```
def test_parse_constant(self):
        """Test parsing a single constant."""
        line = "a: 5"
        result = parse_row(line)
        self.assertIsInstance(result, Variable)
        self.assertEqual(result.name, "a")
        self.assertEqual(result.value.value, 5)
        self.assertEqual(result.type, Token.CONST)
```
## Парсинг словаря
```
    def test_parse_dictionary(self):
        """Test parsing a dictionary."""
        line = "my_dict: ([ a: 1, b: 2 ])"
        result = parse_row(line)
        self.assertIsInstance(result, Variable)
        self.assertEqual(result.name, "my_dict")
        self.assertEqual(result.type, Token.DICT)
        self.assertEqual(len(result.value.l), 2)

        # Validate items in the dictionary
        self.assertEqual(result.value.l[0].name, "a")
        self.assertEqual(result.value.l[0].value.value, 1)
        self.assertEqual(result.value.l[1].name, "b")
        self.assertEqual(result.value.l[1].value.value, 2)
```
## Пробное выражение
```
    def test_substitute(self):
        """Test variable substitution in expressions."""
        global stack
        stack = [
            Variable("x", Const(10), Token.CONST),
            Variable("y", Const(5), Token.CONST),
        ]
        line = "x + y"
        substituted_line = substitute(line, stack)
        self.assertEqual(substituted_line, "10 + 5")
```
## Генерации вывода .xml файла
```
    def test_process_output(self):
        """Test XML output generation."""
        const_var = Variable("a", Const(5), Token.CONST)
        dict_var = Variable("my_dict", Dictionary([
            Variable("b", Const(10), Token.CONST),
            Variable("c", Const(20), Token.CONST)
        ]), Token.DICT)

        xml_output = ""
        xml_output = process(xml_output, "output.xml", const_var)
        xml_output = process(xml_output, "output.xml", dict_var)

        expected_output = (
            '<var name="a">5</var>\n'
            '<dict name="my_dict">\n'
            '    <var name="b">10</var>\n'
            '    <var name="c">20</var>\n'
            '</dict>\n'
        )
        self.assertEqual(xml_output.strip(), expected_output.strip())
```
## Загрузка файла
```
@patch("builtins.open", new_callable=mock_open, read_data="a: 5\nb: 10\n")
    def test_load_file(self, mock_file):
        """Test loading a file."""
        lines = load_file("test.txt")
        self.assertEqual(lines, ["a: 5\n", "b: 10\n"])
        mock_file.assert_called_with("test.txt", "r")
```
## Сохранение файла
```
@patch("builtins.open", new_callable=mock_open)
    def test_save_file(self, mock_file):
        """Test saving a file."""
        data = "<var name='a'>5</var>\n"
        save_file("output.xml", data)
        mock_file.assert_called_with("output.xml", "w")
        mock_file().write.assert_called_with(data)
```
# Результат тестов
![image](https://github.com/user-attachments/assets/1c754243-9753-472a-96ac-0209a7ce1b6e)

