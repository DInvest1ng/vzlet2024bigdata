from yandex_cloud_ml_sdk import YCloudML

sdk = YCloudML(folder_id="b1g7gl48jc823v41is43", auth="AQVN2U0ap9ilmPWJw9dR5sYoETlO-Al3JD2b4bBT")
model = sdk.models.completions('yandexgpt')
model = model.configure(temperature=0.5)

def answer(ans):
    result = model.run(ans)
    return result.alternatives[0].text