from http.server import HTTPServer, BaseHTTPRequestHandler
import json

def calculate_loan_to_value_ratio(loan_amount: float, property_value: float) -> float:
    return (loan_amount / property_value) * 100

def calculate_debt_to_income_ratio(loan_amount: float, income: float, loan_term: int) -> float:
    monthly_payment = loan_amount / loan_term
    return (monthly_payment / (income / 12)) * 100

def predict_loan_approval(application: dict) -> bool:
    score = 0
    
    # Age factor
    if 25 <= int(application['age']) <= 45:
        score += 10
    elif 45 < int(application['age']) <= 60:
        score += 5
    print(f"Score after age factor: {score}")

    # Employment status
    if application['employmentStatus'] == "Employed":
        score += 15
    elif application['employmentStatus'] == "Self-Employed":
        score += 10
    print(f"Score after employment status: {score}")

    # Credit score
    if int(application['creditScore']) >= 750:
        score += 20
    elif 650 <= int(application['creditScore']) < 750:
        score += 15
    elif 550 <= int(application['creditScore']) < 650:
        score += 5
    print(f"Score after credit score: {score}")

    # Loan to Value ratio
    ltv_ratio = calculate_loan_to_value_ratio(float(application['loanAmount']), float(application['propertyValue']))
    if ltv_ratio <= 80:
        score += 15
    elif 80 < ltv_ratio <= 90:
        score += 10
    elif 90 < ltv_ratio <= 95:
        score += 5
    print(f"Score after loan to value ratio: {score}, LTV Ratio: {ltv_ratio}")

    # Debt to Income ratio
    dti_ratio = calculate_debt_to_income_ratio(float(application['loanAmount']), float(application['income']), int(application['loanTerm']))
    if dti_ratio <= 36:
        score += 20
    elif 36 < dti_ratio <= 43:
        score += 10
    print(f"Score after debt to income ratio: {score}, DTI Ratio: {dti_ratio}")

    # Income to Loan Amount ratio
    income_loan_ratio = float(application['income']) / float(application['loanAmount'])
    if income_loan_ratio >= 1:
        score += 20
    elif 0.5 <= income_loan_ratio < 1:
        score += 10
    print(f"Score after income to loan amount ratio: {score}, Income/Loan Ratio: {income_loan_ratio}")

    # Final decision
    print(f"Final score: {score}")
    return score >= 70

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handles GET requests"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # Custom response message for GET request
        response = {"message": "Use POST to submit loan applications."}
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            application = json.loads(post_data.decode('utf-8'))
            print(f"Received application: {application}")  # Log received application

            approval = predict_loan_approval(application)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = json.dumps({"prediction": "Approved" if approval else "Not Approved"})
            self.wfile.write(response.encode('utf-8'))

        except Exception as e:
            print(f"Error processing request: {e}")
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            error_response = json.dumps({"error": "An error occurred during prediction."})
            self.wfile.write(error_response.encode('utf-8'))

    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
