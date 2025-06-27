#!/usr/bin/env python3
# hod.py
import os
import sys
import logging
import click

# --- Dynamic Loading ---
# This ensures strategies and formats are loaded when the CLI starts.
from strategies import STRATEGIES, load_strategies
from formats import FORMATS, load_formats_by_name, load_formats_by_ext

# --- Utilities ---
from utils.core import generate_bit_runs
from utils.hashing import calculate_file_hash, sign_payload, verify_payload
from utils.meta import create_metadata
from utils.display import pretty_print_payload

# --- Setup ---
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"), format='%(asctime)s [%(levelname)s] %(message)s')
load_strategies()
load_formats_by_name()
load_formats_by_ext()


@click.group()
@click.version_option(version="2.0", prog_name="HoD")
def cli():
    """
    Helmet of Darkness (HoD) v2.0: A tool for symbolic file reconstruction.
    
    HoD encodes files into purely reconstructive keymaps without storing file data.
    This version supports pluggable strategies, disguised output formats, and
    optional trust-pairing via HMAC signing.
    """
    pass


@cli.command()
@click.argument('input_file', type=click.Path(exists=True, dir_okay=False))
@click.argument('output_file', type=click.Path(dir_okay=False))
@click.option('--strategy', '-s', type=click.Choice(list(STRATEGIES.keys())), default='rle', help='Encoding strategy to use.')
@click.option('--hash', 'hash_algo', type=click.Choice(['sha256', 'sha512', 'md5']), help='Calculate and store a hash of the original file for integrity checks.')
@click.option('--passphrase', prompt=False, hide_input=True, confirmation_prompt=False, help='A passphrase to bind the keymap with an HMAC signature.')
@click.option('--format', 'output_format_name', type=click.Choice(list(FORMATS.keys())), help='Output format. Inferred from output extension if not provided.')
def encode(input_file, output_file, strategy, hash_algo, passphrase, output_format_name):
    """Encode a file into a symbolic HoD keymap."""
    logging.info(f"Starting encoding of '{input_file}'")

    # 1. Select Strategy and Format
    encoder = STRATEGIES[strategy]
    if output_format_name:
        output_format = FORMATS[output_format_name]
    else:
        _, ext = os.path.splitext(output_file)
        if ext in FORMATS_BY_EXT:
            output_format = FORMATS_BY_EXT[ext]
            logging.info(f"Inferred output format '{output_format.name}' from extension '{ext}'")
        else:
            output_format = FORMATS['json']
            logging.warning(f"Unknown extension. Defaulting to '{output_format.name}'.")

    # 2. Generate Core Symbolic Representation (Bit Runs)
    logging.info("Generating bit runs from source file...")
    with open(input_file, 'rb') as f:
        bit_runs = list(generate_bit_runs(f))
    
    # 3. Create Metadata
    file_hash = calculate_file_hash(input_file, hash_algo) if hash_algo else None
    input_size = os.path.getsize(input_file)
    metadata = create_metadata(input_file, input_size, encoder.name, hash_algo, file_hash)

    # 4. Use Strategy to Encode Payload
    logging.info(f"Encoding payload with '{encoder.name}' strategy...")
    payload = encoder.encode(bit_runs)
    
    # 5. Build final Keymap
    keymap = {**metadata, "payload": payload}

    # 6. (Optional) Sign Payload with HMAC
    if passphrase:
        logging.info("Signing payload with passphrase-derived HMAC...")
        signature = sign_payload(payload, passphrase)
        keymap['integrity']['payload_hmac_signature'] = signature

    # 7. Serialize to Disguised Format
    logging.info(f"Serializing keymap to '{output_format.name}' format at '{output_file}'")
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            output_format.serialize(keymap, f)
    except Exception as e:
        logging.error(f"Failed to write output file: {e}")
        sys.exit(1)

    logging.info(f"✅ Encoding successful. Keymap saved to '{output_file}'.")


@cli.command()
@click.argument('input_hod', type=click.Path(exists=True, dir_okay=False))
@click.argument('output_file', type=click.Path(dir_okay=False))
@click.option('--passphrase', prompt=False, hide_input=True, help='The passphrase used to sign the keymap.')
@click.option('--show-payload', is_flag=True, help='Pretty-print the symbolic payload and exit.')
def decode(input_hod, output_file, passphrase, show_payload):
    """Decode a HoD keymap to reconstruct the original file."""
    logging.info(f"Starting decoding of '{input_hod}'")

    # 1. Select Format and Deserialize
    _, ext = os.path.splitext(input_hod)
    if ext not in FORMATS_BY_EXT:
        logging.error(f"Unknown file format extension '{ext}'. Cannot decode.")
        sys.exit(1)
    
    input_format = FORMATS_BY_EXT[ext]
    logging.info(f"Detected keymap format '{input_format.name}'")
    try:
        with open(input_hod, 'r', encoding='utf-8') as f:
            keymap = input_format.deserialize(f)
    except Exception as e:
        logging.error(f"Failed to parse keymap file: {e}")
        sys.exit(1)

    # 2. Extract Data and Select Strategy
    strategy_name = keymap.get('strategy')
    payload = keymap.get('payload')
    integrity = keymap.get('integrity', {})
    if not strategy_name or strategy_name not in STRATEGIES:
        logging.error(f"Unknown or missing strategy '{strategy_name}' in keymap.")
        sys.exit(1)
    decoder = STRATEGIES[strategy_name]

    # 3. (Optional) Verify HMAC Signature
    hmac_sig = integrity.get('payload_hmac_signature')
    if hmac_sig:
        if not passphrase:
            logging.error("This keymap is trust-paired. Please provide the --passphrase to decode.")
            sys.exit(1)
        if not verify_payload(payload, hmac_sig, passphrase):
            logging.error("❌ HMAC signature verification FAILED. The keymap may be tampered with or the passphrase is incorrect.")
            sys.exit(1)
        logging.info("HMAC signature verified successfully.")
    elif passphrase:
        logging.warning("Passphrase provided, but the keymap is not trust-paired (no HMAC signature found).")

    # 4. Decode Payload to Universal Bit Runs
    logging.info(f"Decoding payload using '{decoder.name}' strategy...")
    try:
        bit_runs = decoder.decode(payload)
    except Exception as e:
        logging.error(f"Failed to decode payload: {e}")
        sys.exit(1)

    # 5. Handle --show-payload flag
    if show_payload:
        pretty_print_payload(strategy_name, payload)
        sys.exit(0)

    # 6. Reconstruct File
    logging.info(f"Reconstructing original file at '{output_file}'...")
    try:
        with open(output_file, 'wb') as f:
            current_byte = 0
            bit_count = 0
            for bit, count in bit_runs:
                for _ in range(count):
                    current_byte = (current_byte << 1) | (1 if bit == '1' else 0)
                    bit_count += 1
                    if bit_count == 8:
                        f.write(current_byte.to_bytes(1, 'big'))
                        current_byte = 0
                        bit_count = 0
            # Write any remaining bits if the file size isn't a multiple of 8
            if bit_count > 0:
                 current_byte <<= (8 - bit_count)
                 f.write(current_byte.to_bytes(1, 'big'))

    except Exception as e:
        logging.error(f"Failed during file reconstruction: {e}")
        sys.exit(1)

    # 7. (Optional) Verify Reconstructed File Hash
    original_hash = integrity.get('file_hash')
    if original_hash:
        hash_algo = integrity.get('file_hash_algorithm')
        logging.info(f"Verifying reconstructed file against stored {hash_algo} hash...")
        reconstructed_hash = calculate_file_hash(output_file, hash_algo)
        if reconstructed_hash == original_hash:
            logging.info("✅ Hash verification successful. File reconstructed perfectly.")
        else:
            logging.warning("⚠️ HASH MISMATCH! Reconstructed file does not match the original hash.")
            logging.warning(f"  Original:     {original_hash}")
            logging.warning(f"  Reconstructed:{reconstructed_hash}")
    else:
        logging.info(f"✅ Decoding complete. No original file hash was stored to verify against.")


@cli.command("list-strategies")
def list_strategies():
    """List all available encoding strategies."""
    print("Available Encoding Strategies:")
    for name, strategy in STRATEGIES.items():
        print(f"  - {name}")

if __name__ == '__main__':
    cli()
