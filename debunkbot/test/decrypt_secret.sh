#!/bin/sh

# Decrypt the file
mkdir -p $PWD/secrets
# --batch to prevent interactive command
# --yes to assume "yes" for questions
gpg --quiet --batch --yes --decrypt --passphrase="$CREDENTIALS_SECRET_PASSPHRASE" \
--output $PWD/credentials.json credentials.json.gpg
