import tiktoken

# Инициализация кодировщика (проверяем сколько токенов)
encoding = tiktoken.encoding_for_model("gpt-4o")

PROMT_1 = """
Прочитай текст звонка и выдели только ту информацию, которую озвучил клиент.
Постарайся быть максимально точным и следить за правильностью данных,
особенно в таких аспектах как Сроки, ГПР и Конкуренты.

КЭДО - кадровый электронный документооборот
Обрати внимание на правильное понимание кто с кем говорит,
как правило сотрудники нашей компании
представляются (Здравствуйте, меня зовут (имя), я
из компании HRlink)

С кем общаемся:
1. Имя собеседника
2. Должность собеседника (указано, если не указано — пометь как
"не уточнили должность").
Квалификация:

1. Стадия проекта (укажи, согласован ли проект или нет,
обсуждали уже с руководстовм или нет, если не
указано — пометь как "стадию проекта не выяснили.").
2. Ответственный за проект (кто инициатор проекта,
владелец бюджета или РП, если не указанно - пометь
как "не выявили кто ответсвенный за проект").
3. ГПР - группа принятия решения
(решение принимается коллегиально или индивидуально,
если не указано — пометь как "не выявили ГПР").
4. Сроки (уточни, когда планируется выбор вендора,
внедрение или закупка, если сроки не упомянуты,
пометь как "не уточнили сроки").
5. Бюджет (указано ли, что бюджет уже выделен,
будет выделяться под проект или нужно пройти защиту
бюджета, если не указано — пометь как
"вопрос бюджета не обсуждали").

Мотивы:

1. Потребности/боли (что именно клиент хочет
решить или какие проблемы обозначены).
2. Общее количество сотрудников,
дистанционных сотрудников в компании,
начиличе филиалов (если информация
по какому либо моменту не упомянута, пометь как "не указано").
3. Учетная система (какая система используется или будет использоваться,
обычно это 1С ЗУП, но может быть другая).
4. Какие процессы нужно изменить или автоматизировать
(если не уточняются, пометь как "не указано").
5. Активный найм (есть ли информация о найме новых сотрудников,
если есть хотя бы 2-3 найма в месяц проверь предложил ли
сотруднико систему по автоматизации приёма сотрудников СтартЛинк,
отметь качество презентации и заинтересованность клиента).
6. Корпоративный портал (есть ли задача по
разработке/улучшению корпоративного портала,
это вопросы
по командировкам, единого окна обращения, профили сотрудников,
если что то из этого было в разговоре значит обсуждали корпоративный
портал и пометь что именно обсуждали,
если информацию не спарвшивали или её нет в раговоре пометь как
"этот вопрос не обсуждали в звонке").

О чем договорились:

1. Что нужно отправить для согласования
ТЭО(техникоэкономическое обоснование),
ФТ(функциональные требования),
сравнения с конкурентами (если нет — пометь как "не указано").
2. В целом кратко опиши договоренности, если они были в разгоре.
Конкуренты:

1. Кто является конкурентом
(это может быть СБИС, ТЕНЗОР, EasyDocs, Контур, 1С, ВК,
если конкурент не упоминается, пометь как "не указано").

Стоп-факторы:

1. Возражения (если были озвучены, уточни).
2. Вопросы, на которые не смогли ответить (если есть такие, укажи).

Воркшоп и Референс:

1. Нужен ли воркшоп (если нет то не пиши ничего).
2. Нужен ли референс (если нет то не пиши ничего).
3. Нужно ли организовать встречу с ИБ (если нет то не пиши ничего).

Рекомендации по улучшению:

1. Укажи 1–2 конкретных аспекта для повышения результативности звонка.

Рекомендации по следующему действию:

1. Предложи 1–2 шага для продолжения общения.

Анализ клиента:

1. Насколько клиент был заинтересован или вовлечен в
разговор (оцени степень вовлеченности).
2. Категория сделки:
   - **A**: Есть четкие сроки, бюджет, ЛПР, конкретная задача.
   - **B**: Есть сроки или бюджет, ЛПР, общая задача.
   - **C**: ЛПР, интерес, но задача не сформулирована.

В целом ведение диалога сотрудником:
1. Сотрудник задает вопросы, а не рассказывает.
2. Сотрудник отрабатывает возражения.
3. Сотрудник проверяет вовлеченность клиента.
Если что-то не спросил сотрудник, отметь это.

Общий анализ звонка сотрудника:
1. Положительные моменты ( отметь
что сотрудник сделал хорошо, какие техники или моменты
были правильные, кратко)
2. Отрицательные моменты (отметь что сотрудник сделал
не достаточно правильно или не сделал вовсе, на что
стоит обратить внимание, кратко)
"""

PROMT_2 = """
"Пожалуйста, прочитай текст звонка от сотрудника HRlink.
Звонок по проигранной сделке
Обрати внимание на:
1. Была ли выявлена и сформирована потребность.
2. Удалось ли определить психотип клиента.
3. Как была отработана работа с возражениями,
и предложи рекомендации по улучшению.
4. Общую эмоциональную окраску разговора.
5. Длительность разговора и рекомендации по его оптимизации.
6. Было ли предложено назначить встречу и как это было сделано.
7. Определи категорию клиента(
есть интерес, нет интереса,
теплый или холодный клиент) и порекомендуй дальнейшие действия,
учитывая их интерес к КЭДО.
8. Рекомендации сотруднику(Что можно было бы сделать иначе в
том звонке чтобы он прошёл более эффективно?)

КЭДО - кадровый электронный документооборот
Обрати внимание на правильное понимание кто с кем говорит,
как правило сотрудники нашей компании
представляются (Здравствуйте, меня зовут (имя), я
из компании HRlink(по русски звучит как Эйчарлинк или Чарлинк, но
писать в транскрибации нужно HRlink))
"""

PROMT_3 = """
Пожалуйста, прочитай текст звонка и выдели ключевые моменты ведения беседы и договоренностей с клиентом. Обрати внимание на следующие аспекты:

1. Введение:
   - Как сотрудник представился (Здравствуйте, меня зовут (имя),
   я из компании HRlink).
   - Как имя клиента.

2. Основные моменты беседы:
   - Какие вопросы задавал сотрудник.
   - Какие ответы давал клиент.
   - Были ли выявлены потребности или проблемы клиента.
   - Обсуждались ли сроки, бюджет, ГПР и конкуренты.

3. Договоренности:
   - Что было согласовано в ходе звонка
   (например, отправка ТЭО, ФТ, сравнения с конкурентами,
   дополнительная встреча, вебинар).
   - Были ли назначены следующие шаги или встречи.

4. Возражения и их отработка:
   - Были ли озвучены возражения со стороны клиента.
   - Как сотрудник отработал эти возражения.

5. Эмоциональная окраска разговора:
   - Общая атмосфера разговора (положительная, нейтральная, негативная).
   - Был ли клиент заинтересован или вовлечен в разговор.

6. Рекомендации:
   - Какие аспекты сотрудник мог бы улучшить для повышения эффективности
   звонка.
   - Какие шаги рекомендуется предпринять для продолжения общения с клиентом.

7. Общий анализ звонка:
   - Положительные моменты (что сотрудник сделал хорошо).
   - Отрицательные моменты (что сотрудник сделал недостаточно
   правильно или не сделал вовсе).

КЭДО - кадровый электронный документооборот
Обрати внимание на правильное понимание кто с кем говорит, как
правило сотрудники нашей компании представляются
(Здравствуйте, меня зовут (имя), я из компании HRlink).
"""

tokens = encoding.encode(PROMT_1)
token_count = len(tokens)

print(f"Количество токенов: {token_count}")
