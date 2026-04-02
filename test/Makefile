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

VERILOG_SOURCES = $(SRC_DIR)/$(BLOCK).v
TOPLEVEL        = $(BLOCK)
MODULE          = test_$(BLOCK)

include $(shell cocotb-config --makefiles)/Makefile.sim
