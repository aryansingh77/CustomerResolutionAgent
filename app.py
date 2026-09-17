
import streamlit as st
from datetime import datetime

# ============================================================
# Assignment 3 — Customer-Facing Resolution Agent
# Airline Disruption
# Source of truth: Assignment 3 Data Pack
# ============================================================

CUSTOMERS = {
    "Priya Nair": {
        "tier": "Gold",
        "pnr": "SK4821X",
        "contact": "priya.nair@example.com, +91-98xxxxxxx1",
        "history": "6 flights, 1 prior complaint (delayed baggage, resolved with voucher)",
        "flights": {
            "SK-204": {
                "route": "Delhi → Goa",
                "date": "Wed 23 Sep 2026",
                "departure": "18:40",
                "status": "Cancelled (operational reasons)",
            },
            "Return": {
                "route": "Goa → Delhi",
                "date": "Fri 25 Sep 2026",
                "departure": "16:20",
                "status": "Unaffected",
            },
        },
    },
    "Arvind Kulkarni": {
        "tier": "Silver",
        "pnr": "TR1190B",
        "contact": "arvind.kulkarni@example.com, +91-98xxxxxxx2",
        "history": "3 flights, no prior complaints",
        "flights": {
            "SK-118": {
                "route": "Mumbai → Bengaluru",
                "date": "Wed 23 Sep 2026",
                "departure": "11:10",
                "status": "Delayed 4h (originally 07:10)",
            }
        },
    },
    "Meher Kaur": {
        "tier": "Platinum",
        "pnr": "WL7742",
        "contact": "meher.kaur@example.com, +91-98xxxxxxx3",
        "history": "10 flights, 1 prior complaint (overbooking, resolved with a tier-status upgrade)",
        "flights": {
            "SK-305": {
                "route": "Delhi → Hyderabad",
                "date": "Wed 23 Sep 2026",
                "departure": "20:00",
                "status": "Delayed 6h (originally 14:00)",
            }
        },
    },
}

POLICIES = {
    "cancel_rebook": "If a flight is cancelled by the airline, the customer may choose free rebooking on the next available flight within 24 hours or a full refund.",
    "delay_under_3": "Delay under 3 hours: ₹500 meal voucher.",
    "delay_over_3": "Delay more than 3 hours: meal voucher + lounge access.",
    "delay_over_5": "Delay more than 5 hours: meal voucher + hotel accommodation covering only the delayed hours, not a full night's stay.",
    "refund": "Airline-caused cancellation refunds are processed in full within 7 business days to the original payment method only.",
    "fare_difference": "For voluntary rebooking onto a higher-fare flight, the customer pays the fare difference. Agents cannot waive fare differences above ₹1,500 without supervisor approval.",
    "loyalty": "Gold and Platinum customers get priority rebooking, but no additional compensation beyond standard policy.",
}

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def detect_intent(message: str):
    m = message.lower()

    if any(x in m for x in ["legal action", "lawyer", "court", "formal complaint", "file a complaint"]):
        return "legal_or_formal_complaint"

    if any(x in m for x in ["refund", "money back", "cash back"]):
        return "refund"

    if any(x in m for x in ["rebook", "another flight", "different flight", "move me", "change flight"]):
        return "rebooking"

    if any(x in m for x in ["upgrade", "business class"]):
        return "upgrade"

    if any(x in m for x in ["hotel", "accommodation", "stay"]):
        return "hotel"

    if any(x in m for x in ["compensation", "compensate", "voucher", "lounge"]):
        return "compensation"

    if any(x in m for x in ["cancelled", "canceled", "cancel"]):
        return "cancellation"

    if any(x in m for x in ["delay", "delayed", "late"]):
        return "delay"

    if any(x in m for x in ["furious", "angry", "unacceptable", "frustrated", "terrible"]):
        return "emotional_distress"

    return "status_or_general"

def customer_for_pnr(pnr):
    for name, customer in CUSTOMERS.items():
        if customer["pnr"].lower() == pnr.lower():
            return name, customer
    return None, None

def add_action(action, status, reason):
    st.session_state.action_log.append({
        "time": now(),
        "action": action,
        "status": status,
        "reason": reason,
    })

def respond(customer_name, message):
    customer = CUSTOMERS[customer_name]
    intent = detect_intent(message)

    # Immediate escalation required by policy.
    if intent == "legal_or_formal_complaint":
        add_action(
            "Escalate to specialist/human support",
            "ESCALATED",
            "Threat of legal action or formal complaint requires immediate escalation."
        )
        return (
            "I hear you, and I’m sorry this has been frustrating. "
            "Because you mentioned legal action or a formal complaint, I’m escalating "
            "this to specialist support now. A human agent will handle the next step."
        )

    # Priya's cancellation flow.
    if customer_name == "Priya Nair":
        if intent in {"cancellation", "rebooking", "refund", "upgrade", "emotional_distress"}:
            if "business" in message.lower() or "upgrade" in message.lower():
                add_action(
                    "Reject additional business-class upgrade request",
                    "NOT AUTHORIZED",
                    "The data pack permits standard-policy handling only; Gold status gives priority rebooking but no extra compensation."
                )
                return (
                    "I understand why you’re asking for something extra after the cancellation. "
                    "Your SK-204 was cancelled for operational reasons. Under the policy, "
                    "you can choose either free rebooking on the next available flight within "
                    "24 hours or a full refund. Your Gold status gives you priority access to "
                    "the next available seats, but it does not provide additional compensation "
                    "such as a free business-class upgrade."
                )

            if intent == "refund":
                add_action(
                    "Initiate full refund request",
                    "EXECUTED",
                    "Airline-caused cancellation qualifies for a full refund."
                )
                return (
                    "Your SK-204 cancellation qualifies for a full refund. I can initiate the "
                    "refund request now. It will be processed within 7 business days and returned "
                    "to the original payment method only. Your return Goa → Delhi flight on "
                    "25 Sep at 16:20 is unaffected."
                )

            add_action(
                "Offer cancellation resolution choice",
                "READY",
                "Customer is entitled to free rebooking within 24 hours or a full refund."
            )
            return (
                "I understand the frustration. Your SK-204 from Delhi to Goa was cancelled "
                "for operational reasons. You have two options under the policy: "
                "(1) free rebooking on the next available flight within 24 hours, with Gold "
                "priority rebooking, or (2) a full refund to the original payment method "
                "within 7 business days. Which would you prefer?"
            )

    # Arvind's 4-hour delay.
    if customer_name == "Arvind Kulkarni":
        if intent in {"delay", "hotel", "compensation", "emotional_distress"}:
            if intent == "hotel":
                add_action(
                    "Decline hotel request",
                    "NOT ELIGIBLE",
                    "A 4-hour delay qualifies for meal voucher + lounge access, not hotel accommodation."
                )
                add_action(
                    "Issue meal voucher + lounge access",
                    "EXECUTED",
                    "Delay is more than 3 hours."
                )
                return (
                    "I understand that missing your meeting is frustrating. Your SK-118 is "
                    "delayed by 4 hours, from 07:10 to 11:10. Under the policy, a delay of more "
                    "than 3 hours qualifies for a meal voucher and lounge access. Hotel "
                    "accommodation applies only when the delay is more than 5 hours, so I cannot "
                    "provide a hotel for this 4-hour delay."
                )

            add_action(
                "Issue meal voucher + lounge access",
                "EXECUTED",
                "Delay is more than 3 hours."
            )
            return (
                "I’m sorry about the disruption. Your SK-118 is delayed by 4 hours and now "
                "departs at 11:10. Under the policy, I can provide a meal voucher and lounge "
                "access. The hotel accommodation rule does not apply because the delay is not "
                "more than 5 hours."
            )

    # Meher's 6-hour delay.
    if customer_name == "Meher Kaur":
        if intent in {"delay", "hotel", "compensation", "emotional_distress"}:
            if intent == "hotel":
                add_action(
                    "Arrange hotel accommodation for delayed hours",
                    "EXECUTED",
                    "Delay is more than 5 hours."
                )
                return (
                    "Your 6-hour delay qualifies for hotel accommodation under the policy. "
                    "However, the policy covers only the delayed-hours portion; it does not "
                    "cover a full night's stay. I can arrange the eligible delayed-hours "
                    "accommodation."
                )

            if intent == "compensation":
                add_action(
                    "Issue meal voucher + lounge access + hotel accommodation",
                    "EXECUTED",
                    "6-hour delay qualifies for all applicable delay benefits."
                )
                return (
                    "Your SK-305 is delayed by 6 hours. Under the policy, this qualifies for "
                    "a meal voucher, lounge access, and hotel accommodation covering the "
                    "delayed hours only."
                )

            add_action(
                "Apply 6-hour delay benefits",
                "EXECUTED",
                "Delay is more than 5 hours."
            )
            return (
                "I’m sorry for the 6-hour disruption. Your SK-305 now departs at 20:00. "
                "Under the policy, the delay qualifies for a meal voucher, lounge access, "
                "and hotel accommodation covering only the delayed hours."
            )

        if intent == "rebooking":
            add_action(
                "Escalate higher-fare rebooking request",
                "ESCALATED",
                "The requested higher-fare flight has a ₹2,000 fare difference, above the ₹1,500 agent waiver authority."
            )
            return (
                "I can help with the rebooking request, but the requested higher-fare flight "
                "has a ₹2,000 fare difference. Agents cannot waive fare differences above "
                "₹1,500 without supervisor approval, so this request must be escalated to a "
                "supervisor. Your Platinum status provides priority rebooking, but it does not "
                "remove the fare-difference rule."
            )

        if intent == "upgrade":
            add_action(
                "Clarify upgrade/rebooking authority",
                "ESCALATED",
                "A higher-fare flight with ₹2,000 difference exceeds the agent's ₹1,500 waiver authority."
            )
            return (
                "I can’t waive the ₹2,000 fare difference at agent level. Because it exceeds "
                "the ₹1,500 waiver authority, I’m escalating this to a supervisor for approval."
            )

    # General information fallback.
    add_action(
        "Provide booking/status information",
        "INFO",
        "Customer requested information supported by the booking data."
    )
    flight_text = []
    for flight, data in customer["flights"].items():
        flight_text.append(
            f"{flight}: {data['route']}, {data['date']}, departure {data['departure']}, {data['status']}"
        )
    return (
        f"Your booking reference is {customer['pnr']} and your loyalty tier is {customer['tier']}. "
        + " | ".join(flight_text)
        + ". What would you like me to help you resolve?"
    )

def reset_chat():
    st.session_state.messages = []
    st.session_state.action_log = []

st.set_page_config(page_title="Customer Resolution Agent", page_icon="✈️", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "action_log" not in st.session_state:
    st.session_state.action_log = []

st.title("✈️ Customer-Facing Resolution Agent")
st.caption("Assignment 3 — Airline Disruption Prototype | Offline, deterministic, source-grounded")

with st.sidebar:
    st.header("Customer")
    customer_name = st.selectbox("Select customer", list(CUSTOMERS.keys()))

    st.divider()
    st.subheader("Quick scenario")
    presets = {
        "Priya Nair": [
            "My flight was cancelled. I want a full refund and a free business class upgrade on my return flight.",
            "I am furious about this cancellation.",
            "I want a refund."
        ],
        "Arvind Kulkarni": [
            "My flight is delayed 4 hours and I need a hotel because this ruined my meeting.",
            "What compensation do I get for the delay?"
        ],
        "Meher Kaur": [
            "I want a full night's hotel stay because of this 6 hour delay.",
            "Move me to a different higher-fare flight. The fare difference is ₹2,000.",
            "I am extremely frustrated."
        ],
    }

    for i, p in enumerate(presets[customer_name]):
        if st.button(p, key=f"preset_{customer_name}_{i}", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": p})
            answer = respond(customer_name, p)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()

    st.divider()
    if st.button("Reset conversation", use_container_width=True):
        reset_chat()
        st.rerun()

    st.subheader("Customer data")
    c = CUSTOMERS[customer_name]
    st.write(f"**Tier:** {c['tier']}")
    st.write(f"**PNR:** {c['pnr']}")
    st.write(f"**History:** {c['history']}")

col1, col2 = st.columns([2.1, 1])

with col1:
    st.subheader(f"Conversation — {customer_name}")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Type the customer's message…")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        answer = respond(customer_name, user_input)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()

with col2:
    st.subheader("Action Record")
    if not st.session_state.action_log:
        st.info("No actions yet.")
    else:
        for item in reversed(st.session_state.action_log):
            with st.container(border=True):
                st.write(f"**{item['action']}**")
                st.caption(f"{item['time']} · {item['status']}")
                st.write(item["reason"])

    st.subheader("Policy Engine")
    st.write("**Cancellation:** Free rebooking within 24h OR full refund.")
    st.write("**Delay >3h:** Meal voucher + lounge.")
    st.write("**Delay >5h:** Meal voucher + lounge + delayed-hours hotel.")
    st.write("**Fare waiver limit:** ₹1,500; above this requires supervisor.")
    st.write("**Legal/formal complaint:** Immediate human escalation.")
