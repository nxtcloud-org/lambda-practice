import boto3
import logging
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 원하는 리전으로 변경
ec2 = boto3.client("ec2", region_name="ap-northeast-2")


def lambda_handler(event, context):
    # 현재 시간 로그
    logger.info(f"Start Instance Lambda triggered at: {datetime.now().isoformat()}")

    # 중지 상태인 모든 인스턴스 목록
    instances = ec2.describe_instances(
        Filters=[{"Name": "instance-state-name", "Values": ["stopped"]}]
    )["Reservations"]

    # 필터링 조건
    target_instances = []

    for reservation in instances:
        for instance in reservation["Instances"]:
            # 조건에 따라 필터링
            if "Tags" in instance:
                tags = {tag["Key"]: tag["Value"] for tag in instance["Tags"]}
                # 유형 필터링
                if instance["InstanceType"] == "t3.small":
                    target_instances.append(instance["InstanceId"])
                # 태그 필터링
                # if tags.get('Active') == 'Office-Hours':
                #     target_instances.append(instance['InstanceId'])
                # 이름 필터링
                # if tags.get('Name') == 'nxt-test':
                #     target_instances.append(instance['InstanceId'])

    if target_instances:
        ec2.start_instances(InstanceIds=target_instances)
        logger.info(f"Started instances: {target_instances}")
    else:
        logger.info("No instances to start")


# EventBridge cron 예약 표현식
"""
- 규칙 설명 : 매주 월요일부터 금요일까지 한국 시간으로 오전 9시에 트리거
- 규칙 유형 : 예약 표현식
- 예약 표현 식 : cron(0 0 ? * MON-FRI *)
"""
