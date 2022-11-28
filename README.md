# Photo processing Telegram Bot  
Данный бот написан на языке **Python**.  

Данный бот удаляет задний фон с присылаемых пользователем фотографий  
и присылает результат в разрешении PNG.  

Так же он распознаёт (rus&eng) текст с присылаемой пользователем фотографии  
и присылает ответ в видет текстового сообщения.  

### В создании использовались:

- Библиотека для создания бота **pyTelegramBotAPI**  
- Для удаления заднего фона с фото **rembg** созданный [Daniel Gatis](https://github.com/danielgatis)  
- Для определения текста [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)


### Для работы вам понадобится:  

- Установить библиотеку **pyTelegramBotAPI**  
> pip install pyTelegramBotAPI

- Создать бота в **Telegram** и получить секретный ключ
> @BotFather

- Создать файл **.env** в котором нужно будет прописать секретный ключ от Telegram Bota.   
**Пример:**   
> SECRET_KEY=TELEGRAM_SECRET_KEY  
