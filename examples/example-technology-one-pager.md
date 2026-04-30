# Example: OpenTelemetry — Architecture One Pager

## Executive summary

OpenTelemetry is an open standard and tooling ecosystem for collecting telemetry data such as traces, metrics and logs. It is relevant for organizations that need better observability across distributed systems, cloud platforms and microservices. The main architectural value is reduced vendor lock-in for telemetry and a more consistent instrumentation model. Recommended position: **Trial**.

## Classification

- Type: Technology / standard ecosystem
- Maturity: Growing to established
- Recommended position: Trial
- Confidence: Medium

## What it is

OpenTelemetry provides APIs, SDKs and collectors for generating and exporting telemetry data from applications and infrastructure. It aims to make observability data portable across tools and vendors.

## Why it matters

For architecture teams, OpenTelemetry can support better runtime insight, incident analysis, service dependency understanding and platform standardization.

## Typical use cases

- Distributed tracing across microservices
- Standardized metrics and logs collection
- Reducing observability vendor lock-in
- Platform-wide telemetry conventions
- Supporting SRE and DevOps practices

## Architecture impact

| Area | Impact |
|---|---|
| Application architecture | Requires instrumentation patterns and conventions |
| Integration | Improves visibility across service calls |
| Operations | Enables more consistent monitoring and diagnostics |
| Governance | Requires shared telemetry standards |
| Sourcing | Can reduce dependency on proprietary agents |

## Recommendation

**Trial.**

Run a controlled pilot for selected services and define telemetry conventions before broader rollout.
