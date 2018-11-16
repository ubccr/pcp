#
# Copyright (c) 2014-2015 Red Hat.
# 
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
# 
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
# 

TOPDIR = ../../..
include $(TOPDIR)/src/include/builddefs

IAM	= ipmi
DOMAIN	= IPMI

CMDTARGET = pmdaipmi$(EXECSUFFIX)
LIBTARGET = pmda_ipmi.$(DSOSUFFIX)
CFILES	= pmda.c
DFILES	= README
LSRCFILES = Install Remove root help pmns $(DFILES)
LLDLIBS	= $(PCP_PMDALIB) $(IPMI_LIBS)
LCFLAGS += -DDSOSUFFIX=\"$(DSOSUFFIX)\"

PMDADIR = $(PCP_PMDAS_DIR)/$(IAM)
LDIRT	= domain.h *.log *.dir *.pag so_locations

default_pcp default:    build-me

include $(BUILDRULES)

ifeq "$(PMDA_IPMI)" "true"
build-me: $(LIBTARGET) $(CMDTARGET)

install_pcp install: default
	$(INSTALL) -m 755 -d $(PMDADIR)
	$(INSTALL) -m 755 Install Remove $(PMDADIR)
	$(INSTALL) -m 755 $(LIBTARGET) $(CMDTARGET) $(PMDADIR)
	$(INSTALL) -m 644 $(DFILES) root help pmns domain.h $(PMDADIR)
else
build-me:
install_pcp install:
endif

$(OBJECTS): domain.h

domain.h: ../../pmns/stdpmid
	$(DOMAIN_MAKERULE)

default_pcp:	default

install_pcp:	install
