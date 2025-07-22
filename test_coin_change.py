#!/usr/bin/env python3
"""
Test cases for the coin_change.py module.
Tests the dynamic programming coin change algorithm with various scenarios.
"""

import sys
import os

# Add the current directory to the path so we can import coin_change
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from coin_change import calculate_coins

def test_coin_change():
    """Run comprehensive tests for the coin change algorithm."""
    
    print("Testing Coin Change Algorithm")
    print("Denominations: 50¢, 20¢, 2¢, 1¢")
    print("=" * 50)
    
    # Test cases: (amount, expected_result_dict)
    test_cases = [
        # Basic cases
        (0, {50: 0, 20: 0, 2: 0, 1: 0}),  # Zero amount
        (1, {50: 0, 20: 0, 2: 0, 1: 1}),  # Single 1¢ coin
        (2, {50: 0, 20: 0, 2: 1, 1: 0}),  # Single 2¢ coin
        (20, {50: 0, 20: 1, 2: 0, 1: 0}), # Single 20¢ coin
        (50, {50: 1, 20: 0, 2: 0, 1: 0}), # Single 50¢ coin
        
        # Cases where greedy would fail
        (62, {50: 0, 20: 3, 2: 1, 1: 0}), # 3×20¢ + 1×2¢ = 4 coins (optimal)
                                           # vs greedy: 1×50¢ + 6×2¢ = 7 coins
        
        # More complex cases
        (3, {50: 0, 20: 0, 2: 1, 1: 1}),  # 1×2¢ + 1×1¢
        (4, {50: 0, 20: 0, 2: 2, 1: 0}),  # 2×2¢
        (5, {50: 0, 20: 0, 2: 2, 1: 1}),  # 2×2¢ + 1×1¢
        (21, {50: 0, 20: 1, 2: 0, 1: 1}), # 1×20¢ + 1×1¢
        (22, {50: 0, 20: 1, 2: 1, 1: 0}), # 1×20¢ + 1×2¢
        (40, {50: 0, 20: 2, 2: 0, 1: 0}), # 2×20¢
        (42, {50: 0, 20: 2, 2: 1, 1: 0}), # 2×20¢ + 1×2¢
        (60, {50: 0, 20: 3, 2: 0, 1: 0}), # 3×20¢
        (70, {50: 1, 20: 1, 2: 0, 1: 0}), # 1×50¢ + 1×20¢
        (72, {50: 1, 20: 1, 2: 1, 1: 0}), # 1×50¢ + 1×20¢ + 1×2¢
        (100, {50: 2, 20: 0, 2: 0, 1: 0}), # 2×50¢
        (123, {50: 2, 20: 1, 2: 1, 1: 1}), # 2×50¢ + 1×20¢ + 1×2¢ + 1×1¢
    ]
    
    passed_tests = 0
    failed_tests = 0
    
    for i, (amount, expected) in enumerate(test_cases, 1):
        try:
            result = calculate_coins(amount)
            
            # Calculate total coins and verify amount
            total_coins = sum(result.values())
            total_amount = sum(coin * count for coin, count in result.items())
            
            # Check if result matches expected
            if result == expected and total_amount == amount:
                print(f"✅ Test {i:2d}: Amount {amount:3d}¢ -> {total_coins} coins - PASSED")
                passed_tests += 1
            else:
                print(f"❌ Test {i:2d}: Amount {amount:3d}¢ - FAILED")
                print(f"    Expected: {expected}")
                print(f"    Got:      {result}")
                print(f"    Expected total: {amount}¢, Got total: {total_amount}¢")
                failed_tests += 1
                
        except Exception as e:
            print(f"❌ Test {i:2d}: Amount {amount:3d}¢ - ERROR: {e}")
            failed_tests += 1
    
    # Summary
    print("\n" + "=" * 50)
    print(f"Test Results: {passed_tests} passed, {failed_tests} failed")
    
    if failed_tests == 0:
        print("🎉 All tests passed!")
    else:
        print(f"⚠️  {failed_tests} test(s) failed")
    
    return failed_tests == 0

    def test_display_result():
        """
        Test the display_result function for correct output formatting.
        This test checks that the output contains expected lines for various coin counts.
        """

        test_cases = [
            # (amount, coin_count, expected_strings)
            (62, {50: 0, 20: 3, 2: 1, 1: 0}, [
                "To make 62 cents, you need:",
                " 3 x 20¢ coins (max 25 available - limited)",
                " 1 x  2¢ coins (unlimited)",
                "Total coins needed: 4",
                "Remaining: 10 x 50¢, 22 x 20¢"
            ]),
            (0, {50: 0, 20: 0, 2: 0, 1: 0}, [
                "To make 0 cents, you need:",
                "Total coins needed: 0"
            ]),
            (1200, {50: 10, 20: 25, 2: 0, 1: 0}, [
                "10 x 50¢ coins (max 10 available - limited)",
                "25 x 20¢ coins (max 25 available - limited)",
                "Total coins needed: 35",
                "Remaining: 0 x 50¢, 0 x 20¢"
            ]),
            (5, {50: 0, 20: 0, 2: 2, 1: 1}, [
                " 2 x  2¢ coins (unlimited)",
                " 1 x  1¢ coins (unlimited)",
                "Total coins needed: 3",
                "Remaining: 10 x 50¢, 25 x 20¢"
            ]),
        ]

        for amount, coin_count, expected_strings in test_cases:
            captured_output = io.StringIO()
            sys.stdout = captured_output
            display_result(amount, coin_count)
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()
            for expected in expected_strings:
                assert expected in output, f"Expected '{expected}' in output for amount {amount}, got:\n{output}"

    # Add this test to the test runner
    test_display_result()



def demonstrate_greedy_vs_optimal():
    """Demonstrate cases where greedy algorithm fails but DP succeeds."""
    
    print("\n" + "=" * 60)
    print("GREEDY vs OPTIMAL COMPARISON")
    print("=" * 60)
    
    # Cases where greedy fails
    problem_cases = [62, 42, 84, 102]
    
    for amount in problem_cases:
        print(f"\nAmount: {amount}¢")
        
        # Calculate optimal solution using DP
        optimal = calculate_coins(amount)
        optimal_coins = sum(optimal.values())
        
        # Calculate greedy solution manually
        greedy = {50: 0, 20: 0, 2: 0, 1: 0}
        remaining = amount
        for coin in [50, 20, 2, 1]:
            if remaining >= coin:
                greedy[coin] = remaining // coin
                remaining = remaining % coin
        greedy_coins = sum(greedy.values())
        
        print(f"  Optimal (DP): {optimal_coins} coins - {optimal}")
        print(f"  Greedy:       {greedy_coins} coins - {greedy}")
        
        if optimal_coins < greedy_coins:
            print(f"  💡 DP saves {greedy_coins - optimal_coins} coins!")
        elif optimal_coins == greedy_coins:
            print(f"  ✅ Both methods give same result")

def performance_test():
    """Test performance with larger amounts."""
    
    print("\n" + "=" * 60)
    print("PERFORMANCE TEST")
    print("=" * 60)
    
    import time
    
    large_amounts = [1000, 2500, 5000]
    
    for amount in large_amounts:
        start_time = time.time()
        result = calculate_coins(amount)
        end_time = time.time()
        
        total_coins = sum(result.values())
        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        print(f"Amount: {amount:4d}¢ -> {total_coins:3d} coins in {execution_time:.2f}ms")
        print(f"  Breakdown: {result}")

if __name__ == "__main__":
    # Run all tests
    success = test_coin_change()
    demonstrate_greedy_vs_optimal()
    performance_test()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)
