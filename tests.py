# tests.py

import pytest

from solution import EventRegistration, UserStatus, DuplicateRequest, NotFound


def test_register_until_capacity_then_waitlist_fifo_positions():
    er = EventRegistration(capacity=2)

    s1 = er.register("u1")
    s2 = er.register("u2")
    s3 = er.register("u3")
    s4 = er.register("u4")

    assert s1 == UserStatus("registered")
    assert s2 == UserStatus("registered")
    assert s3 == UserStatus("waitlisted", 1)
    assert s4 == UserStatus("waitlisted", 2)

    snap = er.snapshot()
    assert snap["registered"] == ["u1", "u2"]
    assert snap["waitlist"] == ["u3", "u4"]


def test_cancel_registered_promotes_earliest_waitlisted_fifo():
    er = EventRegistration(capacity=1)
    er.register("u1")
    er.register("u2")  # waitlist
    er.register("u3")  # waitlist

    er.cancel("u1")  # should promote u2

    assert er.status("u1") == UserStatus("none")
    assert er.status("u2") == UserStatus("registered")
    assert er.status("u3") == UserStatus("waitlisted", 1)

    snap = er.snapshot()
    assert snap["registered"] == ["u2"]
    assert snap["waitlist"] == ["u3"]


def test_duplicate_register_raises_for_registered_and_waitlisted():
    er = EventRegistration(capacity=1)
    er.register("u1")
    with pytest.raises(DuplicateRequest):
        er.register("u1")

    er.register("u2")  # waitlisted
    with pytest.raises(DuplicateRequest):
        er.register("u2")


def test_waitlisted_cancel_removes_and_updates_positions():
    er = EventRegistration(capacity=1)
    er.register("u1")
    er.register("u2")  # waitlist pos1
    er.register("u3")  # waitlist pos2

    er.cancel("u2")    # remove from waitlist

    assert er.status("u2") == UserStatus("none")
    assert er.status("u3") == UserStatus("waitlisted", 1)

    snap = er.snapshot()
    assert snap["registered"] == ["u1"]
    assert snap["waitlist"] == ["u3"]


def test_capacity_zero_all_waitlisted_and_promotion_never_happens():
    er = EventRegistration(capacity=0)
    assert er.register("u1") == UserStatus("waitlisted", 1)
    assert er.register("u2") == UserStatus("waitlisted", 2)

    # No one can ever be registered when capacity=0
    assert er.status("u1") == UserStatus("waitlisted", 1)
    assert er.status("u2") == UserStatus("waitlisted", 2)
    assert er.snapshot()["registered"] == []

    # Cancel unknown should raise NotFound
    with pytest.raises(NotFound):
        er.cancel("missing")



#################################################################################
# Add your own additional tests here to cover more cases and edge cases as needed.
#################################################################################


# Validates FIFO promotion order under multiple cancellations and deterministic behavior.
def test_multiple_cancellations_promote_in_fifo_order():
    er = EventRegistration(capacity=2)
    er.register("u1")
    er.register("u2")
    er.register("u3")  # waitlist 1
    er.register("u4")  # waitlist 2
    er.register("u5")  # waitlist 3

    er.cancel("u1")
    assert er.snapshot()["registered"] == ["u2", "u3"]
    assert er.snapshot()["waitlist"] == ["u4", "u5"]

    er.cancel("u2")
    assert er.snapshot()["registered"] == ["u3", "u4"]
    assert er.snapshot()["waitlist"] == ["u5"]

    assert er.status("u3") == UserStatus("registered")
    assert er.status("u4") == UserStatus("registered")
    assert er.status("u5") == UserStatus("waitlisted", 1)


# Validates re-registration after cancellation is allowed and treated as a new incoming request.
def test_reregister_after_cancel_goes_to_end_based_on_current_state():
    er = EventRegistration(capacity=1)
    er.register("u1")
    er.cancel("u1")

    assert er.status("u1") == UserStatus("none")
    assert er.register("u1") == UserStatus("registered")
    assert er.snapshot()["registered"] == ["u1"]
    assert er.snapshot()["waitlist"] == []


# Validates that a previously waitlisted user can cancel and later register again with a fresh position.
def test_waitlisted_user_can_cancel_and_reregister():
    er = EventRegistration(capacity=1)
    er.register("u1")
    er.register("u2")  # waitlist 1
    er.register("u3")  # waitlist 2

    er.cancel("u2")
    assert er.status("u2") == UserStatus("none")
    assert er.status("u3") == UserStatus("waitlisted", 1)

    assert er.register("u2") == UserStatus("waitlisted", 2)
    assert er.snapshot()["waitlist"] == ["u3", "u2"]


# Validates that querying status does not modify system state.
def test_status_is_read_only_and_does_not_change_snapshot():
    er = EventRegistration(capacity=2)
    er.register("u1")
    er.register("u2")
    er.register("u3")

    before = er.snapshot()
    assert er.status("u2") == UserStatus("registered")
    assert er.status("u3") == UserStatus("waitlisted", 1)
    assert er.status("missing") == UserStatus("none")
    after = er.snapshot()

    assert before == after


# Validates registered-list ordering: promoted users append to the end of registered order.
def test_promoted_user_appends_to_end_of_registered_order():
    er = EventRegistration(capacity=2)
    er.register("u1")
    er.register("u2")
    er.register("u3")

    er.cancel("u1")

    assert er.snapshot()["registered"] == ["u2", "u3"]
    assert er.status("u2") == UserStatus("registered")
    assert er.status("u3") == UserStatus("registered")


# Validates cancellation of an unknown user raises NotFound consistently.
def test_cancel_unknown_user_raises_not_found():
    er = EventRegistration(capacity=2)
    er.register("u1")

    with pytest.raises(NotFound):
        er.cancel("does_not_exist")


# Validates waitlist positions remain 1-based and update after front removal.
def test_waitlist_positions_update_after_front_waitlisted_cancel():
    er = EventRegistration(capacity=1)
    er.register("u1")
    er.register("u2")  # pos 1
    er.register("u3")  # pos 2
    er.register("u4")  # pos 3

    er.cancel("u2")

    assert er.status("u3") == UserStatus("waitlisted", 1)
    assert er.status("u4") == UserStatus("waitlisted", 2)
    assert er.snapshot()["waitlist"] == ["u3", "u4"]


# Validates capacity=0 keeps all users on waitlist and allows waitlisted cancellation.
def test_capacity_zero_waitlisted_cancel_updates_positions():
    er = EventRegistration(capacity=0)
    er.register("u1")
    er.register("u2")
    er.register("u3")

    er.cancel("u2")

    assert er.snapshot()["registered"] == []
    assert er.snapshot()["waitlist"] == ["u1", "u3"]
    assert er.status("u1") == UserStatus("waitlisted", 1)
    assert er.status("u3") == UserStatus("waitlisted", 2)


# Validates negative capacity is rejected.
def test_negative_capacity_raises_value_error():
    with pytest.raises(ValueError):
        EventRegistration(-1)


# Validates duplicate detection still holds after promotion changes state.
def test_promoted_user_cannot_register_again():
    er = EventRegistration(capacity=1)
    er.register("u1")
    er.register("u2")
    er.cancel("u1")  # promotes u2

    assert er.status("u2") == UserStatus("registered")
    with pytest.raises(DuplicateRequest):
        er.register("u2")
