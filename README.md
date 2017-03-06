# db_API



* документация к API


##FAQ
1. Если создаваемый объект\связь уже существует?
  - Ответ этим уже созданным объектом для всех сущностей, кроме юзера. В случае юзера вернуть ошибку (см. п. 4 и 2)

2. Что такое code в ответах на запросы?
  - Код возврата: 
    * 0 — ОК, 
    * 1 — запрашиваемый объект не найден,
    * 2 — невалидный запрос (например, не парсится json),
    * 3 — некорректный запрос (семантически),
    * 4 — неизвестная ошибка.
    * 5 — такой юзер уже существует

3. Юзер может несколько раз голосовать за один и тот же пост или тред?
  - Да
4. Ответ в случае ошибки?
  - {"code": *code*, "response": *error message*}
5. Удаление треда\поста? 
  - Сущность помечается, как isDeleted. Для поста помечается только он сам, для треда - все его внутренности. При этом удаленные сущности не учитываются при подсчете, например, количества постов в треде, но передаются в теле ответа.
6. Уникален ли username?
  - Нет, уникален email
7. Уникален ли name у Forum?
  - да, как и shortname
8. Что такое related user у Forums.details?
  - Показать полную информацию о создателе форума (вместо просто его email-а)
9. Что за типы сортировок для постов ['flat', 'tree', 'parent_tree']?
  - Есть три вида сортировок с пагинацией, они оказываются очень интересными:
    * по дате (flat), комментарии выводятся простым списком по дате,
    * древовидный (tree), комментарии выводятся отсортированные в дереве по N штук,
    * древовидные с пагинацией по родительским (parent_tree), на странице N родительских комментов и все комментарии прикрепленные к ним, в древвидном отображение,

  У всех вариантов есть asc и desc сортировки.
  
10. Как запускать тесты локально?
  - python func_test.py --address=127.0.0.1:5000 .  Другие опции смотри по ключу -h 
11. Как провести нагрузочное тестирование локально?
  - python perf_test.py  -l --address=127.0.0.1:5000 заполнит вашу базу согласно опциям из конфига (см. test.conf) и создаст файлик me_httperf_scenario. Его нужно подавать на вход httperf так: httperf --hog --client=0/1 --server=127.0.0.1 --port=5000 --uri=/ --send-buffer=4096 --recv-buffer=16384  --add-header='Content-Type:application/json\n' --wsesslog=100,0.000,me_httperf_scenario . Запускать на 5 минут, смотреть на Reply rate -> avg 

#API Documentation

##Общие
* [clear](./doc/clear.md)
* [status](./doc/status.md)

##Forum
* [create](./doc/forum/create.md)
* [details](./doc/forum/details.md)
* [listPosts](./doc/forum/listPosts.md)
* [listThreads](./doc/forum/listThreads.md)
* [listUsers](./doc/forum/listUsers.md)

##Post
* [create](./doc/post/create.md)
* [details](./doc/post/details.md)
* [list](./doc/post/list.md)
* [remove](./doc/post/remove.md)
* [restore](./doc/post/restore.md)
* [update](./doc/post/update.md)
* [vote](./doc/post/vote.md)

##User
* [create](./doc/user/create.md)
* [details](./doc/user/details.md)
* [follow](./doc/user/follow.md)
* [listFollowers](./doc/user/listFollowers.md)
* [listFollowing](./doc/user/listFollowing.md)
* [listPosts](./doc/user/listPosts.md)
* [unfollow](./doc/user/unfollow.md)
* [updateProfile](./doc/user/updateProfile.md)

##Thread
* [close](./doc/thread/close.md)
* [create](./doc/thread/create.md)
* [details](./doc/thread/details.md)
* [list](./doc/thread/list.md)
* [listPosts](./doc/thread/listPosts.md)
* [open](./doc/thread/open.md)
* [remove](./doc/thread/remove.md)
* [restore](./doc/thread/restore.md)
* [subscribe](./doc/thread/subscribe.md)
* [unsubscribe](./doc/thread/unsubscribe.md)
* [update](./doc/thread/update.md)
* [vote](./doc/thread/vote.md)
