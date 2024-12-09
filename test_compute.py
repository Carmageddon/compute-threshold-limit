import io
import pytest
from compute_pkg.compute import parse_arguments, read_input_values, apply_constraints, MAX_VALUE, MIN_VALUE, MAX_INPUTS

def test_valid_arguments(monkeypatch):
    # Test valid argument parsing
    test_args = ['compute', 'compute', '100.0', '500.0']
    monkeypatch.setattr('sys.argv', test_args)
    
    threshold, limit = parse_arguments()
    assert threshold == 100.0
    assert limit == 500.0

    # Test without 'compute' argument
    test_args = ['compute', '100.0', '500.0']
    monkeypatch.setattr('sys.argv', test_args)
    
    threshold, limit = parse_arguments()
    assert threshold == 100.0
    assert limit == 500.0

def test_invalid_threshold(monkeypatch):
    # Test threshold out of range
    test_args = ['compute', '-1.0', '500.0']
    monkeypatch.setattr('sys.argv', test_args)
    
    with pytest.raises(SystemExit):
        parse_arguments()
        
    test_args = ['compute', '1000000001.0', '500.0']
    monkeypatch.setattr('sys.argv', test_args)
    
    with pytest.raises(SystemExit):
        parse_arguments()

def test_invalid_limit(monkeypatch):
    # Test limit out of range
    test_args = ['compute', '100.0', '-1.0']
    monkeypatch.setattr('sys.argv', test_args)
    
    with pytest.raises(SystemExit):
        parse_arguments()
        
    test_args = ['compute', '100.0', '1000000001.0']
    monkeypatch.setattr('sys.argv', test_args)
    
    with pytest.raises(SystemExit):
        parse_arguments()

def test_read_and_apply_threshold():
    # Test threshold functionality
    input_data = "10.0\n20.0\n5.0\n"
    threshold = 15.0
    limit = 100.0
    
    inputs = read_input_values(io.StringIO(input_data))
    outputs = apply_constraints(inputs, threshold, limit)
    
    assert outputs[0] == 0.0  # 10.0 - 15.0 = -5.0 -> 0.0
    assert outputs[1] == 5.0  # 20.0 - 15.0 = 5.0
    assert outputs[2] == 0.0  # 5.0 - 15.0 = -10.0 -> 0.0
    assert outputs[3] == 5.0  # Sum of all outputs

def test_read_and_apply_limit():
    input_data = "100.0\n200.0\n300.0\n"
    threshold = 0.0
    limit = 400.0
    
    inputs = read_input_values(io.StringIO(input_data))
    outputs = apply_constraints(inputs, threshold, limit)
    
    assert outputs[0] == 100.0
    assert outputs[1] == 200.0
    assert outputs[2] == 100.0  # Limited by remaining amount
    assert outputs[3] == 400.0  # Sum equals limit

def test_read_and_apply_combined():
    input_data = "1000.0\n2000.0\n3000.0\n"
    threshold = 500.0
    limit = 1000.0
    
    inputs = read_input_values(io.StringIO(input_data))
    outputs = apply_constraints(inputs, threshold, limit)
    
    assert outputs[0] == 500.0  # 1000.0 - 500.0 = 500.0
    assert outputs[1] == 500.0  # Limited by remaining amount
    assert outputs[2] == 0.0    # No remaining limit
    assert outputs[3] == 1000.0 # Sum equals limit

def test_read_input_invalid_values():
    input_data = "abc\n100.0\n"
    
    with pytest.raises(SystemExit):
        read_input_values(io.StringIO(input_data))
        
    input_data = "-1.0\n100.0\n"
    with pytest.raises(SystemExit):
        read_input_values(io.StringIO(input_data))
        
    input_data = "1000000001.0\n100.0\n"
    with pytest.raises(SystemExit):
        read_input_values(io.StringIO(input_data))

def test_read_input_too_many_inputs():
    # Test more than 100 inputs
    input_data = "100.0\n" * (MAX_INPUTS+1)
    
    with pytest.raises(SystemExit):
        read_input_values(io.StringIO(input_data))

def test_read_and_apply_empty_input():
    input_data = ""
    threshold = 0.0
    limit = 1000.0
    
    inputs = read_input_values(io.StringIO(input_data))
    outputs = apply_constraints(inputs, threshold, limit)
    assert len(outputs) == 1
    assert outputs[0] == 0.0 

def test_decimal_precision_up_to_tenths():
    input_data = "10.1\n10.12345\n"
    
    with pytest.raises(SystemExit):
        read_input_values(io.StringIO(input_data))

def test_threshold_equals_limit():
    input_data = "100.0\n200.0\n"
    threshold = 100.0
    limit = 100.0
    
    inputs = read_input_values(io.StringIO(input_data))
    outputs = apply_constraints(inputs, threshold, limit)
    assert outputs[-1] <= limit

def test_threshold_greater_than_limit():
    input_data = "100.0\n200.0\n"
    threshold = 150.0
    limit = 100.0
    
    inputs = read_input_values(io.StringIO(input_data))
    outputs = apply_constraints(inputs, threshold, limit)
    assert outputs[-1] <= limit

def test_max_value_input():
    input_data = f"{MAX_VALUE}\n"
    inputs = read_input_values(io.StringIO(input_data))
    assert inputs[0] == MAX_VALUE

def test_min_value_input():
    input_data = f"{MIN_VALUE}\n"
    inputs = read_input_values(io.StringIO(input_data))
    assert inputs[0] == MIN_VALUE