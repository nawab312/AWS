import json
import datetime
import jwt  # PyJWT library for signing

# CloudFront settings
CLOUDFRONT_DOMAIN = "d1k32j2m5z2tf8.cloudfront.net"
PRIVATE_KEY_PATH = "/home/siddharth312/Downloads/pk-APKA57VDLLAA3F7HMJWX.pem"
KEY_PAIR_ID = "APKA57VDLLAA3F7HMJWX"

# Generate a signed URL
def create_signed_url(file_path, expiry_seconds=3600):
    expiration_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=expiry_seconds)

    # Generate policy
    policy = {
        "Statement": [
            {
                "Resource": f"https://{CLOUDFRONT_DOMAIN}/{file_path}",
                "Condition": {"DateLessThan": {"AWS:EpochTime": int(expiration_time.timestamp())}},
            }
        ]
    }

    # Sign with private key
    with open(PRIVATE_KEY_PATH, "r") as key_file:
        private_key = key_file.read()
    signed_token = jwt.encode(policy, private_key, algorithm="RS256")

    # Construct signed URL
    signed_url = (
        f"https://{CLOUDFRONT_DOMAIN}/{file_path}?"
        f"Policy={signed_token}&Key-Pair-Id={KEY_PAIR_ID}"
    )
    return signed_url

# Generate signed URL for a test file
signed_url = create_signed_url("index.html")
print("Signed URL:", signed_url)
