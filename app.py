from flask import Flask, render_template, request, jsonify
import hashlib

app = Flask(__name__, template_folder='./templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crack', methods=['POST'])
def crack():
    hash_to_crack = request.form.get('hash')
    wordlist_path = request.form.get('wordlist')

    if not hash_to_crack or not wordlist_path:
        return jsonify({'status': 'error', 'message': 'Hash or wordlist not provided'})

    def crack_hash():
        try:
            with open(wordlist_path, 'r') as f:
                for line in f:
                    word = line.strip()

                    md5_hash = hashlib.md5(word.encode()).hexdigest()
                    sha1_hash = hashlib.sha1(word.encode()).hexdigest()
                    sha256_hash = hashlib.sha256(word.encode()).hexdigest()

                    if md5_hash == hash_to_crack:
                        return word, "MD5"
                    elif sha1_hash == hash_to_crack:
                        return word, "SHA-1"
                    elif sha256_hash == hash_to_crack:
                        return word, "SHA-256"
        except FileNotFoundError:
            return None, None

        return None, None

    cracked_password, algorithm = crack_hash()
    if cracked_password:
        return jsonify({'status': 'success', 'password': cracked_password, 'algorithm': algorithm})
    else:
        return jsonify({'status': 'failure', 'message': 'Password not found in wordlist'})

if __name__ == '__main__':
    app.run(debug=True)
