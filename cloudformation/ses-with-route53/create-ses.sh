#!/usr/bin/env bash

domain="ys-dev-web"

echo "start"

#aws ses verify-domain-identity \
#  --domain ${domain} \
#  --region us-west-2

#{
#    "VerificationToken": "xxxxxxxxxxxxxxxxxx"
#}

aws ses get-identity-verification-attributes \
  --identities ${domain} \
  --query 'VerificationAttributes.*.VerificationStatus' \
  --region us-west-2 \
  --output text

aws ses get-identity-verification-attributes \
  --identities ${domain} \
  --region us-west-2 \
  --output json