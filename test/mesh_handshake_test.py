#!/usr/bin/env python3
"""
MESH Handshake Test Script

Tests connectivity and authentication with a MESH mailbox using the handshake endpoint.
This is useful for verifying your local sandbox or testing environment.

API Reference: https://digital.nhs.uk/developer/api-catalogue/message-exchange-for-social-care-and-health-api#post-/messageexchange/-mailbox_id-

Usage:
    python test/mesh_handshake_test.py
"""

import os
import sys
import requests
import hashlib
import uuid
from datetime import datetime


def generate_authorization_header(mailbox_id, password, nonce, nonce_count, timestamp):
    """
    Generate the MESH authorization header.
    
    MESH uses HMAC-based authentication similar to HTTP Digest Auth.
    
    Args:
        mailbox_id: MESH mailbox identifier
        password: MESH mailbox password
        nonce: Unique nonce for this request
        nonce_count: Nonce counter
        timestamp: ISO 8601 timestamp
        
    Returns:
        Authorization header value
    """
    # Create the hash chain
    # Hash 1: mailbox_id:nonce:nonce_count:password:timestamp
    hash_data = f"{mailbox_id}:{nonce}:{nonce_count}:{password}:{timestamp}"
    myhash = hashlib.sha256(hash_data.encode()).hexdigest()
    
    # Build authorization header
    auth_header = (
        f'NHSMESH {mailbox_id}:'
        f'{nonce}:'
        f'{nonce_count}:'
        f'{timestamp}:'
        f'{myhash}'
    )
    
    return auth_header


def perform_handshake(endpoint_url, mailbox_id, password, verify_ssl=True):
    """
    Perform a handshake with the MESH mailbox.
    
    Args:
        endpoint_url: Base MESH API URL (e.g., https://localhost:8700)
        mailbox_id: MESH mailbox identifier
        password: MESH mailbox password
        verify_ssl: Whether to verify SSL certificates (False for local sandbox)
        
    Returns:
        Tuple of (success: bool, response_data: dict, error: str)
    """
    # Generate authentication parameters
    nonce = str(uuid.uuid4())
    nonce_count = "0"
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    
    # Build handshake URL
    handshake_url = f"{endpoint_url}/messageexchange/{mailbox_id}"
    
    # Generate authorization header
    auth_header = generate_authorization_header(
        mailbox_id, password, nonce, nonce_count, timestamp
    )
    
    # Set up headers
    headers = {
        'Authorization': auth_header,
        'Mex-ClientVersion': 'Python-Test-Client-1.0',
        'Mex-OSName': 'Linux',
        'Mex-OSVersion': '1.0',
        'Content-Type': 'application/json'
    }
    
    print(f"Attempting handshake with MESH mailbox...")
    print(f"  URL: {handshake_url}")
    print(f"  Mailbox: {mailbox_id}")
    print(f"  Nonce: {nonce}")
    print(f"  Timestamp: {timestamp}")
    print(f"  Auth Header: {auth_header[:50]}...")
    
    try:
        response = requests.post(
            handshake_url,
            headers=headers,
            verify=verify_ssl,
            timeout=10
        )
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("\n✓ Handshake successful!")
            return True, response.json() if response.content else {}, None
        else:
            error_msg = f"Handshake failed with status {response.status_code}"
            try:
                error_details = response.json()
                print(f"\nError Details: {error_details}")
                error_msg += f": {error_details}"
            except:
                print(f"\nError Body: {response.text}")
                error_msg += f": {response.text}"
            
            return False, {}, error_msg
            
    except requests.exceptions.SSLError as e:
        error_msg = f"SSL Error: {e}\nTry setting verify_ssl=False for local sandbox"
        print(f"\n✗ {error_msg}")
        return False, {}, error_msg
        
    except requests.exceptions.ConnectionError as e:
        error_msg = f"Connection Error: {e}\nIs the MESH sandbox running?"
        print(f"\n✗ {error_msg}")
        return False, {}, error_msg
        
    except Exception as e:
        error_msg = f"Unexpected error: {e}"
        print(f"\n✗ {error_msg}")
        return False, {}, error_msg


def test_with_mesh_client_library(endpoint_url, mailbox_id, password, cert_file=None, key_file=None):
    """
    Alternative: Test using the mesh-client library if available.
    
    Args:
        endpoint_url: MESH endpoint URL
        mailbox_id: MESH mailbox identifier
        password: MESH mailbox password
        cert_file: Path to client certificate (optional)
        key_file: Path to client key (optional)
    """
    try:
        from mesh_client import MeshClient
        
        print("\n" + "=" * 60)
        print("Testing with mesh-client library")
        print("=" * 60)
        
        # Prepare certificate tuple if provided
        cert = (cert_file, key_file) if cert_file and key_file else None
        
        with MeshClient(
            endpoint_url,
            mailbox_id,
            password,
            cert=cert
        ) as client:
            print("\n✓ Successfully initialized MeshClient")
            
            # Try to list messages as a connectivity test
            try:
                messages = client.list_messages()
                print(f"✓ Successfully listed messages: {len(messages)} found")
                return True
            except Exception as e:
                print(f"✗ Error listing messages: {e}")
                return False
                
    except ImportError:
        print("\nmesh-client library not installed")
        print("Install with: pip install mesh-client")
        return False
    except Exception as e:
        print(f"\n✗ Error with mesh-client: {e}")
        return False


def main():
    """
    Main function to test MESH handshake.
    """
    print("=" * 60)
    print("NHS MESH Handshake Test")
    print("=" * 60)
    
    # Get configuration from environment or use defaults for local sandbox
    endpoint_url = os.environ.get('MESH_ENDPOINT_URL', 'https://localhost:8700')
    mailbox_id = os.environ.get('MESH_MAILBOX_ID', 'X26ABC1')
    password = os.environ.get('MESH_PASSWORD', 'password')
    verify_ssl = os.environ.get('MESH_VERIFY_SSL', 'false').lower() == 'true'
    
    cert_file = os.environ.get('MESH_CERT_FILE')
    key_file = os.environ.get('MESH_KEY_FILE')
    
    print(f"\nConfiguration:")
    print(f"  Endpoint: {endpoint_url}")
    print(f"  Mailbox ID: {mailbox_id}")
    print(f"  Verify SSL: {verify_ssl}")
    print(f"  Cert File: {cert_file or 'Not provided'}")
    print(f"  Key File: {key_file or 'Not provided'}")
    
    # Test 1: Manual handshake
    print("\n" + "=" * 60)
    print("Test 1: Manual Handshake")
    print("=" * 60)
    
    success, data, error = perform_handshake(
        endpoint_url, mailbox_id, password, verify_ssl
    )
    
    if success:
        print(f"\n✓ Handshake Response Data:")
        for key, value in data.items():
            print(f"    {key}: {value}")
    
    # Test 2: mesh-client library
    print("\n" + "=" * 60)
    print("Test 2: mesh-client Library")
    print("=" * 60)
    
    library_success = test_with_mesh_client_library(
        endpoint_url, mailbox_id, password, cert_file, key_file
    )
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Manual Handshake: {'✓ PASSED' if success else '✗ FAILED'}")
    print(f"mesh-client Library: {'✓ PASSED' if library_success else '✗ FAILED'}")
    
    if success or library_success:
        print("\n✓ At least one method succeeded - connectivity confirmed!")
        return 0
    else:
        print("\n✗ All tests failed - check configuration and sandbox status")
        return 1


if __name__ == '__main__':
    sys.exit(main())
