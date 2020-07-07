import factory

from debunkbot.models import (GSheetClaimsDatabase, 
                                GoogleSheetCredentials, Claim, )


class GSheetClaimsDatabaseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GSheetClaimsDatabase
        django_get_or_create = ("key", )
    
    key = "17vwTgIhP_bmIJsSDetYlCFJo6kOO7VuUE8HBgB2-tZ4"
    worksheets = ["Debunked Claims", ]
    claim_first_appearance_column_name = "Platform URL"
    claim_url_column_names = ["Platform URL", ]
    claim_rating_column_name = "Conclusion"
    claim_description_column_name = "Claim Checked"
    claim_debunk_url_column_name = "PesaCheck URL"
    claim_db_name = "Claim Database For Integration test"
    message_templates_source_key = "17vwTgIhP_bmIJsSDetYlCFJo6kOO7VuUE8HBgB2-tZ4"
    message_templates_worksheet = "Bot Responses"
    messages_template_column = "Response Messages"


class GoogleSheetCredentialsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoogleSheetCredentials
        django_get_or_create = ("credentials", )
    
    credentials = {"type": "service_account", "auth_uri": "https://accounts.google.com/o/oauth2/auth", "client_id": "107208172094855572616", "token_uri": "https://oauth2.googleapis.com/token", "project_id": "debunkbotdev", "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCkMQ3vvaAJt1ET\nz8qTCLhcCzAzTX6xOBZFWFSNgqlvswQqiyfJzdRvi9WUAKqpQv1vVHTpoAJR2U4C\nnJ/5Xdbi03ot91HasPp6yl8XEsE7+T9aYKQRPnLEpaFJGFxYMIN7L5d7toT7vT6Y\nEwORlGd3+K3XAXaiiapEHiLSqlD4qpZgZAHhbvvlUH6TrtN85A2I4YlFSetATx+U\nIoRlr0B7xNN0pIpEylj9uCYHjx1DOoQHF0K1KJzbg3KjybOOR7Cpn3Zs7rR+I6Xq\nfgcNNLuyQ7B1AwK+78rRvwqRsdsJsWUtif0E7wKzqS5tOigxnoGc6fkcaXinF5lh\no4TCFdyHAgMBAAECggEADrRKvtLioQjtYxk6CrTxnclt7ApF2fH5IwWBsDKooSJA\nS0PiSlMupT0gR+Lo/10w4sy55uC3lHdVLyxLso9rp5PjRN6TUnYePutRj/igz/gt\nN+QG89+Xc6XJre9XX2aCcxouAzXmiIz7YBWQo9ozvscvxyn2yYbYQsVxvoZ8pE6t\nxpYKlShU0UsrkJ8wczAogxzWVobI56ppBA3OUbXO8frLC7fIpf9EK1TNDDuM41/O\npXLUqhjrpbliEb8WcUNbqFeGIbquGOrmq/rWUv7g8eKdt8YpxRXxSmMIiN8snSPM\nsaIV7q759X4g/jHS8IGBzsgQaeCZsG0vYafNHxxQkQKBgQDiOPDN0ta5j4FfRxFR\ngskpMGB37hiWsJHDZxiXRyIUib+vcPrLFThPwqToR5cj/IRH5MJh1O8fPOzWbE+e\n7wxQCnz5HqKGj48RsTMXD567+G3g2MfmhDCj7XwLBkZS9ox2KwiH6m/NnteObLpP\nsZqS60alwRaKQyl1/QKEbqAfxQKBgQC5zdmi2Hga+UDSZuR4ZkjuJdlWs+jT8J4v\n+te/8+NQWV7BkswMkqffWWzv7Q9+6jZdZzNFQqlI6zkV9wwEPcyQ8gsxyvkxCaHN\n5mxjN8n+XdsztEcvoOBoLnMhFPewOV6+KlsF7re1KCV0RABLIUarxaNKeo/ta75F\no8mwTyPj2wKBgQCRFXGinzilE1smbt61hwpaRzNnVyUf56fkSQdlZfJ+d4WfD/dY\nLYjK5ot6iQduxfFUZmsf8T9Wqm0+a4J47NjZsJBL+RDE+ecIsruQa60i4oYdsQor\nVdYYHCP0shaB+KtG0fyLppgDqH6YUjT/DWmUFh5eCcLZ847wo85sfsJk/QKBgCQ8\n/8uBCLvKDVh79Od+m47HFwKQCEL91PxqohWwDY+oPpDmfqGdINyw5kxNIg6Qw5Wo\nARnrDHVKW1HrYw6YtwM2EfTeL4fe5w3veQhI4z6XM597875YVCw9kvrKyhw2tEHG\npQYdLvtIHzXz5VLB5LSv0U8/ZD7cGroeXcHjTY6tAoGAGEzL2yjniLkU3Yx38u+T\nqwLBcjC88arf8/U3cT7OEKKpWTsarmGpTntNlR+ET6F/21BqLFnLA5GU0w1JNG02\niVKQiaFmbL4KRU/z+JKtdDXyDiHZk/K5sQPUJ4dbqSmPdUicn47IqJQdTKCcMhd8\n0HOPGC3yNCCu8MnVBHqn/gA=\n-----END PRIVATE KEY-----\n", "client_email": "bot-140@debunkbotdev.iam.gserviceaccount.com", "private_key_id": "23341e04c25eb3e510ce824d4a1e9c6f03ca24a5", "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/bot-140%40debunkbotdev.iam.gserviceaccount.com", "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs"}
