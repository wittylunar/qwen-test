#!/usr/bin/env python3

# Test the format_number function separately
def format_number(num):
    """Format large numbers into human-readable format (e.g., 1000 -> 1.0K, 1000000 -> 1.0M)"""
    if num is None:
        return "0"
    
    # Handle negative numbers
    is_negative = num < 0
    num = abs(num)
    
    # Define the units
    magnitude = 0
    while num >= 1000 and magnitude < 8:  # Up to 'Y' (yotta)
        magnitude += 1
        num /= 1000.0
    
    # Define unit labels
    units = ['', 'K', 'M', 'B', 'T', 'q', 'Q', 's', 'S']
    
    # Format the number with 1 decimal place if it's not a whole number
    if num == int(num):
        formatted_num = f"{int(num)}{units[magnitude]}"
    else:
        formatted_num = f"{num:.1f}{units[magnitude]}"
    
    # Add negative sign back if needed
    if is_negative:
        formatted_num = "-" + formatted_num
        
    return formatted_num

# Test the function
test_numbers = [
    1000, 
    1000000, 
    1000000000, 
    1000000000000, 
    1000000000000000, 
    1000000000000000000, 
    1234, 
    56789, 
    1234567, 
    -123456789,
    100000000000000000000000000000000,  # Very large number from the example
    0,
    1,
    999,
    1000000000000000000000000  # 1 septillion
]

print('Testing format_number function:')
for num in test_numbers:
    result = format_number(num)
    print(f'{num} -> {result}')