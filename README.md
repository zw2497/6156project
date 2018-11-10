# QALite
## Introduction
QALite is a forum for **Qestions** and **Answers**. This website uses **Event-centric model** and breaks a **Monolith** into **Microservices** which makes it more convenient for more groups to collaborate. 

## Components
### Browser-based UI 
* AngularJS, Bootstrap
### Microservices
* AWS Elastic Beanstalk: Basic user identity and information
* AWS Lambda : User profile and contact management
### Cloud services
* SmartyStreets: address verification.
* Facebook: basic profile information and authentication via OAuth2
### Cloud databases
* Amazon RDS: hold basic user info.
* Amazon DynamoDB: hold contact and profile information.
### Management and supporting services:
* AWS CloudWatch: monitoring and problem determination.
* Virtual Private Cloud: security and isolation.
* AWS Route 53: domain management.
* AWS Certificate Manager: SSL certificates and authentication.
* AWS Identity and Access Manager: user identity, authorization and policy based security.
### More Thing
* Amazon S3: static content delivery and management.
* AWS SES: email ownership verification and email user interaction.
* AWS SNS: texting and phone number verification.
* AWS API Gateway: single system image and API Management.
* AWS CloudFront: single site image and content delivery network.

## Contributor
* Zhicheng Wu zw2497
* Zian Zhao zz2558
* Yipeng Zhou yz3169
* Xinwei Zhang xz2663
* Lin Bai lb3161

## License

[MIT](http://opensource.org/licenses/MIT)

Copyright (c) 2018-present


