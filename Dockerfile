FROM python
COPY . /app
WORKDIR /app
RUN pip3 install flask
RUN pip3 install dash
RUN pip3 install pandas
RUN pip3 install plotly
RUN pip3 install pysqlite3
RUN pip3 install seaborn
RUN pip3 install matplotlib
RUN chmod +x /app/app.py
CMD ["python3", "app.py"]