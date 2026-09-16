import sys

sys.stdout.reconfigure(encoding='utf-8')

diagram = r"""                         Program
                            │
                            ▼
                    ┌───────────────┐
                    │  Condition?   │
                    └───────┬───────┘
                            │
              ┌─────────────┴─────────────┐
          [ True ]                    [ False ]
              │                           │
              ▼                           ▼
       ┌──────────────┐         ┌───────────────────┐
       │   if Block   │         │ Another Condition?│
       │  (Executes)  │         │    (else if)      │
       └──────┬───────┘         └─────────┬─────────┘
              │                           │
              │             ┌─────────────┴─────────────┐
              │         [ True ]                    [ False ]
              │             │                           │
              │             ▼                           ▼
              │     ┌───────────────┐            ┌──────────────┐
              │     │ else if Block │            │  else Block  │
              │     │  (Executes)   │            │  (Fallback)  │
              │     └───────┬───────┘            └──────┬───────┘
              │             │                           │
              └─────────────┴─────────────┬─────────────┘
                                          │
                                          ▼
                                   Program Continues"""

for line in diagram.splitlines():
    print(line)
