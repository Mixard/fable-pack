---
name: mailtrap-email-integration
description: Use when implementing transactional email sending via the Mailtrap Email API or debugging non-delivery in dev/staging. Covers the exact production and sandbox send endpoints, Bearer auth, request payload shape, and the sandbox-vs-production routing pattern.
---

# Mailtrap Email Integration

Mailtrap has two separate sending surfaces:

- **Production**: `https://send.api.mailtrap.io/api/send` — delivers to real recipients; requires a DNS-verified sending domain (SPF, DKIM, DMARC). Sending before verification completes fails silently or lands in spam.
- **Sandbox**: `https://sandbox.api.mailtrap.io/api/send/{inbox_id}` — captures emails without delivering them; use for dev/staging so test emails never reach real inboxes.

Authentication is a Bearer token in the `Authorization` header. Tokens are scoped per project; sandbox and production use different tokens — keep them in separate environment variables.

## Send Request

```typescript
async function sendEmail(to: string, subject: string, html: string) {
  const response = await fetch("https://send.api.mailtrap.io/api/send", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${process.env.MAILTRAP_API_TOKEN}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      from: { email: "no-reply@yourverifieddomain.com", name: "Your App" },
      to: [{ email: to }],
      subject,
      html,
    }),
  });

  if (!response.ok) {
    throw new Error(`Email send failed: ${response.status}`);
  }
  return response.json();
}
```

## Environment Routing

```typescript
const MAILTRAP_ENDPOINT = process.env.NODE_ENV === "production"
  ? "https://send.api.mailtrap.io/api/send"
  : `https://sandbox.api.mailtrap.io/api/send/${process.env.MAILTRAP_INBOX_ID}`;
```

## Pitfalls

| Mistake | Consequence | Fix |
| --- | --- | --- |
| Production endpoint in dev/test | Test emails reach real inboxes; spam complaints, leaked test data | Route non-production to the sandbox endpoint |
| Sending before domain verification | Silent failures or spam-folder placement | Verify SPF/DKIM/DMARC first |
| One token shared across environments | No isolation between sandbox and production | Separate env vars per environment |
| Assuming success | Users silently never receive password resets etc. | Check response status; log recipient, template, timestamp, response code on failure |
