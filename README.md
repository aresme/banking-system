# 🏦 Banking System

A professional digital banking application built with Python and CustomTkinter, designed to provide a secure and user-friendly banking experience.

## 📸 Screenshots

![Jambo Bank Professional](screenshots/jambo_bank_pro_home.png)
*Jambo Bank Professional Edition - Welcome Screen*

## Features

- **Account Management**
  - Create new accounts with validation
  - Secure login with PIN verification
  - Account number generation
  
- **Banking Operations**
  - Deposit funds
  - Withdraw funds
  - View account balance
  - Mini statement with transaction history
  - Change PIN securely
  
- **Security**
  - PIN hashing with SHA256
  - Secure password verification
  - Transaction logging
  - Account data persistence

- **Professional Version (jambo_bank_pro.py)**
  - Enhanced UI with better styling
  - Advanced transaction management
  - Comprehensive logging
  - Improved error handling
  - Additional banking features

## Requirements

- Python 3.8+
- customtkinter
- tkinter (usually comes with Python)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/banking-system.git
cd banking-system
```

2. Create a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
source .venv/bin/activate  # On macOS/Linux
```

3. Install dependencies:
```bash
pip install customtkinter
```

## Usage

### Basic Version
```bash
python jambo_bank.py
```

### Professional Version (Recommended)
```bash
python jambo_bank_pro.py
```

## Default Credentials

After creating an account:
- **Account Number**: Randomly generated (e.g., JB1234567890)
- **Temporary PIN**: 1234
- **⚠️ Important**: Change your PIN after first login

## File Structure

```
banking-system/
├── jambo_bank.py           # Basic banking application
├── jambo_bank_pro.py       # Professional banking application
├── README.md               # This file
├── .gitignore             # Git ignore rules
└── jambobank.log          # Application logs (generated)
```

## Account Data Storage

Account information is stored locally in JSON format:
- Basic version: `jambobank_account.json`
- Professional version: `jambobank_pro_account.json`

**⚠️ Security Note**: In production, use proper database encryption and never store sensitive data in plain JSON files.

## Security Considerations

- PINs are hashed using SHA256 in the professional version
- All transactions are logged
- Local file storage for demo purposes only
- For production use, implement:
  - Database encryption
  - HTTPS connections
  - Two-factor authentication
  - Regular security audits

## Development

The system is built with:
- **CustomTkinter**: Modern GUI framework for Python
- **JSON**: Local data persistence
- **Logging**: Transaction and error tracking

## License

This project is open source and available for educational purposes.

## Support

For issues or questions, please open an issue on the repository.

---

**Made with ❤️ for Kenya's Digital Banking Future**
