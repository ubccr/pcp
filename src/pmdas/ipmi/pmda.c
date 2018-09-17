/*
 * Copyright (c) 2018 Martins Innus.
 *
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the
 * Free Software Foundation; either version 2 of the License, or (at your
 * option) any later version.
 *
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
 * or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
 * for more details.
 */
#include "pmapi.h"
#include "impl.h"
#include "pmda.h"
#include "domain.h"

#include <errno.h>
#include <freeipmi/freeipmi.h>

/* List of metric item numbers - increasing from zero, no holes */
enum {
    IPMI_DCMI_POWER = 0,

    IPMI_METRIC_COUNT
};

/* Table of metrics exported by this PMDA */
static pmdaMetric metrictab[] = {
    { NULL, { PMDA_PMID(0, IPMI_DCMI_POWER), PM_TYPE_U32, PM_INDOM_NULL,
	PM_SEM_INSTANT, PMDA_PMUNITS(0, 0, 0, 0, 0, 0) } },
};

typedef struct {
    unsigned int  power;

    int failed[IPMI_METRIC_COUNT];
} dcmi_info_t;

static dcmi_info_t	dcmi_info;
static char		mypath[MAXPATHLEN];
static int		isDSO = 1;
static int              dcim_error = 0;
/* Global IPMI state variables */
ipmi_ctx_t ipmi_ctx = NULL;
fiid_obj_t obj_cmd_rs = NULL;

static int
refresh(dcmi_info_t *dcmi_info)
{
    uint64_t val;
    int j;

    if(dcim_error){
      for (j = 0; j < IPMI_METRIC_COUNT; j++){
        dcmi_info->failed[j] = 1;
        return 1;
      }
    }
    else {
      for (j = 0; j < IPMI_METRIC_COUNT; j++)
        dcmi_info->failed[j] = 0;
    }

    if (ipmi_cmd_dcmi_get_power_reading( ipmi_ctx, IPMI_DCMI_POWER_READING_MODE_SYSTEM_POWER_STATISTICS, 0, obj_cmd_rs) < 0){
        fprintf(stderr, "ipmi_cmd_dcmi_get_power_reading failed: %s\n", ipmi_ctx_errormsg (ipmi_ctx));
        /* This should not fail since we checked it at init, if it does???? */
        dcmi_info->failed[IPMI_DCMI_POWER]=1;
    }

    if (FIID_OBJ_GET (obj_cmd_rs, "current_power", &val) < 0) {
        fprintf(stderr, "current_power fail: %s\n", ipmi_ctx_errormsg (ipmi_ctx));
        /* Should not fail */
        dcmi_info->failed[IPMI_DCMI_POWER]=1;
    }

    dcmi_info->power = val;

    return 0;
}

/*
 * Wrapper for pmdaFetch which refresh the set of values once per fetch
 * PDU.  The fetchCallback is then called once per-metric/instance pair
 * to perform the actual filling of the pmResult (via each pmAtomValue).
 */
static int
ipmi_fetch(int numpmid, pmID pmidlist[], pmResult **resp, pmdaExt *pmda)
{
    refresh(&dcmi_info);
    return pmdaFetch(numpmid, pmidlist, resp, pmda);
}

static int
ipmi_fetchCallBack(pmdaMetric *mdesc, unsigned int inst, pmAtomValue *atom)
{
    __pmID_int	*idp = (__pmID_int *)&(mdesc->m_desc.pmid);

    if (idp->cluster != 0)
	return PM_ERR_PMID;
    if (inst != PM_INDOM_NULL)
        return PM_ERR_INST;

    switch (idp->item) {
        case IPMI_DCMI_POWER:
            if (dcmi_info.failed[IPMI_DCMI_POWER] == 1)
                return PM_ERR_VALUE; 
            atom->ul = dcmi_info.power;
            break;
        default:
            return PM_ERR_PMID;
    }

    return 0;
}

/**
 * Initializes the path to the help file for this PMDA.
 */
static void
initializeHelpPath()
{
    int sep = __pmPathSeparator();
    pmsprintf(mypath, sizeof(mypath), "%s%c" "ipmi" "%c" "help",
            pmGetConfig("PCP_PMDAS_DIR"), sep, sep);
}

void 
__PMDA_INIT_CALL
ipmi_init(pmdaInterface *dp)
{

    if (isDSO) {
    	initializeHelpPath();
    	pmdaDSO(dp, PMDA_INTERFACE_2, "ipmi DSO", mypath);
    }

    if (dp->status != 0)
	return;

    if (!(ipmi_ctx = ipmi_ctx_create ())) {
        __pmNotifyErr(LOG_ERR, "ipmi_ctx_create failed\n");
        dcim_error=1;
    }

    if (ipmi_ctx_find_inband (ipmi_ctx, NULL, 0, 0, 0, NULL, 0, 0  ) < 0) {
      __pmNotifyErr(LOG_ERR, "ipmi_ctx_find_inband failed");
      dcim_error=1;
    }

    if (!(obj_cmd_rs = fiid_obj_create (tmpl_cmd_dcmi_get_power_reading_rs))) {
        __pmNotifyErr(LOG_ERR, "fiid_obj_create: %s\n", strerror (errno));
        dcim_error=1;
    }

    /* Sanity check, confirm we can actually get a reading.  Some older BMCs fail */
    if (ipmi_cmd_dcmi_get_power_reading( ipmi_ctx, IPMI_DCMI_POWER_READING_MODE_SYSTEM_POWER_STATISTICS, 0, obj_cmd_rs) < 0){
        __pmNotifyErr(LOG_ERR, "ipmi_cmd_dcmi_get_power_reading failed: %s\n", ipmi_ctx_errormsg (ipmi_ctx));
        dcim_error=1;
    }

    dp->version.any.fetch = ipmi_fetch;
    pmdaSetFetchCallBack(dp, ipmi_fetchCallBack);

    pmdaInit(dp, NULL, 0, 
	     metrictab, sizeof(metrictab)/sizeof(metrictab[0]));
}

static pmLongOptions longopts[] = {
    PMDA_OPTIONS_HEADER("Options"),
    PMOPT_DEBUG,
    PMDAOPT_DOMAIN,
    PMDAOPT_LOGFILE,
    PMOPT_HELP,
    PMDA_OPTIONS_END
};

static pmdaOptions opts = {
    .short_options = "D:d:l:?",
    .long_options = longopts,
};

int
main(int argc, char **argv)
{
    pmdaInterface	desc;

    isDSO = 0;
    __pmSetProgname(argv[0]);

    initializeHelpPath();
    pmdaDaemon(&desc, PMDA_INTERFACE_2, pmProgname, IPMI,
		"ipmi.log", mypath);

    pmdaGetOptions(argc, argv, &opts, &desc);
    if (opts.errors) {
	pmdaUsageMessage(&opts);
	exit(1);
    }


    pmdaOpenLog(&desc);
    pmdaConnect(&desc);
    ipmi_init(&desc);
    pmdaMain(&desc);

    exit(0);
}
