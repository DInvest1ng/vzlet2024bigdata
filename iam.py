import time
import jwt
import json

with open('<JSON-файл_c_ключами>', 'r') as f: 
  obj = f.read() 
  obj = json.loads(obj)
  private_key = obj['private_key']
  key_id = obj['id']
  service_account_id = obj['service_account_id']

now = int(time.time())
payload = {
        'aud': 'https://iam.api.cloud.yandex.net/iam/v1/tokens',
        'iss': service_account_id,
        'iat': now,
        'exp': now + 3600
      }

encoded_token = jwt.encode(
    payload,
    private_key,
    algorithm='PS256',
    headers={'kid': key_id}
  )

with open('jwt_token.txt', 'w') as j:
   j.write(encoded_token) 

print(encoded_token)