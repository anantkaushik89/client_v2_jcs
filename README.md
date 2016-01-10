# client_v2_jcs
This is a client for creating curl call to with signature v2.

The syntax to use the client is as follows:

./create_request.py "http://10.0.2.15:8788/services/Cloud/?Action=DescribeInstances&Version=2014-10-01"

This returns an output with the Signature Version 2 of AWS and all the relevant parameters in the request.

curl -X GET -H "Accept-Encoding: identity" -H "User-Agent: curl/7.35.0" -H "Content-Type: application/json" "http://10.0.2.15:8788/services/Cloud/?SignatureVersion=2&AWSAccessKeyId=02b0532340f242e090dfc53bb331b3bf&Timestamp=2016-01-10T17:49:32Z&SignatureMethod=HmacSHA256&Version=2014-10-01&Signature=W0atbmSuRQtc2I0VA827hNQFRZUFgWT9HTHHI4boghM=&Action=DescribeInstances"
