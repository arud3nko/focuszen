# FocusZen

Вашему вниманию представлен task manager "FocusZen". Проект разработан в рамках тренировочного задания.

## Общее описание

Стандартная схема работы с системой выглядит следующим образом:

- [X]  Задачи заносятся в систему (создаются, редактируются, удаляются).
- [X]  К любой задаче могут быть добавлены подзадачи.
- [X]  Удалена, может быть только терминальная задача. Удаление поддерева не требуется.
- [X]  Структура задачи и подзадачи одинакова. Подзадача не может принадлежать более чем одной задаче. Количество уровней подзадач не ограничено.
- [X]  Поля «Плановая трудоёмкость задачи» ("Planned effort") и «Фактическое время выполнения» ("Actual effort") вычисляемые и складываются из сумм подзадач, входящих в данную задачу, и самой задачи (приотображении задачи содержащей подзадачи время выполнения подзадач необходимо показывать отдельно). 

## О реализации

### Стек бэкенда: `Django` `Django Rest Framework (DRF)` `PostgreSQL` `pytest`

Выбор пал на DRF ввиду большой популярности и широкой распространенности стиля REST API, к тому же такая архитектура отлично подходит для таск-менеджера. 

Основной функционал реализован в приложении `todolist`. Пройдемся по пакетам внутри `todolist`:

- `views` - здесь можно найти ViewSet'ы и миксины. Я использовал кастомные миксины для сборки ViewSet'ов для того, чтобы правильно разделить DRF и бизнес-логику приложения. Например, в `crud.py` я переопределяю методы `perform_*` у стандартных миксинов, декорируя сохранение сериализованных данных своими методами - `executor`, которые запускают бизнес-логику из `services`. 
- - `hierarchy.py` предоставляет ViewSet для иерархии задач, это очень удобное JSON представление. Однако, в долгосрочной перспективе это будет vulnerability, так как сюда не получится прикрутить Pagination и время выполнения запроса будет расти с количеством данных. В общем, временное решение.

- `models` - здесь расположена модель `Task`, наследующаяся от `BaseModel` (предоставляет некоторые базовые атрибуты). `Task` содержит в себе только работу с данными. Как и полагается слою данных. Поле `chidlren` фильтрует все `Task` по полю `parent`. Так можно получить подзадачи, храня в БД только указатель на родителя. Если совсем докапываться, то можно обойтись вообще без `children` ^-)

- `serializers` - Сериализаторы. Опять же, никакой бизенс-логики, они занимаются сериализацией, валидацией данных. `BaseTaskSerializer` прокидывает к сериализаторам поля, содержащие вычисляемые значения, однако они не высчитываются непосредственно в сериализаторе, а возвращаются методами класса `CountSubTasksEffort`. В `TaskSerializer` также реализован валидатор на случай, если кто-то захочет установить родительской задачей саму эту задачу (так спокойно можно придти к пределу рекурсии, написал регрессионный тест на этот кейс). `NestedTaskSerializer` предоставляет иерархию задач - в него приходят только корневые задачи (`is_root` = True), и он рекурсивно сериализует подзадачи. Опять же, временное решение.

- `enums` - Енум для статусов задач

- `services` - Бизнес-логика таск-менеджера. Здесь реализованы правила, согласно которым обновляются и удаляются задачи, а также расчитываются вычисляемые значения. Здесь все сервисы реализованы в виде паттерна `Команда`, то есть имеют один метод - execute() и ничего не возвращают, но могут вызывать исключение `ServiceException`.
- - `base.py` - Предоставляет `BaseService(ABC)` - абстрактный базовый класс, от которого должны наследоваться сервисы, чтобы придерживаться задуманной архитектуре.
- - `update_status.py` - Содержит правила обновления статуса у задач. `TaskStatusUpdateService` - по шаблону `Фасад` предоставляет удобный доступ к `CompleteTaskService` и `SuspendTaskService` - к сервисам, которые непосредственно проверяют возможность изменения статуса согласно бизнес-логике приложения и обновляют дочерние задачи.
- - `delete_task.py` - `DeleteTaskService` реализует проверку на возможность удаления задачи согласно бизнес-логике.
- - `count_effort.py` - `CountSubTasksEffort` предоставляет методы для расчета вычисляемых полей.
- - `exceptions` - Кастомные исключения, налсдеющиеся от `ServiceException`

Если углубиться в отделение бизнес-логики от фреймворков (в частности Django), то в идеале нужно последовать паттерну `Репозиторий` и создать `ValueObject` для передачи данных `Task` между сервисами, абстрактный `BaseTaskDAO`, от которого унаследовать `DjangoTaskDAO` для работы непосредственно с ORM Django. Таким образом можно будет буквально вырвать пакетник с бизнес-логикой приложения и впилить его, например, в `FastAPI`, написав `FastAPITaskDAO`. 

- `tests` - автоматизированные модульные тесты на `pytest`. `pytest` - "more pythonic way" для реализации тестов, опять же, позволяет меньше зависеть от конкретного фреймворка (не наследовать TestCase, не использовать camelCase assert-ы). 
- - `conftest.py` - Здесь живут фикстуры
- - `api` - Модульные тесты для API
- - `serializers` - Модульные тесты для сериализаторов, в том числе некоторые регрессионные тесты на основе выявленных багов
- - `services` - Тесты бизнес-логики (расчетов, правил обновления/удаления и т.п.)

### Стек фронтенда: `React JS` `TypeScript`

Репозиторий фронта: https://github.com/arud3nko/focuszen-front

Я не совсем фронтеднер, но некоторый результат показать удалось. 

`TaskService` предоставляет сервис для выполнения concrete задач, работая с `TaskClient` - непосредственно клиентом REST API, который собирает запрос и передает его в `APIClient` - базовый API клиент, который выполняет запросы, обрабатывает ошибки и возвращает ответы. 

Я сделал компоненты интерфейса на `Ant Design`, вроде, получилось прикольно.

## Usage examples

![Common screen](https://i.postimg.cc/PxJS1TqX/photo-2024-07-01-03-15-21.jpg)
Общий экран

![Edit screen](https://i.postimg.cc/W4X9DhTY/photo-2024-07-01-03-23-48.jpg)
Редактирование задачи

![Erroe Message](https://i.postimg.cc/P5bVjScj/photo-2024-07-01-03-24-53.jpg)
Сообщения от API

## Installation

- Клонируем Репозиторий
```bash
git clone https://github.com/arud3nko/focuszen.git
```
- Устанавливаем зависимости в виртуальное окружение
```bash
pip install -r requirements.txt
```
- Настраиваем необходимые параметры (подключение, allowed_hosts, cors) не в .env, а в `focuszen/settings.py`
- Делаем миграции
```
python manage.py makemigrations
python manage.py makemigrations todolist
python manage.py migrate
```
- Можно запускать dev-сервер
```
python manege.py runserver
```

## Running tests
- Запуск тестов
```bash
pytest .\foocuszen\tests
```

Нужно учесть, что pytest-django требует корректно настроенного подключения к БД. Он будет создавать тестовые таблицы, а после выполнения тестов удалять их.

## Authors

- [@arud3nko](https://www.github.com/arud3nko)

