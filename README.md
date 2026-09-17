
# Assignment 3 — Customer-Facing Resolution Agent

A complete offline Streamlit prototype for the AIONOS Assignment 3:
**Customer-Facing Resolution Agent — Airline Disruption**.

## What it demonstrates

- Intent understanding
- Minimal questioning / direct resolution when enough information exists
- Source-grounded customer and booking lookup
- Policy-based action selection
- Handling angry/frustrated customers
- Escalation when the agent lacks authority
- Clear action/conversation record
- All three required scenarios

## Source discipline

The app uses only the customer profiles, booking data, service rules, allowed/prohibited actions,
sample tone, and required scenarios supplied in the Assignment 3 data pack.

It does not call an external LLM or invent flight numbers, prices, compensation, or customer facts.

## Run locally

Python 3.10+ recommended.

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal.

## Demo

Select each customer from the left sidebar and use the quick-scenario buttons.

### Priya Nair
Shows:
- cancelled airline flight
- refund vs free rebooking choice
- Gold priority rebooking
- refusal of unsupported extra business-class compensation

### Arvind Kulkarni
Shows:
- 4-hour delay
- meal voucher + lounge access
- hotel request correctly declined because hotel applies only above 5 hours

### Meher Kaur
Shows:
- 6-hour delay
- meal voucher + lounge access + delayed-hours hotel
- full-night hotel request limited to delayed hours
- ₹2,000 higher-fare rebooking escalated because it exceeds ₹1,500 agent authority

## Suggested submission description

"This prototype implements a deterministic customer-resolution agent for airline disruptions.
It identifies customer intent, retrieves the matching customer/booking record, applies the supplied
service policy, executes only authorized actions, escalates prohibited/authority-limited requests,
and maintains an auditable conversation and action log."
