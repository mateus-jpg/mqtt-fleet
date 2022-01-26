import json
baseCrtPath = "/home/mramos/Documents/certificati/awsCert"
config = {"RootCA": f"{baseCrtPath}/root-CA.crt",
          "PrivateKey": f"{baseCrtPath}/fleet-vehicle.private.key",
          "Certificate": f"{baseCrtPath}/fleet-vehicle.cert.pem",
          "host": f"avf6pqezt597s-ats.iot.eu-west-3.amazonaws.com",
          "port": "1883"}

with open('json_data.json', 'w') as outfile:
    json.dump(config, outfile)
