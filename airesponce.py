from yandex_cloud_ml_sdk import YCloudML
import config
import requests

def answer(ans):
    sdk = YCloudML(folder_id=config.folder_id, auth=config.auth)
    model = sdk.models.completions('yandexgpt')
    model = model.configure(temperature=0.5)
    result = model.run(ans)
    return result.alternatives[0].text