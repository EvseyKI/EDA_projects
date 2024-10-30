FROM python:3.11-slim-buster
WORKDIR /app_w
RUN pip install --no-cache-dir numpy==2.0.2 pandas==2.2.3 scikit-learn==1.5.2 explainerdashboard==0.4.7 shap==0.46.0
COPY app/dashboard.py .
COPY app/app.py .
RUN python dashboard.py
EXPOSE 9050
ENTRYPOINT ["python"]
CMD ["app.py"]
