def is_palindrome(text):
    """
    Checks if a string is a palindrome (reads the same forwards and backward).
    Ignores case and non-alphanumeric characters.
    """
    processed_text = ''.join(char.lower() for char in text if char.isalnum())
    return processed_text == processed_text[::-1]

def store_palindrome_result(text, is_palindrome_result, filename="palindrome_results.txt"):
    """
    Stores the string and whether it's a palindrome in a file.
    """
    try:
        with open(filename, "a") as f:  # Open in append mode ("a")
            f.write(f"String: {text}\n")
            f.write(f"Is Palindrome: {is_palindrome_result}\n")
            f.write("-" * 20 + "\n")  # Separator for readability
        print(f"Result stored in '{filename}'")

    except Exception as e:
        print(f"Error writing to file: {e}")

def main():
    """
    Gets input from the user, checks if it's a palindrome, and stores the result.
    """
    input_string = input("Enter a string: ")
    result = is_palindrome(input_string)
    store_palindrome_result(input_string, result)

if __name__ == "__main__":
    main()