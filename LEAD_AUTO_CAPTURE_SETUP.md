# Maitri Global CRM — Automatic Lead Capture

The CRM now has a generic webhook endpoint:

`POST /leads/api/capture/`

Accepted JSON fields: `name`, `phone`, `email`, `company`, `source`, `requirement`.

Supported source labels include Facebook, Instagram, 99acres, Magicbricks, Housing.com, NoBroker, Phone Call, WhatsApp and Website.

## Important
This endpoint is the CRM side of the integration. A real automatic connection from a third-party portal requires that platform's authorised API/webhook/partner access and credentials. The ZIP does not contain or invent those credentials.

For production, set an environment variable named `LEAD_CAPTURE_TOKEN` and send the same value in the `X-Lead-Token` header.

Example JSON:

```json
{
  "name": "Test Client",
  "phone": "9876543210",
  "email": "test@example.com",
  "company": "Example Realty",
  "source": "99acres",
  "requirement": "2 BHK in Mumbai"
}
```
