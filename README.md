# Деревья решений и ценность информации VOI 
Репозиторий содержит примеры построения деревьев решений с использованием http://silverdecisions.pl/ созданные для учебных курсов РГУ нефти и газа имени И.М.Губкина
Также есть полезные расчетные инструменты для облегчения проведения расчетов деревьев решений.

# Задачи

## Задача про КВД, ОПЗ и скин фактор

### Условие задачи
> Скважина дает 40 т/сут  (стоимость нефти 10 тыс.руб./т). 
> Скин-фактор S неизвестен. 
> Стоимость идеального ГДИС - КВД  1 млн.руб. 
> Стоимость ОПЗ  1 млн. руб.  Снижает скин в 2 раза. Эффект длится 1 год.
> Априорная информация 
> * S = 14  вероятность 50%
> * S = 7 вероятность 20%
> * S = 0 вероятность 30%
> Что делать?

### Решение

[Дерево с решением - открыть в silverdecisions.pl](http://silverdecisions.pl/SilverDecisions.html?LOAD_SD_TREE_JSON=https://raw.githubusercontent.com/khabibullinra/decision_tree_examples/main/silverdecision_examples/%D0%97%D0%B0%D0%B4%D0%B0%D1%87%D0%B0_%D0%BF%D1%80%D0%BE_%D0%9A%D0%92%D0%94_%D0%9E%D0%9F%D0%97_%D0%B8_%D1%81%D0%BA%D0%B8%D0%BD.json)


## Задача про строительство скважины
 
### Условие задачи
> У вас имеется возможность построить скважину.
> Стоимость 100 млн.
>
> Геологическая оценка региона бурения:
> * Плохие условия:  Р = 15%, V = 80 млн. 
> * Хорошие условия:  Р = 60%, V = 100 млн. 
> * Отличные условия:  Р = 25%, V = 120 млн. 
>
> V - ожидаемый доход за период оценки
> Вопрос 1. Надо ли строить скважину? 
>
> Есть возможность уточнить геологию за 10 млн руб. Оценка геологии идеальная.
> Вопрос 2. Надо ли проводить исследования для уточнения геологии? Какова стоимость совершенной информации?
>
> Иимеется статистика по успешности геологических исследований, как она повлияет на решения?

|отчет/реальность| плохо | хорошо|отлично| итог|
|---|---|---|---|---|
|"плохо"| 6 | 3 | 1|  10|
|"хорошо"| 3 | 10 | 0|  10|
|"отлично"| 1 | 2 | 4|  10|
|итог| 10 | 15 | 5|  30|
>
> в таблице в столбцах оценка геологических условий, в строках - заключение исследований по изучению геологической обстановки
> Вопрос 3. Надо ли проводить исследования для уточнения геологии если учитывать статистику успешности? Какова стоимость несовершенной информации?

### Решение
[Дерево с решением - открыть в silverdecisions.pl](http://silverdecisions.pl/SilverDecisions.html?LOAD_SD_TREE_JSON=https://raw.githubusercontent.com/khabibullinra/decision_tree_examples/main/silverdecision_examples/%D0%97%D0%B0%D0%B4%D0%B0%D1%87%D0%B0_%D0%BF%D1%80%D0%BE_%D1%81%D1%82%D1%80%D0%BE%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D1%81%D1%82%D0%B2%D0%BE_%D1%81%D0%BA%D0%B2%D0%B0%D0%B6%D0%B8%D0%BD%D1%8B_%D0%B8_%D0%B8%D1%81%D1%81%D0%BB%D0%B5%D0%B4%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F.json)

Для учета статистики исследований и обновления априорной оценки вероятности "хорошести" геологии необходимо использовать [теорему Байеса](https://ru.wikipedia.org/wiki/%D0%A2%D0%B5%D0%BE%D1%80%D0%B5%D0%BC%D0%B0_%D0%91%D0%B0%D0%B9%D0%B5%D1%81%D0%B0). 
Для проведения расчета можно использовать [пример расчета в Excel](https://github.com/khabibullinra/decision_tree_examples/raw/main/excel_utilities/%D0%A0%D0%B0%D1%81%D1%87%D0%B5%D1%82_%D1%83%D1%81%D0%BB%D0%BE%D0%B2%D0%BD%D1%8B%D1%85_%D0%B2%D0%B5%D1%80%D0%BE%D1%8F%D1%82%D0%BD%D0%BE%D1%81%D1%82%D0%B5%D0%B9_%D0%BF%D0%BE_%D1%81%D1%82%D0%B0%D1%82%D0%B8%D1%81%D1%82%D0%B8%D0%BA%D0%B5.xlsx)

![Расчет условных вероятностей по таблице статистики](/pics/excel_bayes.png)


# Расчетные модули

## Дискретизация логнормального распределения по заданным перцентялям p10, p50, p90

[Расчетный модуль Excel скачать](https://github.com/khabibullinra/decision_tree_examples/raw/main/excel_utilities/%D0%A0%D0%B0%D1%81%D1%87%D0%B5%D1%82_%D0%B4%D0%B8%D1%81%D0%BA%D1%80%D0%B5%D1%82%D0%BD%D0%BE%D0%B3%D0%BE_%D0%BB%D0%BE%D0%B3%D0%BD%D0%BE%D1%80%D0%BC%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B3%D0%BE_%D1%80%D0%B0%D1%81%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F.xlsx)

![Подбор логнормального распределения](/pics/excel1.png)

![Аппроксимация логнормального распределения дискретным](/pics/excel2.png)

Хабибуллин Ринат
2020
