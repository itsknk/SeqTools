## SeqTools

A web application for comprehensive DNA sequence analysis, including translation, frame prediction, and open reading frame detection.

### Features

- **Basic DNA sequence operations:**
  - Reverse
  - Complement
  - Reverse Complement
- **Translation:**
  - Converts DNA to amino acid sequence
- **Prediction of coding reading frames:**
  - Filters coding frames based on minimum and maximum length
  - Identifies open reading frames (sequences without a STOP codon)

### Getting Started

#### Prerequisites

- Python 3.x
- Flask

#### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/itsknk/SeqTools.git
   ```
2. Change directory:
   ```bash
   cd SeqTools
   ```
3. Install dependencies:
   ```bash
   pip install Flask
   ```

#### Running the Application

1. Start the Flask server:
   ```bash
   python app.py
   ```
2. Open your web browser and navigate to `http://127.0.0.1:5000`.

### Usage

1. **Enter DNA Sequence:**
   - Input a DNA sequence (A, T, G, C only) in the text area.

2. **Select Operations:**
   - Choose the desired operations (Reverse, Complement, Reverse Complement, Translate, Predict Coding Frames) by checking the corresponding boxes.

3. **Set Options (if applicable):**
   - For translation, select the reading frame.
   - For coding frame prediction, set the minimum and maximum lengths.

4. **Process Sequence:**
   - Click the "Process" button to analyze the DNA sequence.

5. **View Results:**
   - The results will be displayed below the input area.

### Code Overview

#### `templates/index.html`

This file contains the HTML structure and JavaScript for the front-end interface. It includes:
- A text area for DNA sequence input.
- Checkboxes for selecting operations.
- Options for setting translation frame and coding frame length.
- A results section to display the output.

#### `app.py`

This file contains the Flask application logic. It includes:
- Functions for validating, reversing, complementing, and translating DNA sequences.
- Functions for predicting coding frames.
- Routes for rendering the main page and processing sequence data.

#### Key Functions:

- **`validate_dna(sequence)`**: Validates the DNA sequence.
- **`reverse_sequence(sequence)`**: Reverses the DNA sequence.
- **`complement_sequence(sequence)`**: Complements the DNA sequence.
- **`reverse_complement_sequence(sequence)`**: Generates the reverse complement of the DNA sequence.
- **`translate_sequence(sequence, frame)`**: Translates the DNA sequence to an amino acid sequence.
- **`predict_coding_frames(sequence, min_length, max_length)`**: Predicts coding frames in the DNA sequence.


### To do:

- Create a function to predict splice sites from a set of exon and intron sequences, and present the splicing results with likelihood scores indicating natural, wild-type splicing.
