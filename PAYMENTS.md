# Quantum Payments & Credits

Standard payment contract shared with Quantum Mirror Wonderland.

- Prepaid generation credits; never grant credits before a verified payment event.
- Payment events must be authenticated, idempotent, and auditable.
- Stripe and crypto providers are supported through provider adapters/webhooks.
- Never store cryptocurrency private keys or custody funds in this repository.
- Production balances and ledger entries must be persisted transactionally (PostgreSQL recommended).
- Generation jobs should reserve credits before work and release them on failure.
- Configure provider secrets only through the deployment secret manager; never commit them.

This repository can consume the shared credit contract without coupling its application logic to a specific payment provider.
