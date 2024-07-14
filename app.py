from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def validate_dna(sequence):
    valid_nucleotides = ['A', 'T', 'G', 'C']
    for nucleotide in sequence:
        if nucleotide not in valid_nucleotides:
            return False
    return True

def reverse_sequence(sequence):
    reversed_seq = ''
    for i in range(len(sequence) - 1, -1, -1):
        reversed_seq += sequence[i]
    return reversed_seq

def complement_sequence(sequence):
    complement_dict = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
    complemented_seq = ''
    for nucleotide in sequence:
        complemented_seq += complement_dict[nucleotide]
    return complemented_seq

def reverse_complement_sequence(sequence):
    return complement_sequence(reverse_sequence(sequence))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    sequence = request.json['sequence'].upper()
    operations = request.json['operations']
    
    if not validate_dna(sequence):
        return jsonify({'error': 'Invalid DNA sequence. Please enter a sequence containing only A, T, G, and C.'})
    
    results = {'original': sequence}
    
    if 'reverse' in operations:
        results['reverse'] = reverse_sequence(sequence)
    if 'complement' in operations:
        results['complement'] = complement_sequence(sequence)
    if 'reverse_complement' in operations:
        results['reverse_complement'] = reverse_complement_sequence(sequence)
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
