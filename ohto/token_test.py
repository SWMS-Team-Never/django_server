import requests
#INFO: jwt를 최초 획득하려면 username,password를 POST 메서드로 /accounts/token/ 으로 실어 보내면 된다.
JWT_TOKEN = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY3NzkwNDA1LCJpYXQiOjE2Njc3NzUzNDQsImp0aSI6ImFmODQ0ZDA0YTI4MTRhMjliMzc5NTYwNjJjNmQzYzY1IiwidXNlcl9pZCI6Mn0.2jo8fqCgmILMy-o4XBqqFp5rtZWnj1gpM2QT_6inBmc"
)
REFRESH_TOKEN=(
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY2Nzg2MTc0NCwiaWF0IjoxNjY3Nzc1MzQ0LCJqdGkiOiI4MzJjMzNjMzQ2ZTQ0YWQ4OThkOTlkZGNlNWE1Yjg3MSIsInVzZXJfaWQiOjJ9.Y8AKb96eZpTXfcBFJHBhnaeprlCptWL54Rm9e9q4azk"
)
headers={
    "Authorization": f"Bearer {JWT_TOKEN}"
}

#INFO: jwt 얻고 난 후에는 jwt를 header에 담아 인증한다.    
res = requests.put("http://localhost:8000/accounts/mypage/",headers=headers,data={"phone_number":"010-2768-8876"})
print(res.json())
#INFO: jwt만료 되고나면 refresh token을 /accounts/token/refresh/ 로 data에 담아 넘겨 갱신한다.
      #logout시 storage에서 token날린다.