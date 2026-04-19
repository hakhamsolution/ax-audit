# AX_DATA_TENANCY_AND_RETENTION_POLICY

Version: 2026-04-18 v1  
Status: required data-handling policy

## 1. Purpose

This document defines minimum policy for tenant separation, data retention, deletion, and handling of regulated or sensitive client data.

This is required because the AX system may interact with businesses in regulated or confidentiality-sensitive domains, including healthcare, tax/accounting, and legal services.

## 2. Policy objective

The system must not behave as if all business data belongs to one shared workspace.

Tenant separation is mandatory.

## 3. Tenant model

A tenant is any distinct business or client boundary whose data must not be mixed without explicit authorization.

Examples:
- Hakam Solution internal operations
- Abel internal operations
- veterinary research workspace
- clinic client A
- accounting client B
- legal client C

## 4. Data classes

### Class A — public or low-risk operational data
Examples:
- public marketing drafts
- non-sensitive planning notes

### Class B — internal business data
Examples:
- internal strategy notes
- unpublished campaign assets
- internal operational logs without personal data

### Class C — confidential client data
Examples:
- client communications
- proposal drafts
- business records tied to a client
- non-public project documents

### Class D — regulated or highly sensitive data
Examples:
- patient-related healthcare data
- legal-case-sensitive materials
- tax/accounting records with personal or financial identifiers
- identity documents
- secrets and credentials

## 5. Tenant isolation rule

Cross-tenant write access is forbidden by default.

A core agent or specialist must not:
- write one tenant’s data into another tenant’s workspace
- summarize or expose one tenant’s data in another tenant’s context
- share files or outputs across tenants unless a documented exception exists

## 6. Storage rule

Data should be separated by tenant in:
- storage paths
- automation jobs
- credentials
- channel routing
- review context

Recommended minimum separation:
- distinct folder roots
- distinct automation identifiers
- distinct token scopes where possible
- distinct output destinations

## 7. Retention rule

Retention must be defined by data class.

Working default:
- Class A: retain as operationally useful
- Class B: review every 180 days
- Class C: review every 90 days
- Class D: retain only as legally or operationally required, with explicit owner

No data class may be “retain forever” by default.

## 8. Deletion triggers

Deletion or archival review must occur when one or more apply:
- project ended
- client relationship ended
- legal retention expired
- duplicate artifact superseded
- tenant requests deletion where legally allowed
- data classified into a stricter bucket than its current storage allows

## 9. Access rule

### Owner
May define policy and approve exceptional access.

### Operator
May maintain systems but does not automatically gain permission to inspect Class C or D content.

### Approver
May review workflow decisions but does not automatically gain unrestricted data visibility.

### Requester
Only sees outputs explicitly permitted for their tenant scope.

## 10. AI handling rule

Class D data must not be sent to a model or tool path unless:
- the path is explicitly approved,
- the tenancy boundary is preserved,
- the action is documented,
- and the risk is accepted by the responsible owner.

## 11. Archive-memory constraint

archive-memory is not a global memory sink.

archive-memory must:
- preserve tenant boundaries
- avoid cross-tenant synthesis by default
- store references or abstractions when full-content retention is unnecessary
- support deletion and retention review

## 12. Legal-sensitivity handling note

This document is an operating minimum, not legal advice.
Where law, contract, or professional confidentiality imposes stricter handling, the stricter rule wins.

## 13. Minimum audit items

For Class C and D handling, log:
- tenant
- actor
- action
- data class
- destination
- approval basis if any

## 14. Required follow-up

This policy requires a companion implementation map:
- tenant identifiers
- storage roots
- channel ownership by tenant
- automation IDs by tenant
- approved model/tool paths by data class

## 15. Instruction to future sessions

Do not assume all business data can share one context.
If a workflow crosses tenants, treat it as blocked until explicitly approved and documented.
