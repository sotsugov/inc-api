from utils.credits import calculate_credits


def test_empty_message():
    # Tests that an empty message returns base cost of 1 credit
    message = ""
    expected_result = {
        "credits_used": 1,
        "base_cost": 1,
        "char_count_cost": 0,
        "word_length_cost": 0,
        "third_vowel_cost": 0,
        "length_penalty": 0,
        "unique_word_bonus": 0,
        "palindrome_multiplier": 1,
    }

    assert calculate_credits(message) == expected_result


def test_message_baseline():
    # Tests a standard message with multiple cost components
    message = "Are there any restrictions on alterations or improvements?"
    expected_result = {
        "credits_used": 5.2,
        "base_cost": 1,
        "char_count_cost": 2.9,
        "word_length_cost": 1.5,
        "third_vowel_cost": 1.8,
        "length_penalty": 0,
        "unique_word_bonus": -2,
        "palindrome_multiplier": 1,
    }

    assert calculate_credits(message) == expected_result


def test_palindrome():
    # Tests that a palindrome properly doubles the final cost
    message = "Madam, I'm Adam"
    expected_result = {
        "credits_used": 2.0,
        "base_cost": 1,
        "char_count_cost": 0.75,
        "word_length_cost": 0.5,
        "third_vowel_cost": 0.3,
        "length_penalty": 0,
        "unique_word_bonus": -2,
        "palindrome_multiplier": 2,
    }

    assert calculate_credits(message) == expected_result


def test_length_penalty():
    # Tests that messages over 100 characters receive the proper penalty
    message = (
        "This is an exceptionally long message that should definitely trigger "
        "the length penalty because it exceeds one hundred characters quite handily."
    )
    expected_result = {
        "credits_used": 21.2,
        "base_cost": 1.0,
        "char_count_cost": 7.20,
        "word_length_cost": 4.0,
        "third_vowel_cost": 6.0,
        "length_penalty": 5.0,
        "unique_word_bonus": -2.0,
        "palindrome_multiplier": 1.0,
    }

    assert calculate_credits(message) == expected_result


def test_third_vowel_positions():
    # Tests proper counting of vowels in third positions
    message = "The quick brown fox"
    expected_result = {
        "credits_used": 1.45,
        "base_cost": 1.0,
        "char_count_cost": 0.95,
        "word_length_cost": 0.6,
        "third_vowel_cost": 0.9,
        "length_penalty": 0.0,
        "unique_word_bonus": -2.0,
        "palindrome_multiplier": 1.0,
    }

    assert calculate_credits(message) == expected_result


def test_minimum_credit():
    # Tests that credits cannot go below 1 even with unique word bonus
    message = "Hi"
    expected_result = {
        "credits_used": 1,
        "base_cost": 1,
        "char_count_cost": 0.1,
        "word_length_cost": 0.1,
        "third_vowel_cost": 0,
        "length_penalty": 0,
        "unique_word_bonus": -2,
        "palindrome_multiplier": 1,
    }

    assert calculate_credits(message) == expected_result


def test_word_length_categories():
    # Tests different word length categories for proper credit calculation
    message = "I am programming"
    expected_result = {
        "credits_used": 1.0,
        "base_cost": 1,
        "char_count_cost": 0.80,
        "word_length_cost": 0.5,
        "third_vowel_cost": 0.3,
        "length_penalty": 0,
        "unique_word_bonus": -2,
        "palindrome_multiplier": 1,
    }
    assert calculate_credits(message) == expected_result


def test_special_characters():
    # Tests that special characters are properly handled in the calculation
    message = "Hello! @#$% World?"
    expected_result = {
        "credits_used": 1.0,
        "base_cost": 1,
        "char_count_cost": 0.90,
        "word_length_cost": 0.4,
        "third_vowel_cost": 0.0,
        "length_penalty": 0,
        "unique_word_bonus": -2,
        "palindrome_multiplier": 1,
    }
    assert calculate_credits(message) == expected_result
