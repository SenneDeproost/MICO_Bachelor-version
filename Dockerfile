FROM python:2.7
WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt
EXPOSE 80
ENV NAME world
CMD ["python", "WISDEM/OpenMDAO/go-openmdao-0.13.0.py"]
CMD ["python", "WISDEM/CCBlade/setup.py", "install"]
CMD ["python", "app.py"]

