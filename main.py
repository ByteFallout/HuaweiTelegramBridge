from huawei_lte_api.Client import Client
from huawei_lte_api.AuthorizedConnection import AuthorizedConnection
from huawei_lte_api.Connection import Connection
from huawei_lte_api.Client import Client
from huawei_lte_api.AuthorizedConnection import AuthorizedConnection
from huawei_lte_api.Connection import Connection
from huawei_lte_api.api.User import User
from huawei_lte_api.enums.sms import BoxTypeEnum
import huawei_lte_api.exceptions
import urllib
import urllib.parse

import config


connection = AuthorizedConnection(
    "http://{User}:{Passwd}@{Router}/".format(User=config.username, Passwd=config.password, Router=config.router))

# This just simplifies access to separate API groups, you can use device = Device(connection) if you want
client = Client(connection)

# print(client.device.signal())  # Can be accessed without authorization
# print(client.device.information())  # Needs valid authorization, will throw exception if invalid credentials are passed in URL
sms = client.sms.get_sms_list(1, BoxTypeEnum.LOCAL_INBOX, 1, 0, 0, 1)
# print(sms)

# Skip this loop if no messages
if sms['Messages'] == None:
    # Logout
    client.user.logout()
elif int(sms['Messages']['Message']['Smstat']) == 1:
    client.user.logout()
else:

    # Skip this loop if the SMS was read

    body = ('Message date: {Date}\nMessage from: {From}\nMessage content：\n\n{Content}').format(
        Date=sms['Messages']['Message']['Date'], From=sms['Messages']['Message']['Phone'], Content=sms['Messages']['Message']['Content'])

    text = urllib.parse.quote_plus(body)
    url = "https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s" % (
        config.telegramBotToken, config.telegramDestID, text)

    httpReq = urllib.request.urlopen(url)
    httpReq.close()

    client.sms.set_read(int(sms['Messages']['Message']['Index']))

    client.user.logout()
