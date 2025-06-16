# Database-Playground

To deploy the project

1) Navigate to backend directory
2) Execute:
   - cp -r ../frontend ./frontend
   - (sudo) docker build -t django-debug .
   - (sudo) docker run -p 8000:8000 -it --name django-app django-debug
