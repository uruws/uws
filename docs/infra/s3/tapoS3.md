# tapo S3 setup

* We have setup bucketAV for S3 objects scanning
    * https://bucketav.com/help/setup-guide/
    * https://aws.amazon.com/marketplace/pp/prodview-sykoblbsdgw2o

* CloudFormation stack: tapoS3AV
    * https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1

* CloudWatch dashboard
    * https://us-east-1.console.aws.amazon.com/cloudwatch/home?region=us-east-1#dashboards:name=tapoS3AV-us-east-1

* Setup scripts under docker/awscli/utils (s3-app-*.sh)
