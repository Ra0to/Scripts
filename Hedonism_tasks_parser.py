import codecs
import re

from bs4 import BeautifulSoup

INPUT_FILES = (
    r'S:\TEMP\Hedonism\DataExport_2021-09-14\chats\chat_07\messages.html',
    r'S:\TEMP\Hedonism\DataExport_2021-09-14\chats\chat_07\messages2.html'
)
OUTPUT_FILE = r'S:\TEMP\Hedonism\Hedonism_tasks'
ENCODING = 'utf_8_sig'

files_data = []

for file_name in INPUT_FILES:
    with codecs.open(file_name, 'r', ENCODING) as file:
        files_data += file.readlines()

html_data = ''.join(map(lambda x: x.strip(), files_data))

soup = BeautifulSoup(html_data, 'html.parser')

full_task_pattern = re.compile(r'^<div class="text">✅ (.*?)<br/><br/>Поздравляем! <br/><br/>')
task_text_pattern = re.compile(r'.*Поздравляем! Теперь у тебя \d+ 💰 и  \d+ 🍇')

elements = list(soup.find_all(class_='text'))
tasks = dict()


def prettify_task_text(task: str) -> str:
    return task_text_pattern.sub('', task)


i = 1
with codecs.open(OUTPUT_FILE, 'w', ENCODING) as output:
    for element in elements:
        string_ = str(element)
        result = full_task_pattern.search(string_)

        if result is None:
            continue

        name = result.groups('0')[0]

        if name in tasks:
            continue

        task_text = prettify_task_text(element.text)
        print(f'{i}) {name}\n{element}\n{element.text}\n{task_text}\n')
        output.write(f'{i}) {name}\n{task_text}\n\n')
        i += 1
        tasks[name] = element

print(f'Total tasks: {len(tasks)}')
