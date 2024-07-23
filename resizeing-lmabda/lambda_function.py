import boto3
import os
import uuid
from urllib.parse import unquote_plus
from PIL import Image

s3_client = boto3.client("s3")


def resize_image(image_path, resized_path):
    with Image.open(image_path) as image:
        # 원래 크기의 절반으로 이미지 크기를 조정
        image.thumbnail(tuple(x / 2 for x in image.size))
        image.save(resized_path)


def lambda_handler(event, context):
    for record in event["Records"]:
        source_bucket = record["s3"]["bucket"]["name"]
        key = unquote_plus(record["s3"]["object"]["key"])

        print(f"소스 이미지 버킷 이름 : {source_bucket}")
        print(f"소스 이미지 파일 이름 : {key}")
        
        tmpkey = key.replace("/", "")
        download_path = f"/tmp/{uuid.uuid4()}{tmpkey}"
        upload_path = f"/tmp/resized-{tmpkey}"
        s3_client.download_file(source_bucket, key, download_path)
        resize_image(download_path, upload_path)
        target_bucket = "리사이즈된 파일을 저장할 버킷 이름을 작성해주세요."
        s3_client.upload_file(upload_path, target_bucket, f"resized-{key}")
        print(f"resized-{key} 파일 {target_bucket}에 업로드 완료")


# 패키지 폴더 생성 후 필요 패키지 설치
"""
mkdir package
pip install \
--platform manylinux2014_x86_64 \
--target=package \
--implementation cp \
--python-version 3.12 \
--only-binary=:all: --upgrade \
pillow boto3
"""

# 코드와 패키지 압축파일 생성
"""
zip -r Lambda_function.zip .
"""

# 코드 업로드 이후 Add layer
"""
ARN 지정 → arn:aws:lambda:ap-northeast-2:770693421928:layer:Klayers-p312-Pillow:2
참고 : https://github.com/keithrozario/Klayers/tree/master/deployments/python3.12
"""
