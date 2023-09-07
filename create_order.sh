curl -X POST -H "Content-Type: application/json" -d '{
  "customer_name": "fifi",
  "customer_email": "fifi@example.co.za",
  "meals": [4,4,4,1,1,1] 
}' http://localhost:5000/api/orders

