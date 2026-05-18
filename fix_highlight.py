import re
import os

files = ['ui/sorting_tab.py', 'ui/graph_tab.py', 'ui/knapsack_tab.py']
for f in files:
    if not os.path.exists(f):
        continue
    with open(f, 'r') as file:
        content = file.read()
    # Заменяем неправильный вызов
    content = re.sub(r'cursor\.select\(QTextCursor\.document\)', 'cursor.select(QTextCursor.SelectionType.Document)', content)
    # Также заменим возможные другие варианты
    content = re.sub(r'cursor\.select\(QTextCursor\.Document\)', 'cursor.select(QTextCursor.SelectionType.Document)', content)
    # Проверим импорт, добавим если нет
    if 'from PyQt6.QtGui import QTextCursor' not in content:
        content = content.replace('from PyQt6.QtGui import', 'from PyQt6.QtGui import QTextCursor,')
    with open(f, 'w') as file:
        file.write(content)
    print(f"Fixed {f}")
