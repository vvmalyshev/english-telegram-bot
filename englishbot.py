from my_functions import *
import random
import re
def main():
    one = False
    # Количество угадываний, после которого слово пропадает из списка обучения.
    N = 5 
    df = pd.read_csv('dictionary.csv', encoding='cp1251', index_col=False) # Файл со словарем пользователей.
    config = pd.read_csv('config.csv', encoding='cp1251', index_col=False) # Файл с настройками пользователей.
    # Подгружаем файл с номером последнего сообщения, на которое ответил бот.
    date_old = int(date_initial()) 
    RUS = r'[^абвгдеёжзийклмнопрстуфхцчшщъыьэюя]' 
    ENG = r'[^a-z]'
    while True:
        # Получаем обновления с api telegram.
        s = get_update()
        length = len(s)
        # Если список сообщений боту за последние 24 часа пуст, то запоминаем это в логическую переменную.
        if length == 0:
            one = True
        # Ищем новое сообщение, на которое бот еще не ответил.
        for i in reversed(range(length)):
            if s[i]['update_id']==date_old or one:
                if i!=(length-1) or one:
                    # Если сообщение, на которое бот ответил бот,не является последним полученным, то обрабатываем следующее.
                    s = (lambda one: s[i+1] if not one else s[i])(one)
                    update_id = s['update_id']
                    s = s['message']
                    chat_id = s['chat']['id']
                    first_name = s['from']['first_name']
                    # Проверяем на корректность ввода.
                    try:
                        m = s['text'].lower()
                    except KeyError:
                        m = '1'
                    # Проверяем новый клиент или нет. Если да, то вносим в базу.
                    if chat_id not in config.chat_id.values:
                        config = config.append({"chat_id": chat_id, "mode": 0 }, ignore_index=True)
                    new_str = m.split()
                    # Если боту пишу не я, то я получаю копию.
                    if chat_id != MY_CHAT_ID:
                        textm = first_name + " " + ' wrote: ' + m
                        sendme(textm)
                    # Данные о пользователе.
                    config_id = config[config['chat_id'] == chat_id].to_dict('records')[0]
                    df_id = df[df['chat_id'] == chat_id]
                    # Режим добавления слова.
                    if config_id['mode'] == 'add':
                        if len(new_str)>1 and not re.search(ENG,new_str[0]) and not re.search(RUS, new_str[1]):
                            # Проверяем на дубликаты.
                            if m not in df.word.values:
                                df = df.append({'word': new_str[0], 'translate': new_str[1], 'score': 0, "chat_id": chat_id}, ignore_index=True)
                                textm = 'New word ({} : {}) has added'.format(new_str[0],new_str[1])
                            else:
                                textm = 'The word has already added'
                        else:
                            textm = 'Something is wrong. \nPress /add for adding new word(in english) and translation(in russian).\n\nFor example:  money деньги'
                        config.loc[config['chat_id'] == chat_id, ['mode']] = 'default'
                    # Режим обучения.
                    elif config_id['mode'] == 'study':
                        last_w = config_id['last_w']
                        lang_w = config_id['lang_w']
                        # Определяем правильный ответ и отвечаем пользователю.
                        r_answ = list(df_id.loc[(df['word'] == last_w) | (df['translate'] == last_w)].iloc[:,(lambda lang_w: 1 if lang_w == 0 else 0)(lang_w)])[0]
                        if new_str[0] == r_answ:
                            textm = "You are right"
                            config.loc[config['chat_id'] == chat_id, ['mode']] = 'default'
                            # Увеличиваем скор на 1.
                            df.loc[(df['chat_id'] == chat_id) & ((df['word'] == last_w) | (df['translate'] == last_w)), ['score']] += 1
                        elif m == 'no':
                            textm = 'the right answer: ' + r_answ
                            config.loc[config['chat_id'] == chat_id, ['mode']] = 'default'
                        else:
                            textm = 'try it one more time. If you do not know, press: no'
                    # Режим удаления.
                    elif config_id['mode'] == 'delete':
                        if m in df_id.word.values:
                            df = df.drop(df[df['word'] == m].index)
                            textm = 'The word ( {} ) has deleted from your dictionary'.format(m)
                        else:
                            textm = 'The word does not exist in your dictionary'
                        config.loc[config['chat_id'] == chat_id, ['mode']] = 'default'
                    # Режим без обучения.
                    else:
                        if m == "/study":
                            df_study = (df_id[df['score'] < N])
                            if chat_id in df.chat_id.values and len(df_study)!=0:
                                # Выбираем рандомное слово.
                                df_study = df[(df['score'] < N) & (df['chat_id'] == chat_id)].sample(n=1)
                                # Выбираем рандомно англ или рус.
                                indx = random.randint(0, 1)
                                word = list((lambda indx: df_study['word'] if indx == 0 else df_study['translate'])(indx))[0]
                                textm = 'translate this {}'.format(word)
                                # Включаем режим обучения и запоминаем слово и язык.
                                config.loc[config['chat_id'] == chat_id, ['mode']] = 'study'
                                config.loc[config['chat_id'] == chat_id, ['last_w']] = word
                                config.loc[config['chat_id'] == chat_id, ['lang_w']] = indx
                            else:
                                textm = "You have no words in your dictionary. Type /add for adding new words."
                        # Добавляем новое слово
                        elif m == "/add":
                            textm = 'Type new word(in english) and translation(in russian).\n\nFor example:  money деньги'
                            config.loc[config['chat_id'] == chat_id, ['mode']] = 'add'
                        # Удаляем слово
                        elif m == "/delete":
                            if len(df[df['chat_id'] == chat_id])!=0:
                                textm = 'Type word(in english) what you wanna delete'
                                config.loc[config['chat_id'] == chat_id, ['mode']] = 'delete'
                            else:
                                textm = 'You have no words in your dictionary. Type /add for adding new words.'
                        # Показываем словарь пользователя
                        elif m == "/mydictionary":
                            if len(df[df['chat_id'] == chat_id])!=0:
                                textm = 'Your dictionary: \n\n'
                                dff = df.loc[df.chat_id == chat_id,['word','translate']]
                                for index, row in dff.iterrows():
                                    textm = textm + row['word'] + '  ' + row['translate'] + '\n'
                            else:
                                textm = 'You have no words in your dictionary. Type /add for adding new words.'
                        # Если введено что-то, что не вписывается в сценарий, то отправляем инструкцию
                        else:
                            textm = 'Press:\n\n/study for traning \n/add for adding new word \n/delete for deleting word \n/mydictionary for seeing your dictionary'
                    # Отправляем ответ пользователю получившийся после прохождения алгоритма.
                    sendm(chat_id, textm)
                    # Вносим изменения в словарь пользователя и конфигурацию.
                    config.to_csv('config.csv', encoding='cp1251', index=False)
                    df.to_csv('dictionary.csv', encoding='cp1251', index=False)
                    # Записываем в файл номер последнего сообщения, на которое ответил бот.
                    with open('last_update_id.txt', 'w') as f:
                        f.write(str(update_id))
                    date_old = update_id
                    one = False
                break
        time.sleep(1)
if __name__ == "__main__":
    main()