#!/bin/sh

# Decrypt the file

# --batch to prevent interactive command
# --yes to assume "yes" for questions
ls /
gpg --quiet --batch --yes --decrypt --passphrase="$CREDENTIALS_SECRET_PASSPHRASE" \
--output ./debunkbot/test/credentials.json ./debunkbot/test/credentials.json.gpg
