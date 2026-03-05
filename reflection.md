# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

 Hard mode is actually easier than the other modes
 Hard coded info bar line always says guess from 1 - 100 regardless of difficultly
 Looks like the player loses a turn from the intended? Code starts at -1 attempts automatically

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

Claude, just asked it to analyze files and also confirm what I see as bugs when testing the game

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

Just manually looked at if the range was better fitted for the difficultly, also not hard coded

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?
Secret in memory never actaully changed, it's because it was type converted into a string which would change it's lexigraphic number 
Stremlit is like a whiteboard, everytime something happens streamlit erases it and redraws it. That's a rerun
just remove the alternating from string to int

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
Definitely using AI as a tool, manually verifying everything and lookng at diffs
Have it mainly as a debugger, while I write the actual code
LLMs are great tools to be used, not a thinker, it should be used as a tool mainly to support learning/efficency
