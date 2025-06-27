# Helmet of Darkness (HoD) v2.0

**HoD is a symbolic file reconstruction tool, not an encryption utility.**

It works by analyzing the bit patterns in a file and converting them into a set of purely reconstructive instructions, called a "keymap". The original file data is annihilated; only the abstract representation of its structure remains. This keymap can then be used to perfectly reconstruct the original file.

This v2.0 release is a production-grade expansion with a pluggable architecture for encoding strategies and output formats.

Security warning: This is not encryption.

## Features

- **Symbolic Encoding**: No file data is stored in the keymap.
- **Pluggable Strategies**: Use different algorithms to represent bit runs.
  - `rle`: Standard run-length `('1', 500)`.
  - `power`: Power notation `'1^500'`.
  - `fibonacci`: Represents run lengths as a sum of Fibonacci numbers.
- **Disguised Output Formats**: Save keymaps as `.json`, `.csv`, `.conf` (INI-style), or `.log` files to obscure their purpose.
- **Trust Pairing**: Optionally sign a keymap's payload with a passphrase-derived HMAC. This binds the keymap's integrity to the passphrase without encrypting it.
- **Full Integrity Checking**: Verify reconstructed files against a stored SHA256/SHA512/MD5 hash of the original.
