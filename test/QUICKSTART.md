# Quick Start - Local MESH Sandbox Testing

This guide will help you quickly test the MESH client with your local Docker sandbox.

## Prerequisites

- Docker container running MESH sandbox on `http://localhost:8700`
- Python 3.7+ installed

## Setup (5 minutes)

1. **Install dependencies:**
```bash
cd /home/acleveland/repo/nhs/python-mesh-client
pip install -r test/requirements.txt
```

2. **Configure environment (optional):**

The handshake test uses these defaults for local sandbox:
- Endpoint: `http://localhost:8700`
- Mailbox ID: `X26ABC1`
- Password: `password`
- Shared Key: `TestKey`
- SSL Verification: `false`

To override, create a `.env` file:
```bash
cp test/.env.example test/.env
# Edit test/.env if needed
```

## Test Connectivity

Run the handshake test:
```bash
python test/mesh_handshake_test.py
```

**Expected output:**
```
============================================================
NHS MESH Handshake Test
============================================================

Configuration:
  Endpoint: http://localhost:8700
  Mailbox ID: X26ABC1
  Shared Key: TestKey
  Verify SSL: False
  ...

============================================================
Test 1: Manual Handshake
============================================================
Attempting handshake with MESH mailbox...
  URL: http://localhost:8700/messageexchange/X26ABC1
  Shared Key: TestKey
  ...

✓ Handshake successful!

============================================================
Test Summary
============================================================
Manual Handshake: ✓ PASSED
mesh-client Library: ✓ PASSED

✓ At least one method succeeded - connectivity confirmed!
```

## Troubleshooting

### Connection Refused
- Check if Docker container is running: `docker ps`
- Verify port 8700 is exposed: `docker port <container_name>`

### SSL Certificate Error
- Ensure `MESH_VERIFY_SSL=false` in your environment
- The script defaults to `false` for local testing

### Authentication Failed
- Verify mailbox credentials match your sandbox configuration
- Default sandbox credentials are:
  - Mailbox: `X26ABC1` (or `X26ABC2`, `X26ABC3`)
  - Password: `password`
  - Shared Key: `TestKey`

## Next Steps

Once handshake succeeds:

1. **Test message listing:**
```bash
python test/mesh_client_test.py
```

2. **Send test messages** to your sandbox mailbox (using MESH sandbox tools)

3. **Develop custom logic** in `mesh_client_test.py`

4. **Copy working code** to `src/lambda_function.py` for AWS deployment

## Common Sandbox Commands

If you're running the NHS MESH sandbox Docker container:

```bash
# Check if container is running
docker ps | grep mesh

# View container logs
docker logs <container_name>

# Restart container
docker restart <container_name>

# Check mailbox status (example)
curl http://localhost:8700/messageexchange/X26ABC1 \
  -H "Authorization: NHSMESH ..." \
  -X POST
```

## Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| MESH_ENDPOINT_URL | http://localhost:8700 | Sandbox API URL |
| MESH_MAILBOX_ID | X26ABC1 | Mailbox identifier |
| MESH_PASSWORD | password | Mailbox password |
| MESH_SHARED_KEY | TestKey | Shared key for authentication |
| MESH_VERIFY_SSL | false | SSL verification (false for local) |
| MESH_CERT_FILE | - | Client cert (not needed for sandbox) |
| MESH_KEY_FILE | - | Client key (not needed for sandbox) |

## Support

- MESH API Documentation: https://digital.nhs.uk/developer/api-catalogue/message-exchange-for-social-care-and-health-api
- NHS MESH Sandbox: https://github.com/NHSDigital/mesh-sandbox
