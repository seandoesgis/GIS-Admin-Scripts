import os, requests

count = 0
for root, dirs, files in os.walk('u:'):
    for file in files:    
        if file.endswith('.shp'):
            count += 1
data = {"embeds": [{"image": {"url": "http://apimeme.com/meme?meme=But-Thats-None-Of-My-Business&top="+str(count)+"+shapefiles+on+the+U+drive&bottom=but+that+none+of+my+business"}}]}
result = requests.post(url='https://discord.com/api/webhooks/842202207146344490/ucowiXCNb7-r_Mra0X0NtG_LaGO70xhhEWu4C-jx3tA2oXGn6DHoZM8Sl5pAcTqElzXE', json=data)
try:
    result.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(err)
else:
    print("Payload delivered successfully, code {}.".format(result.status_code))
