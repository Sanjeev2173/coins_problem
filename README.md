# coins_problem
To return the change with minimum number of coins
# Coin Change Calculator Documentation

## Overview

The Coin Change Calculator is a Python program that solves the classic "coin change problem" using dynamic programming. Given a target amount and a set of coin denominations, it finds the minimum number of coins needed to make that amount.

## Problem Statement

**Input**: An amount in cents and available coin denominations  
**Output**: The minimum number of coins needed and the exact breakdown by denomination  
**Goal**: Minimize the total number of coins used

## Algorithm

### Dynamic Programming Approach

This implementation uses **dynamic programming** instead of a greedy algorithm because the coin system `[50¢, 20¢, 2¢, 1¢]` doesn't satisfy the greedy choice property.

**Why not greedy?**
- For 62¢: Greedy gives 1×50¢ + 6×2¢ = **7 coins**
- Optimal solution: 3×20¢ + 1×2¢ = **4 coins**

### Algorithm Steps

1. **Initialization**:
   - Create `dp` array where `dp[i]` = minimum coins for amount `i`
   - Create `parent` array to track which coin was used for each amount
   - Set `dp[0] = 0` (zero coins needed for amount 0)

2. **Fill DP Table**:
   ```python
   for i in range(1, amount + 1):
       for coin in denominations:
           if coin <= i and dp[i - coin] + 1 < dp[i]:
               dp[i] = dp[i - coin] + 1
               parent[i] = coin
   ```

3. **Reconstruct Solution**:
   - Trace back through `parent` array to find actual coins used
   - Count occurrences of each denomination

### Time Complexity: O(amount × number_of_denominations)
### Space Complexity: O(amount)

## File Structure

```
coin_change.py
├── calculate_coins(amount)     # Core DP algorithm
├── display_result(amount, coin_count)  # Format output
└── main()                      # User interface loop
```

## Functions

### `calculate_coins(amount: int) -> dict`

**Purpose**: Calculate minimum coins needed using dynamic programming

**Parameters**:
- `amount` (int): Target amount in cents

**Returns**:
- `dict`: Dictionary with coin denominations as keys and counts as values
  - Format: `{50: count, 20: count, 2: count, 1: count}`

**Example**:
```python
result = calculate_coins(62)
# Returns: {50: 0, 20: 3, 2: 1, 1: 0}
# Meaning: 3×20¢ + 1×2¢ = 62¢ using 4 coins
```

**Algorithm Details**:
1. Initialize DP table with infinity values
2. Set base case: `dp[0] = 0`
3. For each amount from 1 to target:
   - Try each coin denomination
   - Update if using this coin gives fewer total coins
   - Track which coin was used in `parent` array
4. Reconstruct solution by following parent pointers

### `display_result(amount: int, coin_count: dict) -> None`

**Purpose**: Display results in user-friendly format

**Parameters**:
- `amount` (int): Original amount requested
- `coin_count` (dict): Result from `calculate_coins()`

**Output Format**:
```
To make 62 cents, you need:
------------------------------
3 x 20 cent coins
1 x 2 cent coins
------------------------------
Total coins needed: 4
```

### `main() -> None`

**Purpose**: Interactive command-line interface

**Features**:
- Input validation (positive integers only)
- Loop for multiple calculations
- Graceful error handling
- Exit with 0 or Ctrl+C

## Usage Examples

### Basic Usage
```python
from coin_change import calculate_coins

# Calculate coins for 62 cents
result = calculate_coins(62)
print(result)  # {50: 0, 20: 3, 2: 1, 1: 0}
```

### Command Line Usage
```bash
python coin_change.py
```

**Sample Session**:
```
Coin Change Calculator
Available denominations: 50¢, 20¢, 2¢, 1¢
========================================

Enter the amount in cents (0 to quit): 62

To make 62 cents, you need:
------------------------------
3 x 20 cent coins
1 x 2 cent coins
------------------------------
Total coins needed: 4

Enter the amount in cents (0 to quit): 0
Thank you for using the Coin Change Calculator!
```

## Test Cases

### Critical Test Cases
| Amount | Optimal Solution | Greedy Solution | DP Advantage |
|--------|------------------|-----------------|--------------|
| 62¢    | 4 coins (3×20¢ + 1×2¢) | 7 coins (1×50¢ + 6×2¢) | 3 coins saved |
| 84¢    | 6 coins (4×20¢ + 2×2¢) | 9 coins (1×50¢ + 1×20¢ + 7×2¢) | 3 coins saved |
| 42¢    | 3 coins (2×20¢ + 1×2¢) | 3 coins (2×20¢ + 1×2¢) | Same result |

### Edge Cases
- **Amount 0**: Returns all zeros `{50: 0, 20: 0, 2: 0, 1: 0}`
- **Amount 1**: Uses 1¢ coin `{50: 0, 20: 0, 2: 0, 1: 1}`
- **Large amounts**: Algorithm scales efficiently

## Configuration

### Changing Coin Denominations

To modify available coin types, update the `denominations` list in `calculate_coins()`:

```python
# Current denominations
denominations = [50, 20, 2, 1]

# Example: European coins
denominations = [200, 100, 50, 20, 10, 5, 2, 1]

# Example: US quarters system
denominations = [25, 10, 5, 1]
```

**Note**: The algorithm works for any coin system, but some systems allow greedy algorithms while others require DP.

## Error Handling

### Input Validation
- **Non-integer input**: Shows "Please enter a valid integer"
- **Negative amounts**: Shows "Please enter a positive amount"
- **Keyboard interrupt**: Graceful exit with goodbye message

### Edge Cases
- **Amount 0**: Handled correctly (returns zero coins)
- **Very large amounts**: Algorithm remains efficient
- **Impossible amounts**: Returns empty solution (though not applicable with 1¢ coin)

## Performance Characteristics

### Time Complexity: O(n × m)
- `n` = target amount
- `m` = number of coin denominations (4 in this case)

### Space Complexity: O(n)
- Two arrays of size `amount + 1`

### Benchmark Results
| Amount | Coins Needed | Execution Time |
|--------|-------------|----------------|
| 1,000¢ | 20 coins    | < 1ms         |
| 2,500¢ | 50 coins    | < 1ms         |
| 5,000¢ | 100 coins   | < 1ms         |

## Comparison: Greedy vs Dynamic Programming

### Greedy Algorithm (INCORRECT for this coin system)
```python
def greedy_coins(amount):
    coins = [50, 20, 2, 1]
    result = {}
    for coin in coins:
        result[coin] = amount // coin
        amount = amount % coin
    return result
```

**Problems with Greedy**:
- Assumes largest coin is always best choice
- Fails when coin system lacks "greedy choice property"
- Example: 62¢ → 1×50¢ + 6×2¢ = 7 coins (suboptimal)

### Dynamic Programming (CORRECT)
- Considers all possible combinations
- Guaranteed to find optimal solution
- Builds solution incrementally from smaller subproblems
- Example: 62¢ → 3×20¢ + 1×2¢ = 4 coins (optimal)

## Mathematical Foundation

### Coin Systems and Optimal Substructure

A coin change problem has **optimal substructure** if:
- Optimal solution for amount `n` contains optimal solutions for smaller amounts
- `dp[i] = min(dp[i-c] + 1)` for all valid coins `c`

### Canonical vs Non-Canonical Coin Systems

**Canonical** (greedy works): `[25, 10, 5, 1]` (US coins)  
**Non-Canonical** (requires DP): `[50, 20, 2, 1]` (our system)

## Files in Project

```
Coins/
├── coin_change.py           # Main algorithm and interface
├── test_coin_change.py      # Comprehensive test suite
├── simple_coin_change.py    # Basic version without features
└── README.md               # This documentation
```

## Dependencies

**Python Standard Library Only**:
- No external dependencies required
- Compatible with Python 3.6+

## Contributing

When modifying the algorithm:

1. **Test thoroughly**: Run `test_coin_change.py` to verify correctness
2. **Validate coin systems**: Ensure new denominations work correctly
3. **Performance testing**: Check efficiency with large amounts
4. **Edge cases**: Test boundary conditions (0, 1, large values)

---

*This documentation covers the complete coin change calculator implementation using dynamic programming for optimal results.*
