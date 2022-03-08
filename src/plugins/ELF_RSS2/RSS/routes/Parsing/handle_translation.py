import re
import unicodedata

import emoji
from deep_translator import GoogleTranslator

from ....config import config
from ....RSS import translation_baidu


# 翻译
async def handle_translation(content: str) -> str:
    proxies = (
        {
            "https": config.rss_proxy,
            "http": config.rss_proxy,
        }
        if config.rss_proxy
        else None
    )
    translator = GoogleTranslator(source="auto", target="zh-CN", proxies=proxies)
    try:
        text = emoji.demojize(content)
        text = re.sub(r":[A-Za-z_]*:", " ", text)
        if config.baidu_id and config.baidu_key:
            content = re.sub(r"\n", "百度翻译 ", content)
            content = unicodedata.normalize("NFC", content)
            text = emoji.demojize(content)
            text = re.sub(r":[A-Za-z_]*:", " ", text)
            text = "\n翻译(BaiduAPI)：\n" + str(
                translation_baidu.baidu_translate(re.escape(text))
            )
        else:
            text = "\n翻译：\n" + str(translator.translate(re.escape(text)))
        text = re.sub(r"\\", "", text)
        text = re.sub(r"百度翻译", "\n", text)
    except Exception as e:
        text = "\n翻译失败！" + str(e) + "\n"
    return text
