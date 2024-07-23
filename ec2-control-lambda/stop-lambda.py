import boto3
import logging
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 원하는 리전으로 변경
ec2 = boto3.client("ec2", region_name="ap-northeast-2")


def lambda_handler(event, context):
    # 현재 시간 로그
    logger.info(f"Stop Instance Lambda triggered at: {datetime.now().isoformat()}")

    # 실행 상태인 모든 인스턴스 목록
    instances = ec2.describe_instances(
        Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
    )["Reservations"]

    # 필터링 조건
    target_instances = []

    for reservation in instances:
        for instance in reservation["Instances"]:
            # 조건에 따라 필터링
            if "Tags" in instance:
                tags = {tag["Key"]: tag["Value"] for tag in instance["Tags"]}
                # 태그 필터링
                if tags.get('owner') == 'YOUR-IAM-USER-NAME':
                   target_instances.append(instance['InstanceId'])

    if target_instances:
        ec2.stop_instances(InstanceIds=target_instances)
        logger.info(f"Stopped instances: {target_instances}")
    else:
        logger.info("No instances to stop")


# EventBridge cron 예약 표현식
"""
- 규칙 설명 : 매주 월요일부터 금요일까지 한국 시간으로 오전 9시에 트리거
- 규칙 유형 : 예약 표현식
- 예약 표현 식 : cron(0 9 ? * MON-FRI *)
"""
