# Hermes session-header plugin

This standalone middleware attaches the current Hermes `session_id` as
`x-session-id` to every outbound LLM request, independent of model provider.

It intentionally does not attach pricing. Pricing is provider/model metadata and
belongs in the gateway's pricing catalog rather than in untrusted request headers.
