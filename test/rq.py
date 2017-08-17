import requests
import json
data={
}
r = requests.delete('http://10.100.62.223:9999/api-operation/v1/script/12/remove/')
print(r.text)