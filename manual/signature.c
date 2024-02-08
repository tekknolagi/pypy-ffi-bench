#include <Python.h>

long inc_impl(long arg) {
  return arg+1;
}

PyObject* inc(PyObject* module, PyObject* obj) {
  (void)module;
  long obj_int = PyLong_AsLong(obj);
  if (obj_int == -1 && PyErr_Occurred()) {
    return NULL;
  }
  long result = inc_impl(obj_int);
  return PyLong_FromLong(result);
}

double add_impl(double left, double right) {
  return left + right;
}

PyObject* add(PyObject* module, PyObject*const *args, Py_ssize_t nargs) {
  (void)module;
  if (nargs != 2) {
    return PyErr_Format(PyExc_TypeError, "add expected 2 arguments but got %ld", nargs);
  }
  if (!PyFloat_CheckExact(args[0])) {
    return PyErr_Format(PyExc_TypeError, "add expected float but got %s", Py_TYPE(args[0])->tp_name);
  }
  double left = PyFloat_AsDouble(args[0]);
  if (PyErr_Occurred()) return NULL;
  if (!PyFloat_CheckExact(args[1])) {
    return PyErr_Format(PyExc_TypeError, "add expected float but got %s", Py_TYPE(args[1])->tp_name);
  }
  double right = PyFloat_AsDouble(args[1]);
  if (PyErr_Occurred()) return NULL;
  double result = add_impl(left, right);
  return PyFloat_FromDouble(result);
}

#ifdef METH_TYPED
#define LIST(...) __VA_ARGS__

#define SIG(name, args, ret) \
  int name##_arg_types[] = {args, -1};\
  PyPyTypedMethodMetadata name##_sig = {\
    .arg_types = name##_arg_types,\
    .ret_type = ret,\
    .underlying_func = name##_impl,\
    .ml_name = #name,\
  };

#define TYPED_SIG(name, fptr, type, doc) \
  {name##_sig.ml_name, (PyCFunction)(void*)fptr, type | METH_TYPED, doc}
#else
#define SIG(...)
#define TYPED_SIG(name, fptr, type, doc) \
  {#name, (PyCFunction)(void*)fptr, type, doc}
#endif

SIG(inc, LIST(T_C_LONG), T_C_LONG)
SIG(add, LIST(T_C_DOUBLE, T_C_DOUBLE), T_C_DOUBLE)

static PyMethodDef signature_methods[] = {
  TYPED_SIG(inc, inc, METH_O, "Add one to an int"),
  TYPED_SIG(add, add, METH_FASTCALL, "Add two doubles"),
  {NULL, NULL, 0, NULL},
};

static struct PyModuleDef signature_definition = {
    PyModuleDef_HEAD_INIT, "signature",
    "A C extension module with type information exposed.", -1,
    signature_methods,
    NULL,
    NULL,
    NULL,
    NULL};

typedef struct {
    PyObject_HEAD
    Py_ssize_t cur;
    Py_ssize_t end;
} RangeIterator;

static int RangeIterator_init(RangeIterator *self, PyObject *args, PyObject *kwds) {
    static char *kwlist[] = {"end", NULL};
    self->cur = 0;
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|i", kwlist,
                                     &self->end)) {
        return -1;
    }
    return 0;
}

// TODO(max): Perhaps we can figure out a way to make this return a C int and
// pass that through to PyPy even though it is not a normal PyMethodDef.
static PyObject * RangeIterator_iternext(RangeIterator *it) {
  if (it->cur == it->end) {
    // Implicit StopIteration raise.
    return NULL;
  }
  long result = it->cur;
  it->cur++;
  return PyLong_FromLong(result);
}

static PyTypeObject RangeIteratorType = {
    .ob_base = PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "signature.RangeIterator",
    .tp_doc = PyDoc_STR("RangeIterator object"),
    .tp_basicsize = sizeof(RangeIterator),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = PyType_GenericNew,
    .tp_init = (initproc) RangeIterator_init,
    .tp_iter = PyObject_SelfIter,
    .tp_iternext = (iternextfunc)RangeIterator_iternext,
};

PyMODINIT_FUNC PyInit_signature(void) {
  PyObject* result = PyModule_Create(&signature_definition);
  if (result == NULL) {
    return NULL;
  }
  // TODO(max): What is that other heap type init function?
  if (PyType_Ready(&RangeIteratorType) < 0) {
    Py_DECREF(result);
    return NULL;
  }
  Py_INCREF(&RangeIteratorType);
  if (PyModule_AddObject(result, "RangeIterator", (PyObject *) &RangeIteratorType) < 0) {
    Py_DECREF(result);
    Py_DECREF(&RangeIteratorType);
    return NULL;
  }
  return result;
}
