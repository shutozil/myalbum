from __future__ import annotations

import os
import json
import urllib.parse as urlparser
from datetime import datetime, timedelta
import time
import base64

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding

import boto3
from botocore.signers import CloudFrontSigner

S3_BUCKET_NAME = os.environ["S3_BUCKET_NAME"]

AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


CDN_ORIGIN = os.environ["CDN_ORIGIN"]
CDN_DOMAIN = urlparser.urlparse(CDN_ORIGIN).netloc

CDN_KEY_PAIR_ID = os.environ["CLOUDFRONT_KEY_PAIR_ID"]


PREFIX = "sample/"
CREDENTIALS_PATH = "credentials/private_key.pem"

EXPIRE_DATE_FOR_MINUTES = 60
EXPIRE_DATE_FOR_DAYS = 2


def get_s3_directory_structure() -> dict[str, str]:
    """対象のバケットからファイルのリスト取得する関数"""

    # 指定したプレフィックスでS3オブジェクトを取得
    response = s3_client.list_objects_v2(
        Bucket=S3_BUCKET_NAME, Prefix=PREFIX, Delimiter="/"
    )

    # ディレクトリとファイルの情報を格納する辞書
    directory_structure = {}

    comment_json_filename = (
        f"data/{PREFIX.replace('-', '_').replace('/', '')}_message.json"
    )
    with open(comment_json_filename, "r", encoding="utf-8") as f:
        comment_dict = json.load(f)

    # ディレクトリを辞書に追加
    for common_prefix in response.get("CommonPrefixes", []):
        directory_name = common_prefix.get("Prefix")
        json_key = directory_name.replace(PREFIX, "").replace("/", "")
        comment_key_data: dict = comment_dict[json_key]

        directory_structure[json_key] = []

        # ディレクトリ直下のファイルを取得して辞書に追加
        files = s3_client.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix=directory_name)
        for file in files.get("Contents", []):
            if file["Key"] == directory_name:
                continue

            storage_key = file.get("Key")
            print(f"{storage_key=}")

            comment = next(
                (
                    item["comment"]
                    for item in comment_key_data
                    if item["storage_key"] == storage_key
                ),
                None,
            )
            if comment:
                encoded_comment = base64.b64encode(comment.encode("utf-8")).decode(
                    "utf-8"
                )
            else:
                encoded_comment = ""

            directory_structure[json_key].append(
                {"filename": storage_key, "comment": encoded_comment}
            )

    return directory_structure


def generate_init_json() -> dict:
    """対象のバケットからファイルの辞書を作成する（初期化）関数"""

    dir_name = PREFIX.replace("-", "_").replace("/", "")
    s3_files_json_filename = f"data/{dir_name}_files.json"
    print(f"{s3_files_json_filename=}")

    if not os.path.isfile(s3_files_json_filename):
        # S3のディレクトリ構造を取得して辞書を作成
        directory_structure = get_s3_directory_structure()
        texts_json = json.dumps(directory_structure, ensure_ascii=False, indent=2)

        with open(s3_files_json_filename, "w", encoding="utf-8") as file:
            file.write(texts_json)
    else:
        print("[WARNING] すでにファイル名のリストは作成済みです.")
        with open(s3_files_json_filename, "r", encoding="utf-8") as f:
            directory_structure = json.load(f)

    return directory_structure


def _rsa_signer(message):
    with open(CREDENTIALS_PATH, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(), password=None, backend=default_backend()
        )
    return private_key.sign(message, padding.PKCS1v15(), hashes.SHA1())


def regenerate_sign_urls_json(directory_structure: dict) -> dict:

    if "test" in PREFIX:
        expire_date = datetime.utcnow() + timedelta(minutes=EXPIRE_DATE_FOR_MINUTES)
    else:
        expire_date = datetime.utcnow() + timedelta(days=EXPIRE_DATE_FOR_DAYS)

    new_directory_structure = {}
    for key, value in directory_structure.items():
        new_directory_structure[key] = []
        for d in value:
            cdn_url = CDN_ORIGIN + "/" + d["filename"]

            time.sleep(1.5)

            # NOTE: ここで署名付きURLを作成
            try:
                cloudfront_signer = CloudFrontSigner(CDN_KEY_PAIR_ID, _rsa_signer)
                signed_url = cloudfront_signer.generate_presigned_url(
                    cdn_url, date_less_than=expire_date
                )
                new_directory_structure[key].append(
                    {"sign_url": signed_url, "comment": d["comment"]}
                )
            except Exception as error:
                print(f'[ERROR] 署名付きURLの発行に失敗しています": {cdn_url}')
                print(f"{error=}")

    return new_directory_structure


def main():
    directory_structure: dict = generate_init_json()
    print(f"{directory_structure=}")

    image_data: dict = regenerate_sign_urls_json(directory_structure)
    final_image_json_filename = "data/images.json"
    texts_json = json.dumps(image_data, ensure_ascii=False, indent=2)
    with open(final_image_json_filename, "w", encoding="utf-8") as file:
        file.write(texts_json)


main()
