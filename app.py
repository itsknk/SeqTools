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

def translate_sequence(sequence, frame=1):
    genetic_code = {
        'AUA':'I', 'AUC':'I', 'AUU':'I', 'AUG':'M',
        'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACU':'T',
        'AAC':'N', 'AAU':'N', 'AAA':'K', 'AAG':'K',
        'AGC':'S', 'AGU':'S', 'AGA':'R', 'AGG':'R',
        'CUA':'L', 'CUC':'L', 'CUG':'L', 'CUU':'L',
        'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCU':'P',
        'CAC':'H', 'CAU':'H', 'CAA':'Q', 'CAG':'Q',
        'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGU':'R',
        'GUA':'V', 'GUC':'V', 'GUG':'V', 'GUU':'V',
        'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCU':'A',
        'GAC':'D', 'GAU':'D', 'GAA':'E', 'GAG':'E',
        'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGU':'G',
        'UCA':'S', 'UCC':'S', 'UCG':'S', 'UCU':'S',
        'UUC':'F', 'UUU':'F', 'UUA':'L', 'UUG':'L',
        'UAC':'Y', 'UAU':'Y', 'UAA':'_', 'UAG':'_',
        'UGC':'C', 'UGU':'C', 'UGA':'_', 'UGG':'W',
    }
    
    rna_sequence = sequence.replace('T', 'U')
    
    offset = frame - 1
    rna_sequence = rna_sequence[offset:]
    
    amino_acid_sequence = ''
    for i in range(0, len(rna_sequence) - 2, 3):
        codon = rna_sequence[i:i+3]
        if len(codon) == 3:
            amino_acid = genetic_code.get(codon, 'X')
            amino_acid_sequence += amino_acid
    
    return amino_acid_sequence

def predict_coding_frames(sequence, min_length=0, max_length=float('inf')):
    genetic_code = {
        'AUA':'I', 'AUC':'I', 'AUU':'I', 'AUG':'M',
        'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACU':'T',
        'AAC':'N', 'AAU':'N', 'AAA':'K', 'AAG':'K',
        'AGC':'S', 'AGU':'S', 'AGA':'R', 'AGG':'R',
        'CUA':'L', 'CUC':'L', 'CUG':'L', 'CUU':'L',
        'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCU':'P',
        'CAC':'H', 'CAU':'H', 'CAA':'Q', 'CAG':'Q',
        'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGU':'R',
        'GUA':'V', 'GUC':'V', 'GUG':'V', 'GUU':'V',
        'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCU':'A',
        'GAC':'D', 'GAU':'D', 'GAA':'E', 'GAG':'E',
        'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGU':'G',
        'UCA':'S', 'UCC':'S', 'UCG':'S', 'UCU':'S',
        'UUC':'F', 'UUU':'F', 'UUA':'L', 'UUG':'L',
        'UAC':'Y', 'UAU':'Y', 'UAA':'_', 'UAG':'_',
        'UGC':'C', 'UGU':'C', 'UGA':'_', 'UGG':'W',
    }
    
    rna_sequence = sequence.replace('T', 'U')
    coding_frames = []

    for frame in range(3):
        frame_sequence = rna_sequence[frame:]
        amino_acid_sequence = ''
        start_index = None

        for i in range(0, len(frame_sequence) - 2, 3):
            codon = frame_sequence[i:i+3]
            if len(codon) == 3:
                amino_acid = genetic_code.get(codon, 'X')
                
                if amino_acid == 'M' and start_index is None:
                    start_index = i
                
                if start_index is not None:
                    amino_acid_sequence += amino_acid
                
                if amino_acid == '_' or i + 3 >= len(frame_sequence) - 2:
                    if start_index is not None and min_length <= len(amino_acid_sequence) <= max_length:
                        coding_frames.append({
                            'frame': frame + 1,
                            'start': start_index + frame + 1,
                            'end': i + frame + 3,
                            'sequence': amino_acid_sequence,
                            'is_open': amino_acid != '_'
                        })
                    start_index = None
                    amino_acid_sequence = ''

    return coding_frames

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
    if 'translate' in operations:
        frame = request.json.get('offset', 0) + 1  # Convert offset to frame
        results['translate'] = translate_sequence(sequence, frame)
    if 'predict_coding_frames' in operations:
        min_length = request.json.get('min_length', 0)
        max_length = request.json.get('max_length', float('inf'))
        results['coding_frames'] = predict_coding_frames(sequence, min_length, max_length)
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
