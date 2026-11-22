# Roadmap

Each item is one small, tested slice.

- [x] 1. Installable addon with the payee model
- [ ] 2. Payee verification states (draft, verified, blocked)
- [ ] 3. Payout user and manager groups, access rights
- [ ] 4. Multi-company record rules
- [ ] 5. Ledger entries (earnings, adjustments)
- [ ] 6. Immutable ledger: block edits and deletes
- [ ] 7. Computed payee balance
- [ ] 8. Payout model with sequence
- [ ] 9. Payout state machine (draft, approved, processing, paid, failed)
- [ ] 10. Payout batch grouping several payouts
- [ ] 11. Approval rule: the creator cannot approve their own batch
- [ ] 12. Reserve balance with row locking (no double spending)
- [ ] 13. Idempotency key with a unique constraint
- [ ] 14. Provider interface and mock provider
- [ ] 15. Send payouts through the provider
- [ ] 16. Signed webhook endpoint
- [ ] 17. Duplicate and out-of-order webhook handling
- [ ] 18. Scheduled retry with backoff
- [ ] 19. Payee statement report
- [ ] 20. Accounting entries (bridge addon)
