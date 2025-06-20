# Forward Testing and Live Testing Functionality

This document describes the new forward testing and live testing capabilities added to the stock trading application.

## Overview

The application now supports two types of testing beyond the initial ML training:

1. **Forward Testing**: Test your trained model on unseen historical data from a specific date range
2. **Live Testing**: Run predictions on the most recent data as if trading in real-time

## Forward Testing

### What is Forward Testing?

Forward testing (also known as walk-forward testing) simulates real-world prediction by:
- Training your model on historical data
- Testing it on unseen, recent historical data that was not used in training
- This provides a realistic assessment of how your model would perform in actual trading

### How to Use Forward Testing

1. **Select Date Range**: Choose the start and end dates for your forward test period
2. **Generate Dataset**: Click "Generate Forward Test Dataset" to create a dataset for the specified period
3. **Run Forward Test**: Click "Run Forward Test" to apply your trained model to the forward test dataset
4. **View Results**: Analyze the results including accuracy, confusion matrix, and detailed predictions

### Forward Testing Features

- **Date Range Selection**: Choose any date range for testing
- **Comprehensive Metrics**: Accuracy, confusion matrix, classification report
- **Visual Results**: Charts showing predictions vs actual price movements
- **Export Results**: Download forward test results as CSV
- **Filtered Views**: View results for specific date ranges within the test period

### Files Generated

- `ml_data/forward_test_dataset.csv`: The forward test dataset
- `ml_data/forward_test_results.csv`: Detailed results with predictions
- `ml_data/forward_test_metrics.json`: Summary metrics and performance statistics

## Live Testing

### What is Live Testing?

Live testing runs your trained model on the most recent data as if you were trading in real-time:
- Uses the latest available market data
- Provides immediate predictions (BUY/SELL)
- Shows confidence levels and probabilities
- Maintains a history of live predictions

### How to Use Live Testing

1. **Run Live Inference**: Click "Run Live Inference" to get the latest prediction
2. **View Results**: See the prediction, confidence, and supporting metrics
3. **View History**: Click "View Live Predictions History" to see all previous predictions
4. **Analyze Performance**: Review the prediction history over time

### Live Testing Features

- **Real-time Predictions**: Get BUY/SELL signals based on latest data
- **Confidence Metrics**: See prediction confidence and buy/sell probabilities
- **Supporting Indicators**: RSI, moving averages, volume, and other technical indicators
- **Prediction History**: Track all live predictions over time
- **Visual Analysis**: Charts showing price movements and prediction points

### Files Generated

- `ml_data/live_predictions.csv`: History of all live predictions

## Technical Implementation

### New Methods in DataPreparation Class

#### `prepare_forward_test_data()`
```python
def prepare_forward_test_data(self, symbol=None, expiry=None, strike=None, option_type=None, 
                             start_date=None, end_date=None, output_path="ml_data/forward_test_dataset.csv")
```
- Generates forward test dataset for specified date range
- Uses same feature engineering as training data
- Supports filtering by contract parameters

#### `run_forward_test()`
```python
def run_forward_test(self, forward_test_path="ml_data/forward_test_dataset.csv", 
                    model_path="ml_data/model.pkl", scaler_path="ml_data/scaler.pkl")
```
- Runs predictions on forward test dataset
- Calculates comprehensive metrics
- Saves results and metrics to files

#### `run_live_inference()`
```python
def run_live_inference(self, symbol=None, expiry=None, strike=None, option_type=None, 
                      model_path="ml_data/model.pkl", scaler_path="ml_data/scaler.pkl")
```
- Runs prediction on latest available data
- Returns prediction with confidence and supporting metrics
- Maintains prediction history

### GUI Integration

The new functionality is integrated into the Streamlit GUI with:

- **Forward Testing Section**: Date selection, dataset generation, and test execution
- **Live Testing Section**: Live inference and prediction history viewing
- **Results Visualization**: Charts and metrics display
- **Export Capabilities**: Download results as CSV files

## Usage Workflow

### Complete Testing Workflow

1. **Train Model**: Use "Run ML Training" to train your model on historical data
2. **Forward Test**: 
   - Select forward test date range
   - Generate forward test dataset
   - Run forward test and analyze results
3. **Live Test**:
   - Run live inference to get current prediction
   - Monitor prediction history over time
   - Analyze live performance

### Example Usage

```python
# Initialize data preparation
dp = DataPreparation()

# Generate forward test dataset
success = dp.prepare_forward_test_data(
    symbol="NIFTY24JUN19000CE",
    start_date=date(2024, 6, 1),
    end_date=date(2024, 6, 10)
)

# Run forward test
if success:
    success, metrics = dp.run_forward_test()
    if success:
        print(f"Forward test accuracy: {metrics['accuracy']:.2%}")

# Run live inference
success, result = dp.run_live_inference(symbol="NIFTY24JUN19000CE")
if success:
    print(f"Live prediction: {result['prediction']} with {result['confidence']:.2%} confidence")
```

## Testing

Run the test script to verify functionality:

```bash
python test_forward_live.py
```

This will test both forward testing and live testing capabilities.

## Requirements

The new functionality requires:
- Trained model (`ml_data/model.pkl`)
- Scaler (`ml_data/scaler.pkl`)
- Database connection with historical data
- All existing dependencies (scikit-learn, pandas, numpy, etc.)

## Benefits

1. **Realistic Evaluation**: Forward testing provides realistic performance assessment
2. **Live Trading Simulation**: Live testing simulates actual trading conditions
3. **Comprehensive Analysis**: Detailed metrics and visualizations
4. **Historical Tracking**: Maintain prediction history for analysis
5. **Easy Integration**: Seamlessly integrated with existing GUI

## Notes

- Forward testing requires a trained model to be available
- Live testing uses the most recent 50 candles to ensure sufficient data for feature engineering
- All predictions include confidence levels and supporting metrics
- Results are automatically saved and can be exported for further analysis 