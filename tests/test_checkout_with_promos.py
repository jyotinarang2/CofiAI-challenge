import pytest
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from checkout_with_promos_improvement import Checkout, load_config, cli
from click.testing import CliRunner

CONFIG_PATH = "config.json"

def test_cli_missing_config():
    runner = CliRunner()
    result = runner.invoke(cli, ['--config', 'nonexistent.json'])
    assert result.exit_code != 0
    assert "Config file nonexistent.json not found." in result.output

def test_cli_no_items_scanned():
    runner = CliRunner()
    result = runner.invoke(cli, ['--config', CONFIG_PATH])
    assert result.exit_code != 0
    assert "No items scanned. Please provide item SKUs as arguments." in result.output

def test_cli_bad_config(tmp_path):
    bad = tmp_path/'bad.json'
    bad.write_text('{"invalid_json": }', encoding="utf-8")  # Create a bad JSON file
    runner = CliRunner()
    result = runner.invoke(cli, ['--config', str(bad), 'VOUCHER'])
    assert result.exit_code != 0
    assert "Error loading config" in result.output

#Test cli with valid config and items
def test_cli_valid_checkout():
    runner = CliRunner()
    result = runner.invoke(cli, ['--config', CONFIG_PATH, 'VOUCHER', 'TSHIRT', 'MUG'])
    assert result.exit_code == 0
    assert "Total amount" in result.output


def new_checkout():
    return load_config(CONFIG_PATH)

def test_single_voucher_no_discount():
    ck = new_checkout()
    ck.scan("VOUCHER")
    assert ck.total() == "5.00€" # No discount applied

def test_two_for_one_promo():
    ck = new_checkout()
    ck.scan("VOUCHER")
    ck.scan("VOUCHER")
    assert ck.total() == "5.00€"  # 2-for-1 promo applied

def test_bundle_promo():
    ck = new_checkout()
    ck.scan("VOUCHER")
    ck.scan("TSHIRT")
    ck.scan("MUG")
    assert ck.total() == "25.00€"  # Bundle price applied

def test_bulk_discount():
    ck = new_checkout()
    for _ in range(4):
        ck.scan("TSHIRT")
    assert ck.total() == "76.00€"  # Bulk discount applied

def test_unknown_sku():
    ck = new_checkout()
    with pytest.raises(ValueError):
        ck.scan("UNKNOWN") #Scan unknown SKU

def test_empty_cart():
    ck = new_checkout()
    assert ck.total() == "0.00€"  # No items scanned

def test_mixed_items():
    ck = new_checkout()
    items = ["VOUCHER", "TSHIRT", "MUG", "VOUCHER", "MUG", "TSHIRT", "TSHIRT"]
    for item in items:
        ck.scan(item)
    assert ck.total() == "70.00€"  # Mixed items with promos applied

def test_single_tshirt_no_discount():
    ck = new_checkout()
    ck.scan("TSHIRT")
    assert ck.total() == "20.00€"  # No discount applied

def test_single_mug_no_discount():
    ck = new_checkout()
    ck.scan("MUG")
    assert ck.total() == "7.50€"  # No discount applied


def no_discount_multiple_items():
    ck = new_checkout()
    items = ["MUG", "MUG"]
    for item in items:
        ck.scan(item)
    assert ck.total() == "15.00€"  # No promos applied

def test_odd_voucher_tip(capsys):
    ck = new_checkout()
    ck.scan("VOUCHER")
    ck.scan("VOUCHER")
    ck.scan("VOUCHER")  # Odd number of vouchers
    assert ck.total() == "10.00€"  # 2-for-1 promo applied, tip shown
    out = capsys.readouterr().out
    assert "Tip" in out  # Check for tip message

