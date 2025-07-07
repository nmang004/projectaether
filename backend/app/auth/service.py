"""
Core authentication service for Project Aether.

This module contains the critical security logic for password hashing, JWT token
management, and secret key handling. All functions are designed to be framework-agnostic
and follow security best practices including proper secret management and secure hashing.
"""

import json
from datetime import datetime, timedelta
from functools import lru_cache
from typing import Dict, Any, Optional

from google.cloud import secretmanager
from google.cloud.exceptions import GoogleCloudError, NotFound
from jose import jwt
from passlib.context import CryptContext


# Password hashing configuration using bcrypt
# Bcrypt is chosen for its adaptive nature and resistance to timing attacks
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT algorithm configuration
# HS256 is chosen for its simplicity and security for single-service applications
ALGORITHM = "HS256"

# JWT token expiration time (24 hours)
ACCESS_TOKEN_EXPIRE_HOURS = 24


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password.
    
    This function uses constant-time comparison to prevent timing attacks
    and leverages bcrypt's built-in salt verification.
    
    Args:
        plain_password (str): The plain text password to verify
        hashed_password (str): The stored bcrypt hash to compare against
        
    Returns:
        bool: True if the password matches, False otherwise
        
    Security Notes:
        - Uses constant-time comparison to prevent timing attacks
        - Leverages bcrypt's built-in salt handling
        - Does not leak information about password validity through timing
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a plain text password using bcrypt.
    
    This function generates a secure bcrypt hash with automatic salt generation.
    The resulting hash includes the salt and cost factor, making it suitable
    for direct storage in the database.
    
    Args:
        password (str): The plain text password to hash
        
    Returns:
        str: The bcrypt hash including salt and cost factor
        
    Security Notes:
        - Uses bcrypt with automatic salt generation
        - Default cost factor provides good security vs performance balance
        - Hash includes all necessary information for verification
    """
    return pwd_context.hash(password)


@lru_cache(maxsize=1)
def get_jwt_secret() -> str:
    """
    Retrieve JWT secret key from Google Secret Manager.
    
    This function fetches the JWT signing secret from Google Secret Manager
    and caches it for the lifetime of the application. The secret is used
    to sign and verify JWT tokens.
    
    Returns:
        str: The JWT secret key
        
    Raises:
        GoogleCloudError: If the secret cannot be retrieved from Google Secret Manager
        KeyError: If the secret value is not found in the expected format
        
    Security Notes:
        - Secret is cached in memory for performance (single application instance)
        - Uses Google Cloud IAM permissions for access control
        - Secret rotation requires application restart (acceptable for this phase)
        - Secret name follows project naming convention for organization
    """
    # Import config to get project ID
    from app.core.config import get_settings
    settings = get_settings()
    
    # Initialize Google Secret Manager client
    # Uses Application Default Credentials (ADC)
    client = secretmanager.SecretManagerServiceClient()
    
    # Construct the secret name
    # Format: projects/{project}/secrets/{secret_id}/versions/latest
    project_id = settings.GCP_PROJECT_ID
    secret_id = "projectaether-jwt-secret"
    secret_name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    
    try:
        # Access the secret version
        response = client.access_secret_version(request={"name": secret_name})
        
        # Decode the secret payload
        secret_value = response.payload.data.decode("UTF-8")
        
        # Parse the secret value (assuming JSON format)
        secret_dict = json.loads(secret_value)
        
        # Extract the JWT secret key
        return secret_dict['jwt_secret']
        
    except NotFound as e:
        raise GoogleCloudError(
            f"Secret {secret_id} not found in Google Secret Manager. "
            "Please ensure the secret exists and the application has proper IAM permissions."
        ) from e
    
    except GoogleCloudError as e:
        raise GoogleCloudError(
            f"Failed to retrieve secret {secret_id}: {e}"
        ) from e
    
    except (KeyError, json.JSONDecodeError) as e:
        raise KeyError(
            f"Secret {secret_id} does not contain expected 'jwt_secret' key "
            "or is not valid JSON format."
        ) from e


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token with the provided data and expiration time.
    
    This function creates a signed JWT token containing the provided data
    along with standard JWT claims (issued at, expiration, etc.).
    
    Args:
        data (Dict[str, Any]): The data to encode in the token (typically user info)
        expires_delta (Optional[timedelta]): Custom expiration time, defaults to 24 hours
        
    Returns:
        str: The signed JWT token
        
    Security Notes:
        - Uses HS256 algorithm for signing (symmetric key)
        - Includes expiration time to limit token lifetime
        - Secret key is securely retrieved from AWS Secrets Manager
        - Token includes issued-at claim for audit purposes
    """
    # Create a copy of the data to avoid modifying the original
    to_encode = data.copy()
    
    # Set expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    
    # Add standard JWT claims
    to_encode.update({
        "exp": expire,  # Expiration time
        "iat": datetime.utcnow(),  # Issued at time
    })
    
    # Get the secret key and create the token
    secret_key = get_jwt_secret()
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    
    return encoded_jwt


def decode_access_token(token: str) -> Dict[str, Any]:
    """
    Decode and validate a JWT access token.
    
    This function decodes a JWT token, validates its signature and expiration,
    and returns the payload data.
    
    Args:
        token (str): The JWT token to decode
        
    Returns:
        Dict[str, Any]: The decoded token payload
        
    Raises:
        jose.ExpiredSignatureError: If the token has expired
        jose.JWTError: If the token is invalid or malformed
        
    Security Notes:
        - Validates token signature using the secret key
        - Checks token expiration automatically
        - Raises specific exceptions for different failure modes
    """
    secret_key = get_jwt_secret()
    
    # Decode and validate the token
    # This will raise appropriate exceptions for invalid/expired tokens
    payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
    
    return payload