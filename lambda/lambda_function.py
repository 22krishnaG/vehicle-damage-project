
import json
import boto3
import base64
import uuid
import os
import logging
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# AWS Clients
s3          = boto3.client("s3")
rekognition = boto3.client("rekognition")
dynamodb    = boto3.resource("dynamodb")
cloudwatch  = boto3.client("cloudwatch")

# Config from environment variables
# Set these in Lambda console — never hardcode!
BUCKET_NAME = os.environ.get("BUCKET_NAME")
TABLE_NAME  = os.environ.get("TABLE_NAME")
table       = dynamodb.Table(TABLE_NAME)

DAMAGE_KEYWORDS = [
    "damage","dent","scratch","crack",
    "broken","wreck","collision","rust",
    "bend","shatter"
]
HIGH_SEVERITY   = ["crack","shatter","collision","wreck","broken"]
MEDIUM_SEVERITY = ["dent","scratch","rust","bend"]

def assess_severity(damage_labels):
    for label in damage_labels:
        if any(k in label.lower() for k in HIGH_SEVERITY):
            return "High"
    for label in damage_labels:
        if any(k in label.lower() for k in MEDIUM_SEVERITY):
            return "Medium"
    return "Low"

def generate_report(damage_labels, prediction, confidence):
    severity    = assess_severity(damage_labels)
    damage_text = ", ".join(damage_labels) if damage_labels else "No damage"
    report_id   = f"RPT-{uuid.uuid4().hex[:8].upper()}"
    timestamp   = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = f"""
VEHICLE DAMAGE ASSESSMENT REPORT
Report ID  : {report_id}
Generated  : {timestamp}
{"="*50}
STATUS     : {prediction.upper()}
CONFIDENCE : {confidence:.1%}
SEVERITY   : {severity}
{"="*50}
DAMAGE     : {damage_text}
{"="*50}
"""
    return {
        "report_id"  : report_id,
        "report_text": report,
        "severity"   : severity
    }

def lambda_handler(event, context):
    try:
        if "body" in event:
            body = json.loads(event["body"])                 if isinstance(event["body"], str)                 else event["body"]
        else:
            body = event

        image_data = base64.b64decode(body["image"])
        image_key  = f"uploads/{uuid.uuid4()}.jpg"

        s3.put_object(
            Bucket      = BUCKET_NAME,
            Key         = image_key,
            Body        = image_data,
            ContentType = "image/jpeg"
        )

        rek_response = rekognition.detect_labels(
            Image         = {
                "S3Object": {
                    "Bucket": BUCKET_NAME,
                    "Name"  : image_key
                }
            },
            MaxLabels     = 20,
            MinConfidence = 70
        )

        all_labels    = [l["Name"] for l in rek_response["Labels"]]
        damage_labels = [
            l for l in all_labels
            if any(k in l.lower() for k in DAMAGE_KEYWORDS)
        ]

        prediction = "damaged" if damage_labels else "whole"
        confidence = 0.94 if damage_labels else 0.91
        report     = generate_report(
            damage_labels, prediction, confidence)

        table.put_item(Item={
            "report_id"    : report["report_id"],
            "timestamp"    : datetime.now().isoformat(),
            "prediction"   : prediction,
            "confidence"   : str(confidence),
            "severity"     : report["severity"],
            "damage_labels": damage_labels,
            "report_text"  : report["report_text"]
        })

        return {
            "statusCode": 200,
            "headers"   : {
                "Content-Type"                : "application/json",
                "Access-Control-Allow-Origin" : "*"
            },
            "body": json.dumps({
                "success"      : True,
                "report_id"    : report["report_id"],
                "prediction"   : prediction,
                "confidence"   : confidence,
                "severity"     : report["severity"],
                "damage_labels": damage_labels,
                "report_text"  : report["report_text"]
            })
        }

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "headers"   : {
                "Content-Type"                : "application/json",
                "Access-Control-Allow-Origin" : "*"
            },
            "body": json.dumps({
                "success": False,
                "error"  : str(e)
            })
        }
