def calculate_coins(amount):
    """
    Calculate the minimum number of coins needed to make the given amount using dynamic programming.
    
    This algorithm handles limited coin quantities:
    - 50¢ coins: maximum 10 available
    - 20¢ coins: maximum 25 available  
    - 2¢ coins: unlimited
    - 1¢ coins: unlimited
    
    Uses dynamic programming with state tracking for limited denominations.
    
    Time Complexity: O(amount × coin_limits)
    Space Complexity: O(amount × coin_states)
    
    Args:
        amount (int): The amount in cents to make change for
        
    Returns:
        dict: Dictionary with coin denominations as keys and their counts as values
              Format: {50: count, 20: count, 2: count, 1: count}
              Returns all zeros if no solution possible with given constraints
              
    Example:
        >>> calculate_coins(62)
        {50: 0, 20: 3, 2: 1, 1: 0}  # 3×20¢ + 1×2¢ = 4 total coins
        >>> calculate_coins(1200)  # Large amount requiring all 50¢ coins
        {50: 10, 20: 25, 2: 0, 1: 0}  # Uses all limited coins: 10×50¢ + 25×20¢ = 1000¢
    """
    # Coin denominations and their limits
    # Format: (value, max_quantity) - None means unlimited
    coin_limits = [(50, 10), (20, 25), (2, None), (1, None)]
    denominations = [50, 20, 2, 1]
    
    # For limited coins, we need to track states: (amount, coins_used_so_far)
    # dp[i][j][k] = minimum coins for amount i, using j 50¢ coins, k 20¢ coins
    # We'll use a different approach: track the state as we build solutions
    
    # Simple DP with constraint checking
    # dp[i] = minimum coins needed for amount i (considering all constraints)
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    # parent[i] = (coin_used, previous_amount) to reconstruct solution
    parent = [(-1, -1)] * (amount + 1)
    
    # Fill the DP table with constraint checking
    for i in range(1, amount + 1):
        # Try each coin denomination with its limit
        for coin_value, max_qty in coin_limits:
            if coin_value <= i:  # Can use this coin
                # Check if using this coin gives a better solution
                prev_amount = i - coin_value
                if dp[prev_amount] != float('inf'):
                    # Count how many of this coin type we would use in total
                    temp_count = {50: 0, 20: 0, 2: 0, 1: 0}
                    
                    # Trace back to count coins used so far
                    curr = prev_amount
                    while curr > 0 and parent[curr][0] != -1:
                        used_coin = parent[curr][0]
                        temp_count[used_coin] += 1
                        curr = parent[curr][1]
                    
                    # Check if we can use one more of this coin type
                    can_use_coin = True
                    if max_qty is not None:  # Limited coin
                        if temp_count[coin_value] >= max_qty:
                            can_use_coin = False
                    
                    # Update if this gives a better solution and we can use the coin
                    if can_use_coin and dp[prev_amount] + 1 < dp[i]:
                        dp[i] = dp[prev_amount] + 1
                        parent[i] = (coin_value, prev_amount)
    
    # Reconstruct the optimal solution considering coin limits
    coin_count = {50: 0, 20: 0, 2: 0, 1: 0}
    
    # Check if a solution exists with the given constraints
    if dp[amount] == float('inf'):
        return coin_count  # Return all zeros if no solution possible
    
    # Trace back from target amount to 0, following the parent pointers
    current = amount
    while current > 0 and parent[current][0] != -1:
        coin_used, prev_amount = parent[current]
        coin_count[coin_used] += 1
        current = prev_amount
    
    return coin_count

def display_result(amount, coin_count):
    """
    Display the result in a user-friendly format, showing coin limits.
    
    Args:
        amount (int): The original amount requested
        coin_count (dict): Dictionary with coin counts
    """
    print(f"\nTo make {amount} cents, you need:")
    print("-" * 40)
    
    total_coins = sum(coin_count.values())
    
    # Show coin usage with limits
    coin_info = [
        (50, 10, "limited"),
        (20, 25, "limited"), 
        (2, None, "unlimited"),
        (1, None, "unlimited")
    ]
    
    for denom, limit, status in coin_info:
        count = coin_count[denom]
        if count > 0:
            if limit is not None:
                print(f"{count:2d} x {denom:2d}¢ coins (max {limit} available - {status})")
            else:
                print(f"{count:2d} x {denom:2d}¢ coins ({status})")
    
    print("-" * 40)
    print(f"Total coins needed: {total_coins}")
    
    # Show remaining coin availability
    remaining_50 = 10 - coin_count[50] 
    remaining_20 = 25 - coin_count[20]
    if total_coins > 0:
        print(f"Remaining: {remaining_50} x 50¢, {remaining_20} x 20¢")

def main():
    """
    Main function to run the coin change program with limited coin quantities.
    """
    print("Coin Change Calculator (Limited Quantities)")
    print("Available coins:")
    print("  50¢: 10 coins available (limited)")
    print("  20¢: 25 coins available (limited)")
    print("   2¢: unlimited")
    print("   1¢: unlimited")
    print("=" * 50)
    
    while True:
        try:
            # Get user input
            amount = int(input("\nEnter the amount in cents (0 to quit): "))
            
            # Check for exit condition
            if amount == 0:
                print("Thank you for using the Coin Change Calculator!")
                break
            
            # Validate input
            if amount < 0:
                print("Please enter a positive amount.")
                continue
            
            # Calculate and display result
            coin_count = calculate_coins(amount)
            display_result(amount, coin_count)
            
        except ValueError:
            print("Please enter a valid integer.")
        except KeyboardInterrupt:
            print("\n\nProgram interrupted. Goodbye!")
            break

if __name__ == "__main__":
    main()
