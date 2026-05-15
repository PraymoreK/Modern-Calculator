from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from math import sqrt
import uvicorn
import webbrowser
import threading
import time

app = FastAPI()

class CalculationRequest(BaseModel):
    expression: str

class CalculationResponses(BaseModel):
    result: float
    error: str = None

@app.get("/", response_class=HTMLResponse)
def get_calculator():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Modern Calculator</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            .calculator {
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                width: 100%;
                max-width: 400px;
                padding: 30px;
                animation: slideUp 0.5s ease-out;
            }
            @keyframes slideUp {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            .display {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                font-size: 2.5rem;
                padding: 20px;
                border-radius: 15px;
                text-align: right;
                margin-bottom: 20px;
                min-height: 70px;
                word-wrap: break-word;
                word-break: break-all;
                font-weight: 300;
                letter-spacing: 1px;
            }
            .buttons-grid {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 12px;
            }
            button {
                padding: 20px;
                font-size: 1.3rem;
                border: none;
                border-radius: 12px;
                cursor: pointer;
                font-weight: 600;
                transition: all 0.3s ease;
                background: #f0f0f0;
                color: #333;
            }
            button:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
            }
            button:active {
                transform: translateY(0px);
            }
            button.operator {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            button.equals {
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: white;
                grid-column: span 2;
            }
            button.clear {
                background: #ff6b6b;
                color: white;
                grid-column: span 2;
            }
            .input-display {
                font-size: 0.9rem;
                color: rgba(255, 255, 255, 0.8);
                margin-bottom: 5px;
                min-height: 20px;
            }
        </style>
    </head>
    <body>
        <div class="calculator">
            <div class="display">
                <div class="input-display" id="input"></div>
                <div id="result">0</div>
            </div>
            <div class="buttons-grid">
                <button class="clear" onclick="clearDisplay()">Clear</button>
                <button class="operator" onclick="appendOperator('/')">÷</button>
                <button class="operator" onclick="appendOperator('*')">×</button>
                <button onclick="appendNumber('7')">7</button>
                <button onclick="appendNumber('8')">8</button>
                <button onclick="appendNumber('9')">9</button>
                <button class="operator" onclick="appendOperator('-')">−</button>
                <button onclick="appendNumber('4')">4</button>
                <button onclick="appendNumber('5')">5</button>
                <button onclick="appendNumber('6')">6</button>
                <button class="operator" onclick="appendOperator('+')">+</button>
                <button onclick="appendNumber('1')">1</button>
                <button onclick="appendNumber('2')">2</button>
                <button onclick="appendNumber('3')">3</button>
                <button class="operator" onclick="toggleSign()">+/−</button>
                <button onclick="appendNumber('0')" style="grid-column: span 2;">0</button>
                <button onclick="appendNumber('.')">.</button>
                <button class="operator" onclick="calculateSqrt()">√</button>
                <button class="equals" onclick="calculate()">=</button>
            </div>
        </div>
        <script>
            let expression = '';
            const resultDisplay = document.getElementById('result');
            const inputDisplay = document.getElementById('input');
            function appendNumber(num) {
                expression += num;
                updateDisplay();
            }
            function appendOperator(op) {
                if (expression && !isLastCharOperator()) {
                    expression += op;
                    updateDisplay();
                }
            }
            function isLastCharOperator() {
                return ['+', '-', '*', '/'].includes(expression.slice(-1));
            }
            function updateDisplay() {
                inputDisplay.textContent = expression;
            }
            function clearDisplay() {
                expression = '';
                resultDisplay.textContent = '0';
                inputDisplay.textContent = '';
            }
            function toggleSign() {
                if (expression) {
                    if (expression.startsWith('-')) {
                        expression = expression.slice(1);
                    } else {
                        expression = '-' + expression;
                    }
                    updateDisplay();
                }
            }
            function calculate() {
                if (!expression) return;
                fetch('/calculate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ expression })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        resultDisplay.textContent = 'Error';
                        expression = '';
                    } else {
                        resultDisplay.textContent = data.result;
                        expression = data.result.toString();
                    }
                    inputDisplay.textContent = '';
                })
                .catch(() => {
                    resultDisplay.textContent = 'Error';
                    expression = '';
                });
            }
            function calculateSqrt() {
                if (!expression) return;
                fetch('/sqrt', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ expression })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        resultDisplay.textContent = 'Error';
                        expression = '';
                    } else {
                        resultDisplay.textContent = data.result;
                        expression = data.result.toString();
                    }
                    inputDisplay.textContent = '';
                })
                .catch(() => {
                    resultDisplay.textContent = 'Error';
                    expression = '';
                });
            }
        </script>
    </body>
    </html>
    """

@app.post("/calculate")
def calculate(req: CalculationRequest):
    try:
        result = eval(req.expression)
        return CalculationResponses(result=float(result))
    except Exception as e:
        return CalculationResponses(result=0, error=str(e))

@app.post("/sqrt")
def calculate_sqrt(req: CalculationRequest):
    try:
        value = float(req.expression)
        if value < 0:
            return CalculationResponses(result=0, error="Cannot calculate sqrt of negative number")
        result = sqrt(value)
        return CalculationResponses(result=result)
    except Exception as e:
        return CalculationResponses(result=0, error=str(e))

if __name__ == "__main__":
    def open_browser():
        time.sleep(1)
        webbrowser.open("http://127.0.0.1:8000")
    threading.Thread(target=open_browser, daemon=True).start()
    uvicorn.run(app, host="127.0.0.1", port=8000)
