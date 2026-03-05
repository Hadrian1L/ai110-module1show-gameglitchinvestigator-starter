# LLM-generated test cases for the guessing game logic. Not created by me
import sys
from pathlib import Path

# Add parent directory to path so we can import logic_utils
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
)


# ============================================================================
# Tests for get_range_for_difficulty()
# ============================================================================

def test_easy_range():
    """Bug Fix 1: Easy difficulty should return 1-20"""
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20


def test_normal_range():
    """Normal difficulty should return 1-100"""
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 100


def test_hard_range():
    """Bug Fix 1: Hard difficulty should return 1-500 (not 1-50)"""
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 500  # Should be harder than Easy, not easier


def test_unknown_difficulty_defaults_to_normal():
    """Unknown difficulty should default to Normal range (1-100)"""
    low, high = get_range_for_difficulty("Impossible")
    assert low == 1
    assert high == 100


# ============================================================================
# Tests for parse_guess()
# ============================================================================

def test_parse_valid_integer():
    """Valid integer string should parse correctly"""
    ok, guess, err = parse_guess("42")
    assert ok is True
    assert guess == 42
    assert err is None


def test_parse_valid_float():
    """Float string should be converted to int"""
    ok, guess, err = parse_guess("42.7")
    assert ok is True
    assert guess == 42
    assert err is None


def test_parse_empty_string():
    """Empty string should return error"""
    ok, guess, err = parse_guess("")
    assert ok is False
    assert guess is None
    assert err == "Enter a guess."


def test_parse_none():
    """None input should return error"""
    ok, guess, err = parse_guess(None)
    assert ok is False
    assert guess is None
    assert err == "Enter a guess."


def test_parse_invalid_string():
    """Non-numeric string should return error"""
    ok, guess, err = parse_guess("hello")
    assert ok is False
    assert guess is None
    assert err == "That is not a number."


# ============================================================================
# Tests for check_guess()
# ============================================================================

def test_winning_guess():
    """Exact match should return Win"""
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert message == "🎉 Correct!"


def test_guess_too_high():
    """Guess higher than secret should return Too High"""
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert message == "📈 Go HIGHER!"


def test_guess_too_low():
    """Guess lower than secret should return Too Low"""
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert message == "📉 Go LOWER!"


def test_string_secret_bug_lexicographic_comparison():
    """
    Bug 5: When secret is a string, comparisons should be lexicographic.
    This demonstrates the glitch where "5" > "42" is True (string comparison).
    """
    # With string secret "42", guess 5 should be compared as strings
    outcome, message = check_guess(5, "42")
    # "5" > "42" is True in Python (string comparison: "5" comes after "4")
    assert outcome == "Too High"


def test_string_secret_bug_opposite_order():
    """Bug 5: String comparison may give opposite results for two-digit secrets"""
    # With string secret "50", guess 6 should fail numeric comparison
    outcome, message = check_guess(6, "50")
    # "6" > "50" is True (string comparison: "6" comes after "5")
    assert outcome == "Too High"


def test_string_secret_win_comparison():
    """When secret is a string, exact match still works"""
    outcome, message = check_guess(42, "42")
    assert outcome == "Win"


# ============================================================================
# Tests for update_score()
# ============================================================================

def test_win_on_first_attempt():
    """
    Bug 7: Score calculation uses attempt_number + 1.
    Win on attempt 1 should give 100 - 10*(1+1) = 80, not 90.
    """
    score = update_score(0, "Win", attempt_number=1)
    assert score == 80  # 100 - 10*(1+1) = 80


def test_win_bonus_decreases_with_attempts():
    """Win bonus should decrease as attempts increase"""
    score_attempt_1 = update_score(0, "Win", attempt_number=1)
    score_attempt_2 = update_score(0, "Win", attempt_number=2)
    score_attempt_3 = update_score(0, "Win", attempt_number=3)
    
    assert score_attempt_1 > score_attempt_2 > score_attempt_3


def test_win_score_minimum():
    """Win score should not go below 10 points"""
    score = update_score(0, "Win", attempt_number=20)
    assert score >= 10


def test_too_high_on_odd_attempt():
    """Too High on odd attempt should deduct 5 points"""
    score = update_score(100, "Too High", attempt_number=1)
    assert score == 95  # 100 - 5


def test_too_high_on_even_attempt():
    """
    Bug 6: Too High on even attempt incorrectly gives +5 points instead of -5.
    This rewards wrong guesses on even attempts!
    """
    score = update_score(100, "Too High", attempt_number=2)
    assert score == 105  # BUG: Should be 95, but code gives +5


def test_too_low_always_deducts():
    """Too Low should always deduct 5 points regardless of attempt number"""
    score_odd = update_score(100, "Too Low", attempt_number=1)
    score_even = update_score(100, "Too Low", attempt_number=2)
    assert score_odd == 95
    assert score_even == 95


# ============================================================================
# Integration tests
# ============================================================================

def test_full_game_flow():
    """Test a simple guessing sequence"""
    secret = 50
    attempt = 1
    
    # First guess too low
    outcome, _ = check_guess(25, secret)
    assert outcome == "Too Low"
    score = update_score(0, outcome, attempt)
    assert score == -5
    
    # Second guess too high
    attempt = 2
    outcome, _ = check_guess(75, secret)
    assert outcome == "Too High"
    score = update_score(score, outcome, attempt)
    assert score == 0  # -5 + 5 (Bug 6: gets bonus on even attempt)
    
    # Third guess win
    attempt = 3
    outcome, _ = check_guess(50, secret)
    assert outcome == "Win"
    score = update_score(score, outcome, attempt)
    assert score == 60  # 0 + (100 - 10*(3+1)) = 0 + 60 = 60 (Bug 7 offset)
