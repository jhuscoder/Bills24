
import os, json, base64, hashlib
from typing import Any, Optional

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from .settings.configuration import AUTHENTICATION_KEY

AUTHENTICATION_KEY = AUTHENTICATION_KEY

KEY = hashlib.sha256(AUTHENTICATION_KEY.encode('utf-8')).digest()

def _urlsafe_b64encode_no_padding(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode('ascii')


def _urlsafe_b64decode_with_padding(data: str) -> bytes:
    s = data
    # Restore padding if stripped
    padding = (-len(s)) % 4
    if padding:
        s += "=" * padding
    return base64.urlsafe_b64decode(s)


def encrypt_json(json_object: str) -> Optional[str]:
    """
    Encrypt a JSON string and return a URL-safe base64 string.
    Uses AES-256-GCM (authenticated encryption). The returned payload contains
    the 12-byte nonce followed by the ciphertext+tag, encoded with URL-safe
    base64 (no padding).
    """
    if not json_object:
        return None

    aesgcm = AESGCM(KEY)
    nonce = os.urandom(16)  # GCM standard nonce size
    ciphertext = aesgcm.encrypt(nonce, json_object.encode('utf-8'), None)
    return _urlsafe_b64encode_no_padding(nonce + ciphertext)


def decrypt_data(encrypted_text: str) -> Optional[str]:
    """Decrypt a URL-safe base64 encrypted payload and return the plaintext string.

    The input is expected to contain the 12-byte nonce + ciphertext+tag, encoded with
    URL-safe base64 (padding may be omitted).
    """
    if not encrypted_text:
        return None

    try:
        encrypted_bytes = _urlsafe_b64decode_with_padding(encrypted_text)
        nonce = encrypted_bytes[:16]
        ciphertext = encrypted_bytes[16:]

        aesgcm = AESGCM(KEY)
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        return plaintext.decode('utf-8')
    except Exception:
        return None


def handle_incoming_request(encrypted_json: str) -> Optional[Any]:
    """
    Parse envelope JSON, decrypt the `data` value and return the decoded object.
    Returns None on any failure.
    """
    try:
        wrapper = json.loads(encrypted_json)
    except Exception:
        return None

    encrypted_string = wrapper.get('data')

    if not encrypted_string:
        return None

    decrypted_json_string = decrypt_data(encrypted_string)

    if not decrypted_json_string:
        return None

    try:
        return json.loads(decrypted_json_string)
    
    except Exception:
        return None


def handle_outgoing_response(plain_json: Any) -> Optional[str]:
    """
    Take a JSON-serializable object, encrypt it and return an envelope string.
    The returned value is a JSON string containing the `data` field with the
    encrypted payload.
    
    plain_json = {
        'status': '00', 
        'message': 'Login successful', 
        'data': {}
    }

    ENCRYPTED_JSON = {
        "status": "00",
        "message": "Login successful",
        "data": "257b68b6-25cd-457c-b7c3-a63d0514ee9b257b68b6-25cd-457c-b7c3-a63d0514ee9b"
    }

    """
    try:
        json_data = json.dumps(plain_json["data"])
        encrypted_json_data = encrypt_json(json_data)
    except Exception:
        return None
    
    if encrypted_json_data is None:
        return None
    
    plain_json["data"] = encrypted_json_data
    
    encrypted_json = plain_json
    return json.dumps(encrypted_json)