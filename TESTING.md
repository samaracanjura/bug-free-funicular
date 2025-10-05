# Testing Documentation - 2048 Game 
This document explains how to rest to test the 2048 game using deterministic seeds. 

## Understanding Seeds
A **seed** is a number that controls the random number generator, making the game's behavior predictable and repeatable. This is essential for: 
- ✅ Testing game logic consistently
- ✅ Reproducing and fixing bugs
- ✅ Verifying merge rules work correctly
- ✅ Grading and evaluation purposes

## How to Provide a Seed 
### Option 1: Modify the Main Function Call
1. Open 2048.py in your text editor
2. Scroll to the bottom of the file
3. Find this line:
```python
if __name__ = "__main__"
    main(Window)
```
4. Change it to include a seed:
```python
if __name__ == "__main__"
    main(WINDOW, seed=42)
```
5. Save the file and run:
```bash
python3 2048.py
```
### Option 2: Pass Seed as Parameter
The main() function accepts an optional seed parameter: 
```python
def main(window, seed=None):
    # If seed is provided, use it for deterministic behavior
    if seed is not None:
        random.seed(seed)
    # ... rest of game code
```
### Function signature: 
```python
main(WINDOW, seed=NONE) # No seed = random
main(WINDOW, seed=42)   # Seed 42 = deterministic
```

