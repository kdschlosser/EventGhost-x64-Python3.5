#include "Python.h"


#include "registry_funcs.h"
#include "hooks.h"
#include "keyhook.h"
#include "mousehook.h"
#include "win_funcs.h"


static PyMethodDef example_methods[] = {
	{"RegEnumKeysAndValues", (PyCFunction)RegEnumKeysAndValues, METH_VARARGS, NULL },
	{"StartHooks", (PyCFunction)StartHooks, METH_VARARGS, NULL },
	{"StopHooks", (PyCFunction)StopHooks, METH_VARARGS, NULL },
	{"ResetIdleTimer", (PyCFunction)ResetIdleTimer, METH_VARARGS, NULL },
	{"SetIdleTime", (PyCFunction)SetIdleTime, METH_VARARGS, NULL },
	{"SetKeyboardCallback", (PyCFunction)SetKeyboardCallback, METH_KEYWORDS | METH_VARARGS, NULL },
	{"SetMouseCallback", (PyCFunction)SetMouseCallback, METH_VARARGS, NULL },
	{"GetTopLevelWindowList", (PyCFunction)GetTopLevelWindowList, METH_VARARGS, NULL },
	{"GetWindowChildsList", (PyCFunction)GetWindowChildsList, METH_VARARGS, NULL },
	{"GetProcessName", (PyCFunction)GetProcessName, METH_VARARGS, NULL },
	{"GetProcessDict", (PyCFunction)GetProcessDict, METH_VARARGS, NULL },
	{"GetWindowText", (PyCFunction)PyWin_GetWindowText, METH_VARARGS, NULL },
	{"GetClassName", (PyCFunction)PyWin_GetClassName, METH_VARARGS, NULL },
	{NULL, NULL, 0, NULL}
};

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "cFunctions",     /* m_name */
    "Misc C Functions",  /* m_doc */
    -1,                  /* m_size */
    example_methods,    /* m_methods */
    NULL,                /* m_reload */
    NULL,                /* m_traverse */
    NULL,                /* m_clear */
    NULL,                /* m_free */
};

PyObject* PyInit_cFunctions(void)
{
    return PyModule_Create(&moduledef);
};

