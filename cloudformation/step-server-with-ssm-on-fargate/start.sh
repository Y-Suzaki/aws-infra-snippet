#!/bin/bash

amazon-ssm-agent -register -code "${SSM_ACTIVATION_CODE}" -id "${SSM_ACTIVATION_ID}" -region "${AWS_DEFAULT_REGION}" 
amazon-ssm-agent
