# 🔢 Number Puzzle Generator

A web-based number crossword puzzle generator that creates challenging puzzles similar to those found in newspapers and puzzle magazines.

![Number Puzzle Generator](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎯 What is a Number Puzzle?

Number puzzles are crossword-style games played on a 15x15 grid where:
- Players must place numbers (2-7 digits) both horizontally and vertically
- Numbers can intersect and share common digits
- Black cells separate different numbers
- Hint digits are provided to help solve the puzzle
- All given numbers must be used exactly once

## ✨ Features

- **Instant Puzzle Generation**: Creates puzzles in seconds using advanced algorithms
- **Smart Grid Layout**: Automatically places black cells to separate numbers properly
- **Realistic Numbers**: Generates valid numbers (no leading zeros like 001, 04)
- **Pattern Breaking**: Prevents repetitive sequences (8888, 777, etc.)
- **Responsive Design**: Works on desktop and mobile devices
- **Solution Viewer**: Toggle between puzzle and solution views
- **Clean Interface**: Modern, user-friendly web interface

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Flask 2.0 or higher

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/KurKigal/number-puzzle-generator.git
   cd number-puzzle-generator
   ```

2. **Install dependencies**
   ```bash
   pip install flask
   ```

3. **Create folder structure**
   ```bash
   mkdir templates
   mv index.html templates/
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open in browser**
   ```
   http://localhost:5000
   ```

## 📁 Project Structure

```
number-puzzle-generator/
├── app.py              # Flask backend application
├── templates/
│   └── index.html      # Frontend interface
└── README.md           # Documentation
```

## 🎮 How to Use

1. **Generate Puzzle**: Click "Generate New Puzzle" button
2. **View Numbers**: Numbers are categorized by digit count (7-digit to 2-digit)
3. **Solve Puzzle**: Place the given numbers in the 15x15 grid
4. **Check Solution**: Use "Show/Hide Solution" to verify your answers

## 🔧 Algorithm Overview

The puzzle generation uses a sophisticated multi-step algorithm:

1. **Initial Setup**: Place random black cells (~8-12% of grid)
2. **Fill Grid**: Populate all white cells with random digits (0-9)
3. **Pattern Breaking**: Eliminate repetitive sequences (8888 → 8923)
4. **Smart Separation**: Add strategic black cells to separate numbers
5. **Zero Fixing**: Ensure no numbers start with zero
6. **Coverage Check**: Verify all cells belong to valid numbers
7. **Number Extraction**: Collect all horizontal and vertical number sequences
8. **Hint Selection**: Choose 5-8 random cells as hints
9. **Grid Cleaning**: Remove all numbers except hints for the puzzle

## 🎯 Key Features of the Algorithm

- **No Leading Zeros**: Automatically prevents invalid numbers like 04, 003
- **Smart Separation**: Prevents two 4-digit numbers from appearing as one 8-digit number
- **Pattern Prevention**: Breaks up repetitive sequences like 7777, 888
- **Complete Coverage**: Ensures every white cell is part of a valid number
- **Balanced Difficulty**: Creates puzzles with appropriate number distributions

## 🛠️ Technical Details

### Backend (Flask/Python)
- **Fast Generation**: Creates puzzles in 1-3 seconds
- **Robust Algorithm**: Handles edge cases and guarantees valid puzzles
- **RESTful API**: Clean endpoints for puzzle generation
- **Error Handling**: Graceful handling of generation failures

### Frontend (HTML/CSS/JavaScript)
- **Responsive Grid**: 15x15 display that works on all screen sizes
- **Visual Feedback**: Clear distinction between black cells, hints, and empty spaces
- **Sorted Display**: Numbers organized largest to smallest for easy reading
- **Interactive Controls**: Simple buttons for generation and solution viewing

## 🔍 Example Output

**Numbers to Place:**
- 7 DIGITS: 9876543, 8765432, 7654321
- 6 DIGITS: 987654, 876543, 765432
- 5 DIGITS: 98765, 87654, 76543
- 4 DIGITS: 9876, 8765, 7654
- 3 DIGITS: 987, 876, 765
- 2 DIGITS: 98, 87, 76

## 🤝 Contributing

Contributions are welcome! Here are some ways to contribute:

- **Bug Reports**: Found a bug? Open an issue
- **Feature Requests**: Have an idea? Suggest it
- **Code Improvements**: Submit pull requests
- **Documentation**: Help improve the docs

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Inspired by traditional number crossword puzzles found in newspapers
- Built with Flask for simplicity and performance
- Designed for puzzle enthusiasts and developers alike

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/KurKigal/number-puzzle-generator/issues) page
2. Create a new issue if your problem isn't listed
3. Provide clear steps to reproduce any bugs

---

**Enjoy creating and solving number puzzles!** 🧩✨
