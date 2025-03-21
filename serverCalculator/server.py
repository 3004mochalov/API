from flask import Flask, request, jsonify

app = Flask(__name__)

# Пример API для калькулятора
@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    num1 = float(data.get('num1', 0))
    num2 = float(data.get('num2', 0))
    operation = data.get('operation')

    if operation == 'add':
        result = num1 + num2
    elif operation == 'subtract':
        result = num1 - num2
    elif operation == 'multiply':
        result = num1 * num2
    elif operation == 'divide':
        if num2 != 0:
            result = num1 / num2
        else:
            return jsonify({"error": "Деление на ноль"}), 400
    else:
        return jsonify({"error": "Неверная операция"}), 400

    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)
