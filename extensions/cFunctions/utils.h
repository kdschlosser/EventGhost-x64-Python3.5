extern void ErrorExit(LPTSTR lpszFunction);
extern void dbgprint(const char *fmt, ...);

//#define DEBUG

#ifdef DEBUG
	#define DBG dbgprint
    #define DBG1 dbgprint
    #define DBG2 dbgprint
#else
	#define DBG(arg1)
    #define DBG1(arg1, arg2)
    #define DBG2(arg1, arg2, arg3)

#endif

#define RAISE_SYSTEMERR(msg) {PyErr_SetString(PyExc_SystemError, msg); return NULL;}
