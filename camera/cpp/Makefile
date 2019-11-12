CXX=g++
SOURCES=cv_cap.cpp
SOURCES+=xiApiPlusOcv.cpp
OBJECTS=$(SOURCES:.cpp=.o)
PROGRAM=cv_cap


all: $(PROGRAM)

$(PROGRAM): xiApiPlusOcv.o cv_cap.o
	g++ $(OBJECTS) -o cv_cap -lm3api -lopencv_core -lm `pkg-config --libs opencv` -lopencv_highgui -lopencv_imgproc -L/usr/local/lib 

xiApiPlusOcv.o: xiApiPlusOcv.cpp
	g++ -c xiApiPlusOcv.cpp -I . -I /usr/local/include/ -g3 -Wall -c -fmessage-length=0

cv_cap.o: cv_cap.cpp
	g++ -c cv_cap.cpp -I .  -I /usr/local/include/ -g3 -Wall -c -fmessage-length=0

clean:
	rm -f *.o *~ $(PROGRAM) $(OBJECTS)






