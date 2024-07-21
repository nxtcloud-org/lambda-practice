import json


def lambda_handler(event, context):

    # S3 이벤트로부터 버킷 이름과 파일명을 가져옵니다.
    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    file_name = event["Records"][0]["s3"]["object"]["key"]

    print(f"{bucket_name} s3 버킷에 {file_name}이(가) 업로드 되었습니다!")

    return {"statusCode": 200, "body": json.dumps(f"File uploaded: {file_name}")}
