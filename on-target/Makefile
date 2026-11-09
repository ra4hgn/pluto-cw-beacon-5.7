# ============================================================
#  CW Beacon on 5.7 GHz — on-target build for ADALM-PlutoSDR
# ============================================================
#  Static build: links a locally-built static libiio (local backend only).
#
#  One-time: build a static libiio for ARM, then `make`:
#      git clone --branch v0.25 --depth 1 \
#          https://github.com/analogdevicesinc/libiio.git ~/libiio
#      cd ~/libiio && mkdir -p build && cd build
#      cmake .. -DCMAKE_C_COMPILER=arm-linux-gnueabihf-gcc \
#          -DCMAKE_SYSTEM_NAME=Linux -DCMAKE_SYSTEM_PROCESSOR=arm \
#          -DBUILD_SHARED_LIBS=OFF -DWITH_LOCAL_BACKEND=ON \
#          -DWITH_XML_BACKEND=OFF -DWITH_NETWORK_BACKEND=OFF \
#          -DWITH_USB_BACKEND=OFF -DWITH_SERIAL_BACKEND=OFF \
#          -DWITH_IIOD=OFF -DNO_THREADS=ON \
#          -DWITH_TESTS=OFF -DWITH_DOC=OFF -DWITH_EXAMPLES=OFF -DWITH_MAN=OFF
#      make
# ============================================================

CROSS   ?= arm-linux-gnueabihf-
CC      := $(CROSS)gcc

LIBIIO  ?= $(HOME)/libiio

CFLAGS  ?= -O2 -Wall -Wextra
CFLAGS  += -I$(LIBIIO) -I$(LIBIIO)/build
LDFLAGS += -static -L$(LIBIIO)/build
LDLIBS   = -liio -lm

PLUTO_IP   ?= 192.168.2.1
PLUTO_USER ?= root

TARGET = beacon
SRC    = beacon.c

.PHONY: all upload run clean

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $< $(LDLIBS)

upload: $(TARGET)
	scp -O $(TARGET) $(PLUTO_USER)@$(PLUTO_IP):/mnt/jffs2/

run:
	ssh -t $(PLUTO_USER)@$(PLUTO_IP) /mnt/jffs2/$(TARGET)

clean:
	rm -f $(TARGET)
