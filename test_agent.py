
from app import detect_intent, CUSTOMERS

def test_intents():
    assert detect_intent("I want a refund") == "refund"
    assert detect_intent("Please rebook me") == "rebooking"
    assert detect_intent("I need a hotel") == "hotel"
    assert detect_intent("I will take legal action") == "legal_or_formal_complaint"
    assert detect_intent("I am furious") == "emotional_distress"

def test_customer_data():
    assert CUSTOMERS["Priya Nair"]["pnr"] == "SK4821X"
    assert CUSTOMERS["Arvind Kulkarni"]["pnr"] == "TR1190B"
    assert CUSTOMERS["Meher Kaur"]["pnr"] == "WL7742"
