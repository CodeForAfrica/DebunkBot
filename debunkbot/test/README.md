### Running tests Locally
In order to run the tests, ensure you have your [service account keys](https://console.cloud.google.com/apis/credentials/serviceaccountkey) downloaded in json format. Save this file in the `/test` folder nameing it as `credentials.json`.
Finally perform a `make run` followed by a `make test`.

### Running tests on github actions
In order for you to run the tests on github actions, `DEBUNKBOT_TEST_GSHEET_SHEET_ID` and `GOOGLE_APPLICATION_CREDENTIALS` needs to be set on the secrets page. Also remeber to update this values incase they change.
For the `GOOGLE_APPLICATION_CREDENTIALS`, this is a base64 string of the `credentials.json` file you previously created. To update this value, perform the following action `base64 credentials.json` and take the output and save it as the value of `GOOGLE_APPLICATION_CREDENTIALS`.
