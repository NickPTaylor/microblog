import json
import requests
from flask_babel import _
from app import app


def translate(text, source_language, dest_language):
    if 'YANDEX_TRANSLATOR_KEY' not in app.config or \
            not app.config['YANDEX_TRANSLATOR_KEY']:
        return _('Error: the translation service is not configured')
    url = ('https://translate.yandex.net/api/v1.5/tr.json/translate'
           '?key={api_key}&text={text}&lang={source_language}-{dest_language}')
    r = requests.post(url.format(api_key=app.config['YANDEX_TRANSLATOR_KEY'],
                                 text=text,
                                 source_language=source_language,
                                 dest_language=dest_language))
    if r.status_code != 200:
        return _('Error: the translation service failed.')
    return json.loads(r.content.decode('utf-8-sig'))['text'][0]
