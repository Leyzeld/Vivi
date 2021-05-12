# Проект для конкурса "IT-Перспектива 2021"

## Vivi - голосовой помощник.

<b>Тема проекта:</b> создание десктопного голосового помощника для пользователя.

<b>Цель проекта:</b> облегчение использования современных технологий с помощью голоса.

<b>Технологии использумые в проекте:</b> голосовой помощник написан на языке Python и используем множество различных библиотек и различные API, такие как VK, Google, OpenWeatherMap. Vosk и Google SpeechRecognition используются для распознования и синтеза речи.

Мы проанализировали уже существующие варианты голосовых помощников, такие как Алиса, Google Assistant, Alexa, Cortana. И сделали вывод:
1. Алиса работает в браузере и не имеет возможности совершать какие-либо действия на компьютере
2. У Google Assistant нет версии для компьютера.
3. Alexa, как Cortana не поддерживает русский язык.

Поэтому мы решили сделать голосового помощника, который будет работать на компьютере и поддерживать русский язык

Голосовой помощник поддерживает такие функции, как:

1. Сказать погоду, время
2. Отправить сообщение в социальной сети
3. Совершить поиск в Google
4. Открыть видео на YouTube
5. Рассказать о своих возможностях
6. Подбросить монетку
7. Открыть свои настройки

### Установка

<b>Примечание:</b> для корректной работы проекта должен быть установлен Python версии 3.9, и к компьютеру должен быть подключен микрофон.

1. Для установки проекта, во-первых, нужно установить необходимые библиотеки:
- pyaudio
- scipy
- fuzzywuzzy
- speech_recognition
- numpy
- wave
- weatherreport
- webbrowser
- pyttsx3
- vosk
- wifi
- pyautogui
- pygame

Для установки библиотек следует использовать команду:

<code>pip install <имя-библиотеки> </code>

2. Далее нужно скачать проект с github с помощью команды:

<code>git clone <ссылка на этот репозиторий></code>

3. Перейти в папку с проектом

4. Затем с помощью команды <code>python3 vivi.py</code> запустить проект.

Об успешной установке проекта вам сообщит голосовой помощник.



