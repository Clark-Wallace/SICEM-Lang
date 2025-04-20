import json
from pathlib import Path
import pytest

from slang_validate_cli import validate_slang_file

HOTEL_SLUG = '''
system: HotelBooking
function: book_hotel
agent: HotelBookingAI
intent: Reserve a hotel room
context:
  location: "Beach City"
  check_in_date: "2025-05-01"
  check_out_date: "2025-05-05"
  max_price_per_night: 100
  room_type: "standard"
input: N/A
output: booking_confirmation
'''

HOTEL_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "HotelBookingContext",
    "type": "object",
    "properties": {
        "location": {"type": "string"},
        "check_in_date": {"type": "string"},
        "check_out_date": {"type": "string"},
        "max_price_per_night": {"type": "number"},
        "room_type": {"type": "string"}
    },
    "required": ["location", "check_in_date", "check_out_date", "max_price_per_night", "room_type"]
}

def test_validate_with_schema_success(tmp_path):
    slang_file = tmp_path / "hotel.slang"
    slang_file.write_text(HOTEL_SLUG)
    schema_file = tmp_path / "hotel_schema.json"
    schema_file.write_text(json.dumps(HOTEL_SCHEMA))
    assert validate_slang_file(str(slang_file), str(schema_file))

def test_validate_with_schema_failure(tmp_path):
    # Remove required field 'room_type'
    invalid_slug = HOTEL_SLUG.replace('  room_type: \"standard\"\n', '')
    slang_file = tmp_path / "hotel_invalid.slang"
    slang_file.write_text(invalid_slug)
    schema_file = tmp_path / "hotel_schema.json"
    schema_file.write_text(json.dumps(HOTEL_SCHEMA))
    assert not validate_slang_file(str(slang_file), str(schema_file))