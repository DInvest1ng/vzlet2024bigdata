from yandex_cloud_ml_sdk import YCloudML
import urllib.request
import json
import config
import requests

def answer(file):
    with open(file, "r") as f:
        messages = json.load(f)
    prompt = f"Я прикрепил тебе json-file с последними сообщениями пожалуйста, кратко перескажи их, выжми самое важное, также используй ники который приведены в этом файлы, ты можешь не пересказывать каждое сообщение по отдельности просто сохрани суть, более приоритетными сообщениями являются те на которые отвечали другие пользователи. Также не надо делать какое-либо приветственное слово, сразу пиши пересказ\n{messages}"
    sdk = YCloudML(folder_id=config.folder_id, auth=config.auth)
    model = sdk.models.completions('yandexgpt')
    model = model.configure(temperature=0.5)
    result = model.run(prompt)
    return result.alternatives[0].text

def speach2text(voice):
    FOLDER_ID = config.folder_id
    IAM_TOKEN = config.API_TOKEN

    with open(voice, "rb") as f:
        data = f.read()

    params = "&".join([
        "topic=general",
        "folderId=%s" % FOLDER_ID,
        "lang=ru-RU"
    ])

    url = urllib.request.Request("https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?%s" % params, data=data)
    url.add_header("Authorization", "Bearer %s" % IAM_TOKEN)

    responseData = urllib.request.urlopen(url).read().decode('UTF-8')
    decodedData = json.loads(responseData)

    if decodedData.get("error_code") is None:
        print(decodedData.get("result"))

speach2text("speech.ogg")