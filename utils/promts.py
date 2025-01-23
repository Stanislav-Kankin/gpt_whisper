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

Компания в которой работает сейлз HRlink, может слышаться как
Чарлинг, Эйчарлинк, Charling. Будь внимателен.

Возможные сотрудники со стороны HRlink:
Канкин Станислав
Мозговой Александр
Вахрушева Наталья
Лебедев Данил
"""

PROMT_3 = """
Проанализируй текст звонка и выдели ключевые моменты. Структурируй
информацию по следующим разделам:

1. Введение:
Сотрудник: Как представился (имя, компания HRlink).

Клиент: Указано ли имя клиента.

2. Основные моменты беседы:
Вопросы сотрудника: Перечисли ключевые вопросы.

Ответы клиента: Основные ответы и реакция.

Потребности/проблемы клиента: Выявлены ли, если да — кратко опиши.

3. Договоренности:
Согласованные действия: Например, отправка ТЭО, ФТ, сравнение с
конкурентами, назначение встречи, вебинара и т.д.

Следующие шаги: Были ли назначены (дата, время, формат).

4. Возражения и их отработка:
Возражения клиента: Были ли, если да — какие.

Отработка возражений: Как сотрудник их отработал.

5. Эмоциональная окраска:
Атмосфера разговора: Положительная, нейтральная, негативная.

Вовлеченность клиента: Заинтересован ли клиент в разговоре.

6. Рекомендации:
Улучшения для сотрудника: Что можно улучшить в ведении звонка.

Дальнейшие шаги: Рекомендации для повышения вовлеченности клиента.

7. Анализ звонка:
Плюсы: Что сотрудник сделал хорошо (речевые обороты, подход, аргументация).

Минусы: Что можно улучшить или что было упущено.

8. Резюме разговора:
Суть разговора: Кратко опиши, о чем шла речь.

Ключевые моменты: Основные договоренности, возражения, эмоции клиента.

Рекомендации по дальнейшему ведению: Какие шаги предпринять для продолжения
диалога.

Теплота клиента: Оцени уровень заинтересованности клиента в продукте КЭДО
(кадровый электронный документооборот).

Уточнения:

Компания: HRlink (может звучать как "Чарлинг", "Эйчарлинк", "Charling").

Возможные сотрудники HRlink: Канкин Станислав, Мозговой Александр,
Вахрушева Наталья, Лебедев Данил.
"""

PROMT_4 = """
«Представь, что ты – опытный руководитель отдела продаж с
20-летней практикой. Твоя задача – всесторонне проанализировать
телефонный разговор менеджера с клиентом, который закончился тем,
что клиент отказался от покупки.

Шаг 1. Оцени контекст и цели звонка
– Какова была цель звонка с точки зрения менеджера?
– Соответствовала ли цель звонка текущей стадии воронки продаж
(например, закрытие сделки, уточнение деталей, презентация
продукта и т.д.)?

Шаг 2. Изучи структуру разговора и навыки сейлза
– Насколько грамотно менеджер установил контакт (приветствие,
настрой на диалог)?
– Проявил ли он активное слушание, уточнял ли потребности клиента?
– Использовал ли правильные скрипты, аргументы, выгодно ли
представил продукт/услугу?
– Как менеджер реагировал на возражения, были ли применены
техники “переформулировки”, “задания вопросов” и пр.?
– Были ли чётко озвучены выгоды или ценность продукта для конкретного клиента?

Шаг 3. Определи, почему произошёл отказ
– Является ли отказ результатом недостатка информации, неверного
позиционирования, отсутствия нужных “болей” у клиента и/или их нераскрытия?
– Какие возражения или сомнения у клиента остались неотработанными?
– Были ли сигналы о том, что клиент нуждается в дополнительном времени,
материале или уточнениях?

Шаг 4. Предложи рекомендации
– Опиши, как можно улучшить скрипт и структуру разговора.
– Дай советы по техникам продажи и работе с возражениями.
– Укажи, какие конкретные вопросы менеджер мог задать, чтобы выявить
дополнительную мотивацию или сомнения клиента.

Шаг 5. Прими решение, стоит ли повторно связываться с клиентом
– На основании услышанного, есть ли реальный потенциал сделки?
– Определи условия (например, нужны дополнительные материалы, время,
особое предложение) и формат (звонок, e-mail, мессенджер)
для повторного контакта.
– Если повторный контакт не имеет смысла, обоснуй, почему.

Шаг 6. Возможные конкуренты:
Кто является конкурентом
(это может быть СБИС, ТЕНЗОР, EasyDocs, Контур, 1С, ВК,
если конкурент не упоминается, пометь как "не указано")

Формат ответа
– Проведи анализ пошагово, с разбором сильных и слабых сторон менеджера.
– Используй свой 20-летний опыт как РОП, упоминая кейсы, когда похожие
ситуации удавалось развернуть в выигрышную сторону.
– В конце сделай общий вывод, дав менеджеру конкретные рекомендации по
развитию навыков и фиксации “точек роста”.

Основная цель: понять, всё ли сделал правильно менеджер, есть ли недоработки,
а также выяснить, можно ли и нужно ли пытаться восстановить контакт и продажу.»

КЭДО - кадровый электронный документооборот
Обрати внимание на правильное понимание кто с кем говорит, как
правило сотрудники нашей компании представляются
(Здравствуйте, меня зовут (имя), я из компании HRlink).

Компания в которой работает сейлз HRlink, может слышаться как
Чарлинг, Эйчарлинк, Charling. Будь внимателен.

Возможные сотрудники со стороны HRlink:
Канкин Станислав
Мозговой Александр
Вахрушева Наталья
Лебедев Данил
"""

tokens = encoding.encode(PROMT_1)
token_count = len(tokens)

print(f"Количество токенов: {token_count}")
