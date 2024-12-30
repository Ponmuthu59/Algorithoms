from flask import Flask, request, render_template, jsonify
import hashlib
import base64
import secrets

app = Flask(__name__)

# Diffie-Hellman Algorithm
def generate_diffie_hellman_steps(p, g, a, b):
    steps = []
    steps.append(f"Step 1: Chosen prime number p = {p}")
    steps.append(f"Step 2: Chosen primitive root modulo p, g = {g}")
    steps.append(f"Step 3: Random private keys selected: a = {a}, b = {b}")
    
    A = pow(g, a, p)
    B = pow(g, b, p)
    steps.append(f"Step 4: Compute public keys: A = g^a mod p = {A}, B = g^b mod p = {B}")
    
    shared_key_A = pow(B, a, p)
    shared_key_B = pow(A, b, p)
    steps.append(f"Step 5: Compute shared secrets: shared_key_A = B^a mod p = {shared_key_A}, shared_key_B = A^b mod p = {shared_key_B}")
    
    steps.append(f"Final Step: Shared Key (should match): {shared_key_A}")
    return steps

# MD5 Algorithm
def generate_md5_steps(text):
    return [
        f"Step 1: Convert the text to bytes: '{text.encode()}'",
        f"Step 2: Compute MD5 hash: '{hashlib.md5(text.encode()).hexdigest()}'"
    ]

# SHA256 Algorithm
def generate_sha256_steps(text):
    return [
        f"Step 1: Convert the text to bytes: '{text.encode()}'",
        f"Step 2: Compute SHA256 hash: '{hashlib.sha256(text.encode()).hexdigest()}'"
    ]

# Base64 Algorithm
def generate_base64_steps(text):
    return [
        f"Step 1: Convert the text to bytes: '{text.encode()}'",
        f"Step 2: Encode using Base64: '{base64.b64encode(text.encode()).decode()}'"
    ]

# Binary Conversion
def generate_binary_steps(text):
    binary_values = [format(ord(char), '08b') for char in text]
    steps = ["Step 1: Convert each character to binary:"]
    steps += [f"Character '{char}' -> Binary '{binary}'" for char, binary in zip(text, binary_values)]
    steps.append(f"Final Step: Binary Representation: {' '.join(binary_values)}")
    return steps

# Octal Conversion
def generate_octal_steps(text):
    octal_values = [oct(ord(char))[2:] for char in text]
    steps = ["Step 1: Convert each character to octal:"]
    steps += [f"Character '{char}' -> Octal '{octal}'" for char, octal in zip(text, octal_values)]
    steps.append(f"Final Step: Octal Representation: {' '.join(octal_values)}")
    return steps

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    algorithm = request.form.get('algorithm')
    text = request.form.get('text')
    p = request.form.get('p')
    g = request.form.get('g')
    a = request.form.get('a')
    b = request.form.get('b')
    
    steps = []

    # Handling non-Diffie-Hellman algorithms (MD5, SHA-256, Base64, Binary, Octal)
    if algorithm != "diffie_hellman" and text:
        if algorithm == "md5":
            steps = generate_md5_steps(text)
        elif algorithm == "sha256":
            steps = generate_sha256_steps(text)
        elif algorithm == "base64":
            steps = generate_base64_steps(text)
        elif algorithm == "binary":
            steps = generate_binary_steps(text)
        elif algorithm == "octal":
            steps = generate_octal_steps(text)
    
    # Handling Diffie-Hellman Algorithm (requires numbers only)
    elif algorithm == "diffie_hellman" and p and g and a and b:
        p = int(p)
        g = int(g)
        a = int(a)
        b = int(b)
        steps = generate_diffie_hellman_steps(p, g, a, b)
    
    else:
        return jsonify({"error": "Invalid input!"}), 400

    return jsonify({"steps": steps})

if __name__ == '__main__':
    app.run(debug=True)
