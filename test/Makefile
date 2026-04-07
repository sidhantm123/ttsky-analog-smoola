# Makefile for cocotb simulation
# Usage:
#   make                          # run sar_fsm tests (default)
#   make BLOCK=threshold_det      # run threshold_det tests
#   make BLOCK=refractory_ctr     # etc.
#
# Requires cocotb in active venv: source ../.venv/bin/activate

SIM ?= icarus
TOPLEVEL_LANG ?= verilog
SRC_DIR = $(PWD)/../src

BLOCK ?= sar_fsm

# digital_top requires all sub-block sources
ifeq ($(BLOCK),digital_top)
VERILOG_SOURCES = $(SRC_DIR)/sar_fsm.v \
                  $(SRC_DIR)/threshold_det.v \
                  $(SRC_DIR)/refractory_ctr.v \
                  $(SRC_DIR)/spike_counter.v \
                  $(SRC_DIR)/output_mux.v \
                  $(SRC_DIR)/digital_top.v
else
VERILOG_SOURCES = $(SRC_DIR)/$(BLOCK).v
endif

TOPLEVEL        = $(BLOCK)
MODULE          = test_$(BLOCK)

include $(shell cocotb-config --makefiles)/Makefile.sim
