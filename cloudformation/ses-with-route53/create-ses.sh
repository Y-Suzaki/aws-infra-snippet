#!/usr/bin/env bash

DOMAIN="ys-dev-web.tk"
ZONE_ID="Z1FON0KVY2AAH8"

echo "*************************************"
echo "Create SES domain."
echo "*************************************"
#aws ses verify-domain-identity \
#  --domain ${DOMAIN} \
#  --region us-west-2

TOKEN=`aws ses get-identity-verification-attributes \
  --identities ${DOMAIN} \
  --query 'VerificationAttributes.*.VerificationToken' \
  --region us-west-2 \
  --output text`


echo "*************************************"
echo "Create TXT record on Route53."
echo "*************************************"
RECORD_NAME="_amazonses.${DOMAIN}"
RECORD_VALUE=${TOKEN}

cp txt-template.json txt.json
sed -i -e "s/{{RECORD_NAME}}/${RECORD_NAME}/g" txt.json
sed -i -e "s/{{RECORD_VALUE}}/${RECORD_VALUE}/g" txt.json

#aws route53 change-resource-record-sets \
#  --hosted-zone-id ${ZONE_ID} \
#  --change-batch file://txt.json \
#  --region us-west-2
#
#aws ses wait identity-exists \
#  --identities ${DOMAIN} \
#  --region us-west-2


echo "*************************************"
echo "Enable DKIM Setting."
echo "*************************************"
#aws ses verify-domain-dkim \
#  --domain ${DOMAIN} \
#  --region us-west-2

echo "*************************************"
echo "Create CNAME record on Route53."
echo "*************************************"
for dkim_token in $(
    aws ses get-identity-dkim-attributes \
        --identities ${DOMAIN} \
        --query 'DkimAttributes.*.DkimTokens' \
        --region us-west-2 \
        --output text); do
  echo ${dkim_token}
done