#!/usr/bin/env python3
import requests

class Translate(object):
    def google_translate(self, msg, source_lang="en", target_lang="ja"):
        URL="https://script.google.com/macros/s/AKfycbweJFfBqKUs5gGNnkV2xwTZtZPptI6ebEhcCU2_JvOmHwM2TCk/exec?text=" + msg + "&source="+ source_lang + "&target=" + target_lang
        res = requests.get(URL)
        return res.text


if __name__ == "__main__":
    MSG="There are many kends of flowers in the garden."
    SOURCE_LANG="en"
    TARGET_LANG="ja"
    trans = Translate()
    ret = trans.google_translate(MSG, SOURCE_LANG, TARGET_LANG)
    print(ret)

