from flask import render_template, current_app as app, request, jsonify
import math


@app.route('/')
def index():
    return render_template('index.html', title='Home')


@app.route('/arithmetic')
def arithmetic_view():
    return render_template('arithmetic.html', title='Operasi Aritmatika')


@app.route('/logic')
def logic_view():
    return render_template('logic.html', title='Operator Logika')


@app.route('/transform')
def transform_view():
    return render_template('transform.html', title='Transformasi Bilangan')


@app.route('/history')
def history_view():
    return render_template('history.html', title='Riwayat Perhitungan')


# Arithmetic operations
@app.route('/api/arithmetic', methods=['POST'])
def arithmetic():
    data = request.get_json() or {}
    a = data.get('a')
    b = data.get('b')
    op = data.get('op')
    formula = ""
    steps = []
    try:
        if op == 'add':
            res = a + b
            formula = f"{a} + {b}"
            steps = [f"Input: {a}, {b}", f"Langkah: Jumlahkan {a} dengan {b}", f"Hasil: {res}"]
        elif op == 'sub':
            res = a - b
            formula = f"{a} - {b}"
            steps = [f"Input: {a}, {b}", f"Langkah: Kurangkan {a} dengan {b}", f"Hasil: {res}"]
        elif op == 'mul':
            res = a * b
            formula = f"{a} × {b}"
            steps = [f"Input: {a}, {b}", f"Langkah: Kalikan {a} dengan {b}", f"Hasil: {res}"]
        elif op == 'div':
            res = a / b
            formula = f"{a} ÷ {b}"
            steps = [f"Input: {a}, {b}", f"Langkah: Bagi {a} dengan {b}", f"Hasil: {res}"]
        elif op == 'pow':
            res = a ** b
            formula = f"{a}^{b}"
            steps = [f"Input: {a}, {b}", f"Langkah: Hitung {a} pangkat {b}", f"Hasil: {res}"]
        elif op == 'root':
            res = a ** (1.0 / b)
            formula = f"{b}√{a}"
            steps = [f"Input: {a}, {b}", f"Langkah: Hitung akar ke-{b} dari {a}", f"Hasil: {res}"]
        elif op == 'mod':
            res = a % b
            formula = f"{a} mod {b}"
            steps = [f"Input: {a}, {b}", f"Langkah: Sisa bagi {a} dibagi {b}", f"Hasil: {res}"]
        elif op == 'floordiv':
            res = a // b
            formula = f"{a} // {b}"
            steps = [f"Input: {a}, {b}", f"Langkah: Pembagian bulat {a} dibagi {b}", f"Hasil: {res}"]
        else:
            return jsonify({'error': 'Unknown operation'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    return jsonify({'result': res, 'formula': formula, 'steps': steps})


# Logical / bitwise operations (integers)
@app.route('/api/logic', methods=['POST'])
def logic():
    data = request.get_json() or {}
    # Convert incoming strings "true"/"false" to actual Python Booleans
    a_str = str(data.get('a')).lower()
    b_str = str(data.get('b')).lower()
    a = True if a_str == 'true' else False
    b = True if b_str == 'true' else False
    op = data.get('op')
    formula = ""
    steps = []
    try:
        if op == 'not':
            res = not a
            formula = f"NOT {a}"
            steps = [f"Input: {a}", "Langkah: Membalikkan nilai logika", f"Hasil: {res}"]
        elif op == 'and':
            res = a and b
            formula = f"{a} AND {b}"
            steps = [f"Input: {a}, {b}", f"Langkah: True jika keduanya True", f"Hasil: {res}"]
        elif op == 'or':
            res = a or b
            formula = f"{a} OR {b}"
            steps = [f"Input: {a}, {b}", f"Langkah: True jika salah satu True", f"Hasil: {res}"]
        elif op == 'xor':
            res = a != b
            formula = f"{a} XOR {b}"
            steps = [f"Input: {a}, {b}", f"Langkah: True jika nilai berbeda", f"Hasil: {res}"]
        elif op == 'nand':
            res = not (a and b)
            formula = f"NOT ({a} AND {b})"
            steps = [f"Input: {a}, {b}", f"Langkah: NOT dari (a AND b)", f"Hasil: {res}"]
        elif op == 'nor':
            res = not (a or b)
            formula = f"NOT ({a} OR {b})"
            steps = [f"Input: {a}, {b}", f"Langkah: NOT dari (a OR b)", f"Hasil: {res}"]
        else:
            return jsonify({'error': 'Unknown logic op'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    return jsonify({'result': res, 'formula': formula, 'steps': steps})


# Base conversion
@app.route('/api/convert/base', methods=['POST'])
def convert_base():
    data = request.get_json() or {}
    value = str(data.get('value', ''))
    fb = int(data.get('from', 10))
    tb = int(data.get('to', 10))
    try:
        n = int(value, fb)
        steps = [f"Input: {value} (Basis {fb})"]
        
        # Detail conversion to decimal
        if fb != 10:
            explanation = " + ".join([f"({digit} × {fb}^{i})" for i, digit in enumerate(reversed(value))])
            steps.append(f"Langkah 1: Konversi ke Desimal (Base 10)")
            steps.append(f"Rumus: Σ (digit × basis^posisi)")
            steps.append(f"Proses: {explanation} = {n}")
        else:
            steps.append(f"Langkah 1: Nilai sudah dalam Desimal ({n})")

        if tb == 2:
            out = bin(n)[2:]
            steps.append(f"Langkah 2: Konversi Desimal {n} ke Biner (Base 2)")
            steps.append(f"Hasil: {out}")
        elif tb == 8:
            out = oct(n)[2:]
            steps.append(f"Langkah 2: Konversi Desimal {n} ke Oktal (Base 8)")
            steps.append(f"Hasil: {out}")
        elif tb == 16:
            out = hex(n)[2:].upper()
            steps.append(f"Langkah 2: Konversi Desimal {n} ke Heksadesimal (Base 16)")
            steps.append(f"Hasil: {out}")
        else:
            out = str(n)
            steps.append(f"Langkah 2: Target adalah Desimal, tidak ada perubahan.")
            
        formula = f"{value}({fb}) → {out}({tb})"
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    return jsonify({'result': out, 'formula': formula, 'steps': steps})


# Temperature conversion
@app.route('/api/convert/temp', methods=['POST'])
def convert_temp():
    data = request.get_json() or {}
    v = float(data.get('value', 0))
    frm = data.get('from')
    to = data.get('to')
    
    formula = f"{v}°{frm} → {to}"
    steps = [f"Input: {v}°{frm}"]

    def to_celsius(x, f):
        if f == 'C': return x, x
        if f == 'F': return (x - 32) * 5.0 / 9.0, f"({x}-32)*5/9"
        if f == 'K': return x - 273.15, f"{x}-273.15"
        if f == 'R': return x * 5.0 / 4.0, f"{x}*5/4"

    def from_celsius(c, t):
        if t == 'C': return c, c
        if t == 'F': return c * 9.0 / 5.0 + 32, f"({c}*9/5)+32"
        if t == 'K': return c + 273.15, f"{c}+273.15"
        if t == 'R': return c * 4.0 / 5.0, f"{c}*4/5"

    try:
        c, s1 = to_celsius(v, frm)
        if frm != 'C': steps.append(f"Langkah 1: Konversi ke Celsius = {s1} = {c}°C")
        res, s2 = from_celsius(c, to)
        if to != 'C': steps.append(f"Langkah 2: Konversi ke {to} = {s2} = {res}°{to}")
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    return jsonify({'result': res, 'formula': formula, 'steps': steps})


# Simple currency conversion (static rates updated)
RATES = {'IDR': 1.0, 'USD': 17516.84, 'EUR': 20452.50, 'SGD': 13761.30}

@app.route('/api/convert/currency', methods=['POST'])
def convert_currency():
    data = request.get_json() or {}
    amt = float(data.get('amount', 0))
    frm = data.get('from')
    to = data.get('to')
    try:
        idr = amt * RATES[frm]
        out = idr / RATES[to]
        formula = f"{amt} {frm} → {to}"
        steps = [
            f"Kurs 1 {frm} = Rp{RATES[frm]:,.2f}",
            f"Kurs 1 {to} = Rp{RATES[to]:,.2f}",
            f"Langkah 1: {amt} {frm} × {RATES[frm]} = Rp{idr:,.2f} (Base IDR)",
            f"Langkah 2: Rp{idr:,.2f} ÷ {RATES[to]} = {out:,.2f} {to}"
        ]
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    return jsonify({'result': f"{out:,.2f}", 'formula': formula, 'steps': steps})


# Factorial
@app.route('/api/factorial', methods=['POST'])
def factorial():
    data = request.get_json() or {}
    n = int(data.get('n', 0))
    if n < 0: return jsonify({'error': 'n must be >= 0'}), 400
    res = 1
    for i in range(2, n + 1): res *= i
    formula = f"{n}! = n × (n-1) × ... × 1"
    steps = [
        f"Input: n = {n}",
        f"Rumus: {n}! = " + " × ".join([str(i) for i in range(n, 0, -1)]) if n <= 10 else f"{n} × {n-1} × ... × 1",
        f"Langkah: Mengalikan semua bilangan bulat positif hingga {n}",
        f"Hasil: {res}"
    ]
    return jsonify({'result': res, 'formula': formula, 'steps': steps})


# Fibonacci sequence
@app.route('/api/fibonacci', methods=['POST'])
def fibonacci():
    data = request.get_json() or {}
    n = int(data.get('n', 10))
    if n < 0: return jsonify({'error': 'n must be >= 0'}), 400
    seq = []
    a, b = 0, 1
    for _ in range(n):
        seq.append(a)
        a, b = b, a + b
    formula = "F(n) = F(n-1) + F(n-2)"
    steps = [
        f"Target: {n} suku pertama",
        "Rumus: Suku berikutnya adalah jumlah dari dua suku sebelumnya.",
        f"Proses: 0, 1, (0+1)=1, (1+1)=2, (1+2)=3, ...",
        f"Hasil: {seq}"
    ]
    return jsonify({'result': seq, 'formula': formula, 'steps': steps})
