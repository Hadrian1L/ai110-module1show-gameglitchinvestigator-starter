# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose.
- [x] Detail which bugs you found.
- [x] Explain what fixes you applied.

### Game Purpose
The application is a number guessing game where players try to guess a secret number with a difficulty range. The game provides feedback, tracks attempts and scores, and includes three difficulty levels with varying attempt limits.

### Bugs Found

1. **Bug 1 — Hard difficulty has easier range than Easy**
   - Hard returned 1-50 instead of something harder (1-500)
   - Made Hard mode paradoxically easier than Easy mode

2. **Bug 2 — Attempts initialized to 1 instead of 0**
   - Players started with `attempts = 1`, losing their first attempt before guessing
   - Only after first "Submit" click would attempts increment normally

3. **Bug 3 — Hardcoded range in info message**
   - Message always said "Guess a number between 1 and 100"
   - Ignored actual difficulty-based range (Easy: 1-20, Hard: 1-500)

5. **Bug 4 — Secret converted to string on even attempts**
   - `if st.session_state.attempts % 2 == 0: secret = str(st.session_state.secret)`
   - Causes lexicographic string comparison: "5" > "42" returns True (wrong hints!)

### Fixes Applied

1. ✅ Changed Hard difficulty range from 1-50 to 1-500
2. ✅ Changed attempts initialization from 1 to 0
3. ✅ Updated info message to use `low` and `high` variables
5. ✅ Removed the string conversion: `secret = st.session_state.secret` (always keeps as int)
8. ✅ **Refactored logic functions** to `logic_utils.py`:
   - `get_range_for_difficulty()`
   - `parse_guess()`
   - `check_guess()`
   - `update_score()`
9. ✅ **Created comprehensive pytest suite** (22 tests) to verify fixes and detect remaining bugs 

## 📸 Demo

- [ ] [Insert a screenshot of your fixed, winning game here]
