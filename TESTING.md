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
## 🧪 Test Cases
### Test Case 1: Verify Deterministic Behavior 
##Purpose:## Confirm the same seed prodices identical results
### Steps: 
1. Set seed to 42:
```python
main(WINOW, seed=42)
```
2. Run the game and record the positions of the first three tiles
3. Restart the game witht he same seed
4. Verify tiles spawn in identical positions
##Expected Result:## Tiles appear in the exact same locations both times 

## Test Case 2: Verify Tile Spawn Probability
##Purpose:## Test that tiles spawn with correct probability (90% = 2, 10% = 4) 
##Steps:##
1. Use a seed for consistency:
```python
main(WINDOW, seed=100)
```
2. Play through 20 moves
3. Count how many 2s vs 4s spawned
4. Ration should be approximately 9:1
##Expected Result:## Roughly 18 tiles with value 2, and 2 tiles with value 4


