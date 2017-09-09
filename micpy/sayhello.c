#include <Python.h>

static PyObject* sayhello(PyObject *self, PyObject *args) {
	const char *name;

	if (!PyArg_ParseTuple(args, "s", &name)) {
		return NULL;
	}

	printf("Surprise Motherf*cker : %s\n", name);

	Py_INCREF(Py_None);
	return Py_None;
}

static struct PyMethodDef sayhello_methods[] = {
	{"sayhello", sayhello, METH_VARARGS, "Nothing"},
	{NULL, NULL, 0, NULL}	
};

PyMODINIT_FUNC initsayhello(void)
{
    PyObject *m = Py_InitModule("sayhello", sayhello_methods);
    if (m == NULL)
        return;
}
