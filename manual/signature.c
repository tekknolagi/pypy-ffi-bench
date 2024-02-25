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

long inc_might_raise_impl(long arg) {
  if (arg == 10000000) {
    PyErr_Format(PyExc_StopIteration, "done");
    return -1;
  }
  return arg+1;
}

PyObject* inc_might_raise(PyObject* module, PyObject* obj) {
  (void)module;
  long obj_int = PyLong_AsLong(obj);
  if (obj_int == -1 && PyErr_Occurred()) {
    return NULL;
  }
  long result = inc_might_raise_impl(obj_int);
  if (result == -1 && PyErr_Occurred()) {
    return NULL;
  }
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
    return PyErr_Format(PyExc_TypeError, "add expected float but got %S", Py_TYPE(args[0]));
  }
  double left = PyFloat_AsDouble(args[0]);
  if (PyErr_Occurred()) return NULL;
  if (!PyFloat_CheckExact(args[1])) {
    return PyErr_Format(PyExc_TypeError, "add expected float but got %S", Py_TYPE(args[1]));
  }
  double right = PyFloat_AsDouble(args[1]);
  if (PyErr_Occurred()) return NULL;
  double result = add_impl(left, right);
  return PyFloat_FromDouble(result);
}

long takes_object_impl(PyObject* obj, long arg) {
  (void)obj;
  return arg + 1;
}

PyObject* takes_object(PyObject* module, PyObject*const *args, Py_ssize_t nargs) {
  (void)module;
  if (nargs != 2) {
    return PyErr_Format(PyExc_TypeError, "takes_object expected 2 arguments but got %ld", nargs);
  }
  PyObject* obj = args[0];
  assert(obj != NULL);
  long obj_int = PyLong_AsLong(args[1]);
  if (obj_int == -1 && PyErr_Occurred()) {
    return NULL;
  }
  long result = takes_object_impl(obj, obj_int);
  return PyLong_FromLong(result);
}

PyObject* meth_o_object_impl(PyObject* arg) {
  Py_INCREF(arg);
  return arg;
}

PyObject* meth_o_object(PyObject* module, PyObject* arg) {
  (void)module;
  return meth_o_object_impl(arg);
}

PyObject* meth_o_object_may_raise_impl(PyObject* arg) {
  Py_INCREF(arg);
  return arg;
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
#define MAY_RAISE(ty) - ty
#else
#define SIG(...)
#define TYPED_SIG(name, fptr, type, doc) \
  {#name, (PyCFunction)(void*)fptr, type, doc}
#define MAY_RAISE(ty)
#endif

SIG(inc, LIST(T_C_LONG), T_C_LONG)
SIG(inc_might_raise, LIST(T_C_LONG), MAY_RAISE(T_C_LONG))
SIG(add, LIST(T_C_DOUBLE, T_C_DOUBLE), T_C_DOUBLE)
SIG(takes_object, LIST(T_PY_OBJECT, T_C_LONG), T_C_LONG)
SIG(meth_o_object, LIST(T_PY_OBJECT), T_PY_OBJECT)
SIG(meth_o_object_may_raise, LIST(T_PY_OBJECT), MAY_RAISE(T_PY_OBJECT))

static PyMethodDef signature_methods[] = {
  TYPED_SIG(inc, inc, METH_O, "Add one to an int"),
  TYPED_SIG(inc_might_raise, inc_might_raise, METH_O, "Add one to an int but finish by raising an exception"),
  TYPED_SIG(add, add, METH_FASTCALL, "Add two doubles"),
  TYPED_SIG(takes_object, takes_object, METH_FASTCALL, "Takes an object and an int and increments the int"),
  TYPED_SIG(meth_o_object, meth_o_object, METH_O, "id(x)"),
  TYPED_SIG(meth_o_object_may_raise, meth_o_object, METH_O, "id(x)"),
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

PyMODINIT_FUNC PyInit_signature(void) {
  return PyModule_Create(&signature_definition);
}
