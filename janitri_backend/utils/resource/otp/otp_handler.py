import random
from utils.redis_client import redis_client

OTP_EXPIRY = 300  # 5 minutes

def generate_otp():
    """Generate a 6-digit random OTP"""
    return str(random.randint(100000, 999999))

def store_otp(email, otp):
    """Store OTP in Redis with expiry"""
    redis_client.setex(f"otp:{email}", OTP_EXPIRY, otp)

def verify_otp(email, otp):
    """Verify if OTP matches"""
    stored = redis_client.get(f"otp:{email}")
    return stored == otp

def delete_otp(email):
    """Delete OTP after successful verification"""
    redis_client.delete(f"otp:{email}")
