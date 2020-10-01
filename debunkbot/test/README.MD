### Note
The tests use `credentials.json` to store the authentication credentials required to authenticate to google sheets. https://cloud.google.com/docs/authentication/getting-started
Incase the credentials change, create a `credentials.json` file in the current directory containing the google credentials. After this, encrypt the json file using `gpg` as described here https://docs.github.com/en/free-pro-team@latest/actions/reference/encrypted-secrets#limits-for-secrets remember to name the file as `credentials.json` in order to get `credentials.json.gpg` as the encrypted file.
