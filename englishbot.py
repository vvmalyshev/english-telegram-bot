from my_functions import *
def main():
    date_old = int(date_initial()) 

    while True:
        print("1")
        s = get_update()
        print('2')
        length = len(s)
        min = time.strftime("%M")
        if min=="00":
            textm = "new hour!"

            sendme(textm)
            time.sleep(60)

        for i in reversed(range(length)):
            print(i)

            if s[i]['update_id']==date_old:

                if i!=(length-1):

                    s = s[i+1]                
                    update_id = s['update_id']
                    s = s['message']
                    chat_id = s['chat']['id']
                    first_name = s['from']['first_name']
                    m = s['text'].lower()
                    # проверяем новый клиент или нет. Если да, то вносим в базу
                    if chat_id in config.chat_id.values:
                        pass
                    else:
                        config = config.append({"chat_id": chat_id, "mode": 0}, ignore_index=True)
                    new_str = m.split()
                    # Если боту пишу не я, то я получаю копию
                    if chat_id != my_chat_id:
                        textm = first_name + " " + ' wrote: ' + m
                        sendme(textm)

                        # данные о пользователе
                    config_id = config[config['chat_id'] == chat_id]

                    # режим обучения
                    if int(config_id['mode']) == 1:
                        last_w = list(config_id['last_w'])[0]
                        lang_w = int(config_id['lang_w'])
                        # определяем правильный ответ и отвечаем пользователю
                        r_answ = list(df.loc[(df['chat_id'] == chat_id) & (
                                    (df['word'] == last_w) | (df['translate'] == last_w))].iloc[:,
                                      (lambda lang_w: 1 if lang_w == 0 else 0)(lang_w)])[0]
                        if m == r_answ:
                            textm = "You are right"
                            config.loc[config['chat_id'] == chat_id, ['mode']] = 0
                            # увеличиваем скор на 1
                            df.loc[
                                (df['chat_id'] == chat_id) & ((df['word'] == last_w) | (df['translate'] == last_w)), [
                                    'score']] += 1

                        elif m == 'no':
                            textm = 'the right answer: ' + r_answ
                            config.loc[config['chat_id'] == chat_id, ['mode']] = 0
                        else:
                            textm = 'try it one more time. If you do not know, press no'
                    # режим без обучения
                    else:
                        if m == "/study":
                            if chat_id in df.chat_id.values:
                                # выбираем рандомное слово
                                df_study = df[(df['score'] < n) & (df['chat_id'] == chat_id)].sample(n=1)
                                # Выбираем рандомно англ или рус
                                indx = random.randint(0, 1)
                                word = \
                                list((lambda indx: df_study['word'] if indx == 0 else df_study['translate'])(indx))[0]
                                textm = 'translate this {}'.format(word)
                                # включаем режим обучения и запоминаем слово и язык
                                config.loc[config['chat_id'] == chat_id, ['mode']] = 1
                                config.loc[config['chat_id'] == chat_id, ['last_w']] = word
                                config.loc[config['chat_id'] == chat_id, ['lang_w']] = indx
                            else:
                                textm = "Please, add words for traning"
                        # добавляем новое слово
                        elif new_str[0] == 'add':
                            try:
                                df = df.append(
                                    {'word': new_str[1], 'translate': new_str[2], 'score': 0, "chat_id": chat_id},
                                    ignore_index=True)
                                textm = 'new word has added'
                            except:
                                textm = 'add a new word: \nFor ex: add money деньги'
                        else:
                            textm = 'Press /study for traning \n\nOr add a new word: \nFor ex: add money деньги \n\nBot version 1.0'
                    sendm(chat_id, textm)
                    config.to_csv('config.csv', encoding='cp1251', index=False)
                    df.to_csv('dictionary.csv', encoding='cp1251', index=False)
                    with open('last_update_id.txt', 'w') as f:
                        f.write(str(update_id))
                    date_old = update_id 
                break
        time.sleep(1)
if __name__ == "__main__":
    main()
