"""Small, dependency-free helpers for signed login cookies and expiring OTPs.

Kept free of Streamlit imports so they can be unit tested.
"""
import base64
import hashlib
import hmac
import secrets
import time

COOKIE_TTL = 24 * 3600      # seconds a login cookie stays valid
OTP_TTL = 10 * 60           # seconds an OTP stays valid
OTP_MAX_ATTEMPTS = 5        # wrong guesses before the OTP is burned
OTP_RESEND_COOLDOWN = 60    # seconds between "send code" requests


# ---------- signed login cookie ----------
def _sign(secret, payload):
    return hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()


def sign_cookie(email, secret, ttl=COOKIE_TTL, now=None):
    """Return 'b64(email).expiry.signature'. The signature covers email + expiry."""
    now = time.time() if now is None else now
    b64 = base64.urlsafe_b64encode(email.encode()).decode().rstrip("=")
    payload = f"{b64}.{int(now + ttl)}"
    return f"{payload}.{_sign(secret, payload)}"


def verify_cookie(token, secret, now=None):
    """Return the email if the token is authentic and unexpired, else None."""
    now = time.time() if now is None else now
    try:
        b64, exp, sig = token.split(".")
        if not hmac.compare_digest(sig, _sign(secret, f"{b64}.{exp}")):
            return None
        if int(exp) < now:
            return None
        return base64.urlsafe_b64decode(b64 + "=" * (-len(b64) % 4)).decode()
    except Exception:
        return None


# ---------- one-time password ----------
def generate_otp():
    """6-digit code from a cryptographically secure source."""
    return f"{secrets.randbelow(900000) + 100000}"


def _otp_hash(otp, salt):
    return hashlib.sha256(f"{salt}:{otp}".encode()).hexdigest()


def create_otp_record(otp, now=None, ttl=OTP_TTL):
    """Store only a salted hash of the code, plus expiry and attempt counter."""
    now = time.time() if now is None else now
    salt = secrets.token_hex(8)
    return {"salt": salt, "hash": _otp_hash(otp, salt), "expires": now + ttl,
            "attempts": 0, "sent_at": now}


def verify_otp(record, entered, now=None, max_attempts=OTP_MAX_ATTEMPTS):
    """Return (ok, reason). Mutates record['attempts']. reason is None on success."""
    now = time.time() if now is None else now
    if not record:
        return False, "No code requested."
    if now > record["expires"]:
        return False, "Code expired. Request a new one."
    if record["attempts"] >= max_attempts:
        return False, "Too many attempts. Request a new code."
    record["attempts"] += 1
    if hmac.compare_digest(record["hash"], _otp_hash(entered.strip(), record["salt"])):
        return True, None
    left = max_attempts - record["attempts"]
    return False, f"Invalid code. {left} attempt(s) left." if left else "Too many attempts. Request a new code."


def resend_wait(record, now=None, cooldown=OTP_RESEND_COOLDOWN):
    """Seconds the user must still wait before requesting another code (0 if none)."""
    now = time.time() if now is None else now
    if not record:
        return 0
    return max(0, int(record["sent_at"] + cooldown - now))
