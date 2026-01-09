#!/usr/bin/env python3
"""
Local test script for NHS MESH client logic.

This script allows you to develop and test the MESH mailbox integration
locally before deploying to AWS Lambda.

Usage:
    python test/mesh_client_test.py
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any


def initialize_mesh_client():
    """
    Initialize the MESH client with credentials from environment variables.
    
    Returns:
        MeshClient: Initialized MESH client instance
    """
    # Get configuration from environment
    mailbox_id = os.environ.get('MESH_MAILBOX_ID', 'TEST_MAILBOX')
    password = os.environ.get('MESH_PASSWORD', 'test_password')
    endpoint = os.environ.get('MESH_ENDPOINT', 'INT')
    cert_file = os.environ.get('MESH_CERT_FILE', '/path/to/cert.pem')
    key_file = os.environ.get('MESH_KEY_FILE', '/path/to/key.pem')
    
    print(f"Initializing MESH client...")
    print(f"  Mailbox ID: {mailbox_id}")
    print(f"  Endpoint: {endpoint}")
    print(f"  Cert File: {cert_file}")
    print(f"  Key File: {key_file}")
    
    # TODO: Uncomment when mesh-client is installed
    # from mesh_client import MeshClient, INT_ENDPOINT, LIVE_ENDPOINT
    # 
    # endpoint_url = INT_ENDPOINT if endpoint == 'INT' else LIVE_ENDPOINT
    # 
    # client = MeshClient(
    #     endpoint_url,
    #     mailbox_id,
    #     password,
    #     cert=(cert_file, key_file)
    # )
    # 
    # return client
    
    # For now, return None - this will be replaced with actual client
    return None


def list_messages(client) -> List[str]:
    """
    List all available messages in the MESH mailbox.
    
    Args:
        client: MESH client instance
        
    Returns:
        List of message IDs
    """
    print("\nListing messages in mailbox...")
    
    # TODO: Implement with actual MESH client
    # message_ids = client.list_messages()
    # print(f"Found {len(message_ids)} messages")
    # return message_ids
    
    # Mock data for testing
    mock_messages = [f"MSG_{i:04d}" for i in range(1, 150)]
    print(f"Found {len(mock_messages)} messages (mock data)")
    return mock_messages


def process_batch(client, message_ids: List[str], batch_number: int) -> Dict[str, Any]:
    """
    Process a batch of messages (download, store metadata).
    
    Args:
        client: MESH client instance
        message_ids: List of message IDs to process
        batch_number: Batch number for tracking
        
    Returns:
        Dictionary with batch processing results
    """
    print(f"\nProcessing batch {batch_number} ({len(message_ids)} messages)...")
    
    batch_results = {
        'batch_number': batch_number,
        'processed': 0,
        'failed': 0,
        'messages': []
    }
    
    for message_id in message_ids:
        try:
            # TODO: Implement actual message retrieval
            # message_data = client.retrieve_message(message_id)
            
            # Mock message retrieval
            message_data = {
                'message_id': message_id,
                'content': f'Mock content for {message_id}',
                'timestamp': datetime.utcnow().isoformat()
            }
            
            # Store message metadata
            metadata = {
                'message_id': message_id,
                'timestamp': datetime.utcnow().isoformat(),
                'status': 'received',
                'batch_id': f'batch-{batch_number}'
            }
            
            batch_results['messages'].append(metadata)
            batch_results['processed'] += 1
            
            print(f"  ✓ Processed message: {message_id}")
            
        except Exception as e:
            print(f"  ✗ Failed to process {message_id}: {e}")
            batch_results['failed'] += 1
    
    return batch_results


def acknowledge_messages(client, message_ids: List[str]) -> int:
    """
    Acknowledge messages to remove them from the MESH queue.
    
    Args:
        client: MESH client instance
        message_ids: List of message IDs to acknowledge
        
    Returns:
        Number of messages successfully acknowledged
    """
    print(f"\nAcknowledging {len(message_ids)} messages...")
    
    acknowledged = 0
    for message_id in message_ids:
        try:
            # TODO: Implement actual acknowledgment
            # client.acknowledge_message(message_id)
            
            acknowledged += 1
            
        except Exception as e:
            print(f"  ✗ Failed to acknowledge {message_id}: {e}")
    
    print(f"  ✓ Acknowledged {acknowledged}/{len(message_ids)} messages")
    return acknowledged


def save_batch_to_file(batch_results: Dict[str, Any], output_dir: str = './test/output'):
    """
    Save batch results to a local file (simulates S3 storage).
    
    Args:
        batch_results: Batch processing results
        output_dir: Directory to save results
    """
    os.makedirs(output_dir, exist_ok=True)
    
    batch_number = batch_results['batch_number']
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    filename = f"{output_dir}/batch-{timestamp}-{batch_number}.json"
    
    with open(filename, 'w') as f:
        json.dump(batch_results, f, indent=2)
    
    print(f"  Saved batch results to: {filename}")


def main():
    """
    Main function to test MESH client logic locally.
    """
    print("=" * 60)
    print("NHS MESH Client - Local Testing")
    print("=" * 60)
    
    # Configuration
    batch_size = int(os.environ.get('BATCH_SIZE', 500))
    print(f"\nConfiguration:")
    print(f"  Batch Size: {batch_size}")
    
    # Initialize client
    client = initialize_mesh_client()
    
    # List available messages
    message_ids = list_messages(client)
    
    if not message_ids:
        print("\nNo messages to process.")
        return
    
    # Process messages in batches
    total_batches = (len(message_ids) + batch_size - 1) // batch_size
    print(f"\nWill process {len(message_ids)} messages in {total_batches} batches")
    
    all_results = []
    
    for batch_num in range(total_batches):
        start_idx = batch_num * batch_size
        end_idx = min(start_idx + batch_size, len(message_ids))
        batch_messages = message_ids[start_idx:end_idx]
        
        # Process the batch
        batch_results = process_batch(client, batch_messages, batch_num + 1)
        
        # Save results locally (simulates S3 upload)
        save_batch_to_file(batch_results)
        
        # TODO: Save to DynamoDB (for now, just collect results)
        all_results.append(batch_results)
        
        # Acknowledge messages
        acknowledge_messages(client, batch_messages)
    
    # Summary
    print("\n" + "=" * 60)
    print("Processing Summary")
    print("=" * 60)
    total_processed = sum(r['processed'] for r in all_results)
    total_failed = sum(r['failed'] for r in all_results)
    print(f"Total Messages: {len(message_ids)}")
    print(f"Processed: {total_processed}")
    print(f"Failed: {total_failed}")
    print(f"Batches: {total_batches}")
    print("\nTest complete!")


if __name__ == '__main__':
    main()
