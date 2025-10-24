import string
import secrets

def unique_code():
    # First part: 5 characters (letters + digits)
    part1 = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(5))
    
    # Second part: 6 digits
    part2 = ''.join(secrets.choice(string.digits) for _ in range(6))
    
    # Combine with a dash
    code = f"{part1}-{part2}"
    
    return code

# Example usage
print(unique_code())