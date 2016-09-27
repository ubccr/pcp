#pypmlogextract.pyx
cimport pypmlogextract

from libc.stdlib cimport malloc, free
from cpython.string cimport PyString_AsString

cdef char ** to_cstring_array(list_str):
    cdef char **ret = <char **>malloc(len(list_str) * sizeof(char *))
    for i in xrange(len(list_str)):
        ret[i] = PyString_AsString(list_str[i])
    return ret

def pypmlogextract(args):

    cdef void *handle = pypmlogextract.dlopen("libpcp_pmlogextract.so.1",RTLD_LAZY)
    
    if handle == NULL:
        print pypmlogextract.dlerror()
        return 1
    
    cdef void *mainFunc = pypmlogextract.dlsym(handle, "mainFunc")
    if mainFunc == NULL:
        print pypmlogextract.dlerror()
        return 1
    
    args.insert(0, "pypmlogextract")

    cdef char **myargv = to_cstring_array(args)
    cdef int myargc = len(args)
    
    cdef int retval = (<int (*)(int, char**)> mainFunc)(myargc, myargv)

    # PyString_AsString returns a ref to an internal buffer that shouldn't be freed per the docs
    # Just free our malloc
    free(myargv)
    dlclose(handle)

    return retval
