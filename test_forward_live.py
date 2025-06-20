#!/usr/bin/env python3
"""
Test script for forward testing and live testing functionality
"""

import os
import sys
from datetime import date
from data_preparation import DataPreparation

def test_forward_testing():
    """Test forward testing functionality"""
    print("Testing Forward Testing Functionality...")
    
    try:
        dp = DataPreparation()
        
        # Test 1: Generate forward test dataset
        print("1. Testing forward test dataset generation...")
        success = dp.prepare_forward_test_data(
            start_date=date(2024, 6, 1),
            end_date=date(2024, 6, 10)
        )
        
        if success:
            print("✓ Forward test dataset generated successfully")
            
            # Check if file exists
            if os.path.exists("ml_data/forward_test_dataset.csv"):
                print("✓ Forward test dataset file created")
            else:
                print("✗ Forward test dataset file not found")
                return False
        else:
            print("✗ Failed to generate forward test dataset")
            return False
        
        # Test 2: Run forward test (if model exists)
        print("2. Testing forward test execution...")
        if os.path.exists("ml_data/model.pkl") and os.path.exists("ml_data/scaler.pkl"):
            success, metrics = dp.run_forward_test()
            if success and metrics:
                print(f"✓ Forward test completed with {metrics['accuracy']:.2%} accuracy")
                print(f"  - Total samples: {metrics['total_samples']}")
                print(f"  - Buy predictions: {metrics['buy_predictions']}")
                print(f"  - Sell predictions: {metrics['sell_predictions']}")
                
                # Check if results file exists
                if os.path.exists("ml_data/forward_test_results.csv"):
                    print("✓ Forward test results file created")
                else:
                    print("✗ Forward test results file not found")
                    return False
            else:
                print("✗ Failed to run forward test")
                return False
        else:
            print("⚠ Skipping forward test execution (no trained model found)")
        
        return True
        
    except Exception as e:
        print(f"✗ Error in forward testing: {e}")
        return False

def test_live_testing():
    """Test live testing functionality"""
    print("\nTesting Live Testing Functionality...")
    
    try:
        dp = DataPreparation()
        
        # Test live inference
        print("1. Testing live inference...")
        if os.path.exists("ml_data/model.pkl") and os.path.exists("ml_data/scaler.pkl"):
            success, result = dp.run_live_inference()
            if success and result:
                print("✓ Live inference completed successfully")
                print(f"  - Prediction: {result['prediction']}")
                print(f"  - Confidence: {result['confidence']:.2%}")
                print(f"  - Current Price: ₹{result['current_price']:.2f}")
                print(f"  - RSI: {result['rsi']:.2f}")
                
                # Check if live predictions file exists
                if os.path.exists("ml_data/live_predictions.csv"):
                    print("✓ Live predictions file created")
                else:
                    print("✗ Live predictions file not found")
                    return False
            else:
                print("✗ Failed to run live inference")
                return False
        else:
            print("⚠ Skipping live inference (no trained model found)")
        
        return True
        
    except Exception as e:
        print(f"✗ Error in live testing: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 60)
    print("FORWARD TESTING AND LIVE TESTING FUNCTIONALITY TEST")
    print("=" * 60)
    
    # Create ml_data directory if it doesn't exist
    os.makedirs("ml_data", exist_ok=True)
    
    # Test forward testing
    forward_success = test_forward_testing()
    
    # Test live testing
    live_success = test_live_testing()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Forward Testing: {'✓ PASSED' if forward_success else '✗ FAILED'}")
    print(f"Live Testing: {'✓ PASSED' if live_success else '✗ FAILED'}")
    
    if forward_success and live_success:
        print("\n🎉 All tests passed! The new functionality is working correctly.")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the logs for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 