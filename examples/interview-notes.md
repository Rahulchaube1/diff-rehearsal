# Diff Rehearsal

Reject orders that exceed available stock

Commit 2b31542c7903d1b31774f6dcec14cd4531808a66

## Context

What problem was worth changing?

A request for three units when only two were available returned negative one. A caller could treat that as a successful reservation.

## Decision

Why put this change in reservations.py? Describe one other place or layer you considered.

I put the guard in reserve() so callers share the same rule. Checking only in the order form would leave other callers able to subtract too much.

## Verification

Walk through one case in tests/test_reservations.py. What nearby failure could still pass that check?

The test calls reserve(2, 3) and expects ValueError. Changing > to >= would still pass. I would add reserve(2, 2) and assert that it returns 0.

## Outcome

What happened after this change reached users?

The example shows a guard and a regression test. I have no production measurements. I would check how often accepted orders exceed available stock after rollout.
