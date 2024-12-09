#!/usr/bin/env python3

import sys
import argparse
from typing import List, TextIO

MIN_VALUE = 0.0
MAX_VALUE = 1_000_000_000.0
MAX_INPUTS = 100
DECIMAL_PLACES = 1

def parse_arguments() -> tuple[float, float]:
    """Parse and validate command line arguments for threshold and limit values.
    
    Returns:
        tuple[float, float]: The validated threshold and limit values.
        
    Exits:
        1: If arguments are invalid or out of allowed range.
    """
    # Remove 'compute' from arguments if present, due to readme instructions
    if len(sys.argv) > 1 and sys.argv[1] == 'compute':
        sys.argv[1:] = sys.argv[2:]
    
    parser = argparse.ArgumentParser(description='Numeric input risk analysis with threshold and limit sd constraints')
    parser.add_argument('threshold', type=float, 
                       help=f'Threshold value between {MIN_VALUE} and {MAX_VALUE}')
    parser.add_argument('limit', type=float,
                       help=f'Limit value between {MIN_VALUE} and {MAX_VALUE}')
    
    args = parser.parse_args()
    
    if not (MIN_VALUE <= args.threshold <= MAX_VALUE):
        parser.error(f"Threshold must be between {MIN_VALUE} and {MAX_VALUE}")
    if not (MIN_VALUE <= args.limit <= MAX_VALUE):
        parser.error(f"Limit must be between {MIN_VALUE} and {MAX_VALUE}")
        
    return args.threshold, args.limit

def is_valid_decimal_precision(value: float) -> bool:
    """Check if value has precision only to the tenths place.
    
    Args:
        value: The float value to check.
        
    Returns:
        bool: True if value has no decimal places or matches configured precision.
    """
    decimal_part = str(value).split('.')[-1]
    return decimal_part in ['0', ''] or len(decimal_part) == DECIMAL_PLACES

def read_input_values(input_stream: TextIO = sys.stdin) -> List[float]:
    """Read and validate numeric input values from the input stream.
    
    Args:
        input_stream: Input stream to read values from, defaults to stdin.
        
    Returns:
        List[float]: List of validated input values.
        
    Exits:
        1: If any value is invalid, out of range, or too many inputs received.
           Note: Silent exit on invalid input is an implementation choice as
           error handling was not specified in requirements.
    """
    inputs = []
    for line in input_stream:
        try:
            value = float(line.strip())
            if not (MIN_VALUE <= value <= MAX_VALUE) or not is_valid_decimal_precision(value):
                raise ValueError
            inputs.append(value)
        except ValueError:
            sys.exit(1)
        
        if len(inputs) > MAX_INPUTS:
            sys.exit(1)
            
    return inputs

def apply_constraints(inputs: List[float], threshold: float, limit: float) -> List[float]:
    """Apply threshold and limit constraints to input values.
    
    Args:
        inputs: List of input values to process.
        threshold: Minimum value before counting towards total.
        limit: Maximum allowed sum of processed values.
        
    Returns:
        List[float]: Processed values plus final sum as last element.
    """
    outputs = []
    running_sum = MIN_VALUE
    
    for value in inputs:
        output = max(MIN_VALUE, value - threshold)
        
        if running_sum + output > limit:
            output = max(MIN_VALUE, limit - running_sum)
        
        outputs.append(output)
        running_sum += output
    
    outputs.append(running_sum)
    return outputs

def main():
    """Process numeric input applying threshold and limit constraints."""
    threshold, limit = parse_arguments()
    inputs = read_input_values()
    outputs = apply_constraints(inputs, threshold, limit)
    
    for output in outputs:
        print(f"{output:.{DECIMAL_PLACES}f}")

if __name__ == "__main__":
    main() 